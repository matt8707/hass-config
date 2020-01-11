"""Config flow for Apple TV integration."""
import asyncio
import logging
from random import randrange
from ipaddress import ip_address

import voluptuous as vol

from homeassistant import core, config_entries, exceptions
from homeassistant.core import callback
from homeassistant.const import CONF_PIN, CONF_NAME, CONF_PROTOCOL, CONF_TYPE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_ADDRESS, CONF_IDENTIFIER, CONF_CREDENTIALS, CONF_START_OFF

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required(CONF_IDENTIFIER): str})
INPUT_PIN_SCHEMA = vol.Schema({vol.Required(CONF_PIN, default=None): int})

DEFAULT_START_OFF = False


class AppleTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Apple TV."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow for this handler."""
        return AppleTVOptionsFlow(config_entry)

    def __init__(self):
        self._atv = None
        self._identifier = None
        self._protocol = None
        self._pairing = None
        self._credentials = {}  # Protocol -> credentials

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        import pyatv

        errors = {}
        description_placeholders = {'devices': ''}
        if user_input is not None:
            try:
                self._identifier = user_input[CONF_IDENTIFIER]
                return await self.async_find_device()
            except DeviceNotFound as ex:
                errors["base"] = "device_not_found"

                # This is a hack that will be removed in final version
                description_placeholders["devices"] = '<br/><br/>Found devices: ' + ', '.join(ex.devices)
            except pyatv.exceptions.NoServiceError:
                errors["base"] = "no_usable_service"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA,
            description_placeholders=description_placeholders, errors=errors)


    async def async_step_zeroconf(self, discovery_info):
        """Handle device found via zeroconf."""
        from pyatv import const

        service_type = discovery_info[CONF_TYPE]
        properties = discovery_info['properties']

        if service_type == "_mediaremotetv._tcp.local.":
            self._identifier = properties['UniqueIdentifier']
            name = properties["Name"]
        elif service_type == "_touch-able._tcp.local.":
            self._identifier = discovery_info['name'].split('.')[0]
            name = properties["CtlN"]
        elif service_type == "_appletv-v2._tcp.local.":
            self._identifier = discovery_info['name'].split('.')[0]
            name = "{0} (Home Sharing)".format(properties["Name"])
        else:
            return self.async_abort(reason="unrecoverable")

        self.context["title_placeholders"] = {"name": name}
        return await self.async_find_device()

    async def async_find_device(self):
        """Scan for the selected device to discover services."""
        import pyatv

        def _matches_device(dev):
            if self._identifier == dev.name.encode('ascii', 'ignore').decode():  # TODO: encoding should be done in pyatv
                return True
            if self._identifier == str(dev.address):
                return True

            for service in dev.services:
                if self._identifier == service.identifier:
                    return True

            return False

        def _host_filter():
            try:
                return [ip_address(self._identifier)]
            except ValueError:
                return None

        atvs = await pyatv.scan(self.hass.loop, timeout=3, hosts=_host_filter())
        matches = [atv for atv in atvs if _matches_device(atv)]
        if not matches:
            raise DeviceNotFound([atv.name.encode('ascii', 'ignore').decode() for atv in atvs])


        self._atv = matches[0]
        self._protocol = self._atv.main_service().protocol

        for identifier in self._atv.all_identifiers:
            if self._is_already_configured(identifier):
                return self.async_abort(reason="already_configured")

        # If credentials were found, save them
        for service in self._atv.services:
            if service.credentials:
                self._credentials[service.protocol.value] = service.credentials

        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        """Handle user-confirmation of discovered node."""
        if user_input is not None:
            if self._is_already_configured(self._identifier):
                return self.async_abort(reason="already_configured")

            return await self.async_begin_pairing()
        return self.async_show_form(
            step_id="confirm", description_placeholders={"name": self._atv.name})

    async def async_begin_pairing(self):
        """Start pairing process for the next available protocol."""
        from pyatv import pair, exceptions

        self._protocol = self._next_protocol_to_pair()

        # Dispose previous pairing sessions
        if self._pairing is not None:
            await self._pairing.close()
            self._pairing = None

        # Any more protocols to pair? Else bail out here
        if not self._protocol:
            return self._async_get_entry()

        # Initiate the pairing process
        abort_reason = None
        try:
            session = async_get_clientsession(self.hass)
            self._pairing = await pair(
                self._atv, self._protocol, self.hass.loop, session=session)
            await self._pairing.begin()
        except asyncio.TimeoutError:
            abort_reason = "timeout"
        except OSError:
            return await self.async_step_service_problem()
        except exceptions.BackOffError:
            abort_reason = "backoff"
        except exceptions.AuthenticationError:
            abort_reason = "auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            abort_reason = "unrecoverable_error"

        if abort_reason:
            if self._pairing:
                await self._pairing.close()
            return self.async_abort(reason=abort_reason)

        # Choose step depending on if PIN is required from user or not
        if self._pairing.device_provides_pin:
            return await self.async_step_pair_with_pin()

        return await self.async_step_pair_no_pin()

    async def async_step_pair_with_pin(self, user_input=None):
        """Handle pairing step where a PIN is required from the user."""
        import pyatv
        from pyatv import convert

        errors = {}
        if user_input is not None:
            try:
                self._pairing.pin(user_input[CONF_PIN])
                await self._pairing.finish()
                self._credentials[self._protocol.value] = self._pairing.service.credentials
                return await self.async_begin_pairing()
            except pyatv.exceptions.DeviceAuthenticationError:
                errors["base"] = "auth"
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="pair_with_pin", data_schema=INPUT_PIN_SCHEMA, errors=errors,
            description_placeholders={
                "protocol": convert.protocol_str(self._protocol)})

    async def async_step_pair_no_pin(self, user_input=None):
        """Handle step where user has to enter a PIN on the device."""
        from pyatv import convert

        if user_input is not None:
            if self._pairing.has_paired:
                await self._pairing.close()
                return await self.async_begin_pairing()
            return self.async_abort(reason="device_did_not_pair")

        random_pin = randrange(1000, stop=10000)
        self._pairing.pin(random_pin)
        return self.async_show_form(
            step_id="pair_no_pin",
            description_placeholders={
                "protocol": convert.protocol_str(self._protocol),
                "pin": random_pin
                })

    async def async_step_service_problem(self, user_input=None):
        """Inform user that a service will not be added."""
        from pyatv import convert
        if user_input is not None:
            self._credentials[self._protocol.value] = None
            return await self.async_begin_pairing()

        return self.async_show_form(
            step_id="service_problem",
            description_placeholders={"protocol": convert.protocol_str(self._protocol)})

    def _async_get_entry(self):
        return self.async_create_entry(
            title=self._atv.name,
            data={
                CONF_IDENTIFIER: self._atv.identifier,
                CONF_PROTOCOL: self._atv.main_service().protocol.value,
                CONF_NAME: self._atv.name,
                CONF_CREDENTIALS: self._credentials,
                CONF_ADDRESS: str(self._atv.address),
            },
        )

    def _next_protocol_to_pair(self):
        def _needs_pairing(protocol):
            if self._atv.get_service(protocol) is None:
                return False
            return protocol.value not in self._credentials

        from pyatv.const import Protocol

        protocols = [Protocol.MRP, Protocol.DMAP, Protocol.AirPlay]
        for protocol in protocols:
            if _needs_pairing(protocol):
                return protocol

        return None

    def _is_already_configured(self, identifier):
        for ident in self._atv.all_identifiers:
            for entry in self._async_current_entries():
                if entry.data[CONF_IDENTIFIER] == identifier:
                    return True
        return False


class AppleTVOptionsFlow(config_entries.OptionsFlow):
    """Handle Apple TV options."""

    def __init__(self, config_entry):
        """Initialize Apple TV options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the Apple TV options."""
        return await self.async_step_device_options()

    async def async_step_device_options(self, user_input=None):
        """Manage the devices options."""
        if user_input is not None:
            self.options[CONF_START_OFF] = user_input[CONF_START_OFF]
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="device_options",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_START_OFF,
                        default=self.config_entry.options.get(
                            CONF_START_OFF, DEFAULT_START_OFF
                        ),
                    ): bool,
                }
            ),
        )


class DeviceNotFound(exceptions.HomeAssistantError):
    """Error to indicate device could not be found."""

    def __init__(self, devices):
        """Initialize a new DeviceNotFound error."""
        self.devices = devices
