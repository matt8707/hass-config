"""
From : https://community.home-assistant.io/t/iphone-device-tracker-on-linux/13698
Tracks iPhones by sending a udp message to port 5353.
An entry in the arp cache is then made and checked.

device_tracker:
  - platform: iphonedetect
    hosts:
      host_one: 192.168.2.12
      host_two: 192.168.2.25

"""

import logging
import socket
import subprocess

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.components.device_tracker.const import (SCAN_INTERVAL,
                                                           SOURCE_TYPE_ROUTER)
from homeassistant.const import CONF_HOSTS, CONF_SCAN_INTERVAL


from .const import (
    HOME_STATES,
    CONST_MESSAGE,
    CONST_MESSAGE_PORT,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOSTS): {cv.string: cv.string},
        vol.Optional(CONF_SCAN_INTERVAL): cv.time_period,
    }
)

_LOGGER = logging.getLogger(__name__)


class Host:
    """Host object with arp detection."""

    def __init__(self, dev_id, dev_ip, dev_mac=None):
        """Initialize the Host."""
        self.dev_id = dev_id
        self.dev_ip = dev_ip

    def ping_device(self):
        """Send UDP message to probe device."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.sendto(CONST_MESSAGE, (self.dev_ip, CONST_MESSAGE_PORT))
        _LOGGER.debug(f"Probe message sent to {self.dev_ip}")

    @staticmethod
    def find_in_arp(devices, see):
        """Queries the network neighbours and looks for tracked devices"""

        state_filter = " nud " + " nud ".join(HOME_STATES.values()).lower()
        cmd = f"ip neigh show {state_filter}".split()

        # Get all entries
        neighbours = subprocess.check_output(cmd, shell=False).decode()
        # Split the lines to a list of lists
        neighbour = [_.split() for _ in neighbours.splitlines()]

        for device in devices:
            if device[0] in [(_[0]) for _ in neighbour]:
                _LOGGER.debug(f"Device {device[1]} on {device[0]} is HOME")
                see(dev_id=device[1], source_type=SOURCE_TYPE_ROUTER)
            else:
                _LOGGER.debug(f"Device {device[1]} on {device[0]} is AWAY")


def setup_scanner(hass, config, see, discovery_info=None):
    """Set up the Host objects and return the update function."""
    hosts = [Host(dev_id, dev_ip) for (dev_id, dev_ip) in
             config[CONF_HOSTS].items()]
    interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

    _LOGGER.info("Started iphonedetect with interval=%s on hosts: %s",
                  interval, ", ".join([host.dev_ip for host in hosts]))

    def update_interval(now):
        """Update all the hosts on every interval time."""
        try:
            for host in hosts:
                Host.ping_device(host)

            devices = [(host.dev_ip, host.dev_id) for host in hosts]
            Host.find_in_arp(devices, see)

        finally:
            hass.helpers.event.track_point_in_utc_time(
                update_interval, dt_util.utcnow() + interval)

    update_interval(None)
    return True
