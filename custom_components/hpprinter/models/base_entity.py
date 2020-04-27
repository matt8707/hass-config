import logging
import sys
from typing import Any, Callable, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from ..helpers import get_ha
from ..helpers.const import *
from .entity_data import EntityData

_LOGGER = logging.getLogger(__name__)


async def async_setup_base_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
    domain: str,
    component: Callable[[HomeAssistant, Any, EntityData], Any],
):

    """Set up EdgeOS based off an entry."""
    _LOGGER.debug(f"Starting async_setup_entry {domain}")

    try:
        entry_data = entry.data
        name = entry_data.get(CONF_NAME)

        ha = get_ha(hass, name)
        entity_manager = ha.entity_manager
        entity_manager.set_domain_component(domain, async_add_entities, component)
    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f"Failed to load {domain}, error: {ex}, line: {line_number}")


class HPPrinterEntity(Entity):
    """Representation a binary sensor that is updated by BlueIris."""

    hass: HomeAssistant = None
    integration_name: str = None
    entity: EntityData = None
    remove_dispatcher = None
    current_domain: str = None

    ha = None
    entity_manager = None
    device_manager = None

    def initialize(
        self,
        hass: HomeAssistant,
        integration_name: str,
        entity: EntityData,
        current_domain: str,
    ):
        self.hass = hass
        self.integration_name = integration_name
        self.entity = entity
        self.remove_dispatcher = None
        self.current_domain = current_domain

        self.ha = get_ha(self.hass, self.integration_name)

        if self.ha is None:
            _LOGGER.error(
                f"HPPrinterHomeAssistant was not found for {self.integration_name}"
            )

        else:
            self.entity_manager = self.ha.entity_manager
            self.device_manager = self.ha.device_manager

    @property
    def unique_id(self) -> Optional[str]:
        """Return the name of the node."""
        return self.entity.unique_id

    @property
    def device_info(self):
        return self.device_manager.get(self.entity.device_name)

    @property
    def name(self):
        """Return the name of the node."""
        return self.entity.name

    @property
    def icon(self):
        """Return the name of the node."""
        return self.entity.icon

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def device_state_attributes(self):
        """Return true if the binary sensor is on."""
        return self.entity.attributes

    async def async_added_to_hass(self):
        """Register callbacks."""
        async_dispatcher_connect(
            self.hass, SIGNALS[self.current_domain], self._schedule_immediate_update
        )

        await self.async_added_to_hass_local()

    async def async_will_remove_from_hass(self) -> None:
        if self.remove_dispatcher is not None:
            self.remove_dispatcher()
            self.remove_dispatcher = None

        await self.async_will_remove_from_hass_local()

    @callback
    def _schedule_immediate_update(self):
        self.hass.async_create_task(self._async_schedule_immediate_update())

    async def _async_schedule_immediate_update(self):
        if self.entity_manager is None:
            _LOGGER.debug(
                f"Cannot update {self.current_domain} - Entity Manager is None | {self.name}"
            )
        else:
            if self.entity is not None:
                previous_state = self.entity.state

                self.entity = self.entity_manager.get_entity(
                    self.current_domain, self.name
                )

                if self.entity is not None:
                    self._immediate_update(previous_state)

    async def async_added_to_hass_local(self):
        pass

    async def async_will_remove_from_hass_local(self):
        pass

    def _immediate_update(self, previous_state: bool):
        self.async_schedule_update_ha_state(True)
