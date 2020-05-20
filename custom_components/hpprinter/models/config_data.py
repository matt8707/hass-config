from typing import Any

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL

from ..helpers.const import *


class ConfigData:
    name: str
    host: str
    ssl: bool
    port: int
    should_store: bool
    update_interval: int
    log_level: str
    file_reader: Any

    def __init__(self):
        self.name = ""
        self.host = ""
        self.ssl = False
        self.port = 80
        self.should_store = False
        self.update_interval = 60
        self.log_level = LOG_LEVEL_DEFAULT
        self.file_reader = None

    @property
    def protocol(self):
        protocol = PROTOCOLS[self.ssl]

        return protocol

    def __repr__(self):
        obj = {
            CONF_NAME: self.name,
            CONF_HOST: self.host,
            CONF_SSL: self.ssl,
            CONF_PORT: self.port,
            CONF_STORE_DATA: self.should_store,
            CONF_UPDATE_INTERVAL: self.update_interval,
            CONF_LOG_LEVEL: self.log_level,
        }

        to_string = f"{obj}"

        return to_string
