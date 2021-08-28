#!/usr/bin/env python3
"""Support for Tuya switches."""

import json
import logging
from typing import List, Optional, Tuple

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.components.number import DOMAIN as DEVICE_DOMAIN, NumberEntity
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
    "hps",  # Human Presence Sensor
    "kfj",  # Coffee Maker
}

# Switch(kg), Socket(cz), Power Strip(pc)
# https://developer.tuya.com/docs/iot/open-api/standard-function/electrician-category/categorykgczpc?categoryId=486118
DPCODE_SENSITIVITY = "sensitivity"

# Coffee Maker
# https://developer.tuya.com/en/docs/iot/f?id=K9gf4701ox167
DPCODE_TEMPSET = "temp_set"
DPCODE_WARMTIME = "warm_time"
DPCODE_WATERSET = "water_set"
DPCODE_POWDERSET = "powder_set"
DPCODE_CLOUDRECIPE = "cloud_recipe_number"

async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya number dynamically through tuya discovery."""
    _LOGGER.info("number init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya number."""
        _LOGGER.info(f"number add-> {dev_ids}")
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


def _setup_entities(hass, device_ids: List):
    """Set up Tuya Switch device."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue

        if DPCODE_SENSITIVITY in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_SENSITIVITY))

        if DPCODE_TEMPSET in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_TEMPSET))

        if DPCODE_WARMTIME in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_WARMTIME))

        if DPCODE_WATERSET in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_WATERSET))

        if DPCODE_POWDERSET in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_POWDERSET))

        if DPCODE_CLOUDRECIPE in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_CLOUDRECIPE))

    return entities


class TuyaHaNumber(TuyaHaDevice, NumberEntity):
    """Tuya Device Number."""

    def __init__(
        self, device: TuyaDevice, device_manager: TuyaDeviceManager, code: str = ""
    ):
        """Init tuya number device."""
        self._code = code
        super().__init__(device, device_manager)

    # ToggleEntity

    def set_value(self, value: float) -> None:
        """Update the current value."""
        self._send_command([{"code": self._code, "value": int(value)}])

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return f"{super().unique_id}{self._code}"

    @property
    def name(self) -> Optional[str]:
        """Return Tuya device name."""
        return self.tuya_device.name + self._code

    @property
    def value(self) -> float:
        """Return current value."""
        return self.tuya_device.status.get(self._code, 0)

    @property
    def min_value(self) -> float:
        """Return min value."""
        return self._get_code_range()[0]

    @property
    def max_value(self) -> float:
        """Return max value."""
        return self._get_code_range()[1]

    @property
    def step(self) -> float:
        """Return step."""
        return self._get_code_range()[2]

    def _get_code_range(self) -> Tuple[int, int, int]:
        dp_range = json.loads(self.tuya_device.function.get(self._code).values)
        return dp_range.get("min", 0), dp_range.get("max", 0), dp_range.get("step", 0)
