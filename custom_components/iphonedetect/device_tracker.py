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
                                                           SOURCE_TYPE_ROUTER,
                                                           ATTR_IP)
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

REACHABLE_DEVICES = []

class Host:
    """Host object with arp detection."""

    def __init__(self, dev_id, dev_ip):
        """Initialize the Host."""
        self.dev_id = dev_id
        self.dev_ip = dev_ip

    def ping_device(self):
        """Send UDP message to probe device."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.sendto(CONST_MESSAGE, (self.dev_ip, CONST_MESSAGE_PORT))
        _LOGGER.debug(f"Probe sent to {self.dev_id} on {self.dev_ip}")

    def update_device(self, see):
        """Update tracked devices"""
        if self.dev_ip in REACHABLE_DEVICES:
            _LOGGER.debug(f"Device {self.dev_id} on {self.dev_ip} is HOME")
            see(dev_id=self.dev_id,
            attributes = {ATTR_IP: self.dev_ip},
            source_type=SOURCE_TYPE_ROUTER)
        else:
            _LOGGER.debug(f"Device {self.dev_id} on {self.dev_ip} is AWAY")

    @staticmethod
    def find_with_ip():
        """Queries the network neighbours and lists found IP's"""
        state_filter = " nud " + " nud ".join(HOME_STATES.values()).lower()
        cmd = f"ip neigh show {state_filter}".split()
        neighbours = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        neighbours_ip = [_.split()[0] for _ in neighbours.stdout.splitlines()]
        return neighbours_ip

    @staticmethod
    def find_with_arp():
        """Queries the arp table and lists found IP's"""
        cmd = "arp -na"
        neighbours = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        neighbours_ip = [_.split()[1][1:-1] for _ in neighbours.stdout.splitlines() if _.count(":") == 5]
        return neighbours_ip

def setup_scanner(hass, config, see, discovery_info=None):
    """Set up the Host objects and return the update function."""

    if subprocess.run("which ip", shell=True, stdout=subprocess.DEVNULL).returncode == 0:
        _LOGGER.debug("Using 'IP' to find tracked devices")
        _use_cmd_ip = True
    elif subprocess.run("which arp", shell=True, stdout=subprocess.DEVNULL).returncode == 0:
        _LOGGER.warn("Using 'ARP' to find tracked devices")
        _use_cmd_ip = False
    else:
        _LOGGER.fatal("Can't get neighbours from host OS!")
        return

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

            global REACHABLE_DEVICES
            if _use_cmd_ip:
                REACHABLE_DEVICES = Host.find_with_ip()
            else:
                REACHABLE_DEVICES = Host.find_with_arp()

            for host in hosts:
                Host.update_device(host, see)

        except Exception as e:
            _LOGGER.error(e)

        finally:
            hass.helpers.event.track_point_in_utc_time(
                update_interval, dt_util.utcnow() + interval)

    update_interval(None)
    return True
