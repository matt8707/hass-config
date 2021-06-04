from datetime import datetime

from homeassistant.const import (
    STATE_UNAVAILABLE,
    ATTR_BATTERY_CHARGING,
    ATTR_BATTERY_LEVEL,
    STATE_ON,
    STATE_OFF,
)
from homeassistant.components.binary_sensor import DEVICE_CLASS_MOTION

from .helpers import setup_platform, BrowserModEntity

PLATFORM = "binary_sensor"


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
        if self.data.get("motion", False):
            return STATE_ON
        return STATE_OFF

    @property
    def is_on(self):
        return not self.data.get("motion", False)

    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION

    @property
    def device_state_attributes(self):
        return {
            "type": "browser_mod",
            "last_seen": self.last_seen,
            ATTR_BATTERY_LEVEL: self.data.get("battery", None),
            ATTR_BATTERY_CHARGING: self.data.get("charging", None),
            **self.data,
        }
