DOMAIN = "browser_mod"

FRONTEND_SCRIPT_URL = "/browser_mod.js"

DATA_EXTRA_MODULE_URL = 'frontend_extra_module_url'

DATA_DEVICES = "devices"
DATA_ALIASES = "aliases"
DATA_ADDERS = "adders"
DATA_CONFIG = "config"
DATA_SETUP_COMPLETE = "setup_complete"

CONFIG_DEVICES = "devices"
CONFIG_PREFIX = "prefix"
CONFIG_DISABLE = "disable"
CONFIG_DISABLE_ALL = "all"

WS_ROOT = DOMAIN
WS_CONNECT = "{}/connect".format(WS_ROOT)
WS_UPDATE = "{}/update".format(WS_ROOT)
WS_CAMERA = "{}/camera".format(WS_ROOT)

USER_COMMANDS = [
        "debug",
        "popup",
        "close-popup",
        "navigate",
        "more-info",
        "set-theme",
        "lovelace-reload",
        "window-reload",
        "blackout",
        "no-blackout",
        "toast",
        "commands",
        "call_service",
        "delay",
        ]
