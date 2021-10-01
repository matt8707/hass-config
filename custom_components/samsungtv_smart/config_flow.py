"""Config flow for Samsung TV."""
import socket
from typing import Any, Dict
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.config_entries import SOURCE_IMPORT

from homeassistant.const import (
    CONF_API_KEY,
    CONF_DEVICE_ID,
    CONF_HOST,
    CONF_ID,
    CONF_MAC,
    CONF_NAME,
    CONF_PORT,
)

# pylint:disable=unused-import
from . import SamsungTVInfo

from .const import (
    DOMAIN,
    CONF_APP_LAUNCH_METHOD,
    CONF_APP_LOAD_METHOD,
    CONF_DEVICE_NAME,
    CONF_DEVICE_MODEL,
    CONF_DEVICE_OS,
    CONF_DUMP_APPS,
    CONF_POWER_ON_DELAY,
    CONF_POWER_ON_METHOD,
    CONF_USE_ST_CHANNEL_INFO,
    CONF_USE_ST_STATUS_INFO,
    CONF_USE_MUTE_CHECK,
    CONF_SHOW_CHANNEL_NR,
    CONF_SYNC_TURN_OFF,
    CONF_SYNC_TURN_ON,
    CONF_WOL_REPEAT,
    CONF_WS_NAME,
    CONF_LOGO_OPTION,
    DEFAULT_POWER_ON_DELAY,
    MAX_WOL_REPEAT,
    RESULT_NOT_SUCCESSFUL,
    RESULT_ST_DEVICE_NOT_FOUND,
    RESULT_ST_DEVICE_USED,
    RESULT_ST_MULTI_DEVICES,
    RESULT_SUCCESS,
    RESULT_WRONG_APIKEY,
    AppLaunchMethod,
    AppLoadMethod,
    PowerOnMethod,
)

from .logo import (
    LogoOption,
    LOGO_OPTION_DEFAULT,
)

APP_LAUNCH_METHODS = {
    AppLaunchMethod.Standard.value: "Standard Web Socket Channel",
    AppLaunchMethod.Remote.value: "Remote Web Socket Channel",
    AppLaunchMethod.Rest.value: "Rest API Call",
}

APP_LOAD_METHODS = {
    AppLoadMethod.All.value: "All Apps",
    AppLoadMethod.Default.value: "Default Apps",
    AppLoadMethod.NotLoad.value: "Not Load",
}

POWER_ON_METHODS = {
    PowerOnMethod.WOL.value: "WOL Packet (better for wired connection)",
    PowerOnMethod.SmartThings.value: "SmartThings (better for wireless connection)",
}

LOGO_OPTIONS = {
    LogoOption.Disabled.value: "Disabled",
    LogoOption.WhiteColor.value: "White background, Color logo",
    LogoOption.BlueColor.value: "Blue background, Color logo",
    LogoOption.BlueWhite.value: "Blue background, White logo",
    LogoOption.DarkWhite.value: "Dark background, White logo",
    LogoOption.TransparentColor.value: "Transparent background, Color logo",
    LogoOption.TransparentWhite.value: "Transparent background, White logo",
}

CONFIG_RESULTS = {
    RESULT_NOT_SUCCESSFUL: "Local connection to TV failed.",
    RESULT_ST_DEVICE_NOT_FOUND: "SmartThings TV deviceID not found.",
    RESULT_ST_DEVICE_USED: "SmartThings TV deviceID already used.",
    RESULT_ST_MULTI_DEVICES: "Multiple TVs found, unable to identify the SmartThings device to pair.",
    RESULT_WRONG_APIKEY: "Wrong SmartThings token.",
}

CONF_SHOW_ADV_OPT = "show_adv_opt"
CONF_ST_DEVICE = "st_devices"
CONF_USE_HA_NAME = "use_ha_name_for_ws"
DEFAULT_TV_NAME = "Samsung TV"

ADVANCED_OPTIONS = [
    CONF_APP_LOAD_METHOD,
    CONF_APP_LAUNCH_METHOD,
    CONF_DUMP_APPS,
    CONF_WOL_REPEAT,
    CONF_POWER_ON_DELAY,
    CONF_USE_MUTE_CHECK,
]
OPT_LOGO_OPTION = f"{CONF_LOGO_OPTION}_opt"
OPT_APP_LOAD_METHOD = f"{CONF_APP_LOAD_METHOD}_opt"
OPT_APP_LAUNCH_METHOD = f"{CONF_APP_LAUNCH_METHOD}_opt"
OPT_POWER_ON_METHOD = f"{CONF_POWER_ON_METHOD}_opt"

_LOGGER = logging.getLogger(__name__)


def _get_ip(host):
    if host is None:
        return None
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


class SamsungTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Samsung TV config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    # pylint: disable=no-member # https://github.com/PyCQA/pylint/issues/3167

    def __init__(self):
        """Initialize flow."""
        self._user_data = None
        self._st_devices_schema = None

        self._tvinfo = None
        self._host = None
        self._api_key = None
        self._device_id = None
        self._name = None
        self._mac = None
        self._ws_name = None
        self._use_default_name = False
        self._logo_option = None

    def _stdev_already_used(self, devices_id):
        """Check if a device_id is in HA config."""
        for entry in self._async_current_entries():
            if entry.data.get(CONF_DEVICE_ID, "") == devices_id:
                return True
        return False

    def _remove_stdev_used(self, devices_list: Dict[str, Any]) -> Dict[str, Any]:
        """Remove entry already used"""
        res_dev_list = devices_list.copy()

        for dev_id in devices_list.keys():
            if self._stdev_already_used(dev_id):
                res_dev_list.pop(dev_id)
        return res_dev_list

    def _extract_dev_name(self, device):
        """Extract device neme from SmartThings Info"""
        name = device["name"]
        label = device.get("label", "")
        if label:
            name += f" ({label})"
        return name

    def _prepare_dev_schema(self, devices_list):
        """Prepare the schema for select correct ST device"""
        validate = {}
        for dev_id, infos in devices_list.items():
            device_name = self._extract_dev_name(infos)
            validate[dev_id] = device_name
        return vol.Schema({vol.Required(CONF_ST_DEVICE): vol.In(validate)})

    async def _get_st_deviceid(self, st_device_label=""):
        """Try to detect SmartThings device id."""
        session = self.hass.helpers.aiohttp_client.async_get_clientsession()
        devices_list = await SamsungTVInfo.get_st_devices(
            self._api_key, session, st_device_label
        )
        if devices_list is None:
            return RESULT_WRONG_APIKEY

        devices_list = self._remove_stdev_used(devices_list)
        if devices_list:
            if len(devices_list) > 1:
                self._st_devices_schema = self._prepare_dev_schema(devices_list)
            else:
                self._device_id = list(devices_list.keys())[0]

        return RESULT_SUCCESS

    async def _try_connect(self):
        """Try to connect and check auth."""
        self._tvinfo = SamsungTVInfo(self.hass, self._host, self._name, self._ws_name)

        session = self.hass.helpers.aiohttp_client.async_get_clientsession()
        result = await self._tvinfo.get_device_info(
            session, self._api_key, self._device_id
        )

        return result

    async def async_step_import(self, user_input=None):
        """Handle configuration by yaml file."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is None:
            return self._show_form()

        self._user_data = user_input
        ip_address = await self.hass.async_add_executor_job(
            _get_ip, user_input[CONF_HOST]
        )
        if not ip_address:
            return self._show_form(errors={"base": "invalid_host"})

        await self.async_set_unique_id(ip_address)
        self._abort_if_unique_id_configured()

        self._host = ip_address
        self._api_key = user_input.get(CONF_API_KEY)
        self._name = user_input.get(CONF_NAME)
        if not self._name:
            self._name = DEFAULT_TV_NAME
            self._use_default_name = True

        self._device_id = user_input.get(CONF_DEVICE_ID) if self._api_key else None
        self._mac = user_input.get(CONF_MAC, "")

        use_ha_name = user_input.get(CONF_USE_HA_NAME, False)
        if use_ha_name:
            ha_conf = self.hass.config
            if hasattr(ha_conf, "location_name"):
                self._ws_name = ha_conf.location_name
        if not self._ws_name:
            self._ws_name = self._name

        st_device_label = user_input.get(CONF_DEVICE_NAME, "")
        is_import = user_input.get(SOURCE_IMPORT, False)

        result = RESULT_SUCCESS
        if self._api_key and not self._device_id:
            result = await self._get_st_deviceid(st_device_label)

            if result == RESULT_SUCCESS and not self._device_id:
                if self._st_devices_schema:
                    if not is_import:
                        return self._show_form(errors=None, step_id="stdevice")
                    result = RESULT_ST_MULTI_DEVICES
                else:
                    if not is_import:
                        return self._show_form(errors=None, step_id="stdeviceid")
                    result = RESULT_ST_DEVICE_NOT_FOUND
        elif self._device_id and self._stdev_already_used(self._device_id):
            result = RESULT_ST_DEVICE_USED

        if result == RESULT_SUCCESS:
            result = await self._try_connect()

        return self._manage_result(result, is_import)

    async def async_step_stdevice(self, user_input=None):
        """Handle a flow to select ST device."""
        self._device_id = user_input.get(CONF_ST_DEVICE)

        result = await self._try_connect()
        return self._manage_result(result)

    async def async_step_stdeviceid(self, user_input=None):
        """Handle a flow to manual input a ST device."""
        device_id = user_input.get(CONF_DEVICE_ID)
        if self._stdev_already_used(device_id):
            return self._show_form(
                {"base": RESULT_ST_DEVICE_USED}, step_id="stdeviceid"
            )

        self._device_id = device_id

        result = await self._try_connect()
        return self._manage_result(result)

    @callback
    def _manage_result(self, result, is_import=False):
        """Manage the previous result."""

        if result != RESULT_SUCCESS:
            if is_import:
                _LOGGER.error(
                    "Error during setup of host %s using configuration.yaml info. Reason: %s",
                    self._host,
                    CONFIG_RESULTS[result],
                )
                return self.async_abort(reason=result)
            else:
                step_id = (
                    "stdeviceid" if result == RESULT_ST_DEVICE_NOT_FOUND else "user"
                )
                return self._show_form({"base": result}, step_id)

        return self._save_entry()

    @callback
    def _save_entry(self):
        """Generate new entry."""
        data = {
            CONF_HOST: self._host,
            CONF_NAME: self._name,
            CONF_ID: self._tvinfo._uuid,
            CONF_MAC: self._tvinfo._macaddress or self._mac,
            CONF_DEVICE_NAME: self._tvinfo._device_name,
            CONF_DEVICE_MODEL: self._tvinfo._device_model,
            CONF_PORT: self._tvinfo._port,
        }

        if self._ws_name:
            data[CONF_WS_NAME] = self._ws_name

        title = self._name if not self._use_default_name else self._tvinfo._device_name
        if self._api_key and self._device_id:
            data[CONF_API_KEY] = self._api_key
            data[CONF_DEVICE_ID] = self._device_id
            title += " (SmartThings)"
            self.CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
        else:
            self.CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

        if self._tvinfo._device_os:
            data[CONF_DEVICE_OS] = self._tvinfo._device_os

        _LOGGER.info("Configured new entity %s with host %s", title, self._host)
        return self.async_create_entry(title=title, data=data)

    def _get_init_schema(self):
        data = self._user_data or {}
        init_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=data.get(CONF_HOST, "")): str,
                vol.Required(CONF_NAME, default=data.get(CONF_NAME, "")): str,
                vol.Optional(
                    CONF_USE_HA_NAME, default=data.get(CONF_USE_HA_NAME, False)
                ): bool,
                vol.Optional(CONF_API_KEY, default=data.get(CONF_API_KEY, "")): str,
            }
        )

        return init_schema

    @callback
    def _show_form(self, errors=None, step_id="user"):
        """Show the form to the user."""
        if step_id == "stdevice":
            data_schema = self._st_devices_schema
        elif step_id == "stdeviceid":
            data_schema = vol.Schema({vol.Required(CONF_DEVICE_ID): str})
        else:
            data_schema = self._get_init_schema()

        return self.async_show_form(
            step_id=step_id, data_schema=data_schema, errors=errors if errors else {},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Samsung TV Smart."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._adv_options = {
            key: values
            for key, values in config_entry.options.items()
            if key in ADVANCED_OPTIONS
        }
        api_key = config_entry.data.get(CONF_API_KEY)
        st_dev = config_entry.data.get(CONF_DEVICE_ID)
        self._use_st = api_key and st_dev

    def _save_entry(self, data: dict):
        """Save configuration options"""
        data[CONF_POWER_ON_METHOD] = _get_key_from_value(
            POWER_ON_METHODS, data.pop(OPT_POWER_ON_METHOD, None)
        )
        data[CONF_LOGO_OPTION] = _get_key_from_value(
            LOGO_OPTIONS, data.pop(OPT_LOGO_OPTION, None)
        )
        data.update(self._adv_options)
        return self.async_create_entry(title="", data=data)

    async def async_step_init(self, user_input: dict = None):
        """Handle options flow."""
        if user_input is not None:
            if user_input.pop(CONF_SHOW_ADV_OPT, False):
                return await self.async_step_adv_opt()
            return self._save_entry(data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema({})

        if self._use_st:
            data_schema = data_schema.extend(
                {
                    vol.Optional(
                        CONF_USE_ST_STATUS_INFO,
                        default=options.get(
                            CONF_USE_ST_STATUS_INFO, True
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_USE_ST_CHANNEL_INFO,
                        default=options.get(
                            CONF_USE_ST_CHANNEL_INFO, True
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_SHOW_CHANNEL_NR,
                        default=options.get(
                            CONF_SHOW_CHANNEL_NR, False
                        ),
                    ): bool,
                    vol.Optional(
                        OPT_POWER_ON_METHOD,
                        default=POWER_ON_METHODS.get(
                            options.get(
                                CONF_POWER_ON_METHOD, PowerOnMethod.WOL.value
                            )
                        ),
                    ): vol.In(list(POWER_ON_METHODS.values())),
                }
            )

        data_schema = data_schema.extend(
            {
                vol.Optional(
                    OPT_LOGO_OPTION,
                    default=LOGO_OPTIONS.get(
                        options.get(CONF_LOGO_OPTION, LOGO_OPTION_DEFAULT[0])
                    ),
                ): vol.In(list(LOGO_OPTIONS.values())),
                vol.Optional(
                    CONF_SYNC_TURN_OFF,
                    description={
                        "suggested_value": options.get(
                            CONF_SYNC_TURN_OFF, ""
                        )
                    },
                ): str,
                vol.Optional(
                    CONF_SYNC_TURN_ON,
                    description={
                        "suggested_value": options.get(
                            CONF_SYNC_TURN_ON, ""
                        )
                    },
                ): str,
                vol.Optional(CONF_SHOW_ADV_OPT, default=False): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)

    async def async_step_adv_opt(self, user_input=None):
        """Handle advanced options flow."""

        if user_input is not None:
            user_input[CONF_APP_LOAD_METHOD] = _get_key_from_value(
                APP_LOAD_METHODS, user_input.pop(OPT_APP_LOAD_METHOD, None)
            )
            user_input[CONF_APP_LAUNCH_METHOD] = _get_key_from_value(
                APP_LAUNCH_METHODS, user_input.pop(OPT_APP_LAUNCH_METHOD, None)
            )
            self._adv_options.update(user_input)
            return await self.async_step_init()

        return self._async_adv_opt_form()

    @callback
    def _async_adv_opt_form(self):
        """Return configuration form for advanced options."""
        options = self._adv_options
        data_schema = vol.Schema(
            {
                vol.Optional(
                    OPT_APP_LOAD_METHOD,
                    default=APP_LOAD_METHODS.get(
                        options.get(
                            CONF_APP_LOAD_METHOD, AppLoadMethod.All.value
                        )
                    ),
                ): vol.In(list(APP_LOAD_METHODS.values())),
                vol.Optional(
                    OPT_APP_LAUNCH_METHOD,
                    default=APP_LAUNCH_METHODS.get(
                        options.get(
                            CONF_APP_LAUNCH_METHOD, AppLaunchMethod.Standard.value
                        )
                    ),
                ): vol.In(list(APP_LAUNCH_METHODS.values())),
                vol.Optional(
                    CONF_DUMP_APPS,
                    default=options.get(CONF_DUMP_APPS, False),
                ): bool,
                vol.Optional(
                    CONF_USE_MUTE_CHECK,
                    default=options.get(CONF_USE_MUTE_CHECK, True),
                ): bool,
                vol.Optional(
                    CONF_WOL_REPEAT,
                    default=min(
                        options.get(CONF_WOL_REPEAT, 1),
                        MAX_WOL_REPEAT,
                    ),
                ): vol.All(vol.Coerce(int), vol.Clamp(min=1, max=MAX_WOL_REPEAT)),
                vol.Optional(
                    CONF_POWER_ON_DELAY,
                    default=options.get(
                        CONF_POWER_ON_DELAY, DEFAULT_POWER_ON_DELAY
                    ),
                ): vol.All(vol.Coerce(int), vol.Clamp(min=0, max=60)),
            }
        )

        return self.async_show_form(step_id="adv_opt", data_schema=data_schema)


def _get_key_from_value(source: dict, value: str):
    """Get dict key from corresponding value."""
    if value:
        for src_key, src_value in source.items():
            if src_value == value:
                return src_key
    return None
