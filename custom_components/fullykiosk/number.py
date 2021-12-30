"""Fully Kiosk Browser number."""

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

ENTITY_TYPES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="timeToScreensaverV2",
        name="Screensaver Timer",
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="screensaverBrightness",
        name="Screensaver Brightness",
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="timeToScreenOffV2",
        name="Screen Off Timer",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser number entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        FullyNumberEntity(coordinator, entity)
        for entity in ENTITY_TYPES
        if entity.key in coordinator.data["settings"]
    ]

    async_add_entities(entities, False)


class FullyNumberEntity(CoordinatorEntity, NumberEntity):
    """Representation of a Fully Kiosk Browser entity."""

    def __init__(self, coordinator, description: NumberEntityDescription):
        """Initialize the number entity."""
        self.entity_description = description
        self._key = description.key
        self.coordinator = coordinator

        self._attr_name = f"{coordinator.data['deviceName']} {description.name}"
        self._attr_unique_id = f"{coordinator.data['deviceID']}-{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self.coordinator.data["deviceID"])},
            "name": self.coordinator.data["deviceName"],
            "manufacturer": self.coordinator.data["deviceManufacturer"],
            "model": self.coordinator.data["deviceModel"],
            "sw_version": self.coordinator.data["appVersionName"],
            "configuration_url": f"http://{self.coordinator.data['ip4']}:2323",
        }

        # Min, max, and step are not available in EntityDescription until HA 2022.2 release.
        self._attr_step = 1
        self._attr_min_value = 0

        if self._key in ["timeToScreensaverV2", "timeToScreenOffV2"]:
            self._attr_max_value = 9999
        if self._key == "screensaverBrightness":
            self._attr_max_value = 255

    @property
    def state(self):
        """Return the state of the number entity."""
        if not self.coordinator.data:
            return None

        return self.coordinator.data["settings"][self._key]

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()

    async def async_set_value(self, value):
        """Set the value of the entity."""
        await self.coordinator.fully.setConfigurationString(self._key, int(value))
