from datetime import datetime

from homeassistant.const import STATE_UNAVAILABLE

from .helpers import setup_platform, BrowserModEntity

PLATFORM = "sensor"


async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    return setup_platform(hass, config, async_add_devices, PLATFORM, BrowserModSensor)


async def async_setup_entry(hass, config_entry, async_add_entities):
    await async_setup_platform(hass, {}, async_add_entities)


class BrowserModSensor(BrowserModEntity):
    domain = PLATFORM

    def __init__(self, hass, connection, deviceID, alias=None):
        super().__init__(hass, connection, deviceID, alias)
        self.last_seen = None

    def updated(self):
        self.last_seen = datetime.now()
        self.schedule_update_ha_state()

    @property
    def state(self):
        if not self.connection.connection:
            return STATE_UNAVAILABLE
        return len(self.connection.connection)

    @property
    def device_state_attributes(self):
        return {
            "type": "browser_mod",
            "last_seen": self.last_seen,
            "deviceID": self.deviceID,
            **self.data,
        }
