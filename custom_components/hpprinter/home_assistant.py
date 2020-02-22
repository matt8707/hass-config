"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
from datetime import datetime
import sys
import logging

from homeassistant.helpers import device_registry as dr
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later, async_track_time_interval
from homeassistant.helpers.dispatcher import async_dispatcher_send

from custom_components.hpprinter import HPDeviceData
from .const import *

_LOGGER = logging.getLogger(__name__)


class HPPrinterHomeAssistant:
    def __init__(self, hass, name, host, config_entry):
        self._scan_interval = SCAN_INTERVAL
        self._hass = hass
        self._name = name
        self._hp_data = HPDeviceData(hass, host, name)
        self._entities = {}
        self._domain_loaded = {}
        self._config_entry = config_entry
        self._components_hash = None
        self._remove_async_track_time = None
        self._unload_domain = []
        self._load_domain = []
        self._should_reload = False
        self._last_update = None
        self._is_first_time_online = True

    @property
    def name(self):
        return self._name

    def initialize(self):
        if self._hp_data is not None:
            async_call_later(self._hass, 5, self.async_finalize)

    async def async_finalize(self, event_time):
        _LOGGER.debug(f"async_finalize called at {event_time}")

        self._hass.services.async_register(DOMAIN, 'save_debug_data', self.save_debug_data)

        self._remove_async_track_time = async_track_time_interval(self._hass, self.async_update, SCAN_INTERVAL)

        self._hass.async_create_task(self.async_init_entry())

    async def async_remove(self):
        _LOGGER.debug(f"async_remove called")

        self._hass.services.async_remove(DOMAIN, 'save_debug_data')

        if self._remove_async_track_time is not None:
            self._remove_async_track_time()

        unload = self._hass.config_entries.async_forward_entry_unload

        self._hass.async_create_task(unload(self._config_entry, DOMAIN_BINARY_SENSOR))
        self._hass.async_create_task(unload(self._config_entry, DOMAIN_SENSOR))

    async def async_update_entry(self, entry, clear_all):
        _LOGGER.info(f"async_update_entry: {entry}")

        self._config_entry = entry
        self._last_update = datetime.now()

        self._load_domain = []
        self._unload_domain = []

        if clear_all:
            device_reg = await dr.async_get_registry(self._hass)
            device_reg.async_clear_config_entry(self._config_entry.entry_id)

        for domain in [DOMAIN_SENSOR, DOMAIN_BINARY_SENSOR]:
            has_entities = self._domain_loaded.get(domain, False)

            if domain not in self._load_domain:
                self._load_domain.append(domain)

            if has_entities and domain not in self._unload_domain:
                self._unload_domain.append(domain)

        if clear_all:
            await self.async_update(datetime.now())

    async def async_init_entry(self):
        _LOGGER.debug(f"async_init_entry called")

        await self.async_update_entry(self._config_entry, True)

    def set_domain_entities_state(self, domain, has_entities):
        self._domain_loaded[domain] = has_entities

    def get_entities(self, domain):
        return self._entities.get(domain, {})

    def get_entity(self, domain, name):
        entities = self.get_entities(domain)
        entity = {}
        if entities is not None:
            entity = entities.get(name, {})

        return entity

    def set_entity(self, domain, name, data):
        entities = self._entities.get(domain)

        if entities is None:
            self._entities[domain] = {}

            entities = self._entities.get(domain)

        entities[name] = data

    def save_debug_data(self, service_data):
        """Call BlueIris to refresh information."""
        _LOGGER.debug(f"Saving debug data {DOMAIN} ({service_data})")

        self._hass.async_create_task(self._hp_data.get_data(self.store_data))

    def store_data(self, file, content):
        try:
            path = self._hass.config.path(file)

            with open(path, 'w+') as out:
                out.write(content)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to log {file} data, Error: {ex}, Line: {line_number}')

    async def async_update(self, event_time):
        _LOGGER.info(f"Updating {event_time}")

        data = await self._hp_data.get_data()

        cartridges_data = data.get(HP_DEVICE_CARTRIDGES)

        is_online = self.create_status_binary_sensor(data)

        self.create_status_sensor(data)

        if is_online:
            self.create_printer_sensor(data)
            self.create_scanner_sensor(data)

            if cartridges_data is not None:
                for key in cartridges_data:
                    cartridge = cartridges_data.get(key)

                    if cartridge is not None:
                        self.create_cartridge_sensor(data, cartridge, key)

        if self._is_first_time_online:
            self._is_first_time_online = False

            await self.async_update_entry(self._config_entry, False)

        await self.discover_all()

    async def discover_all(self):
        for domain in [DOMAIN_SENSOR, DOMAIN_BINARY_SENSOR]:
            await self.discover(domain)

    async def discover(self, domain):
        signal = SIGNALS.get(domain)

        if signal is None:
            _LOGGER.error(f"Cannot discover domain {domain}")
            return

        unload = self._hass.config_entries.async_forward_entry_unload
        setup = self._hass.config_entries.async_forward_entry_setup

        entry = self._config_entry

        can_unload = domain in self._unload_domain
        can_load = domain in self._load_domain
        can_notify = not can_load and not can_unload

        if can_unload:
            _LOGGER.info(f"Unloading domain {domain}")

            self._hass.async_create_task(unload(entry, domain))
            self._unload_domain.remove(domain)

        if can_load:
            _LOGGER.info(f"Loading domain {domain}")

            self._hass.async_create_task(setup(entry, domain))
            self._load_domain.remove(domain)

        if can_notify:
            async_dispatcher_send(self._hass, signal)

    def create_status_sensor(self, data):
        is_online = data.get(HP_DEVICE_IS_ONLINE, False)
        status = data.get(PRINTER_CURRENT_STATUS, "Off")
        model = data.get(ENTITY_MODEL)

        name = data.get("Name", DEFAULT_NAME)
        sensor_name = f"{name} {HP_DEVICE_STATUS}"

        icon = "mdi:printer" if is_online else "mdi:printer-off"

        attributes = {
            "friendly_name": sensor_name,
            "device_class": "connectivity"
        }

        entity = {
            ENTITY_NAME: sensor_name,
            ENTITY_STATE: status,
            ENTITY_ATTRIBUTES: attributes,
            ENTITY_ICON: icon,
            ENTITY_MODEL: model
        }

        self.set_entity(DOMAIN_SENSOR, sensor_name, entity)

    def create_status_binary_sensor(self, data):
        is_online = data.get(HP_DEVICE_IS_ONLINE, False)
        model = data.get(ENTITY_MODEL)

        name = data.get("Name", DEFAULT_NAME)
        sensor_name = f"{name} {HP_DEVICE_STATUS}"

        icon = "mdi:printer-off"

        if is_online:
            icon = "mdi:printer"

        attributes = {
            "friendly_name": sensor_name,
            "device_class": "connectivity"
        }

        entity = {
            ENTITY_NAME: sensor_name,
            ENTITY_STATE: is_online,
            ENTITY_ATTRIBUTES: attributes,
            ENTITY_ICON: icon,
            ENTITY_MODEL: model
        }

        self.set_entity(DOMAIN_BINARY_SENSOR, sensor_name, entity)

        return is_online

    def create_printer_sensor(self, data):
        printer_data = data.get(HP_DEVICE_PRINTER)
        model = data.get(ENTITY_MODEL)

        if printer_data is not None:
            name = data.get("Name", DEFAULT_NAME)
            sensor_name = f"{name} {HP_DEVICE_PRINTER}"

            state = printer_data.get(HP_DEVICE_PRINTER_STATE)

            attributes = {
                "unit_of_measurement": "Pages",
                "friendly_name": sensor_name
            }

            for key in printer_data:
                if key != HP_DEVICE_PRINTER_STATE:
                    attributes[key] = printer_data[key]

            entity = {
                ENTITY_NAME: sensor_name,
                ENTITY_STATE: state,
                ENTITY_ATTRIBUTES: attributes,
                ENTITY_ICON: PAGES_ICON,
                ENTITY_MODEL: model
            }

            self.set_entity(DOMAIN_SENSOR, sensor_name, entity)

    def create_scanner_sensor(self, data):
        scanner_data = data.get(HP_DEVICE_SCANNER)
        model = data.get(ENTITY_MODEL)

        if scanner_data is not None:
            name = data.get("Name", DEFAULT_NAME)
            sensor_name = f"{name} {HP_DEVICE_SCANNER}"

            state = scanner_data.get(HP_DEVICE_SCANNER_STATE)

            attributes = {
                "unit_of_measurement": "Pages",
                "friendly_name": sensor_name
            }

            for key in scanner_data:
                if key != HP_DEVICE_SCANNER_STATE:
                    attributes[key] = scanner_data[key]

            entity = {
                ENTITY_NAME: sensor_name,
                ENTITY_STATE: state,
                ENTITY_ATTRIBUTES: attributes,
                ENTITY_ICON: SCANNER_ICON,
                ENTITY_MODEL: model
            }

            self.set_entity(DOMAIN_SENSOR, sensor_name, entity)

    def create_cartridge_sensor(self, data, cartridge, key):
        name = data.get("Name", DEFAULT_NAME)
        model = data.get(ENTITY_MODEL)
        sensor_name = f"{name} {key}"

        state = cartridge.get(HP_DEVICE_CARTRIDGE_STATE, 0)

        attributes = {
            "unit_of_measurement": "%",
            "friendly_name": sensor_name
        }

        for key in cartridge:
            if key != HP_DEVICE_CARTRIDGE_STATE:
                attributes[key] = cartridge[key]

        entity = {
            ENTITY_NAME: sensor_name,
            ENTITY_STATE: state,
            ENTITY_ATTRIBUTES: attributes,
            ENTITY_ICON: INK_ICON,
            ENTITY_MODEL: model
        }

        self.set_entity(DOMAIN_SENSOR, sensor_name, entity)


def _get_printer(hass: HomeAssistant, name) -> HPPrinterHomeAssistant:
    if DATA_HP_PRINTER not in hass.data:
        hass.data[DATA_HP_PRINTER] = {}

    printers = hass.data[DATA_HP_PRINTER]
    printer = None

    if name in printers:
        printer = printers[name]

    return printer
