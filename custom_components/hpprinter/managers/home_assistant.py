"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
from datetime import datetime, timedelta
import logging
import sys
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity_registry import (
    EntityRegistry,
    async_get_registry as er_async_get_registry,
)
from homeassistant.helpers.event import async_call_later, async_track_time_interval

from ..helpers.const import *
from ..managers.HPDeviceData import HPDeviceData
from ..managers.configuration_manager import ConfigManager
from ..managers.device_manager import DeviceManager
from ..managers.entity_manager import EntityManager
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)


class HPPrinterHomeAssistant:
    def __init__(self, hass: HomeAssistant):
        self._hass = hass

        self._remove_async_track_time = None

        self._is_initialized = False
        self._is_updating = False

        self._entity_registry = None

        self._api = None
        self._entity_manager = None
        self._device_manager = None
        self._data_manager = None

        self._config_manager = ConfigManager()

        def update_entities(now):
            self._hass.async_create_task(self.async_update(now))

        self._update_entities = update_entities

    @property
    def data(self):
        return self._data_manager.device_data

    @property
    def data_manager(self) -> HPDeviceData:
        return self._data_manager

    @property
    def entity_manager(self) -> EntityManager:
        return self._entity_manager

    @property
    def device_manager(self) -> DeviceManager:
        return self._device_manager

    @property
    def entity_registry(self) -> EntityRegistry:
        return self._entity_registry

    @property
    def config_data(self) -> Optional[ConfigData]:
        if self._config_manager is not None:
            return self._config_manager.data

        return None

    async def async_init(self, entry: ConfigEntry):
        try:
            self._config_manager.update(entry)

            self._data_manager = HPDeviceData(self._hass, self._config_manager)
            self._entity_manager = EntityManager(self._hass, self)
            self._device_manager = DeviceManager(self._hass, self)

            await self._data_manager.initialize()

            def internal_async_init(now):
                self._hass.async_create_task(self._async_init(now))

            self._entity_registry = await er_async_get_registry(self._hass)

            async_call_later(self._hass, 2, internal_async_init)

            self._is_initialized = True
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f"Failed to async_init, error: {ex}, line: {line_number}")

    async def _async_init(self, event_time):
        if not self._is_initialized:
            _LOGGER.info(
                f"NOT INITIALIZED - Failed finalizing initialization of integration ({self.config_data.host})"
            )
            return

        _LOGGER.info(
            f"Finalizing initialization of integration ({self.config_data.host}) at {event_time}"
        )

        load = self._hass.config_entries.async_forward_entry_setup

        for domain in SIGNALS:
            self._hass.async_create_task(
                load(self._config_manager.config_entry, domain)
            )

        await self.async_update_entry()

    async def async_update_entry(self, entry: ConfigEntry = None):
        is_update = entry is not None

        if is_update:
            _LOGGER.info(f"Handling ConfigEntry change: {entry.as_dict()}")

            previous_interval = self.config_data.update_interval

            self._config_manager.update(entry)

            current_interval = self.config_data.update_interval

            is_interval_changed = previous_interval != current_interval

            if is_interval_changed and self._remove_async_track_time is not None:
                msg = f"ConfigEntry interval changed from {previous_interval} to {current_interval}"
                _LOGGER.info(msg)

                self._remove_async_track_time()
                self._remove_async_track_time = None
        else:
            entry = self._config_manager.config_entry

            _LOGGER.info(f"Handling ConfigEntry initialization: {entry.as_dict()}")

            current_interval = self.config_data.update_interval

        if self._remove_async_track_time is None:
            interval = timedelta(seconds=current_interval)

            self._remove_async_track_time = async_track_time_interval(
                self._hass, self._update_entities, interval
            )

        await self.async_update(datetime.now())

    async def async_remove(self):
        _LOGGER.info(f"Removing current integration - {self.config_data.host}")

        if self._remove_async_track_time is not None:
            self._remove_async_track_time()
            self._remove_async_track_time = None

        unload = self._hass.config_entries.async_forward_entry_unload

        for domain in SIGNALS:
            self._hass.async_create_task(
                unload(self._config_manager.config_entry, domain)
            )

        await self._device_manager.async_remove()

        _LOGGER.info(f"Current integration ({self.config_data.host}) removed")

    async def async_update(self, event_time):
        if not self._is_initialized:
            _LOGGER.info(f"NOT INITIALIZED - Failed updating @{event_time}")
            return

        try:
            if self._is_updating:
                _LOGGER.debug(f"Skip updating @{event_time}")
                return

            _LOGGER.debug(f"Updating @{event_time}")

            self._is_updating = True

            await self.data_manager.update()

            self.device_manager.update()
            self.entity_manager.update()

            await self.dispatch_all()
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f"Failed to async_update, Error: {ex}, Line: {line_number}")

        self._is_updating = False

    async def delete_entity(self, domain, name):
        try:
            entity = self.entity_manager.get_entity(domain, name)
            device_name = entity.device_name
            unique_id = entity.unique_id

            self.entity_manager.delete_entity(domain, name)

            device_in_use = self.entity_manager.is_device_name_in_use(device_name)

            entity_id = self.entity_registry.async_get_entity_id(
                domain, DOMAIN, unique_id
            )
            self.entity_registry.async_remove(entity_id)

            if not device_in_use:
                await self.device_manager.delete_device(device_name)
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f"Failed to delete_entity, Error: {ex}, Line: {line_number}")

    async def dispatch_all(self):
        if not self._is_initialized:
            _LOGGER.info(f"NOT INITIALIZED - Failed discovering components")
            return

        for domain in SIGNALS:
            signal = SIGNALS.get(domain)

            async_dispatcher_send(self._hass, signal)
