# -*- coding: utf-8 -*-

"""Remote control Samsung televisions via TCP/IP connection"""


__title__ = "samsungctl"
__version__ = "0.8.65b"
__url__ = "https://github.com/kdschlosser/samsungctl"
__author__ = "Lauri Niskanen, Kevin Schlosser"
__author_email__ = "kevin.g.schlosser@gmail.com"
__license__ = "MIT"

from . import utils # NOQA
from .config import Config # NOQA
from .remote import Remote  # NOQA


def discover(timeout=8):
    from .upnp.discover import discover as _discover
    res = list(_discover(timeout=timeout))

    return res
