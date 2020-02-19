# -*- coding: utf-8 -*-
from __future__ import print_function
import ctypes
import socket
import struct
import platform
import sys

import logging

logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] < 3

USHORT = ctypes.c_uint16
SHORT = ctypes.c_int16
CHAR = ctypes.c_uint8
INT = ctypes.c_int
UINT = ctypes.c_uint
INT8 = ctypes.c_int8
UINT8 = ctypes.c_uint8
NULL = None
PWCHAR = ctypes.c_wchar_p
PCHAR = ctypes.c_char_p
POINTER = ctypes.POINTER


logging.debug(platform.system())

if platform.system() == "Darwin" or "BSD" in platform.system():

    # BSD derived systems use marginally different structures
    # than either Linux or Windows.
    # I still keep it in `shared` since we can use
    # both structures equally.
    # noinspection PyTypeChecker,PyPep8Naming
    class sockaddr(ctypes.Structure):
        _fields_ = [
            ('sa_len', UINT8),
            ('sa_familiy', UINT8),
            ('sa_data', CHAR * 14)
        ]

    # noinspection PyTypeChecker,PyPep8Naming
    class sockaddr_in(ctypes.Structure):
        _fields_ = [
            ('sa_len', UINT8),
            ('sa_familiy', UINT8),
            ('sin_port', USHORT),
            ('sin_addr', UINT8 * 4),
            ('sin_zero', CHAR * 8)
        ]
else:
    # noinspection PyTypeChecker,PyPep8Naming
    class sockaddr(ctypes.Structure):
        _fields_ = [
            ('sa_familiy', USHORT),
            ('sa_data', CHAR * 14)
        ]

    # noinspection PyTypeChecker,PyPep8Naming
    class sockaddr_in(ctypes.Structure):
        _fields_ = [
            ('sin_familiy', SHORT),
            ('sin_port', USHORT),
            ('sin_addr', UINT8 * 4),
            ('sin_zero', CHAR * 8)
        ]


def sockaddr_to_ip(sockaddr_ptr):
    if sockaddr_ptr:
        if sockaddr_ptr[0].sa_familiy == socket.AF_INET:
            ipv4 = ctypes.cast(sockaddr_ptr, POINTER(sockaddr_in))
            ippacked = bytes(bytearray(ipv4[0].sin_addr))

            if PY2:
                byte_ip = list(struct.unpack(b'!B', b)[0] for b in ippacked)

                ip_int = 0
                for bv in byte_ip:
                    ip_int = (ip_int << 8) + bv
                if ip_int:
                    res = '.'.join(
                        str(
                            struct.unpack(b'!B', b)[0]
                            if isinstance(b, bytes) else b
                        )
                        for b in struct.pack(b'!I', ip_int)
                    )
                else:
                    res = None
            else:
                res = '.'.join(str(b) for b in ippacked)

            return res
    return None


if platform.system() == 'Windows':
    from ctypes.wintypes import ULONG, DWORD, UINT, INT

    iphlpapi = ctypes.windll.Iphlpapi

    NO_ERROR = 0
    ERROR_BUFFER_OVERFLOW = 111
    AF_UNSPEC = 0

    # noinspection PyTypeChecker,PyPep8Naming
    class SOCKET_ADDRESS(ctypes.Structure):
        _fields_ = [
            ('lpSockaddr', POINTER(sockaddr)),
            ('iSockaddrLength', INT)
        ]


    # noinspection PyTypeChecker,PyPep8Naming
    class IP_ADAPTER_UNICAST_ADDRESS(ctypes.Structure):
        pass

    IP_ADAPTER_UNICAST_ADDRESS._fields_ = [
        ('Length', ULONG),
        ('Flags', DWORD),
        ('Next', POINTER(IP_ADAPTER_UNICAST_ADDRESS)),
        ('Address', SOCKET_ADDRESS),
        ('PrefixOrigin', UINT),
        ('SuffixOrigin', UINT),
        ('DadState', UINT),
        ('ValidLifetime', ULONG),
        ('PreferredLifetime', ULONG),
        ('LeaseLifetime', ULONG),
        ('OnLinkPrefixLength', UINT8),
    ]

    # noinspection PyTypeChecker,PyPep8Naming
    class IP_ADAPTER_ADDRESSES(ctypes.Structure):
        pass


    IP_ADAPTER_ADDRESSES._fields_ = [
        ('Length', ULONG),
        ('IfIndex', DWORD),
        ('Next', POINTER(IP_ADAPTER_ADDRESSES)),
        ('AdapterName', PCHAR),
        ('FirstUnicastAddress', POINTER(IP_ADAPTER_UNICAST_ADDRESS)),
        ('FirstAnycastAddress', POINTER(NULL)),
        ('FirstMulticastAddress', POINTER(NULL)),
        ('FirstDnsServerAddress', POINTER(NULL)),
        ('DnsSuffix', PWCHAR),
        ('Description', PWCHAR),
        ('FriendlyName', PWCHAR)
    ]


    def get_adapter_ips():
        addressbuffersize = ULONG(15 * 1024)
        addressbuffer = (
            ctypes.create_string_buffer(addressbuffersize.value)
        )

        retval = iphlpapi.GetAdaptersAddresses(
            ULONG(AF_UNSPEC),
            ULONG(0),
            None,
            ctypes.byref(addressbuffer),
            ctypes.byref(addressbuffersize)
        )

        while retval == ERROR_BUFFER_OVERFLOW:
            addressbuffer = (
                ctypes.create_string_buffer(addressbuffersize.value)
            )

            retval = iphlpapi.GetAdaptersAddresses(
                ULONG(AF_UNSPEC),
                ULONG(0),
                None,
                ctypes.byref(addressbuffer),
                ctypes.byref(addressbuffersize)
            )

        if retval != NO_ERROR:
            raise ctypes.WinError()

        # Iterate through adapters fill array
        address_info = IP_ADAPTER_ADDRESSES.from_buffer(addressbuffer)

        while True:
            if address_info.FirstUnicastAddress:
                address = address_info.FirstUnicastAddress[0]
                while True:
                    ip = sockaddr_to_ip(address.Address.lpSockaddr)
                    if ip and ip != '127.0.0.1':
                        logger.debug('adapter ip: ' + ip)
                        yield ip

                    if not address.Next:
                        break

                    address = address.Next[0]

            if not address_info.Next:
                break

            address_info = address_info.Next[0]
else:
    import os
    import ctypes.util

    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

    # noinspection PyTypeChecker,PyPep8Naming
    class ifaddrs(ctypes.Structure):
        pass


    ifaddrs._fields_ = [
        ('ifa_next', POINTER(ifaddrs)),
        ('ifa_name', PCHAR),
        ('ifa_flags', UINT),
        ('ifa_addr', POINTER(sockaddr)),
        ('ifa_netmask', POINTER(sockaddr))
    ]


    def get_adapter_ips():
        addr0 = addr = POINTER(ifaddrs)()
        retval = libc.getifaddrs(ctypes.byref(addr))

        if retval != 0:
            eno = ctypes.get_errno()
            raise OSError(eno, os.strerror(eno))

        while addr:
            ip = sockaddr_to_ip(addr[0].ifa_addr)

            if ip:
                if (
                    addr[0].ifa_netmask and not
                    addr[0].ifa_netmask[0].sa_familiy
                ):
                    addr[0].ifa_netmask[0].sa_familiy = (
                        addr[0].ifa_addr[0].sa_familiy
                    )

                logging.debug('adapter ip: ' + ip)
                yield ip

            addr = addr[0].ifa_next

        libc.freeifaddrs(addr0)


if __name__ == '__main__':
    from logging import NullHandler
    logger.addHandler(NullHandler())
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    for _ip in get_adapter_ips():
        print(_ip)
