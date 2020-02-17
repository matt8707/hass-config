"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
import sys
import logging

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
        self._binary_sensors = {}
        self._sensors = {}
        self._config_entry = config_entry
        self._components_hash = None
        self._remove_async_track_time = None

    @property
    def name(self):
        return self._name

    @property
    def sensors(self):
        return self._sensors

    @property
    def binary_sensors(self):
        return self._binary_sensors

    def get_sensor(self, name):
        return self._sensors.get(name)

    def get_binary_sensor(self, name):
        return self._binary_sensors.get(name)

    def initialize(self):
        if self._hp_data is not None:
            async_call_later(self._hass, 5, self.async_finalize)

    async def async_finalize(self, event_time):
        _LOGGER.debug(f"async_finalize called at {event_time}")

        self._hass.services.async_register(DOMAIN, 'save_debug_data', self.save_debug_data)

        await self.async_update(None)

        self._remove_async_track_time = async_track_time_interval(self._hass, self.async_update, SCAN_INTERVAL)

    async def async_remove(self):
        _LOGGER.debug(f"async_remove called")

        self._hass.services.async_remove(DOMAIN, 'save_debug_data')

        if self._remove_async_track_time is not None:
            self._remove_async_track_time()

    def save_debug_data(self, service_data):
        """Call BlueIris to refresh information."""
        _LOGGER.debug(f"Saving debug data {DOMAIN} ({service_data})")

        self._hp_data.get_data(self.store_data)

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
        _LOGGER.info(f"Updating")

        data = await self._hp_data.get_data()

        cartridges_data = data.get(HP_DEVICE_CARTRIDGES)

        is_online = self.create_status_sensor(data)

        if is_online:
            self.create_printer_sensor(data)
            self.create_scanner_sensor(data)

            if cartridges_data is not None:
                for key in cartridges_data:
                    cartridge = cartridges_data.get(key)

                    if cartridge is not None:
                        self.create_cartridge_sensor(data, cartridge, key)

        previous_hash = self._components_hash

        entities = []
        for binary_sensor_name in self._binary_sensors:
            entities.append(binary_sensor_name)

        for sensor_name in self._sensors:
            entities.append(sensor_name)

        self._components_hash = ', '.join(entities)

        hash_changed = previous_hash is None or previous_hash != self._components_hash

        _LOGGER.info(f"Hash: {self._components_hash}, Previous Hash: {previous_hash}, changed: {hash_changed}")

        if hash_changed:
            entry = self._config_entry

            if previous_hash is not None:
                unload = self._hass.config_entries.async_forward_entry_unload

                self._hass.async_create_task(unload(entry, DOMAIN_BINARY_SENSOR))
                self._hass.async_create_task(unload(entry, DOMAIN_SENSOR))

            if self._components_hash is not None:
                setup = self._hass.config_entries.async_forward_entry_setup

                self._hass.async_create_task(setup(entry, DOMAIN_BINARY_SENSOR))
                self._hass.async_create_task(setup(entry, DOMAIN_SENSOR))
        else:
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_HP_PRINTER)

    def create_status_sensor(self, data):
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

        self._binary_sensors[sensor_name] = entity

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

            self._sensors[sensor_name] = entity

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

            self._sensors[sensor_name] = entity

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

        self._sensors[sensor_name] = entity


def _get_printers(hass: HomeAssistant):
    if DATA_HP_PRINTER not in hass.data:
        hass.data[DATA_HP_PRINTER] = {}

    printers = hass.data[DATA_HP_PRINTER]

    return printers
