import logging
from datetime import datetime
import base64

from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF, STATE_IDLE
from homeassistant.components.camera import Camera

from .helpers import setup_platform, BrowserModEntity

PLATFORM = 'camera'

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    return setup_platform(hass, config, async_add_devices, PLATFORM, BrowserModCamera)


async def async_setup_entry(hass, config_entry, async_add_entities):
    await async_setup_platform(hass, {}, async_add_entities)


class BrowserModCamera(Camera, BrowserModEntity):
    domain = PLATFORM

    def __init__(self, hass, connection, deviceID, alias=None):
        Camera.__init__(self)
        BrowserModEntity.__init__(self, hass, connection, deviceID, alias)
        self.last_seen = None

    def updated(self):
        if self.last_seen is None or (datetime.now() - self.last_seen).seconds > 15:
            self.last_seen = datetime.now()
        self.schedule_update_ha_state()

    def camera_image(self):
        return base64.b64decode(self.data.split(',')[1])

    @property
    def device_state_attributes(self):
        return {
                "type": "browser_mod",
                "deviceID": self.deviceID,
                "last_seen": self.last_seen,
                }
