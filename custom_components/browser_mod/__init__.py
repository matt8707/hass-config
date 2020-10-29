import logging

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

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):

    aliases = {}
    for d in config[DOMAIN].get(CONFIG_DEVICES, {}):
        name = config[DOMAIN][CONFIG_DEVICES][d].get("name", None)
        if name:
            aliases[name] = d.replace('_', '-')

    hass.data[DOMAIN] = {
        DATA_DEVICES: {},
        DATA_ALIASES: aliases,
        DATA_ADDERS: {},
        DATA_CONFIG: config[DOMAIN],
        DATA_SETUP_COMPLETE: False,
        }

    await setup_connection(hass, config)
    setup_view(hass)

    async_load_platform = hass.helpers.discovery.async_load_platform
    await async_load_platform("media_player", DOMAIN, {}, config)
    await async_load_platform("sensor", DOMAIN, {}, config)
    await async_load_platform("binary_sensor", DOMAIN, {}, config)
    await async_load_platform("light", DOMAIN, {}, config)
    await async_load_platform("camera", DOMAIN, {}, config)

    await setup_service(hass)

    hass.data[DOMAIN][DATA_SETUP_COMPLETE] = True

    for device in hass.data[DOMAIN][DATA_DEVICES].values():
        device.trigger_update()

    return True
