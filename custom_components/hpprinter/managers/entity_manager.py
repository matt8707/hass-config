import logging
import sys
from typing import Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import EntityRegistry

from ..helpers.const import *
from ..managers.HPDeviceData import HPDeviceData
from ..models.config_data import ConfigData
from ..models.entity_data import EntityData

_LOGGER = logging.getLogger(__name__)


def _get_camera_binary_sensor_key(topic, event_type):
    key = f"{topic}_{event_type}".lower()

    return key


class EntityManager:
    hass: HomeAssistant
    ha = None
    entities: dict
    domain_component_manager: dict

    def __init__(self, hass, ha):
        self.hass = hass
        self.ha = ha
        self.domain_component_manager = {}
        self.entities = {}

    @property
    def data_manager(self) -> HPDeviceData:
        return self.ha.data_manager

    @property
    def data(self):
        return self.data_manager.device_data

    @property
    def entity_registry(self) -> EntityRegistry:
        return self.ha.entity_registry

    @property
    def config_data(self) -> ConfigData:
        return self.ha.config_data

    def set_domain_component(self, domain, async_add_entities, component):
        self.domain_component_manager[domain] = {
            "async_add_entities": async_add_entities,
            "component": component,
        }

    def is_device_name_in_use(self, device_name):
        result = False

        for entity in self.get_all_entities():
            if entity.device_name == device_name:
                result = True
                break

        return result

    def get_all_entities(self) -> List[EntityData]:
        entities = []
        for domain in self.entities:
            for name in self.entities[domain]:
                entity = self.entities[domain][name]

                entities.append(entity)

        return entities

    def check_domain(self, domain):
        if domain not in self.entities:
            self.entities[domain] = {}

    def get_entities(self, domain) -> Dict[str, EntityData]:
        self.check_domain(domain)

        return self.entities[domain]

    def get_entity(self, domain, name) -> Optional[EntityData]:
        entities = self.get_entities(domain)
        entity = entities.get(name)

        return entity

    def get_entity_status(self, domain, name):
        entity = self.get_entity(domain, name)

        status = ENTITY_STATUS_EMPTY if entity is None else entity.status

        return status

    def set_entity_status(self, domain, name, status):
        if domain in self.entities and name in self.entities[domain]:
            self.entities[domain][name].status = status

    def delete_entity(self, domain, name):
        if domain in self.entities and name in self.entities[domain]:
            del self.entities[domain][name]

    def set_entity(self, domain, name, data: EntityData):
        try:
            self.check_domain(domain)

            self.entities[domain][name] = data
        except Exception as ex:
            self.log_exception(
                ex, f"Failed to set_entity, domain: {domain}, name: {name}"
            )

    async def create_components(self):
        cartridges_data = self.data.get(HP_DEVICE_CARTRIDGES)

        self.create_status_binary_sensor()
        self.create_status_sensor()
        self.create_printer_sensor()
        self.create_scanner_sensor()

        if cartridges_data is not None:
            for key in cartridges_data:
                cartridge = cartridges_data.get(key)

                if cartridge is not None:
                    self.create_cartridge_sensor(cartridge, key)

    def update(self):
        self.hass.async_create_task(self._async_update())

    async def _async_update(self):
        step = "Mark as ignore"
        try:
            entities_to_delete = []

            for entity in self.get_all_entities():
                entities_to_delete.append(entity.unique_id)

            step = "Create components"

            await self.create_components()

            step = "Start updating"

            for domain in SIGNALS:
                step = f"Start updating domain {domain}"

                entities_to_add = []
                domain_component_manager = self.domain_component_manager[domain]
                domain_component = domain_component_manager["component"]
                async_add_entities = domain_component_manager["async_add_entities"]

                entities = dict(self.get_entities(domain))

                for entity_key in entities:
                    step = f"Start updating {domain} -> {entity_key}"

                    entity = entities[entity_key]

                    entity_id = self.entity_registry.async_get_entity_id(
                        domain, DOMAIN, entity.unique_id
                    )

                    if entity.status == ENTITY_STATUS_CREATED:
                        if entity.unique_id in entities_to_delete:
                            entities_to_delete.remove(entity.unique_id)

                        step = f"Mark as created - {domain} -> {entity_key}"

                        entity_component = domain_component(
                            self.hass, self.config_data.name, entity
                        )

                        if entity_id is not None:
                            entity_component.entity_id = entity_id

                            state = self.hass.states.get(entity_id)

                            if state is None:
                                restored = True
                            else:
                                restored = state.attributes.get("restored", False)

                                if restored:
                                    _LOGGER.info(
                                        f"Entity {entity.name} restored | {entity_id}"
                                    )

                            if restored:
                                entity_item = self.entity_registry.async_get(entity_id)

                                if entity_item is None or not entity_item.disabled:
                                    entities_to_add.append(entity_component)
                        else:
                            entities_to_add.append(entity_component)

                        entity.status = ENTITY_STATUS_READY

                step = f"Add entities to {domain}"

                if len(entities_to_add) > 0:
                    async_add_entities(entities_to_add, True)

            if len(entities_to_delete) > 0:
                _LOGGER.info(f"Following items will be deleted: {entities_to_delete}")

                for domain in SIGNALS:
                    entities = dict(self.get_entities(domain))

                    for entity_key in entities:
                        entity = entities[entity_key]
                        if entity.unique_id in entities_to_delete:
                            await self.ha.delete_entity(domain, entity.name)

        except Exception as ex:
            self.log_exception(ex, f"Failed to update, step: {step}")

    def create_status_sensor(self):
        status = self.data.get(PRINTER_CURRENT_STATUS, "Off")

        name = self.data.get("Name", DEFAULT_NAME)
        entity_name = f"{name} {HP_DEVICE_STATUS}"

        device_name = DEFAULT_NAME
        unique_id = entity_name

        icon = self.get_printer_icon()

        attributes = {"friendly_name": entity_name, "device_class": "connectivity"}

        entity = EntityData()

        entity.unique_id = unique_id
        entity.name = entity_name
        entity.attributes = attributes
        entity.icon = icon
        entity.device_name = device_name
        entity.state = status

        self.set_entity(DOMAIN_SENSOR, entity_name, entity)

    def get_printer_name(self):
        printer_name = self.data.get("Name", DEFAULT_NAME)

        return printer_name

    def is_online(self):
        is_online = self.data.get(HP_DEVICE_IS_ONLINE, False)

        return is_online

    def get_printer_icon(self):
        is_online = self.is_online()

        icon = "mdi:printer" if is_online else "mdi:printer-off"

        return icon

    def create_status_binary_sensor(self):
        is_online = self.is_online()

        name = self.data.get("Name", DEFAULT_NAME)
        entity_name = f"{name} {HP_DEVICE_CONNECTIVITY}"
        unique_id = f"{DEFAULT_NAME}-{DOMAIN_BINARY_SENSOR}-{entity_name}"
        device_name = DEFAULT_NAME
        icon = self.get_printer_icon()

        attributes = {"friendly_name": entity_name, "device_class": "connectivity"}

        entity = EntityData()

        entity.unique_id = unique_id
        entity.name = entity_name
        entity.attributes = attributes
        entity.icon = icon
        entity.device_name = device_name
        entity.state = is_online

        self.set_entity(DOMAIN_BINARY_SENSOR, entity_name, entity)

    def create_printer_sensor(self):
        printer_data = self.data.get(HP_DEVICE_PRINTER)

        if printer_data is not None:
            name = self.get_printer_name()
            entity_name = f"{name} {HP_DEVICE_PRINTER}"
            unique_id = f"{DEFAULT_NAME}-{DOMAIN_SENSOR}-{entity_name}"
            device_name = DEFAULT_NAME

            state = printer_data.get(HP_DEVICE_PRINTER_STATE)

            attributes = {"unit_of_measurement": "Pages", "friendly_name": entity_name}

            for key in printer_data:
                if key != HP_DEVICE_PRINTER_STATE:
                    attributes[key] = printer_data[key]

            entity = EntityData()

            entity.unique_id = unique_id
            entity.name = entity_name
            entity.attributes = attributes
            entity.icon = PAGES_ICON
            entity.device_name = device_name
            entity.state = state

            self.set_entity(DOMAIN_SENSOR, entity_name, entity)

    def create_scanner_sensor(self):
        scanner_data = self.data.get(HP_DEVICE_SCANNER)

        if scanner_data is not None:
            name = self.get_printer_name()
            entity_name = f"{name} {HP_DEVICE_SCANNER}"
            unique_id = f"{DEFAULT_NAME}-{DOMAIN_SENSOR}-{entity_name}"
            device_name = DEFAULT_NAME

            state = scanner_data.get(HP_DEVICE_SCANNER_STATE)

            attributes = {"unit_of_measurement": "Pages", "friendly_name": entity_name}

            for key in scanner_data:
                if key != HP_DEVICE_SCANNER_STATE:
                    attributes[key] = scanner_data[key]

            entity = EntityData()

            entity.unique_id = unique_id
            entity.name = entity_name
            entity.attributes = attributes
            entity.icon = SCANNER_ICON
            entity.device_name = device_name
            entity.state = state

            self.set_entity(DOMAIN_SENSOR, entity_name, entity)

    def create_cartridge_sensor(self, cartridge, key):
        name = self.get_printer_name()
        entity_name = f"{name} {key}"
        unique_id = f"{DEFAULT_NAME}-{DOMAIN_SENSOR}-{entity_name}"
        device_name = DEFAULT_NAME

        state = cartridge.get(HP_DEVICE_CARTRIDGE_STATE, 0)

        attributes = {"unit_of_measurement": "%", "friendly_name": entity_name}

        for key in cartridge:
            if key != HP_DEVICE_CARTRIDGE_STATE:
                attributes[key] = cartridge[key]

        entity = EntityData()

        entity.unique_id = unique_id
        entity.name = entity_name
        entity.attributes = attributes
        entity.icon = INK_ICON
        entity.device_name = device_name
        entity.state = state

        self.set_entity(DOMAIN_SENSOR, entity_name, entity)

    @staticmethod
    def log_exception(ex, message):
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f"{message}, Error: {str(ex)}, Line: {line_number}")
