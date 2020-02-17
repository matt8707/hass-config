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
import re
import socket
import subprocess

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.components.device_tracker.const import (SCAN_INTERVAL,
                                                           SOURCE_TYPE_ROUTER)
from homeassistant.const import CONF_HOSTS, CONF_SCAN_INTERVAL


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
    vol.Required(CONF_HOSTS): {cv.string: cv.string},
    vol.Optional(CONF_SCAN_INTERVAL): cv.time_period,
    }
)

_LOGGER = logging.getLogger(__name__)


class Host:
    """Host object with arp detection."""

    def __init__(self, ip_address, dev_id, hass, config):
        """Initialize the Host."""
        self.hass = hass
        self.ip_address = ip_address
        self.dev_id = dev_id

    def detectiphone(self):
        """Send udp message and look for MAC address."""
        aSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        aSocket.settimeout(1)
        addr = (self.ip_address, 5353)
        message = b'Steve Jobs'
        aSocket.sendto(message, addr)
    
        try:
            output = subprocess.check_output('ip neigh show to ' + self.ip_address, shell=True)
            output = output.decode('utf-8').rstrip()
            _LOGGER.debug(f'ip n output for {self.dev_id} is: {output}')
        except subprocess.CalledProcessError:
            try:
                output = subprocess.check_output('arp -na|grep ' + self.ip_address, shell=True)
                output = output.decode('utf-8').rstrip()
                _LOGGER.debug(f'arp output for {self.dev_id} is: {output}')
            except subprocess.CalledProcessError:
                _LOGGER.fatal("Could not probe network")
                return False

        mac = re.compile(r'(?:[0-9A-F]{2}[:-]){5}(?:[0-9A-F]{2})', re.IGNORECASE)

        if re.findall(mac, output):
            _LOGGER.debug(f"Device {self.dev_id} ({self.ip_address}) is HOME")
            return True
        else:
            _LOGGER.debug(f"Device {self.dev_id} ({self.ip_address}) is AWAY")
            return False

    def update(self, see):
        """Update device state by sending one or more ping messages."""
        if self.detectiphone():
            see(dev_id=self.dev_id, source_type=SOURCE_TYPE_ROUTER)
            return True

def setup_scanner(hass, config, see, discovery_info=None):
    """Set up the Host objects and return the update function."""
    hosts = [Host(ip, dev_id, hass, config) for (dev_id, ip) in
             config[CONF_HOSTS].items()]
    interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

    _LOGGER.debug("Started iphonedetect with interval=%s on hosts: %s",
                  interval, ",".join([host.ip_address for host in hosts]))
    
    def update_interval(now):
        """Update all the hosts on every interval time."""
        try:
            for host in hosts:
                host.update(see)
        finally:
            hass.helpers.event.track_point_in_utc_time(
                update_interval, dt_util.utcnow() + interval)

    update_interval(None)
    return True
