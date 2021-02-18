import logging

from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_entries_for_device
)
from homeassistant.const import STATE_UNAVAILABLE

from .const import (
    DOMAIN, DATA_DEVICES, DATA_ALIASES,
    USER_COMMANDS, DATA_CONFIG, CONFIG_DEVICES
)

_LOGGER = logging.getLogger(__name__)


async def setup_service(hass):

    def handle_command(call):
        command = call.data.get("command", None)
        if not command:
            return

        targets = call.data.get("deviceID", None)
        if isinstance(targets, str):
            targets = [targets]
        devices = hass.data[DOMAIN][DATA_DEVICES]
        aliases = hass.data[DOMAIN][DATA_ALIASES]
        if not targets:
            targets = devices.keys()
        targets = [aliases.get(t, t) for t in targets]

        data = dict(call.data)
        del data["command"]

        for t in targets:
            if t in devices:
                devices[t].send(command, **data)

    def command_wrapper(call):
        command = call.service.replace('_', '-')
        call.data = dict(call.data)
        call.data['command'] = command
        handle_command(call)

    hass.services.async_register(DOMAIN, 'command', handle_command)
    for cmd in USER_COMMANDS:
        hass.services.async_register(
            DOMAIN,
            cmd.replace('-', '_'),
            command_wrapper
        )

    async def call_service(service_call):
        await async_clean_devices(hass, service_call.data)

    hass.services.async_register(DOMAIN, 'clean_devices', call_service)


async def async_clean_devices(hass, data):
    config_entry = hass.config_entries.async_entries(DOMAIN)[0]

    entity_registry = await hass.helpers.entity_registry.async_get_registry()
    device_registry = await hass.helpers.device_registry.async_get_registry()
    entity_entries = async_entries_for_config_entry(
        entity_registry,
        config_entry.entry_id
    )

    device_entries = [
        entry
        for entry
        in device_registry.devices.values()
        if config_entry.entry_id in entry.config_entries
    ]

    user_config = hass.data[DOMAIN][DATA_CONFIG]

    devices_to_keep = []
    if CONFIG_DEVICES in user_config:
        for d in device_entries:
            for c in user_config[CONFIG_DEVICES]:
                if (DOMAIN, c) in d.identifiers:
                    devices_to_keep.append(d.id)

    entities_to_remove = []
    for e in entity_entries:
        entity = hass.states.get(e.entity_id)
        if entity.state != STATE_UNAVAILABLE:
            continue
        if e.device_id in devices_to_keep:
            continue
        entities_to_remove.append(e)

    for e in entities_to_remove:
        entity_registry.async_remove(e.entity_id)

    removed = []
    for d in device_entries:
        if len(async_entries_for_device(entity_registry, d.id)) == 0:
            removed.append(d.name)
            device_registry.async_remove_device(d.id)

    devices = hass.data[DOMAIN][DATA_DEVICES]
    for rec in devices:
        devices[rec].send(
            'toast',
            message=f"Removed devices: {removed}"
        )
