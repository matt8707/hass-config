#!/usr/bin/env python3
"""Support for Tuya vacuum."""
from __future__ import annotations

import logging
from typing import Any

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.components.vacuum import (
    DOMAIN as DEVICE_DOMAIN,
    SUPPORT_STATE,
    SUPPORT_STATUS,
    SUPPORT_BATTERY,
    SUPPORT_START,
    SUPPORT_PAUSE,
    SUPPORT_RETURN_HOME,
    SUPPORT_STOP,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_PAUSED,
    STATE_IDLE,
    STATE_RETURNING,
    StateVacuumEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .base import TuyaHaDevice
from .const import (
    DOMAIN,
    TUYA_DEVICE_MANAGER,
    TUYA_DISCOVERY_NEW,
    TUYA_HA_DEVICES,
    TUYA_HA_TUYA_MAP,
)

_LOGGER = logging.getLogger(__name__)

TUYA_SUPPORT_TYPE = {
    "sd",  # Robot Vaccuum
}

# Vacuum(sd),
# https://developer.tuya.com/docs/iot/open-api/standard-function/electrician-category/categorykgczpc?categoryId=486118
DPCODE_MODE = "mode"
DPCODE_POWER = "power"  # Device switch
DPCODE_POWER_GO = "power_go"    # Cleaning switch
DPCODE_STATUS = "status"
DPCODE_PAUSE = "pause"
DPCODE_RETURN_HOME = "switch_charge"

DPCODE_BATTERY = "electricity_left"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up tuya vacuum dynamically through tuya discovery."""
    _LOGGER.info("vacuum init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya sensor."""
        _LOGGER.info(f"vacuum add -> {dev_ids}")
        if not dev_ids:
            return
        entities = await hass.async_add_executor_job(_setup_entities, hass, dev_ids)
        hass.data[DOMAIN][TUYA_HA_DEVICES].extend(entities)
        async_add_entities(entities)

    async_dispatcher_connect(
        hass, TUYA_DISCOVERY_NEW.format(DEVICE_DOMAIN), async_discover_device
    )

    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    device_ids = []
    for (device_id, device) in device_manager.device_map.items():
        if device.category in TUYA_SUPPORT_TYPE:
            device_ids.append(device_id)
    await async_discover_device(device_ids)


def _setup_entities(hass, device_ids: list):
    """Set up Tuya Switch device."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue

        entities.append(TuyaHaVacuum(device, device_manager))

    return entities


class TuyaHaVacuum(TuyaHaDevice, StateVacuumEntity):
    """Tuya Vacuum Device."""

    @property
    def name(self) -> str | None:
        """Return Tuya device name."""
        return self.tuya_device.name

    @property
    def battery_level(self) -> int | None:
        """Return Tuya device state."""
        return self.tuya_device.status.get(DPCODE_BATTERY)

    @property
    def state(self):
        """Return Tuya device state."""
        if DPCODE_PAUSE in self.tuya_device.status and self.tuya_device.status[DPCODE_PAUSE]:
            return STATE_PAUSED

        status = self.tuya_device.status.get(DPCODE_STATUS)

        if status == "standby":
            return STATE_IDLE
        if status == "goto_charge":
            return STATE_RETURNING
        if status == "charging" or status == "charge_done":
            return STATE_DOCKED
        return STATE_CLEANING

    @property
    def supported_features(self):
        """Flag supported features."""
        supports = 0
        if DPCODE_PAUSE in self.tuya_device.status:
            supports = supports | SUPPORT_PAUSE
        if DPCODE_RETURN_HOME in self.tuya_device.status:
            supports = supports | SUPPORT_RETURN_HOME
        if DPCODE_STATUS in self.tuya_device.status:
            supports = supports | SUPPORT_STATE
            supports = supports | SUPPORT_STATUS
        if DPCODE_POWER_GO in self.tuya_device.status:
            supports = supports | SUPPORT_STOP
            supports = supports | SUPPORT_START
        if DPCODE_BATTERY in self.tuya_device.status:
            supports = supports | SUPPORT_BATTERY
        return supports

    # Functions
    # def turn_on(self, **kwargs: Any) -> None:
    #     """Turn the device on."""
    #     _LOGGER.debug(f"Turning on {self.name}")

    #     self.tuya_device_manager.sendCommands(
    #         self.tuya_device.id, [{"code": DPCODE_POWER, "value": True}]
    #     )

    def start(self, **kwargs: Any) -> None:
        """Turn the device on."""
        _LOGGER.debug(f"Starting {self.name}")

        self._send_command([{"code": DPCODE_POWER_GO, "value": True}])

    # Turn off/pause/stop all do the same thing

    # def turn_off(self, **kwargs: Any) -> None:
    #     """Turn the device off."""
    #     _LOGGER.debug(f"Turning off {self.name}")
    #     self.tuya_device_manager.sendCommands(
    #         self.tuya_device.id, [{"code": DPCODE_POWER, "value": False}]
    #     )

    def stop(self, **kwargs: Any) -> None:
        """Turn the device off."""
        _LOGGER.debug(f"Stopping {self.name}")
        self._send_command([{"code": DPCODE_POWER_GO, "value": False}])

    def pause(self, **kwargs: Any) -> None:
        """Pause the device."""
        _LOGGER.debug(f"Pausing {self.name}")
        self._send_command([{"code": DPCODE_PAUSE, "value": True}])

    # def start_pause(self, **kwargs: Any) -> None:
    #     """Start/Pause the device"""
    #     _LOGGER.debug(f"Start/Pausing {self.name}")
    #     status = False
    #     status = self.tuya_device.status.get(DPCODE_PAUSE)
    #     self.tuya_device_manager.sendCommands(
    #         self.tuya_device.id, [{"code": DPCODE_PAUSE, "value": not status}]
    #     )

    def return_to_base(self, **kwargs: Any) -> None:
        """Return device to Dock"""
        _LOGGER.debug(f"Return to base device {self.name}")
        self._send_command([{"code": DPCODE_MODE, "value": "chargego"}])
