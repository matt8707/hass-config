import logging

from homeassistant import config_entries

from .mod_view import setup_view
from .connection import setup_connection
from .service import setup_service
from .const import (
    DOMAIN,
    DATA_DEVICES,
    DATA_ALIASES,
    DATA_ADDERS,
    CONFIG_DEVICES,
    DATA_CONFIG,
    DATA_SETUP_COMPLETE,
)

COMPONENTS = [
    "media_player",
    "sensor",
    "binary_sensor",
    "light",
    "camera",
]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):

    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
            )
        )

    aliases = {}
    for d in config[DOMAIN].get(CONFIG_DEVICES, {}):
        name = config[DOMAIN][CONFIG_DEVICES][d].get("name", None)
        if name:
            aliases[name] = d.replace("_", "-")

    hass.data[DOMAIN] = {
        DATA_DEVICES: {},
        DATA_ALIASES: aliases,
        DATA_ADDERS: {},
        DATA_CONFIG: config[DOMAIN],
        DATA_SETUP_COMPLETE: False,
    }

    await setup_connection(hass, config)
    setup_view(hass)

    for component in COMPONENTS:
        hass.async_create_task(
            hass.helpers.discovery.async_load_platform(component, DOMAIN, {}, config)
        )

    await setup_service(hass)

    hass.data[DOMAIN][DATA_SETUP_COMPLETE] = True

    for device in hass.data[DOMAIN][DATA_DEVICES].values():
        device.trigger_update()

    return True


async def async_setup_entry(hass, config_entry):
    for component in COMPONENTS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, component)
        )
    return True
