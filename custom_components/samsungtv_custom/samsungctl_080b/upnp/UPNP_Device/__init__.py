# -*- coding: utf-8 -*-
"""UPNP device mapping tool"""


import logging
from logging import NullHandler

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)


from .discover import discover as _discover # NOQA
from .listen import listen # NOQA
from .upnp_class import UPNPObject # NOQA


def discover(timeout=5, log_level=None, ips=(), dump=''):
    for addr, locations in _discover(timeout, log_level, ips, dump):
        yield UPNPObject(addr, locations, dump)


__title__ = "UPNP_Device"
__version__ = "0.1.0b"
__url__ = "https://github.com/kdschlosser/UPNP_Device"
__author__ = "Kevin Schlosser"
__author_email__ = "kevin.g.schlosser@gmail.com"
__all__ = (
    '__title__', '__version__', '__url__', '__author__', '__author_email__',
    'discover'
)

