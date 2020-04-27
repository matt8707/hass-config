"""
Support for Blue Iris binary sensors.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.blueiris/
"""
import logging

from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant

from .helpers.const import *
from .models.base_entity import HPPrinterEntity, async_setup_base_entry
from .models.entity_data import EntityData

_LOGGER = logging.getLogger(__name__)


CURRENT_DOMAIN = DOMAIN_BINARY_SENSOR


def get_binary_sensor(hass: HomeAssistant, integration_name: str, entity: EntityData):
    binary_sensor = HPPrinterBinarySensor()
    binary_sensor.initialize(hass, integration_name, entity, CURRENT_DOMAIN)

    return binary_sensor


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up EdgeOS based off an entry."""
    await async_setup_base_entry(
        hass, entry, async_add_entities, CURRENT_DOMAIN, get_binary_sensor
    )


async def async_unload_entry(hass, config_entry):
    _LOGGER.info(f"async_unload_entry {CURRENT_DOMAIN}: {config_entry}")

    return True


class HPPrinterBinarySensor(HPPrinterEntity):
    """Representation a binary sensor that is updated by EdgeOS."""

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.entity.state)

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return STATE_ON if self.is_on else STATE_OFF

    async def async_added_to_hass_local(self):
        _LOGGER.info(f"Added new {self.name}")

    def _immediate_update(self, previous_state: bool):
        if previous_state != self.entity.state:
            _LOGGER.debug(
                f"{self.name} updated from {previous_state} to {self.entity.state}"
            )

        super()._immediate_update(previous_state)
