"""Calendar platform support for Waste Collection Schedule."""

import logging
from datetime import timedelta

from homeassistant.components.calendar import CalendarEventDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up calendar platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    entities = []

    api = discovery_info["api"]

    for scraper in api.scrapers:
        entities.append(WasteCollectionCalendar(api, scraper))

    async_add_entities(entities)


class WasteCollectionCalendar(CalendarEventDevice):
    """Calendar entity class."""

    def __init__(self, api, scraper):
        self._api = api
        self._scraper = scraper

    @property
    def name(self):
        """Return entity name."""
        return self._scraper.calendar_title

    @property
    def event(self):
        """Return next collection event."""
        collections = self._scraper.get_upcoming(count=1, include_today=True)
        if len(collections) == 0:
            return None
        else:
            return self._convert(collections[0])

    async def async_get_events(self, hass, start_date, end_date):
        """Return all events within specified time span."""
        collections = []
        for a in self._scraper.get_upcoming(include_today=True):
            if a.date >= start_date.date() and a.date <= end_date.date():
                collections.append(self._convert(a))
        return collections

    def _convert(self, collection):
        """Convert an collection into a Home Assistant calendar event."""
        return {
            "uid": f"{self._scraper.calendar_title}-{collection.date.isoformat()}-{collection.type}",
            "summary": collection.type,
            "start": {"date": collection.date.isoformat()},
            "end": {"date": (collection.date + timedelta(days=1)).isoformat()},
            "allDay": True,
        }
