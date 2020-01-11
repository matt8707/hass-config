"""Remote control support for Apple TV."""

from homeassistant.core import callback
from homeassistant.const import CONF_NAME
from homeassistant.components import remote

from .const import DOMAIN, KEY_MANAGER, CONF_IDENTIFIER


PARALLEL_UPDATES = 0


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Apple TV remote platform."""
    if not discovery_info:
        return

    identifier = discovery_info[CONF_IDENTIFIER]
    name = discovery_info[CONF_NAME]
    manager = hass.data[DOMAIN][identifier]
    async_add_entities([AppleTVRemote(name, identifier, manager)])


class AppleTVRemote(remote.RemoteDevice):
    """Device that sends commands to an Apple TV."""

    def __init__(self, name, identifier, manager):
        """Initialize device."""
        self.atv = None
        self._name = name
        self._identifier = identifier
        self._manager = manager

    async def async_added_to_hass(self):
        """Handle when an entity is about to be added to Home Assistant."""
        self._manager.listeners.append(self)

    @callback
    def device_connected(self):
        self.atv = self._manager.atv

    @callback
    def device_disconnected(self):
        self.atv = None

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._identifier)},
            "manufacturer": "Apple",
            "model": "Remote",
            "name": self.name,
            "sw_version": "0.0",
            "via_device": (DOMAIN, self._identifier),
        }

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "remote_" + self._identifier

    @property
    def is_on(self):
        """Return true if device is on."""
        return self.atv is not None

    @property
    def should_poll(self):
        """No polling needed for Apple TV."""
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the device on.

        This method is a coroutine.
        """
        await self._manager.connect()

    async def async_turn_off(self, **kwargs):
        """Turn the device off.

        This method is a coroutine.
        """
        await self._manager.disconnect()

    def async_send_command(self, command, **kwargs):
        """Send a command to one device.

        This method must be run in the event loop and returns a coroutine.
        """
        # Send commands in specified order but schedule only one coroutine
        async def _send_commands():
            for single_command in command:
                if not hasattr(self.atv.remote_control, single_command):
                    continue

                await getattr(self.atv.remote_control, single_command)()

        return _send_commands()
