"""Fully Kiosk Browser button."""

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


@dataclass
class FullyButtonEntityDescription(ButtonEntityDescription):
    """Fully Kiosk Browser button description."""

    press_action: Callable = None


ENTITY_TYPES: tuple[FullyButtonEntityDescription, ...] = [
    FullyButtonEntityDescription(
        key="restartApp",
        name="Restart Browser",
        press_action=lambda fully: fully.restartApp(),
    ),
    FullyButtonEntityDescription(
        key="rebootDevice",
        name="Reboot Device",
        press_action=lambda fully: fully.rebootDevice(),
    ),
    FullyButtonEntityDescription(
        key="toForeground",
        name="Bring to Foreground",
        press_action=lambda fully: fully.toForeground(),
    ),
    FullyButtonEntityDescription(
        key="toBackground",
        name="Send to Background",
        press_action=lambda fully: fully.toBackground(),
    ),
    FullyButtonEntityDescription(
        key="loadStartUrl",
        name="Load Start URL",
        press_action=lambda fully: fully.loadStartUrl(),
    ),
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser button entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [FullyButtonEntity(coordinator, entity) for entity in ENTITY_TYPES]

    async_add_entities(entities, False)


class FullyButtonEntity(CoordinatorEntity, ButtonEntity):
    """Representation of a Fully Kiosk Browser entity."""

    def __init__(self, coordinator, description: FullyButtonEntityDescription):
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

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()

    async def async_press(self):
        """Set the value of the entity."""
        await self.entity_description.press_action(self.coordinator.fully)
        await self.coordinator.async_refresh()
