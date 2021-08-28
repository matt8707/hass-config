#!/usr/bin/env python3
"""Support for Tuya Binary Sensor."""

import logging
import json
from typing import Callable, List, Optional

from tuya_iot import TuyaDevice, TuyaDeviceManager
from threading import Timer

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_GARAGE_DOOR,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_SMOKE,
    DEVICE_CLASS_LOCK,
    DEVICE_CLASS_BATTERY,
    DOMAIN as DEVICE_DOMAIN,
    BinarySensorEntity,
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

TUYA_SUPPORT_TYPE = [
    "mcs",  # Door Window Sensor
    "ywbj",  # Smoke Detector
    "rqbj",  # Gas Detector
    "pir",  # PIR Detector
    "sj",  # Water Detector
    "sos",  # Emergency Button
    "hps",  # Human Presence Sensor
    "ms",  # Residential Lock
    "ckmkzq",  # Garage Door Opener
]

# Door Window Sensor
# https://developer.tuya.com/en/docs/iot/s?id=K9gf48hm02l8m

DPCODE_SWITCH = "switch"


DPCODE_BATTERY_STATE = "battery_state"

DPCODE_DOORCONTACT_STATE = "doorcontact_state"
DPCODE_SMOKE_SENSOR_STATE = "smoke_sensor_state"
DPCODE_SMOKE_SENSOR_STATUS = "smoke_sensor_status"
DPCODE_GAS_SENSOR_STATE = "gas_sensor_state"
DPCODE_PIR = "pir"
DPCODE_WATER_SENSOR_STATE = "watersensor_state"
DPCODE_SOS_STATE = "sos_state"
DPCODE_PRESENCE_STATE = "presence_state"
DPCODE_TEMPER_ALRAM = "temper_alarm"
DPCODE_DOORLOCK_STATE = "closed_opened"


async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya binary sensors dynamically through tuya discovery."""
    _LOGGER.info("binary sensor init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update(
        {DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya sensor."""
        _LOGGER.info(f"binary sensor add->{dev_ids}")
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

        if DPCODE_DOORLOCK_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_DOOR,
                    DPCODE_DOORLOCK_STATE,
                    (lambda d: d.status.get(DPCODE_DOORLOCK_STATE, "none") != "closed"),
                )
            )
        if DPCODE_DOORCONTACT_STATE in device.status:
            if device.category == "ckmkzq":
                device_class_d = DEVICE_CLASS_GARAGE_DOOR
            else:
                device_class_d = DEVICE_CLASS_DOOR
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    device_class_d,
                    DPCODE_DOORCONTACT_STATE,
                    (lambda d: d.status.get(DPCODE_DOORCONTACT_STATE, False)),
                )
            )
        if DPCODE_SWITCH in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_DOOR,
                    DPCODE_SWITCH,
                    (lambda d: d.status.get(DPCODE_SWITCH, False)),
                )
            )
        if DPCODE_SMOKE_SENSOR_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_SMOKE,
                    DPCODE_SMOKE_SENSOR_STATE,
                    (lambda d: d.status.get(DPCODE_SMOKE_SENSOR_STATE, 1) == "1"),
                )
            )
        if DPCODE_SMOKE_SENSOR_STATUS in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_SMOKE,
                    DPCODE_SMOKE_SENSOR_STATUS,
                    (lambda d: d.status.get(
                        DPCODE_SMOKE_SENSOR_STATUS, 'normal') == "alarm"),
                )
            )
        if DPCODE_BATTERY_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_BATTERY,
                    DPCODE_BATTERY_STATE,
                    (lambda d: d.status.get(DPCODE_BATTERY_STATE, 'normal') == "low"),
                )
            )
        if DPCODE_TEMPER_ALRAM in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_MOTION,
                    DPCODE_TEMPER_ALRAM,
                    (lambda d: d.status.get(DPCODE_TEMPER_ALRAM, False)),
                )
            )
        if DPCODE_GAS_SENSOR_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_GAS,
                    DPCODE_GAS_SENSOR_STATE,
                    (lambda d: d.status.get(DPCODE_GAS_SENSOR_STATE, 1) == "1"),
                )
            )
        if DPCODE_PIR in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_MOTION,
                    DPCODE_PIR,
                    (lambda d: d.status.get(DPCODE_PIR, "none") == "pir"),
                )
            )
        if DPCODE_WATER_SENSOR_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_MOISTURE,
                    DPCODE_WATER_SENSOR_STATE,
                    (lambda d: d.status.get(
                        DPCODE_WATER_SENSOR_STATE, "normal") == "alarm"),
                )
            )
        if DPCODE_SOS_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_PROBLEM,
                    DPCODE_SOS_STATE,
                    (lambda d: d.status.get(DPCODE_SOS_STATE, False)),
                )
            )
        if DPCODE_PRESENCE_STATE in device.status:
            entities.append(
                TuyaHaBSensor(
                    device,
                    device_manager,
                    DEVICE_CLASS_MOTION,
                    DPCODE_PRESENCE_STATE,
                    (
                        lambda d: d.status.get(DPCODE_PRESENCE_STATE, "none")
                        == "presence"
                    ),
                )
            )

    return entities


class TuyaHaBSensor(TuyaHaDevice, BinarySensorEntity):
    """Tuya Binary Sensor Device."""

    def __init__(
        self,
        device: TuyaDevice,
        device_manager: TuyaDeviceManager,
        sensor_type: str,
        sensor_code: str,
        sensor_is_on: Callable[..., bool],
    ):
        """Init TuyaHaBSensor."""
        self._type = sensor_type
        self._code = sensor_code
        self._is_on = sensor_is_on
        super().__init__(device, device_manager)

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return f"{super().unique_id}{self._code}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.tuya_device.name + "_" + self._code

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._is_on(self.tuya_device)

    @property
    def device_class(self):
        """Device class of this entity."""
        return self._type

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return True

    def reset_pir(self):
        self.tuya_device.status[DPCODE_PIR] = "none"
        self.schedule_update_ha_state()

    def schedule_update_ha_state(self, force_refresh: bool = False) -> None:

        if self._code == DPCODE_PIR:
            pir_range = json.loads(self.tuya_device.status_range.get(DPCODE_PIR, {}).values).get(
                "range"
            )
            if len(pir_range) == 1 and self.tuya_device.status[DPCODE_PIR] == "pir":
                timer = Timer(10, lambda: self.reset_pir())
                timer.start()

        super().schedule_update_ha_state(force_refresh)
