"""Config flow to configure HPPrinter."""
import logging

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from .helpers import get_ha
from .helpers.const import *
from .managers.config_flow_manager import ConfigFlowManager

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class HPPrinterFlowHandler(config_entries.ConfigFlow):
    """Handle a HPPrinter config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        super().__init__()

        self._config_flow = ConfigFlowManager()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return HPPrinterOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow start."""
        _LOGGER.debug(f"Starting async_step_user of {DOMAIN}")

        errors = None

        self._config_flow.initialize(self.hass)

        if user_input is not None:
            self._config_flow.update_data(user_input, True)

            name = self._config_flow.config_data.name

            ha = get_ha(self.hass, name)

            if ha is None:
                result = await self._config_flow.valid_login()
                errors = result.get("errors")
            else:
                _LOGGER.warning(f"{DEFAULT_NAME} ({name}) already configured")

                return self.async_abort(
                    reason="already_configured", description_placeholders=user_input
                )

            if errors is None:
                _LOGGER.info(f"Storing configuration data: {user_input}")

                return self.async_create_entry(title=name, data=user_input)

        data_schema = self._config_flow.get_default_data()

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_import(self, info):
        """Import existing configuration from Z-Wave."""
        _LOGGER.debug(f"Starting async_step_import of {DOMAIN}")

        return self.async_create_entry(
            title="HPPrinter (import from configuration.yaml)", data=info,
        )


class HPPrinterOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle HP Printer options."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize HP Printer options flow."""
        super().__init__()

        self._config_flow = ConfigFlowManager(config_entry)

    async def async_step_init(self, user_input=None):
        """Manage the HP Printer options."""
        return await self.async_step_hp_printer_additional_settings(user_input)

    async def async_step_hp_printer_additional_settings(self, user_input=None):
        errors = None

        self._config_flow.initialize(self.hass)

        if user_input is not None:
            self._config_flow.update_options(user_input, True)

            if errors is None:
                return self.async_create_entry(title="", data=user_input)

        data_schema = self._config_flow.get_default_options()

        return self.async_show_form(
            step_id="hp_printer_additional_settings",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=self._config_flow.data,
        )
