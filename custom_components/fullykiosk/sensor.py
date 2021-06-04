"""Fully Kiosk Browser sensor."""
import logging

from homeassistant.const import DATA_MEGABYTES, DEVICE_CLASS_BATTERY, PERCENTAGE
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "batteryLevel": "Battery Level",
    "screenOrientation": "Screen Orientation",
    "foregroundApp": "Foreground App",
    "lastAppStart": "Last App Start",
    "wifiSignalLevel": "WiFi Signal Level",
    "currentPage": "Current Page",
    "internalStorageFreeSpace": "Internal Storage Free Space",
    "internalStorageTotalSpace": "Internal Storage Total Space",
    "ramFreeMemory": "RAM Free Memory",
    "ramTotalMemory": "RAM Total Memory",
}

STORAGE_SENSORS = [
    "internalStorageFreeSpace",
    "internalStorageTotalSpace",
    "ramFreeMemory",
    "ramTotalMemory",
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser sensor."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []

    for sensor in SENSOR_TYPES:
        sensors.append(FullySensor(coordinator, sensor))

    async_add_entities(sensors, False)


class FullySensor(CoordinatorEntity, Entity):
    """Representation of a Fully Kiosk Browser sensor."""

    def __init__(self, coordinator, sensor):
        """Initialize the sensor entity."""
        self._name = f"{coordinator.data['deviceName']} {SENSOR_TYPES[sensor]}"
        self._sensor = sensor
        self.coordinator = coordinator
        self._unique_id = f"{coordinator.data['deviceID']}-{sensor}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        if self._sensor in STORAGE_SENSORS:
            return round(self.coordinator.data[self._sensor] * 0.000001, 1)

        return self.coordinator.data[self._sensor]

    @property
    def device_class(self):
        """Return the device class."""
        if self._sensor == "batteryLevel":
            return DEVICE_CLASS_BATTERY

        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._sensor == "batteryLevel":
            return PERCENTAGE

        if self._sensor in STORAGE_SENSORS:
            return DATA_MEGABYTES

        return None

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data["deviceID"])},
            "name": self.coordinator.data["deviceName"],
            "manufacturer": self.coordinator.data["deviceManufacturer"],
            "model": self.coordinator.data["deviceModel"],
            "sw_version": self.coordinator.data["appVersionName"],
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
