"""Fully Kiosk Browser light entity for controlling screen brightness & on/off."""
import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser light."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([FullyLight(coordinator)], False)


class FullyLight(CoordinatorEntity, LightEntity):
    """Representation of a Fully Kiosk Browser light."""

    def __init__(self, coordinator):
        """Initialize the light (screen) entity."""
        self._name = f"{coordinator.data['deviceName']} Screen"
        self.coordinator = coordinator
        self._unique_id = f"{coordinator.data['deviceID']}-screen"

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def is_on(self):
        """Return if the screen is on."""
        if self.coordinator.data:
            if self.coordinator.data["appVersionCode"] < 784:
                return self.coordinator.data["isScreenOn"]
            return self.coordinator.data["screenOn"]

    @property
    def brightness(self):
        """Return the screen brightness."""
        return self.coordinator.data["screenBrightness"]

    @property
    def supported_features(self):
        """Return the supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data["deviceID"])},
            "name": self.coordinator.data["deviceName"],
            "manufacturer": self.coordinator.data["deviceManufacturer"],
            "model": self.coordinator.data["deviceModel"],
            "sw_version": self.coordinator.data["appVersionName"],
            "configuration_url": f"http://{self.coordinator.data['ip4']}:2323",
        }

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    async def async_turn_on(self, **kwargs):
        """Turn on the screen."""
        await self.coordinator.fully.screenOn()
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness is None:
            await self.coordinator.async_refresh()
            return
        if brightness != self.coordinator.data["screenBrightness"]:
            await self.coordinator.fully.setScreenBrightness(brightness)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the screen."""
        await self.coordinator.fully.screenOff()
        await self.coordinator.async_refresh()

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
