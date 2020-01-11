"""The Apple TV integration."""
import asyncio
import logging
from functools import partial

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.helpers import discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import (
    CONF_NAME,
    EVENT_HOMEASSISTANT_STOP,
)

from .const import (
    DOMAIN, CONF_ADDRESS, CONF_IDENTIFIER, CONF_PROTOCOL,
    CONF_CREDENTIALS, CONF_START_OFF, KEY_MANAGER
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up the Apple TV integration."""
    return True


async def async_setup_entry(hass, entry):
    """Set up a config entry for Apple TV."""
    def address_updater(address):
        _LOGGER.debug("Changing address to %s", address)
        entry.data[CONF_ADDRESS] = address
        update_entry = partial(
            hass.config_entries.async_update_entry, data={**entry.data}
        )
        hass.add_job(update_entry, entry)

    from pyatv.const import Protocol
    address = entry.data[CONF_ADDRESS]
    identifier = entry.data[CONF_IDENTIFIER]
    protocol = Protocol(entry.data[CONF_PROTOCOL])
    credentials = entry.data[CONF_CREDENTIALS]
    start_off = entry.options.get(CONF_START_OFF, False)

    manager = AppleTVManager(
        hass, address, identifier, protocol, credentials, not start_off, address_updater)
    hass.data.setdefault(DOMAIN, {})[identifier] = manager

    @callback
    def on_hass_stop(event):
        """Stop push updates when hass stops."""
        asyncio.ensure_future(manager.disconnect(), loop=hass.loop)

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)

    dev_reg = await hass.helpers.device_registry.async_get_registry()
    dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections=set(),
        identifiers={(DOMAIN, entry.data[CONF_IDENTIFIER])},
        manufacturer="Apple",
        name="Apple TV",
        model="Unknown",
        sw_version="Unknown"
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "media_player")
    )

    hass.async_create_task(
        discovery.async_load_platform(hass, "remote", DOMAIN, entry.data, entry.data)
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload Twente Milieu config entry."""
    # TODO: This is not finished yet
    identifier = entry.data[CONF_IDENTIFIER]
    manager = hass.data[DOMAIN].pop(identifier)
    await manager.disconnect()

    await hass.config_entries.async_forward_entry_unload(entry, "media_player")

    # TODO: unload remote?

    return True


class AppleTVManager:
    """Connection and power manager for an Apple TV.

    An instance is used per device to share the same power state between
    several platforms. It also manages scanning and connection establishment
    in case of problems.
    """

    def __init__(self, hass, address, identifier, protocol, credentials, is_on, address_updater):
        """Initialize power manager."""
        self.hass = hass
        self.address = address
        self.identifier = identifier
        self.protocol = protocol
        self.credentials = credentials
        self.address_updater = address_updater
        self.session = async_get_clientsession(hass)
        self.listeners = []
        self.message = None
        self.atv = None
        self._is_on = is_on
        self._task = None

    async def init(self):
        """Initialize power management."""
        if self._is_on:
            await self.connect()

    def connection_lost(self, exception):
        """Device was unexpectedly disconnected."""
        _LOGGER.warning('Connection lost to Apple TV named %s',
                        self.atv.service.name)

        self.atv = None
        self._start_connect_loop()
        self._update_state(disconnected=True)

    def connection_closed(self):
        """Device connection was (intentionally) closed."""
        self.atv = None
        self._start_connect_loop()
        self._update_state(disconnected=True)

    async def connect(self):
        self._is_on = True
        self._start_connect_loop()

    async def disconnect(self):
        self._is_on = False
        try:
            if self.atv:
                await self.atv.close()
                self.atv = None
            if self._task:
                self._task.cancel()
                self._task = None
        finally:
            self._update_state(disconnected=False)

    def _start_connect_loop(self):
        if not self._task and self.atv is None and self._is_on:
            self._task = asyncio.ensure_future(
                self._connect_loop(), loop=self.hass.loop)

    async def _connect_loop(self):
        _LOGGER.debug("Starting connect loop")

        # Try to find device and connect as long as the user has said that
        # we are allowed to connect and we are not already connected.
        while self._is_on and self.atv is None:
            try:
                conf = await self._scan()
                if conf:
                    await self._connect(conf)
            except asyncio.CancelledError:
                pass
            except Exception:
                _LOGGER.exception("Failed to connect")
                self.atv = None

            if self.atv is None:
                await asyncio.sleep(3)

        _LOGGER.debug("Connect loop ended")
        self._task = None

    async def _scan(self):
        import pyatv

        self._update_state(message="Discovering device...")
        atvs = await pyatv.scan(self.hass.loop,
                                identifier=self.identifier,
                                protocol=self.protocol,
                                hosts=[self.address])
        if atvs:
            return atvs[0]

        _LOGGER.debug("Failed to find device %s with address %s, trying to scan",
                      self.identifier, self.address)

        atvs = await pyatv.scan(self.hass.loop,
                                identifier=self.identifier,
                                protocol=self.protocol)
        if atvs:
            return atvs[0]

        self._update_state("Device not found, trying again later...")
        _LOGGER.debug("Failed to find device %s, trying later", self.identifier)

        return None

    async def _connect(self, conf):
        import pyatv
        from pyatv.const import Protocol

        for protocol, credentials in self.credentials.items():
            conf.set_credentials(Protocol(int(protocol)), credentials)

        self._update_state("Connecting to device...")
        self.atv = await pyatv.connect(conf, self.hass.loop, session=self.session)
        self.atv.listener = self

        self._update_state("Connected, waiting for update...", connected=True)
        self.atv.push_updater.start()

        self.address_updater(str(conf.address))

    @property
    def is_connecting(self):
        """Return true if connection is in progress."""
        return self._task is not None

    def _update_state(self, message="", connected=False, disconnected=False):
        for listener in self.listeners:
            if connected:
                listener.device_connected()
            if disconnected:
                listener.device_disconnected()
            self.message = message
            self.hass.async_create_task(listener.async_update_ha_state())
