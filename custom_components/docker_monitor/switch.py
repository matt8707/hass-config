'''
Docker Monitor component

For more details about this component, please refer to the documentation at
https://github.com/Sanderhuisman/home-assistant-custom-components
'''
import logging

from homeassistant.components.switch import (
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
    SwitchDevice
)
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_NAME
)
from homeassistant.core import callback
from homeassistant.util import slugify as util_slugify

from .const import (
    CONF_ATTRIBUTION,
    CONF_CONTAINERS,
    CONF_CONTAINER_SWITCH,
    CONTAINER_INFO,
    CONTAINER_INFO_STATUS,
    DOMAIN,
    ICON_SWITCH
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None):
    """Set up the Docker Monitor Switch."""

    if discovery_info is None:
        _LOGGER.warning(
            "To use this you need to configure the 'docker_monitor' component")
        return

    host_name = discovery_info[CONF_NAME]
    api = hass.data[DOMAIN][host_name]

    switches = [ContainerSwitch(host_name, api, name)
            for name in discovery_info[CONF_CONTAINERS].keys()
            if discovery_info[CONF_CONTAINERS][name][CONF_CONTAINER_SWITCH]]

    if switches:
        async_add_entities(switches)
    else:
        _LOGGER.info("No containers setup")


class ContainerSwitch(SwitchDevice):
    def __init__(self, clientname, api, name):
        self._clientname = clientname
        self._api = api
        self._name = name

        self._container = None
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._clientname, self._name)

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return ICON_SWITCH

    @property
    def device_state_attributes(self):
        return {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION
        }

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._state is not None

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self):
        """Turn Mill unit on."""
        if self._container:
            try:
                self._container.start()
            except Exception as ex:
                _LOGGER.info("Cannot start container ({})".format(ex))

    async def async_turn_off(self):
        """Turn Mill unit off."""
        if self._container:
            try:
                self._container.stop()
            except Exception as ex:
                _LOGGER.info("Cannot stop container ({})".format(ex))

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._container = self._api.watch_container(
            self._name, self.event_callback)
        self.event_callback()

    def event_callback(self):
        """Update callback."""

        state = None
        try:
            info = self._container.get_info()
        except Exception as ex:
            _LOGGER.info("Cannot request container info ({})".format(ex))
        else:
            state = info.get(CONTAINER_INFO_STATUS) == 'running'

        if state is not self._state:
            self._state = state
            self.async_schedule_update_ha_state()
