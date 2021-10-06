"""Config flow for Apple TV integration."""
from collections import deque
from ipaddress import ip_address
import logging
from random import randrange

from pyatv import exceptions, pair, scan
from pyatv.const import DeviceModel, PairingRequirement
from pyatv.convert import model_str, protocol_str
from pyatv.helpers import get_unique_id
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.zeroconf import async_get_instance
from homeassistant.const import CONF_ADDRESS, CONF_NAME, CONF_PIN, CONF_TYPE
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_CREDENTIALS,
    CONF_IDENTIFIERS,
    CONF_RECONFIGURE,
    CONF_START_OFF,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

DEVICE_INPUT = "device_input"

INPUT_PIN_SCHEMA = vol.Schema({vol.Required(CONF_PIN, default=None): int})

DEFAULT_START_OFF = False
DEFAULT_RECONFIGURE = False


async def device_scan(identifier, loop, cache=None):
    """Scan for a specific device using identifier as filter."""

    def _filter_device(dev):
        if identifier is None:
            return True
        if identifier == str(dev.address):
            return True
        if identifier == dev.name:
            return True
        return any(service.identifier == identifier for service in dev.services)

    def _host_filter():
        try:
            return [ip_address(identifier)]
        except ValueError:
            return None

    if cache:
        matches = [atv for atv in cache if _filter_device(atv)]
        if matches:
            return cache, matches[0], matches[0].all_identifiers

    for hosts in (_host_filter(), None):
        scan_result = await scan(loop, timeout=3, hosts=hosts)
        matches = [atv for atv in scan_result if _filter_device(atv)]

        if matches:
            return scan_result, matches[0], matches[0].all_identifiers

    return scan_result, None, None


class AppleTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple TV."""

    VERSION = 3

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow for this handler."""
        return AppleTVOptionsFlow(config_entry)

    def __init__(self):
        """Initialize a new AppleTVConfigFlow."""
        self.target_device = None
        self.scan_result = None
        self.atv = None
        self.atv_identifiers = None
        self.protocol = None
        self.pairing = None
        self.credentials = {}  # Protocol -> credentials
        self.protocols_to_pair = deque()

    @property
    def device_identifier(self):
        """Return a identifier for the config entry.

        A device has multiple unique identifier, but Home Assistant only supports one
        per config entry. Normally, a "main identifier" is determined by pyatv by
        first collecting all identifiers and then picking one in a pre-determine order.
        Under normal circumstances, this works fine but if a service is missing or
        removed due to deprecation (which happened with MRP), then another identifier
        will be calculated instead. To fix this, all identifiers belonging to a device
        is stored with the config entry and one of them (could be random) is used as
        unique_id for said entry. When a new (zeroconf) service or device is
        discovered, the identifier is first used to look up if it belongs to an
        existing config entry. If that's the case, the unique_id from that entry is
        re-used, otherwise the newly discovered identifier is used instead.
        """
        for entry in self._async_current_entries():
            if self.atv.identifier in entry.data[CONF_IDENTIFIERS]:
                return entry.unique_id
        return self.atv.identifier

    async def async_step_reauth(self, user_input=None):
        """Handle initial step when updating invalid credentials."""
        self.target_device = self.unique_id
        self.context["identifier"] = self.unique_id
        return await self.async_step_reconfigure()

    async def async_step_reconfigure(self, user_input=None):
        """Inform user that reconfiguration is about to start."""
        if user_input is not None:
            return await self.async_find_device_wrapper(
                self.async_pair_next_protocol, allow_exist=True
            )

        return self.async_show_form(step_id="reconfigure")

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Be helpful to the user and look for devices
        if self.scan_result is None:
            self.scan_result, _, _ = await device_scan(None, self.hass.loop)

        errors = {}
        if user_input is not None:
            self.target_device = user_input[DEVICE_INPUT]
            try:
                await self.async_find_device()
            except DeviceNotFound:
                errors["base"] = "no_devices_found"
            except DeviceAlreadyConfigured:
                errors["base"] = "already_configured_device"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    self.device_identifier, raise_on_progress=False
                )
                return await self.async_step_confirm()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(DEVICE_INPUT, default=self._prefill_identifier()): str}
            ),
            errors=errors,
            description_placeholders={"devices": self._devices_str()},
        )

    async def async_step_zeroconf(self, discovery_info):
        """Handle device found via zeroconf."""
        service_type = discovery_info[CONF_TYPE][:-1]  # Remove leading .
        name = discovery_info[CONF_NAME].replace(f".{service_type}.", "")
        properties = discovery_info["properties"]

        # Extract unique identifier from service
        self.target_device = get_unique_id(service_type, name, properties)
        if self.target_device is None:
            return self.async_abort(reason="unknown")

        # Scan for the device in order to extract _all_ unique identifiers assigned to
        # it. Not doing it like this will yield multiple config flows for the same
        # device, one per protocol, which is undesired.
        return await self.async_find_device_wrapper(self.async_found_zeroconf_device)

    async def async_found_zeroconf_device(self, user_input=None):
        """Handle device found after Zeroconf discovery."""
        await self.async_set_unique_id(self.device_identifier)
        self._abort_if_unique_id_configured()

        self.context["identifier"] = self.unique_id
        return await self.async_step_confirm()

    async def async_find_device_wrapper(self, next_func, allow_exist=False):
        """Find a specific device and call another function when done.

        This function will do error handling and bail out when an error
        occurs.
        """
        try:
            await self.async_find_device(allow_exist)
        except DeviceNotFound:
            return self.async_abort(reason="no_devices_found")
        except DeviceAlreadyConfigured:
            return self.async_abort(reason="already_configured_device")
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            return self.async_abort(reason="unknown")

        return await next_func()

    async def async_find_device(self, allow_exist=False):
        """Scan for the selected device to discover services."""
        self.scan_result, self.atv, self.atv_identifiers = await device_scan(
            self.target_device, self.hass.loop, cache=self.scan_result
        )
        if not self.atv:
            raise DeviceNotFound()

        # Protocols supported by the device are prospects for pairing
        self.protocols_to_pair.extend(service.protocol for service in self.atv.services)

        dev_info = self.atv.device_info
        self.context["title_placeholders"] = {
            "name": self.atv.name,
            "type": (
                dev_info.raw_model
                if dev_info.model == DeviceModel.Unknown and dev_info.raw_model
                else model_str(dev_info.model)
            ),
        }

        if not allow_exist:
            for identifier in self.atv.all_identifiers:
                if identifier in self._async_current_ids():
                    raise DeviceAlreadyConfigured()

        # If credentials were found, save them
        for service in self.atv.services:
            if service.credentials:
                self.credentials[service.protocol.value] = service.credentials

    async def async_step_confirm(self, user_input=None):
        """Handle user-confirmation of discovered node."""
        if user_input is not None:
            return await self.async_pair_next_protocol()
        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "name": self.atv.name,
                "type": model_str(self.atv.device_info.model),
            },
        )

    async def async_pair_next_protocol(self):
        """Start pairing process for the next available protocol."""
        await self._async_cleanup()

        # Any more protocols to pair? Else bail out here
        if not self.protocols_to_pair:
            return await self._async_get_entry()

        self.protocol = self.protocols_to_pair.popleft()
        service = self.atv.get_service(self.protocol)

        # Figure out, depending on protocol, what kind of pairing is needed
        if service.pairing == PairingRequirement.Unsupported:
            _LOGGER.debug("%s does not support pairing", self.protocol)
            return await self.async_pair_next_protocol()
        if service.pairing == PairingRequirement.Disabled:
            return await self.async_step_protocol_disabled()
        elif service.pairing == PairingRequirement.NotNeeded:
            _LOGGER.debug("%s does not require pairing", self.protocol)
            self.credentials[self.protocol.value] = None
            return await self.async_pair_next_protocol()
        else:
            _LOGGER.debug("%s requires pairing", self.protocol)

        # Initiate the pairing process
        abort_reason = None
        session = async_get_clientsession(self.hass)
        zeroconf = await async_get_instance(self.hass)
        self.pairing = await pair(
            self.atv,
            self.protocol,
            self.hass.loop,
            session=session,
            name="Home Assistant",
            zeroconf=zeroconf,
        )
        try:
            await self.pairing.begin()
        except exceptions.ConnectionFailedError:
            return await self.async_step_service_problem()
        except exceptions.BackOffError:
            abort_reason = "backoff"
        except exceptions.PairingError:
            _LOGGER.exception("Authentication problem")
            abort_reason = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            abort_reason = "unknown"

        if abort_reason:
            await self._async_cleanup()
            return self.async_abort(reason=abort_reason)

        # Choose step depending on if PIN is required from user or not
        if self.pairing.device_provides_pin:
            return await self.async_step_pair_with_pin()

        return await self.async_step_pair_no_pin()

    async def async_step_protocol_disabled(self, user_input=None):
        """Inform user that a protocol is disabled and cannot be paired."""
        if user_input is not None:
            return await self.async_pair_next_protocol()
        return self.async_show_form(
            step_id="protocol_disabled",
            description_placeholders={"protocol": protocol_str(self.protocol)},
        )

    async def async_step_pair_with_pin(self, user_input=None):
        """Handle pairing step where a PIN is required from the user."""
        errors = {}
        if user_input is not None:
            try:
                self.pairing.pin(user_input[CONF_PIN])
                await self.pairing.finish()
                self.credentials[self.protocol.value] = self.pairing.service.credentials
                return await self.async_pair_next_protocol()
            except exceptions.PairingError:
                _LOGGER.exception("Authentication problem")
                errors["base"] = "invalid_auth"
            except AbortFlow:
                raise
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="pair_with_pin",
            data_schema=INPUT_PIN_SCHEMA,
            errors=errors,
            description_placeholders={"protocol": protocol_str(self.protocol)},
        )

    async def async_step_pair_no_pin(self, user_input=None):
        """Handle step where user has to enter a PIN on the device."""
        if user_input is not None:
            await self.pairing.finish()
            if self.pairing.has_paired:
                self.credentials[self.protocol.value] = self.pairing.service.credentials
                return await self.async_pair_next_protocol()

            await self.pairing.close()
            return self.async_abort(reason="device_did_not_pair")

        pin = randrange(1000, stop=10000)
        self.pairing.pin(pin)
        return self.async_show_form(
            step_id="pair_no_pin",
            description_placeholders={
                "protocol": protocol_str(self.protocol),
                "pin": pin,
            },
        )

    async def async_step_service_problem(self, user_input=None):
        """Inform user that a service will not be added."""
        if user_input is not None:
            return await self.async_pair_next_protocol()

        return self.async_show_form(
            step_id="service_problem",
            description_placeholders={"protocol": protocol_str(self.protocol)},
        )

    async def _async_cleanup(self):
        """Clean up allocated resources."""
        if self.pairing is not None:
            await self.pairing.close()
            self.pairing = None

    async def _async_get_entry(self):
        """Return config entry or update existing config entry."""
        # Abort if no protocols were paired
        if not self.credentials:
            return self.async_abort(reason="setup_failed")

        data = {
            CONF_NAME: self.atv.name,
            CONF_CREDENTIALS: self.credentials,
            CONF_ADDRESS: str(self.atv.address),
            CONF_IDENTIFIERS: self.atv_identifiers,
        }

        existing_entry = await self.async_set_unique_id(
            self.device_identifier, raise_on_progress=False
        )

        # If an existing config entry is updated, then this was a re-auth
        if existing_entry:
            self.hass.config_entries.async_update_entry(
                existing_entry, data=data, unique_id=self.unique_id
            )
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(existing_entry.entry_id)
            )
            return self.async_abort(reason="reauth_successful")

        return self.async_create_entry(
            title=self.atv.name, data=data, options={CONF_RECONFIGURE: False}
        )

    def _devices_str(self):
        return ", ".join(
            [
                f"`{atv.name} ({atv.address})`"
                for atv in self.scan_result
                if atv.identifier not in self._async_current_ids()
            ]
        )

    def _prefill_identifier(self):
        # Return identifier (address) of one device that has not been paired with
        for atv in self.scan_result:
            if atv.identifier not in self._async_current_ids():
                return str(atv.address)
        return ""


class AppleTVOptionsFlow(config_entries.OptionsFlow):
    """Handle Apple TV options."""

    def __init__(self, config_entry):
        """Initialize Apple TV options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the Apple TV options."""
        if user_input is not None:
            self.options[CONF_START_OFF] = user_input[CONF_START_OFF]
            self.options[CONF_RECONFIGURE] = user_input[CONF_RECONFIGURE]
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_START_OFF,
                        default=self.config_entry.options.get(
                            CONF_START_OFF, DEFAULT_START_OFF
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_RECONFIGURE,
                        default=self.config_entry.options.get(
                            CONF_RECONFIGURE, DEFAULT_RECONFIGURE
                        ),
                    ): bool,
                }
            ),
        )


class DeviceNotFound(HomeAssistantError):
    """Error to indicate device could not be found."""


class DeviceAlreadyConfigured(HomeAssistantError):
    """Error to indicate device is already configured."""
