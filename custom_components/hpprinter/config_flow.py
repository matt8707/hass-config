"""Config flow to configure HPPrinter."""
import logging

import voluptuous as vol
from homeassistant.const import (CONF_NAME, CONF_HOST)

from homeassistant import config_entries

from custom_components.hpprinter import ProductUsageDynPrinterDataAPI
from .const import *

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class HPPrinterFlowHandler(config_entries.ConfigFlow):
    """Handle a HPPrinter config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow start."""
        _LOGGER.debug(f"Starting async_step_user of {DOMAIN}")

        fields = {
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_HOST): str
        }

        errors = None

        if user_input is not None:

            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            host = user_input.get(CONF_HOST)

            usage_data_manager = ProductUsageDynPrinterDataAPI(self.hass, host)
            usage_data_manager.initialize()

            if await usage_data_manager.get_data() is None:
                _LOGGER.warning(f"Failed to access HP Printer ({name})")

                errors = {
                    "base": "cannot_reach_printer"
                }

            if errors is None:
                data = {
                        CONF_NAME: name,
                        CONF_HOST: host
                    }

                return self.async_create_entry(title=name, data=data)

        return self.async_show_form(step_id="user", data_schema=vol.Schema(fields), errors=errors)

    async def async_step_import(self, info):
        """Import existing configuration from Z-Wave."""
        _LOGGER.debug(f"Starting async_step_import of {DOMAIN}")

        return self.async_create_entry(
            title="HPPrinter (import from configuration.yaml)",
            data={
                CONF_NAME: info.get(CONF_NAME, DEFAULT_NAME),
                CONF_HOST: info.get(CONF_HOST)
            },
        )
