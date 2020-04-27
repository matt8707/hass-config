"""Storage handers."""
import logging

from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.storage import Store
from homeassistant.util import slugify

from ..helpers.const import *
from ..models.config_data import ConfigData
from .configuration_manager import ConfigManager

STORAGE_VERSION = 1

_LOGGER = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, hass, config_manager: ConfigManager):
        self._hass = hass
        self._config_manager = config_manager

    @property
    def config_data(self) -> ConfigData:
        config_data = None

        if self._config_manager is not None:
            config_data = self._config_manager.data

        return config_data

    @property
    def file_name(self):
        file_name = f".{DOMAIN}.{slugify(self.config_data.name)}"

        return file_name

    async def async_load_from_store(self):
        """Load the retained data from store and return de-serialized data."""
        store = Store(self._hass, STORAGE_VERSION, self.file_name, encoder=JSONEncoder)

        data = await store.async_load()

        return data

    async def async_save_to_store(self, data):
        """Generate dynamic data to store and save it to the filesystem."""
        store = Store(self._hass, STORAGE_VERSION, self.file_name, encoder=JSONEncoder)

        await store.async_save(data)
