"""The samsungtv_smart integration."""

from aiohttp import ClientConnectionError, ClientSession, ClientResponseError
from async_timeout import timeout
import asyncio
import logging
import os
from shutil import copyfile
import socket
import voluptuous as vol
from websocket import WebSocketException

from .api.samsungws import SamsungTVWS
from .api.exceptions import ConnectionFailure
from .api.smartthings import SmartThingsTV

from homeassistant.components.media_player.const import DOMAIN as MP_DOMAIN
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.storage import STORAGE_DIR
from homeassistant.helpers.typing import HomeAssistantType

from homeassistant.const import (
    CONF_API_KEY,
    CONF_BROADCAST_ADDRESS,
    CONF_DEVICE_ID,
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
)

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    CONF_APP_LIST,
    CONF_CHANNEL_LIST,
    CONF_DEVICE_NAME,
    CONF_LOAD_ALL_APPS,
    CONF_SOURCE_LIST,
    CONF_SHOW_CHANNEL_NR,
    CONF_WS_NAME,
    CONF_UPDATE_METHOD,
    CONF_UPDATE_CUSTOM_PING_URL,
    CONF_SCAN_APP_HTTP,
    DATA_OPTIONS,
    DEFAULT_SOURCE_LIST,
    WS_PREFIX,
    RESULT_NOT_SUCCESSFUL,
    RESULT_NOT_SUPPORTED,
    RESULT_ST_DEVICE_NOT_FOUND,
    RESULT_SUCCESS,
    RESULT_WRONG_APIKEY,
    AppLoadMethod,
)

SAMSMART_SCHEMA = {
    vol.Optional(CONF_SOURCE_LIST, default=DEFAULT_SOURCE_LIST): cv.string,
    vol.Optional(CONF_APP_LIST): cv.string,
    vol.Optional(CONF_CHANNEL_LIST): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_MAC): cv.string,
    vol.Optional(CONF_BROADCAST_ADDRESS): cv.string,
}


def ensure_unique_hosts(value):
    """Validate that all configs have a unique host."""
    vol.Schema(vol.Unique("duplicate host entries found"))(
        [socket.gethostbyname(entry[CONF_HOST]) for entry in value]
    )
    return value


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                cv.deprecated(CONF_LOAD_ALL_APPS),
                cv.deprecated(CONF_PORT),
                cv.deprecated(CONF_UPDATE_METHOD),
                cv.deprecated(CONF_UPDATE_CUSTOM_PING_URL),
                cv.deprecated(CONF_SCAN_APP_HTTP),
                vol.Schema(
                    {
                        vol.Required(CONF_HOST): cv.string,
                        vol.Optional(CONF_NAME): cv.string,
                        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                        vol.Optional(CONF_API_KEY): cv.string,
                        vol.Optional(CONF_DEVICE_NAME): cv.string,
                        vol.Optional(CONF_DEVICE_ID): cv.string,
                        vol.Optional(CONF_LOAD_ALL_APPS, default=True): cv.boolean,
                        vol.Optional(CONF_UPDATE_METHOD): cv.string,
                        vol.Optional(CONF_UPDATE_CUSTOM_PING_URL): cv.string,
                        vol.Optional(CONF_SCAN_APP_HTTP, default=True): cv.boolean,
                        vol.Optional(CONF_SHOW_CHANNEL_NR, default=False): cv.boolean,
                        vol.Optional(CONF_WS_NAME): cv.string,
                    }
                ).extend(SAMSMART_SCHEMA),
            ],
            ensure_unique_hosts,
        )
    },
    extra=vol.ALLOW_EXTRA,
)

DATA_LISTENER = "listener"

_LOGGER = logging.getLogger(__name__)


def tv_url(host: str, address: str = "") -> str:
    return f"http://{host}:8001/api/v2/{address}"


def token_file_name(hostname: str) -> str:
    return f"{DOMAIN}_{hostname}_token"


def get_token_file(hass, hostname, port, overwrite=False):
    """Get token file name and try to create it if not exists."""
    if port != 8002:
        return None

    token_file = hass.config.path(STORAGE_DIR, token_file_name(hostname))

    if not os.path.isfile(token_file) or overwrite:
        # Create token file for catch possible errors
        try:
            handle = open(token_file, "w+", closefd=True)
            handle.close()
        except OSError:
            _LOGGER.error(
                "Samsung TV - Error creating token file: %s", token_file
            )
            return None

    return token_file


def remove_token_file(hass, hostname):
    """Try to remove token file."""
    token_file = hass.config.path(STORAGE_DIR, token_file_name(hostname))

    if os.path.isfile(token_file):
        try:
            os.remove(token_file)
        except:
            _LOGGER.error(
                "Samsung TV - Error deleting token file: %s", token_file
            )


def _migrate_token_file(hass: HomeAssistantType, hostname: str):
    """Migrate token file from old path to new one."""

    token_file = hass.config.path(STORAGE_DIR, token_file_name(hostname))
    if os.path.isfile(token_file):
        return

    old_token_file = (
        os.path.dirname(os.path.realpath(__file__)) + f"/token-{hostname}.txt"
    )

    if os.path.isfile(old_token_file):
        try:
            copyfile(old_token_file, token_file)
        except IOError:
            _LOGGER.error("Failed migration of token file from %s to %s", old_token_file, token_file)
            return

        try:
            os.remove(old_token_file)
        except:
            _LOGGER.warning("Error while deleting old token file %s", old_token_file)

    return


class SamsungTVInfo:
    def __init__(self, hass, hostname, name, ws_name=None):
        self._hass = hass
        self._hostname = hostname
        self._name = name
        self._ws_name = ws_name if ws_name else name

        self._uuid = None
        self._macaddress = None
        self._device_name = None
        self._device_model = None
        self._device_os = None
        self._token_support = False
        self._port = 0

    def _try_connect_ws(self):
        """Try to connect to device using web sockets on port 8001 and 8002"""

        for port in (8001, 8002):

            try:
                _LOGGER.info(
                    "Try to configure SamsungTV %s using port %s",
                    self._hostname,
                    str(port),
                )
                token_file = get_token_file(self._hass, self._hostname, port, True)
                with SamsungTVWS(
                    name=WS_PREFIX
                    + " "
                    + self._ws_name,  # this is the name shown in the TV list of external device.
                    host=self._hostname,
                    port=port,
                    token_file=token_file,
                    timeout=45,  # We need this high timeout because waiting for auth popup is just an open socket
                ) as remote:
                    remote.open()
                _LOGGER.info("Found working configuration using port %s", str(port))
                self._port = port
                return RESULT_SUCCESS
            except (OSError, ConnectionFailure, WebSocketException) as err:
                _LOGGER.info("Configuration failed using port %s, error: %s", str(port), err)

        _LOGGER.error("Web socket connection to SamsungTV %s failed", self._hostname)
        return RESULT_NOT_SUCCESSFUL

    async def _try_connect_st(self, api_key, device_id, session: ClientSession):
        """Try to connect to ST device"""

        try:
            with timeout(10):
                _LOGGER.info(
                    "Try connection to SmartThings TV with id [%s]", device_id
                )
                with SmartThingsTV(
                    api_key=api_key, device_id=device_id, session=session,
                ) as st:
                    result = await st.async_device_health()
                if result:
                    _LOGGER.info("Connection completed successfully.")
                    return RESULT_SUCCESS
                else:
                    _LOGGER.error("Connection to SmartThings TV not available.")
                    return RESULT_ST_DEVICE_NOT_FOUND
        except ClientResponseError as err:
            _LOGGER.error("Failed connecting to SmartThings TV, error: %s", err)
            if err.status == 400:  # Bad request, means that token is valid
                return RESULT_ST_DEVICE_NOT_FOUND
        except Exception as err:
            _LOGGER.error("Failed connecting with SmartThings, error: %s", err)

        return RESULT_WRONG_APIKEY

    @staticmethod
    async def get_st_devices(api_key, session: ClientSession, st_device_label=""):
        """Get list of available ST devices"""

        try:
            with timeout(4):
                devices = await SmartThingsTV.get_devices_list(
                    api_key, session, st_device_label
                )
        except Exception as err:
            _LOGGER.error("Failed connecting with SmartThings, error: %s", err)
            return None

        return devices

    async def get_device_info(
        self, session: ClientSession, api_key=None, st_device_id=None
    ):
        """Get device information"""

        if session is None:
            return RESULT_NOT_SUCCESSFUL

        result = await self._hass.async_add_executor_job(self._try_connect_ws)
        if result != RESULT_SUCCESS:
            return result

        try:
            with timeout(2):
                async with session.get(
                    tv_url(host=self._hostname),
                    raise_for_status=True
                ) as resp:
                    info = await resp.json()
        except (asyncio.TimeoutError, ClientConnectionError):
            _LOGGER.error("Error getting HTTP info for TV: " + self._hostname)
            return RESULT_NOT_SUCCESSFUL

        device = info.get("device", None)
        if not device:
            return RESULT_NOT_SUCCESSFUL

        device_id = device.get("id")
        if device_id and device_id.startswith("uuid:"):
            self._uuid = device_id[len("uuid:") :]
        else:
            self._uuid = device_id
        self._macaddress = device.get("wifiMac")
        self._device_name = device.get("name")
        self._device_model = device.get("modelName")
        self._device_os = device.get("OS")
        self._token_support = device.get("TokenAuthSupport")
        if api_key and st_device_id:
            result = await self._try_connect_st(api_key, st_device_id, session)

        return result


async def async_setup(hass: HomeAssistantType, config: ConfigEntry):
    """Set up the Samsung TV integration."""
    if DOMAIN in config:
        hass.data[DOMAIN] = {}
        entries_list = hass.config_entries.async_entries(DOMAIN)
        for entry_config in config[DOMAIN]:

            # get ip address
            ip_address = entry_config[CONF_HOST]

            # check if already configured
            valid_entries = [entry for entry in entries_list if entry.unique_id == ip_address]
            if not valid_entries:
                _LOGGER.warning(
                    "Found yaml configuration for not configured device %s. Please use UI to configure",
                    ip_address
                )
                continue

            hass.data[DOMAIN].setdefault(ip_address, {})
            for key in SAMSMART_SCHEMA:
                value = entry_config.get(key)
                if value:
                    hass.data[DOMAIN][ip_address][key] = value

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the Samsung TV platform."""

    # migrate old token file if required
    _migrate_token_file(hass, entry.unique_id)

    # setup entry
    hass.data.setdefault(DOMAIN, {}).setdefault(
        entry.unique_id, {}
    )  # unique_id = host
    hass.data[DOMAIN].setdefault(
        entry.entry_id,
        {
            DATA_OPTIONS: entry.options.copy(),
            DATA_LISTENER: [entry.add_update_listener(update_listener)],
        }
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, MP_DOMAIN)
    )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await asyncio.gather(
        *[hass.config_entries.async_forward_entry_unload(config_entry, MP_DOMAIN)]
    )
    for listener in hass.data[DOMAIN][config_entry.entry_id][DATA_LISTENER]:
        listener()
    remove_token_file(hass, config_entry.unique_id)
    hass.data[DOMAIN].pop(config_entry.entry_id)
    hass.data[DOMAIN].pop(config_entry.unique_id)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
    return True


async def update_listener(hass, config_entry):
    """Update when config_entry options update."""
    entry_id = config_entry.entry_id
    hass.data[DOMAIN][entry_id][DATA_OPTIONS] = config_entry.options.copy()
