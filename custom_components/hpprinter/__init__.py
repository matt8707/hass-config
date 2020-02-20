"""
This component provides support for HP Printers.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
import logging

from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant

from .const import *
from .HPDeviceData import *
from .home_assistant import HPPrinterHomeAssistant, _get_printer

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a HPPrinter component."""
    _LOGGER.debug(f"Loading HP Printer domain")

    _LOGGER.debug(f"Starting async_setup_entry of {DOMAIN}")
    entry_data = entry.data

    host = entry_data.get(CONF_HOST)

    if DATA_HP_PRINTER not in hass.data:
        hass.data[DATA_HP_PRINTER] = {}

    name = entry_data.get(CONF_NAME)

    if host is None:
        _LOGGER.info("Invalid hostname")
        return False

    if name in hass.data:
        _LOGGER.info(f"Printer {name} already defined")
        return False

    ha = HPPrinterHomeAssistant(hass, name, host, entry)
    ha.initialize()

    hass.data[DATA_HP_PRINTER][name] = ha

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    entry_data = entry.data
    name = entry_data.get(CONF_NAME)
    printer = _get_printer(hass, name)

    if printer is not None:
        await printer.async_remove()

        del hass.data[DATA_HP_PRINTER][name]

        return True

    return False


async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Triggered by config entry options updates."""
    entry_data = entry.data
    name = entry_data.get(CONF_NAME)
    printer = _get_printer(hass, name)

    if printer is not None:
        printer.options = entry.options
