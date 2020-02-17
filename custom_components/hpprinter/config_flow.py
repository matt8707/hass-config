"""Config flow to configure HPPrinter."""
import logging

import voluptuous as vol
from homeassistant.const import (CONF_NAME, CONF_HOST)

from homeassistant import config_entries

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

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data={
                    CONF_NAME: user_input.get(CONF_NAME, DEFAULT_NAME),
                    CONF_HOST: user_input.get(CONF_HOST)
                },
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema(fields))

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
