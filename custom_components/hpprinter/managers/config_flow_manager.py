import logging
from typing import Optional

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers import config_validation as cv

from .. import LoginError
from ..api.HPPrinterAPI import ProductConfigDynDataAPI
from ..helpers.const import *
from ..managers.configuration_manager import ConfigManager
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)


class ConfigFlowManager:
    config_manager: ConfigManager
    options: Optional[dict]
    data: Optional[dict]
    config_entry: ConfigEntry

    def __init__(self, config_entry: Optional[ConfigEntry] = None):
        self.config_entry = config_entry

        self.options = None
        self.data = None
        self._pre_config = False

        if config_entry is not None:
            self._pre_config = True

            self.update_data(self.config_entry.data)
            self.update_options(self.config_entry.options)

        self._is_initialized = True
        self._auth_error = False
        self._hass = None

    def initialize(self, hass):
        self._hass = hass

        if not self._pre_config:
            self.options = {}
            self.data = {}

        self.config_manager = ConfigManager()

        self._update_entry()

    @property
    def config_data(self) -> ConfigData:
        return self.config_manager.data

    def update_options(self, options: dict, update_entry: bool = False):
        if options is not None:
            new_options = {}
            for key in options:
                new_options[key] = options[key]

            self.options = new_options
        else:
            self.options = {}

        if update_entry:
            self._update_entry()

    def update_data(self, data: dict, update_entry: bool = False):
        new_data = None

        if data is not None:
            new_data = {}
            for key in data:
                new_data[key] = data[key]

        self.data = new_data

        if update_entry:
            self._update_entry()

    def _update_entry(self):
        entry = ConfigEntry(0, "", "", self.data, "", "", {}, options=self.options)

        self.config_manager.update(entry)

    @staticmethod
    def get_default_data():
        fields = {
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_HOST): str,
        }

        data_schema = vol.Schema(fields)

        return data_schema

    def get_default_options(self):
        config_data = self.config_data

        fields = {
            vol.Optional(CONF_STORE_DATA, default=config_data.should_store): bool,
            vol.Required(
                CONF_UPDATE_INTERVAL, default=config_data.update_interval
            ): cv.positive_int,
            vol.Required(CONF_LOG_LEVEL, default=config_data.log_level): vol.In(
                LOG_LEVELS
            ),
        }

        data_schema = vol.Schema(fields)

        return data_schema

    async def valid_login(self):
        errors = None

        config_data = self.config_manager.data

        api = ProductConfigDynDataAPI(self._hass, self.config_manager)

        try:
            if await api.async_get(True) is None:
                _LOGGER.warning(f"Failed to access {DEFAULT_NAME} ({config_data.host})")
                errors = {"base": "error_400"}
        except LoginError as ex:
            _LOGGER.warning(
                f"Failed to access {DEFAULT_NAME} ({config_data.host}) due to error {ex.status_code}"
            )

            status_code = ex.status_code
            if status_code not in [400, 404]:
                status_code = 400

            errors = {"base": f"error_{status_code}"}

        return {"logged-in": errors is None, "errors": errors}
