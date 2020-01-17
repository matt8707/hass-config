# -*- coding: utf-8 -*-

import six
# noinspection PyCompatibility
from . import exceptions
from .remote_legacy import RemoteLegacy
from .remote_websocket import RemoteWebsocket
from .remote_encrypted import RemoteEncrypted
from .config import Config
from .key_mappings import KEYS


class KeyWrapper(object):
    def __init__(self, remote, key):
        self.remote = remote
        self.key = key

    def __call__(self):
        self.key(self.remote)


class RemoteMeta(type):

    def __call__(cls, config):

        if isinstance(config, dict):
            config = Config(**config)

        if config.method == "legacy":
            remote = RemoteLegacy(config)
        elif config.method == "websocket":
            remote = RemoteWebsocket(config)
        elif config.method == "encrypted":
            remote = RemoteEncrypted(config)
        else:
            raise exceptions.ConfigUnknownMethod(config.method)

        for name, key in KEYS.items():
            remote.__dict__[name] = KeyWrapper(remote, key)

        return remote


@six.add_metaclass(RemoteMeta)
class Remote(object):

    def __init__(self, config):
        self.config = config



