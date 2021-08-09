"""Waste Collection Schedule Component."""
import logging
import site
from pathlib import Path
from random import randrange

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import dispatcher_send

from .const import DOMAIN, UPDATE_SENSORS_SIGNAL

from homeassistant.helpers.event import async_call_later  # isort:skip
from homeassistant.helpers.event import async_track_time_change  # isort:skip

# add module directory to path
package_dir = Path(__file__).resolve().parents[0]
site.addsitedir(str(package_dir))
from waste_collection_schedule import Customize, Scraper  # type: ignore # isort:skip # noqa: E402

_LOGGER = logging.getLogger(__name__)

CONF_SOURCES = "sources"
CONF_SOURCE_NAME = "name"
CONF_SOURCE_ARGS = "args"  # scraper-source arguments
CONF_SOURCE_CALENDAR_TITLE = "calendar_title"
CONF_SEPARATOR = "separator"
CONF_FETCH_TIME = "fetch_time"
CONF_RANDOM_FETCH_TIME_OFFSET = "random_fetch_time_offset"
CONF_DAY_SWITCH_TIME = "day_switch_time"

CONF_CUSTOMIZE = "customize"
CONF_TYPE = "type"
CONF_ALIAS = "alias"
CONF_SHOW = "show"
CONF_ICON = "icon"
CONF_PICTURE = "picture"

CUSTOMIZE_CONFIG = vol.Schema(
    {
        vol.Optional(CONF_TYPE): cv.string,
        vol.Optional(CONF_ALIAS): cv.string,
        vol.Optional(CONF_SHOW): cv.boolean,
        vol.Optional(CONF_ICON): cv.icon,
        vol.Optional(CONF_PICTURE): cv.url,
    }
)

SOURCE_CONFIG = vol.Schema(
    {
        vol.Required(CONF_SOURCE_NAME): cv.string,
        vol.Required(CONF_SOURCE_ARGS): dict,
        vol.Optional(CONF_CUSTOMIZE, default=[]): vol.All(
            cv.ensure_list, [CUSTOMIZE_CONFIG]
        ),
        vol.Optional(CONF_SOURCE_CALENDAR_TITLE): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_SOURCES): vol.All(cv.ensure_list, [SOURCE_CONFIG]),
                vol.Optional(CONF_SEPARATOR, default=", "): cv.string,
                vol.Optional(CONF_FETCH_TIME, default="01:00"): cv.time,
                vol.Optional(
                    CONF_RANDOM_FETCH_TIME_OFFSET, default=60
                ): cv.positive_int,
                vol.Optional(CONF_DAY_SWITCH_TIME, default="10:00"): cv.time,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component. config contains data from configuration.yaml."""
    # create empty api object as singleton
    api = WasteCollectionApi(
        hass,
        separator=config[DOMAIN][CONF_SEPARATOR],
        fetch_time=config[DOMAIN][CONF_FETCH_TIME],
        random_fetch_time_offset=config[DOMAIN][CONF_RANDOM_FETCH_TIME_OFFSET],
        day_switch_time=config[DOMAIN][CONF_DAY_SWITCH_TIME],
    )

    # create scraper(s)
    for source in config[DOMAIN][CONF_SOURCES]:
        # create customize object
        customize = {}
        for c in source.get(CONF_CUSTOMIZE, {}):
            customize[c[CONF_TYPE]] = Customize(
                waste_type=c[CONF_TYPE],
                alias=c.get(CONF_ALIAS),
                show=c.get(CONF_SHOW, True),
                icon=c.get(CONF_ICON),
                picture=c.get(CONF_PICTURE),
            )
        api.add_scraper(
            source_name=source[CONF_SOURCE_NAME],
            customize=customize,
            calendar_title=source.get(CONF_SOURCE_CALENDAR_TITLE),
            source_args=source.get(CONF_SOURCE_ARGS, {}),
        )

    # store api object
    hass.data.setdefault(DOMAIN, api)

    # load calendar platform
    await hass.helpers.discovery.async_load_platform(
        "calendar", DOMAIN, {"api": api}, config
    )

    # initial fetch of all data
    hass.add_job(api._fetch)

    return True


class WasteCollectionApi:
    def __init__(
        self, hass, separator, fetch_time, random_fetch_time_offset, day_switch_time
    ):
        self._hass = hass
        self._scrapers = []
        self._separator = separator
        self._fetch_time = fetch_time
        self._random_fetch_time_offset = random_fetch_time_offset
        self._day_switch_time = day_switch_time

        # start timer to fetch date once per day
        async_track_time_change(
            hass,
            self._fetch_callback,
            self._fetch_time.hour,
            self._fetch_time.minute,
            self._fetch_time.second,
        )

        # start timer for day-switch time
        if self._day_switch_time != self._fetch_time:
            async_track_time_change(
                hass,
                self._update_sensors_callback,
                self._day_switch_time.hour,
                self._day_switch_time.minute,
                self._day_switch_time.second,
            )

        # add a timer at midnight (if not already there) to update days-to
        midnight = dt_util.parse_time("00:00")
        if midnight != self._fetch_time and midnight != self._day_switch_time:
            async_track_time_change(
                hass,
                self._update_sensors_callback,
                midnight.hour,
                midnight.minute,
                midnight.second,
            )

    @property
    def separator(self):
        """Separator string, used to separator waste types."""
        return self._separator

    @property
    def fetch_time(self):
        """When to fetch to data."""
        return self._fetch_time

    @property
    def day_switch_time(self):
        """When to hide entries for today."""
        return self._day_switch_time

    def add_scraper(self, source_name, customize, source_args, calendar_title):
        self._scrapers.append(
            Scraper.create(
                source_name=source_name,
                customize=customize,
                source_args=source_args,
                calendar_title=calendar_title,
            )
        )

    def _fetch(self, *_):
        for scraper in self._scrapers:
            try:
                scraper.fetch()
            except Exception as error:
                _LOGGER.error(f"fetch failed for source {scraper.source}: {error}")

        self._update_sensors_callback()

    @property
    def scrapers(self):
        return self._scrapers

    def get_scraper(self, index):
        return self._scrapers[index] if index < len(self._scrapers) else None

    @callback
    def _fetch_callback(self, *_):
        async_call_later(
            self._hass,
            randrange(0, 60 * self._random_fetch_time_offset),
            self._fetch_now_callback,
        )

    @callback
    def _fetch_now_callback(self, *_):
        self._hass.add_job(self._fetch)

    @callback
    def _update_sensors_callback(self, *_):
        dispatcher_send(self._hass, UPDATE_SENSORS_SIGNAL)
