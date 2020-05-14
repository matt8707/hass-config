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
from ..models import AlreadyExistsError
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)
_CONF_ARR = [CONF_NAME, CONF_HOST]


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

    async def update_options(self, options: dict, update_entry: bool = False):
        new_options = {}
        validate_login = False
        config_entries = None

        if update_entry:
            config_entries = self._hass.config_entries

            data = self.config_entry.data
            name_changed = False

            for conf in _CONF_ARR:
                if data.get(conf) != options.get(conf):
                    validate_login = True

                    if conf == CONF_NAME:
                        name_changed = True

            if name_changed:
                entries = config_entries.async_entries(DOMAIN)

                for entry in entries:
                    entry_item: ConfigEntry = entry

                    if entry_item.unique_id == self.config_entry.unique_id:
                        continue

                    if options.get(CONF_NAME) == entry_item.data.get(CONF_NAME):
                        raise AlreadyExistsError(entry_item)

            new_options = {}
            for key in options:
                new_options[key] = options[key]

        if update_entry:
            for conf in _CONF_ARR:
                if conf in new_options:
                    self.data[conf] = new_options[conf]

                    del new_options[conf]

            self.options = new_options

            self._update_entry()

            if validate_login:
                errors = await self.valid_login()

                if errors is None:
                    config_entries.async_update_entry(self.config_entry, data=self.data)
                else:
                    raise LoginError(errors)

            return new_options

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
            vol.Required(CONF_NAME, default=config_data.name): str,
            vol.Required(CONF_HOST, default=config_data.host): str,
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
            await api.async_get(True)
        except LoginError as ex:
            _LOGGER.info(
                f"Unable to access {DEFAULT_NAME} ({config_data.host}), HTTP Status Code {ex.status_code}"
            )

            status_code = ex.status_code
            if status_code not in [400, 404]:
                status_code = 400

            errors = {"base": f"error_{status_code}"}

        return errors
