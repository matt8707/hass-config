'''
Docker Monitor component

For more details about this component, please refer to the documentation at
https://github.com/Sanderhuisman/home-assistant-custom-components
'''
import logging
from datetime import timedelta

import homeassistant.util.dt as dt_util
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    STATE_UNAVAILABLE,
    CONF_SENSORS
)
from homeassistant.core import callback
from homeassistant.util import slugify as util_slugify
from homeassistant.helpers.entity import Entity

from .const import (
    ATTR_CREATED,
    ATTR_IMAGE,
    ATTR_MEMORY_LIMIT,
    ATTR_ONLINE_CPUS,
    ATTR_STARTED_AT,
    ATTR_VERSION_API,
    ATTR_VERSION_ARCH,
    ATTR_VERSION_OS,
    CONF_ATTRIBUTION,
    CONF_CONTAINERS,
    CONF_MONITOR_CONTAINER_CONDITIONS,
    CONF_MONITOR_CONTAINER_CPU_PERCENTAGE,
    CONF_MONITOR_CONTAINER_IMAGE,
    CONF_MONITOR_CONTAINER_MEMORY_PERCENTAGE,
    CONF_MONITOR_CONTAINER_MEMORY_USAGE,
    CONF_MONITOR_CONTAINER_NETWORK_TOTAL_DOWN,
    CONF_MONITOR_CONTAINER_NETWORK_TOTAL_UP,
    CONF_MONITOR_CONTAINER_STATUS,
    CONF_MONITOR_CONTAINER_UPTIME,
    CONF_MONITOR_UTILISATION_CONDITIONS,
    CONF_MONITOR_UTILISATION_VERSION,
    CONTAINER_INFO,
    CONTAINER_INFO_CREATED,
    CONTAINER_INFO_ID,
    CONTAINER_INFO_IMAGE,
    CONTAINER_INFO_STARTED,
    CONTAINER_INFO_STATUS,
    DOMAIN,
    PRECISION,
    VERSION_INFO_API_VERSION,
    VERSION_INFO_ARCHITECTURE,
    VERSION_INFO_KERNEL,
    VERSION_INFO_OS,
    VERSION_INFO_VERSION,
    VERSION_INFO_CONTAINERS_TOTAL,
    VERSION_INFO_CONTAINERS_PAUSED,
    VERSION_INFO_CONTAINERS_RUNNING,
    VERSION_INFO_CONTAINERS_STOPPED,
    VERSION_INFO_IMAGES,
    CONF_MONITOR_UTILISATION_CONTAINERS_TOTAL,
    CONF_MONITOR_UTILISATION_CONTAINERS_PAUSED,
    CONF_MONITOR_UTILISATION_CONTAINERS_RUNNING,
    CONF_MONITOR_UTILISATION_CONTAINERS_STOPPED,
    CONF_MONITOR_UTILISATION_IMAGES_TOTAL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Docker Monitor Sensor."""

    if discovery_info is None:
        _LOGGER.warning(
            "To use this you need to configure the 'docker_monitor' component")
        return

    host_name = discovery_info[CONF_NAME]
    api = hass.data[DOMAIN][host_name]

    sensors = [DockerUtilSensor(api, host_name, variable)
               for variable in discovery_info[CONF_MONITORED_CONDITIONS] if variable in CONF_MONITOR_UTILISATION_CONDITIONS]

    interval = discovery_info[CONF_SCAN_INTERVAL].total_seconds()

    for name, conf in discovery_info[CONF_CONTAINERS].items():
        sensors += [DockerContainerSensor(host_name, api, name, variable, interval)
                    for variable in conf[CONF_SENSORS] if variable in CONF_MONITOR_CONTAINER_CONDITIONS]

    if sensors:
        async_add_entities(sensors)
    else:
        _LOGGER.info("No containers setup")


class DockerUtilSensor(Entity):
    """Representation of a Docker Sensor."""

    def __init__(self, api, clientname, variable):
        """Initialize the sensor."""
        self._api = api
        self._clientname = clientname

        self._var_id = variable
        self._var_name = CONF_MONITOR_UTILISATION_CONDITIONS[variable][0]
        self._var_unit = CONF_MONITOR_UTILISATION_CONDITIONS[variable][1]
        self._var_icon = CONF_MONITOR_UTILISATION_CONDITIONS[variable][2]
        self._var_class = CONF_MONITOR_UTILISATION_CONDITIONS[variable][3]

        self._state = None
        self._attributes = {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION
        }

        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._clientname, self._var_name)

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._var_icon

    @property
    def should_poll(self):
        return True

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._var_class

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._state is not None

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._var_unit

    def update(self):
        """Get the latest data for the states."""
        version = None
        try:
            version = self._api.get_info()
        except Exception as ex:
            _LOGGER.info(
                "Could not request docker daemon info ({})".format(ex))
        else:
            if version:
                if self._var_id == CONF_MONITOR_UTILISATION_VERSION:
                    self._state = version.get(VERSION_INFO_VERSION, None)
                    self._attributes[ATTR_VERSION_API] = version.get(
                        VERSION_INFO_API_VERSION, None)
                    self._attributes[ATTR_VERSION_OS] = version.get(
                        VERSION_INFO_OS, None)
                    self._attributes[ATTR_VERSION_ARCH] = version.get(
                        VERSION_INFO_ARCHITECTURE, None)
                elif self._var_id == CONF_MONITOR_UTILISATION_CONTAINERS_TOTAL:
                    self._state = version.get(VERSION_INFO_CONTAINERS_TOTAL, None)
                elif self._var_id == CONF_MONITOR_UTILISATION_CONTAINERS_PAUSED:
                    self._state = version.get(VERSION_INFO_CONTAINERS_PAUSED, None)
                elif self._var_id == CONF_MONITOR_UTILISATION_CONTAINERS_RUNNING:
                    self._state = version.get(VERSION_INFO_CONTAINERS_RUNNING, None)
                elif self._var_id == CONF_MONITOR_UTILISATION_CONTAINERS_STOPPED:
                    self._state = version.get(VERSION_INFO_CONTAINERS_STOPPED, None)
                elif self._var_id == CONF_MONITOR_UTILISATION_IMAGES_TOTAL:
                    self._state = version.get(VERSION_INFO_IMAGES, None)
            else:
                self._state = None
                self._attributes = None

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class DockerContainerSensor(Entity):
    """Representation of a Docker Sensor."""

    def __init__(self,  clientname, api, name, variable, interval):
        """Initialize the sensor."""
        self._clientname = clientname
        self._api = api
        self._name = name
        self._interval = interval

        self._var_id = variable
        self._var_name = CONF_MONITOR_CONTAINER_CONDITIONS[variable][0]
        self._var_unit = CONF_MONITOR_CONTAINER_CONDITIONS[variable][1]
        self._var_icon = CONF_MONITOR_CONTAINER_CONDITIONS[variable][2]
        self._var_class = CONF_MONITOR_CONTAINER_CONDITIONS[variable][3]

        self._state = None
        self._available = False
        self._attributes = {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION
        }

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return "{} {} {}".format(self._clientname, self._name, self._var_name)

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._var_id == CONF_MONITOR_CONTAINER_STATUS:
            if self._state == 'running':
                return 'mdi:checkbox-marked-circle-outline'
            else:
                return 'mdi:checkbox-blank-circle-outline'
        else:
            return self._var_icon

    @property
    def should_poll(self):
        return False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._var_class

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._var_unit

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._available

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._container = self._api.watch_container(
            self._name, self.event_callback)
        self.event_callback()

    def event_callback(self):
        """Update callback."""

        _LOGGER.info("Sensor {} event".format(self._name))

        info = None
        stats = None
        try:
            info = self._container.get_info()
            stats = self._container.get_stats()
        except Exception as ex:
            _LOGGER.info("Cannot request container info ({})".format(ex))
        else:
            if info:
                state = STATE_UNAVAILABLE

                if self._var_id == CONF_MONITOR_CONTAINER_STATUS:
                    state = info.get(CONTAINER_INFO_STATUS)
                else:
                    if info[CONTAINER_INFO_STATUS] == 'running':
                        # Info
                        if self._var_id == CONF_MONITOR_CONTAINER_UPTIME:
                            up_time = info.get(CONTAINER_INFO_STARTED)
                            if up_time:
                                state = dt_util.as_local(up_time).isoformat()
                        elif self._var_id == CONF_MONITOR_CONTAINER_IMAGE:
                            # get first from array
                            images = info.get(CONTAINER_INFO_IMAGE)
                            if images:
                                state = images[0]

                        # cpu
                        elif stats:
                            if self._var_id == CONF_MONITOR_CONTAINER_CPU_PERCENTAGE:
                                cpu = stats.get('cpu', {}).get('total')
                                if cpu is not None:
                                    state = round(cpu, 1)

                            # memory
                            elif self._var_id == CONF_MONITOR_CONTAINER_MEMORY_USAGE:
                                use = stats.get('memory', {}).get('usage')
                                if use is not None:
                                    # Bytes to MB
                                    state = round(use / (1024 ** 2), PRECISION)
                            elif self._var_id == CONF_MONITOR_CONTAINER_MEMORY_PERCENTAGE:
                                use = stats.get('memory', {}).get(
                                    'usage_percent')
                                if use is not None:
                                    state = round(use, 2)

                            # network
                            elif self._var_id == CONF_MONITOR_CONTAINER_NETWORK_TOTAL_UP:
                                up = stats.get('network', {}).get(
                                    'total_tx')  # Bytes to kB
                                if up is not None:
                                    state = round(up / (1024 ** 2), PRECISION)
                            elif self._var_id == CONF_MONITOR_CONTAINER_NETWORK_TOTAL_DOWN:
                                down = stats.get('network', {}).get('total_rx')
                                if down is not None:
                                    state = round(
                                        down / (1024 ** 2), PRECISION)

                self._available = state is not STATE_UNAVAILABLE
                # if self._state is not state:
                self._state = state
                self.async_schedule_update_ha_state()
            else:
                _LOGGER.error("No Docker information available for '%s' and '%s'", self._name, self._var_id)
