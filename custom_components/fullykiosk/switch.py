"""Fully Kiosk Browser switch."""
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser switch."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([FullyScreenSaverSwitch(hass, coordinator)], False)
    async_add_entities([FullyMaintenanceModeSwitch(hass, coordinator)], False)
    async_add_entities([FullyKioskLockSwitch(hass, coordinator)], False)
    async_add_entities([FullyKioskMotionDetectionSwitch(hass, coordinator)], False)


class FullySwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a generic Fully Kiosk Browser switch entity."""

    def __init__(self, hass, coordinator):
        """Initialize the switch."""
        self.coordinator = coordinator
        self.hass = hass

        self._name = ""
        self._unique_id = ""

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

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

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()


class FullyScreenSaverSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser screensaver switch."""

    def __init__(self, hass, coordinator):
        """Initialize the screensaver switch."""
        super().__init__(hass, coordinator)
        self._name = f"{coordinator.data['deviceName']} Screensaver"
        self._unique_id = f"{coordinator.data['deviceID']}-screensaver"

    @property
    def is_on(self):
        """Return if switch is on."""
        if self.coordinator.data:
            if self.coordinator.data["appVersionCode"] < 784:
                return self.coordinator.data["currentFragment"] == "screensaver"
            return self.coordinator.data["isInScreensaver"]

    async def async_turn_on(self, **kwargs):
        """Turn on the screensaver."""
        await self.coordinator.fully.startScreensaver()
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the screensaver."""
        await self.coordinator.fully.stopScreensaver()
        await self.coordinator.async_refresh()


class FullyMaintenanceModeSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser maintenance mode switch."""

    def __init__(self, hass, coordinator):
        """Initialize the maintenance mode switch."""
        super().__init__(hass, coordinator)
        self._name = f"{coordinator.data['deviceName']} Maintenance Mode"
        self._unique_id = f"{coordinator.data['deviceID']}-maintenance"

    @property
    def is_on(self):
        """Return if maintenance mode is on."""
        return self.coordinator.data["maintenanceMode"]

    async def async_turn_on(self, **kwargs):
        """Turn on maintenance mode."""
        await self.coordinator.fully.enableLockedMode()
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off maintenance mode."""
        await self.coordinator.fully.disableLockedMode()
        await self.coordinator.async_refresh()


class FullyKioskLockSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser kiosk lock switch."""

    def __init__(self, hass, coordinator):
        """Intialize the kiosk lock switch."""
        super().__init__(hass, coordinator)
        self._name = f"{coordinator.data['deviceName']} Kiosk Lock"
        self._unique_id = f"{coordinator.data['deviceID']}-kiosk"

    @property
    def is_on(self):
        """Return if kiosk lock is on."""
        return self.coordinator.data["kioskLocked"]

    async def async_turn_on(self, **kwargs):
        """Turn on kiosk lock."""
        await self.coordinator.fully.lockKiosk()
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off kiosk lock."""
        await self.coordinator.fully.unlockKiosk()
        await self.coordinator.async_refresh()


class FullyKioskMotionDetectionSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser kiosk lock switch."""

    def __init__(self, hass, coordinator):
        """Intialize the kiosk lock switch."""
        super().__init__(hass, coordinator)
        self._name = f"{coordinator.data['deviceName']} Motion Detection"
        self._unique_id = f"{coordinator.data['deviceID']}-motion-detection"

    @property
    def is_on(self):
        """Return if motion detection is on."""
        return self.coordinator.data["settings"]["motionDetection"]

    async def async_turn_on(self, **kwargs):
        """Turn on kiosk lock."""
        await self.coordinator.fully.enableMotionDetection()
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off kiosk lock."""
        await self.coordinator.fully.disableMotionDetection()
        await self.coordinator.async_refresh()
