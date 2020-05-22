import logging
from .const import DOMAIN, DATA_DEVICES, DATA_ALIASES, USER_COMMANDS

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
        command = call.service.replace('_','-')
        call.data = dict(call.data)
        call.data['command'] = command
        handle_command(call)

    hass.services.async_register(DOMAIN, 'command', handle_command)
    for cmd in USER_COMMANDS:
        hass.services.async_register(DOMAIN, cmd.replace('-','_'), command_wrapper)
