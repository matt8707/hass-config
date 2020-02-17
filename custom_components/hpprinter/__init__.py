"""
This component provides support for HP Printers.
For more details about this component, please refer to the documentation at
https://home-assistant.io/components/hpprinter/
"""
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant

from .const import *
from .HPDeviceData import *
from .home_assistant import HPPrinterHomeAssistant, _get_printers

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
    data = _get_printers(hass)
    name = entry_data.get(CONF_NAME)

    unload = hass.config_entries.async_forward_entry_unload

    if name in data:
        printer = data[name]
        await printer.async_remove()

        hass.async_create_task(unload(entry, DOMAIN_BINARY_SENSOR))
        hass.async_create_task(unload(entry, DOMAIN_SENSOR))

        del hass.data[DATA_HP_PRINTER][name]

        return True

    return False


async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Triggered by config entry options updates."""
    entry_data = entry.data
    name = entry_data.get(CONF_NAME)
    data = _get_printers(hass)

    if name in data:
        printer = data[name]

        printer.options = entry.options
