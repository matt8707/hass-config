"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Sonarr upcoming releases.

https://github.com/custom-components/sensor.radarr_upcoming_media

https://github.com/custom-cards/upcoming-media-card

"""
import logging
import json
import time
import requests
from datetime import date, datetime
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity

__version__ = '0.1.10'

_LOGGER = logging.getLogger(__name__)

CONF_DAYS = 'days'
CONF_URLBASE = 'urlbase'
CONF_MAX = 'max'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_DAYS, default='7'): cv.string,
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=8989): cv.port,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_URLBASE, default=''): cv.string,
    vol.Optional(CONF_MAX, default=5): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([SonarrUpcomingMediaSensor(hass, config)], True)


class SonarrUpcomingMediaSensor(Entity):

    def __init__(self, hass, conf):
        from pytz import timezone
        self.host = conf.get(CONF_HOST)
        self.port = conf.get(CONF_PORT)
        self.urlbase = conf.get(CONF_URLBASE)
        if self.urlbase:
            self.urlbase = "{}/".format(self.urlbase.strip('/'))
        self.apikey = conf.get(CONF_API_KEY)
        self.days = int(conf.get(CONF_DAYS))
        self.ssl = 's' if conf.get(CONF_SSL) else ''
        self._state = None
        self.data = []
        self._tz = timezone(str(hass.config.time_zone))
        self.max_items = int(conf.get(CONF_MAX))

    @property
    def name(self):
        return 'Sonarr_Upcoming_Media'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        import re
        """Return JSON for the sensor."""
        attributes = {}
        default = {}
        card_json = []
        default['title_default'] = '$title'
        default['line1_default'] = '$episode'
        default['line2_default'] = '$release'
        default['line3_default'] = '$rating - $runtime'
        default['line4_default'] = '$number - $studio'
        default['icon'] = 'mdi:arrow-down-bold'
        card_json.append(default)
        for show in self.data:
            card_item = {}
            if 'series' not in show:
                continue
            card_item['airdate'] = show['airDateUtc']
            if days_until(show['airDateUtc'], self._tz) <= 7:
                card_item['release'] = '$day, $time'
            else:
                card_item['release'] = '$day, $date $time'
            card_item['flag'] = show.get('hasFile', False)
            if 'title' in show['series']:
                card_item['title'] = show['series']['title']
            else:
                continue
            card_item['episode'] = show.get('title', '')
            if 'seasonNumber' and 'episodeNumber' in show:
                card_item['number'] = 'S{:02d}E{:02d}'.format(show['seasonNumber'],
                                                        show['episodeNumber'])
            else:
                card_item['number'] = ''
            if 'runtime' in show['series']:
                card_item['runtime'] = show['series']['runtime']
            else:
                card_item['runtime'] = ''
            if 'network' in show['series']:
                card_item['studio'] = show['series']['network']
            else:
                card_item['studio'] = ''
            if ('ratings' in show['series'] and
               show['series']['ratings']['value'] > 0):
                    card_item['rating'] = ('\N{BLACK STAR} ' +
                                     str(show['series']['ratings']['value']))
            else:
                card_item['rating'] = ''
            if 'genres' in show['series']:
                card_item['genres'] = ', '.join(show['series']['genres'])
            else:
                card_item['genres'] = ''
            try:
                for img in show['series']['images']:
                    if img['coverType'] == 'poster':
                        card_item['poster'] = re.sub('.jpg', '_t.jpg', img['url'])
            except:
                continue
            try:
                card_item['fanart'] = ''
                for img in show['series']['images']:
                    if img['coverType'] == 'fanart':
                        card_item['fanart'] = re.sub('.jpg', '_t.jpg', img['url'])
            except:
                pass
            card_json.append(card_item)
        attributes['data'] = card_json
        return attributes

    def update(self):
        start = get_date(self._tz)
        end = get_date(self._tz, self.days)
        try:
            api = requests.get('http{0}://{1}:{2}/{3}api/calendar?start={4}'
                               '&end={5}'.format(self.ssl, self.host,
                                                 self.port, self.urlbase,
                                                 start, end),
                               headers={'X-Api-Key': self.apikey}, timeout=10)
        except OSError:
            _LOGGER.warning("Host %s is not available", self.host)
            self._state = '%s cannot be reached' % self.host
            return

        if api.status_code == 200:
            self._state = 'Online'
            if self.days == 1:
                self.data = list(filter(lambda x: x['airDate'][:-10] == str(
                    start), api.json()))[:self.max_items]
            else:
                self.data = api.json()[:self.max_items]
        else:
            self._state = '%s cannot be reached' % self.host


def get_date(zone, offset=0):
    """Get date based on timezone and offset of days."""
    return datetime.date(datetime.fromtimestamp(
        time.time() + 86400 * offset, tz=zone))


def days_until(date, tz):
    from pytz import utc
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date = str(date.replace(tzinfo=utc).astimezone(tz))[:10]
    date = time.strptime(date, '%Y-%m-%d')
    date = time.mktime(date)
    now = datetime.now().strftime('%Y-%m-%d')
    now = time.strptime(now, '%Y-%m-%d')
    now = time.mktime(now)
    return int((date - now) / 86400)
