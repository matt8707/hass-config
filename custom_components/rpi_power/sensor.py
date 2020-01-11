"""
A sensor platform which detects underruns and capped status from the official Raspberry Pi Kernel.
Minimal Kernel needed is 4.14+
"""
import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.1.5'

_LOGGER = logging.getLogger(__name__)

SYSFILE = '/sys/devices/platform/soc/soc:firmware/get_throttled'

CONF_TEXT_STATE = 'text_state'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_TEXT_STATE, default=False): cv.boolean,
    })

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    import os
    text_state = config.get(CONF_TEXT_STATE)
    exist = os.path.isfile(SYSFILE)
    if exist:
        add_devices([RaspberryChargerSensor(text_state)], True)
    else:
        _LOGGER.critical('Cant find the system class needed for this component, make sure that your kernel is recent and the hardware is supported.')

class RaspberryChargerSensor(Entity):
    """The class for this sensor"""
    def __init__(self, text_state):
        self._state = None
        self._description = None
        self._text_state = text_state
        self.update()

    def update(self):
        """The update method"""
        _throttled = open(SYSFILE, 'r').read()[:-1]
        _throttled = _throttled[:4]
        if _throttled == '0':
            self._description = 'Everything is working as intended'
        elif _throttled == '1000':
            self._description = 'Under-voltage was detected, consider getting a uninterruptible power supply for your Raspberry Pi.'
        elif _throttled == '2000':
            self._description = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        elif _throttled == '3000':
            self._description = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        elif _throttled == '4000':
            self._description = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        elif _throttled == '5000':
            self._description = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        elif _throttled == '8000':
            self._description = 'Your Raspberry Pi is overheating, consider getting a fan or heat sinks.'
        else:
            self._description = 'There is a problem with your power supply or system.'
        if self._text_state:
            self._state = self._description
            self._attribute = {'value': _throttled}
        else:
            self._state = _throttled
            self._attribute = {'description': self._description}

    @property
    def name(self):
        """Return the name of the sensor"""
        return 'RPi Power status'

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return 'mdi:raspberry-pi'

    @property
    def device_state_attributes(self):
        """Return the attribute(s) of the sensor"""
        return self._attribute
