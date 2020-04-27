from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL

from ..helpers.const import *
from ..models.config_data import ConfigData


class ConfigManager:
    data: ConfigData
    config_entry: ConfigEntry

    def update(self, config_entry: ConfigEntry):
        data = config_entry.data
        options = config_entry.options

        result = ConfigData()

        result.name = data.get(CONF_NAME)
        result.host = data.get(CONF_HOST)
        result.port = data.get(CONF_PORT, 80)
        result.ssl = data.get(CONF_SSL, False)
        result.should_store = self._get_config_data_item(
            CONF_STORE_DATA, options, data, False
        )
        result.update_interval = self._get_config_data_item(
            CONF_UPDATE_INTERVAL, options, data, 60
        )
        result.log_level = self._get_config_data_item(
            CONF_LOG_LEVEL, options, data, LOG_LEVEL_DEFAULT
        )

        self.config_entry = config_entry
        self.data = result

    @staticmethod
    def _get_config_data_item(key, options, data, default_value=None):
        data_result = data.get(key, default_value)

        result = options.get(key, data_result)

        return result
