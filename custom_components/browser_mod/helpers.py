import logging

from homeassistant.helpers.entity import Entity, async_generate_entity_id

from .const import (
    DOMAIN,
    DATA_DEVICES,
    DATA_ALIASES,
    DATA_ADDERS,
    CONFIG_DEVICES,
    DATA_CONFIG,
    CONFIG_PREFIX,
    CONFIG_DISABLE,
    CONFIG_DISABLE_ALL,
    DATA_SETUP_COMPLETE,
)

_LOGGER = logging.getLogger(__name__)


def get_devices(hass):
    return hass.data[DOMAIN][DATA_DEVICES]


def get_alias(hass, deviceID):
    for k, v in hass.data[DOMAIN][DATA_ALIASES].items():
        if v == deviceID:
            return k
    return None


def get_config(hass, deviceID):
    config = hass.data[DOMAIN][DATA_CONFIG].get(CONFIG_DEVICES, {})
    return config.get(deviceID, config.get(deviceID.replace("-", "_"), {}))


def create_entity(hass, platform, deviceID, connection):
    conf = get_config(hass, deviceID)
    if conf and (
        platform in conf.get(CONFIG_DISABLE, [])
        or CONFIG_DISABLE_ALL in conf.get(CONFIG_DISABLE, [])
    ):
        return None
    if not conf and (
        platform in hass.data[DOMAIN][DATA_CONFIG].get(CONFIG_DISABLE, [])
        or CONFIG_DISABLE_ALL in hass.data[DOMAIN][DATA_CONFIG].get(CONFIG_DISABLE, [])
    ):
        return None
    adder = hass.data[DOMAIN][DATA_ADDERS][platform]
    entity = adder(hass, deviceID, connection, get_alias(hass, deviceID))
    return entity


def setup_platform(hass, config, async_add_devices, platform, cls):
    if platform in hass.data[DOMAIN][DATA_ADDERS]:
        return True

    def adder(hass, deviceID, connection, alias=None):
        entity = cls(hass, connection, deviceID, alias)
        async_add_devices([entity])
        return entity

    hass.data[DOMAIN][DATA_ADDERS][platform] = adder
    return True


def is_setup_complete(hass):
    return hass.data[DOMAIN][DATA_SETUP_COMPLETE]


class BrowserModEntity(Entity):
    def __init__(self, hass, connection, deviceID, alias=None):
        self.hass = hass
        self.connection = connection
        self.deviceID = deviceID
        self._data = {}
        self._alias = alias
        prefix = hass.data[DOMAIN][DATA_CONFIG].get(CONFIG_PREFIX, "")
        self.entity_id = async_generate_entity_id(
            self.domain + ".{}", alias or f"{prefix}{deviceID}", hass=hass
        )

    def updated(self):
        pass

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.deviceID)},
            "name": self._alias or self.deviceID,
        }

    @property
    def unique_id(self):
        return f"{self.domain}-{self.deviceID}"

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.updated()

    @property
    def device_id(self):
        return self.deviceID

    def send(self, command, **kwargs):
        self.connection.send(command, **kwargs)
