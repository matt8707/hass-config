# -*- coding: utf-8 -*-
from __future__ import print_function
import ctypes
import socket
import struct
import sys
import platform
import logging


try:
    # noinspection PyUnboundLocalVariable,PyUnresolvedReferences
    ModuleNotFoundError = ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    from .upnp.UPNP_Device import adapter_addresses
except (ValueError, ModuleNotFoundError):
    import os

    if not __file__:
        cwd = os.getcwd()
    else:
        cwd = os.path.dirname(__file__)

    sys.path.insert(0, os.path.join(cwd, 'upnp', 'UPNP_Device'))

    # noinspection PyUnresolvedReferences
    import adapter_addresses


logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2

NULL = None
PVOID = ctypes.c_void_p
UBYTE = ctypes.c_ubyte
POINTER = ctypes.POINTER


if platform.system() == 'Darwin':
    OSX = True
    LINUX = False
    WINDOWS = False
elif platform.system() == 'Windows':
    OSX = False
    LINUX = False
    WINDOWS = True
else:
    OSX = False
    LINUX = True
    WINDOWS = False


def get_mac_address(ip):
    """
    Gets the MAC address of the TV.

    This function will use the ARP lookup tables to see if there is an entry
    for the IP address that was supplied. If no entry is found an APR request
    is sent in an attempt to populate the TV to the ARP table.

    :param ip: IP address of the TV
    :type ip: `str`
    :return: `None` or MAC address of TV formatted ``"00:00:00:00:00"``
    :rtype: `None`, `str`
    """

    if WINDOWS:
        from ctypes.wintypes import DWORD, ULONG
        wsock32 = ctypes.windll.wsock32

        # noinspection PyPep8Naming
        IPAddr = ULONG
        # noinspection PyPep8Naming
        PULONG = POINTER(ULONG)
        # noinspection PyPep8Naming
        INADDR_ANY = 0x00000000

        # noinspection PyPep8Naming
        SendARP = ctypes.windll.Iphlpapi.SendARP
        SendARP.argtype = [IPAddr, IPAddr, PVOID, PULONG]
        SendARP.restype = DWORD

        if not PY2:
            ip = ip.encode()

        # noinspection PyPep8,PyBroadException
        try:
            dst_addr = wsock32.inet_addr(ip)
            if dst_addr in (0, -1):
                raise ValueError
        except:
            dst_ip = socket.gethostbyname(ip)
            dst_addr = wsock32.inet_addr(dst_ip)

        src_addr = ULONG(INADDR_ANY)
        # noinspection PyCallingNonCallable,PyTypeChecker
        buf = (UBYTE * 6)()

        add_len = ULONG(ctypes.sizeof(buf))

        res = SendARP(
            dst_addr,
            src_addr,
            ctypes.byref(buf),
            ctypes.byref(add_len)
        )

        if res != 0:
            return None

        mac_addr = ''
        for int_val in struct.unpack('BBBBBB', buf):
            if int_val > 15:
                replace_str = '0x'
            else:
                replace_str = 'x'
            mac_addr = ''.join(
                [mac_addr, hex(int_val).replace(replace_str, '')]
            )
        mac = ':'.join(
            mac_addr[i:i + 2] for i in range(0, len(mac_addr), 2)
        ).upper()

    else:
        if not PY2 and isinstance(ip, bytes):
            ip = ip.decode('utf-8')

        import os
        import re
        import shlex
        from subprocess import check_output

        mac_re_colon = r'([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})'

        def _popen(command, args):
            path = os.environ.get('PATH', os.defpath).split(os.pathsep)
            path.extend(('/sbin', '/usr/sbin'))

            for directory in path:
                executable = os.path.join(directory, command)
                if (
                    os.path.exists(executable) and
                    os.access(executable, os.F_OK | os.X_OK) and
                    not os.path.isdir(executable)
                ):
                    break
            else:
                executable = command

            return _call_proc(executable, args)

        def _call_proc(executable, args):
            cmd = [executable] + shlex.split(args)
            env = dict(os.environ)
            env['LC_ALL'] = 'C'  # Set system locale to use 'C' this will
            # provide ascii output

            if PY2:
                devnull = open(os.devnull, 'wb')
            else:
                import subprocess

                # noinspection PyUnresolvedReferences
                devnull = subprocess.DEVNULL

            output = check_output(cmd, stderr=devnull, env=env)

            if PY2:
                return str(output)
            elif isinstance(output, bytes):
                # noinspection PyArgumentList
                return str(output, 'utf-8')

        def _uuid_ip():
            # noinspection PyUnresolvedReferences,PyProtectedMember
            from uuid import _arp_getnode

            _gethostbyname = socket.gethostbyname
            try:
                socket.gethostbyname = lambda x: ip
                mac1 = _arp_getnode()
                if mac1 is not None:
                    mac1 = ':'.join(
                        ('%012X' % mac1)[i:i + 2] for i in range(0, 12, 2)
                    )
                    mac2 = _arp_getnode()
                    mac2 = ':'.join(
                        ('%012X' % mac2)[i:i + 2] for i in range(0, 12, 2)
                    )
                    if mac1 == mac2:
                        return mac1
            finally:
                socket.gethostbyname = _gethostbyname

        def _read_arp_file():
            data = _read_file('/proc/net/arp')
            if data is not None and len(data) > 1:
                match = re.search(re.escape(ip) + r' .+' + mac_re_colon, data)
                if match:
                    return match.groups()[0]

        def _read_file(file_path):
            try:
                with open(file_path) as f:
                    return f.read()
            except OSError:
                return None

        def _neighbor_show():
            res = _popen(
                'ip',
                'neighbor show %s' % ip
            )
            res = res.partition(ip)[2].partition('lladdr')[2]
            return res.strip().split()[0]

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'', (ip, 55555))
        except socket.error:
            return None

        def _arpreq():
            return __import__('arpreq').arpreq(ip)

        esc = r'\(' + re.escape(ip) + r'\)\s+at\s+'

        def _search(pattern, command, arg):
            def wrapper():
                match = re.search(esc + pattern, _popen(command, arg))
                if match:
                    return match.groups()[0]

            return wrapper

        methods = [
            _read_arp_file,
            _neighbor_show,
            # -a BSD-style format -n shows numerical addresses
            _search(mac_re_colon, 'arp', ip),
            _search(mac_re_colon, 'arp', '-an'),
            _search(mac_re_colon, 'arp', '-an %s' % ip)
        ]
        if OSX:
            # Darwin (OSX) oddness
            mac_re_darwin = r'([0-9a-fA-F]{1,2}(?::[0-9a-fA-F]{1,2}){5})'

            methods += [
                _search(mac_re_darwin, 'arp', ip),
                _search(mac_re_darwin, 'arp', '-a'),
                _search(mac_re_darwin, 'arp', '-a %s' % ip)
            ]

        methods += [
            _uuid_ip,
            _arpreq,
        ]

        for m in methods:
            # noinspection PyPep8,PyBroadException
            try:
                mac = m()
                if mac:
                    break
            except:
                continue
        else:
            return

        mac = str(mac)
        if not PY2:
            mac = mac.replace("b'", '').replace("'", '')
            mac = mac.replace('\\n', '').replace('\\r', '')

        mac = mac.strip().lower().replace(' ', '').replace('-', ':')

        # Fix cases where there are no colons
        if ':' not in mac and len(mac) == 12:
            mac = ':'.join(mac[i:i + 2] for i in range(0, len(mac), 2))

        # Darwin's ARP output pad single-character octets with a leading zero
        elif len(mac) < 17:
            parts = mac.split(':')
            new_mac = []
            for part in parts:
                if len(part) == 1:
                    new_mac.append('0' + part)
                else:
                    new_mac.append(part)
            mac = ':'.join(new_mac)

        # MAC address should ALWAYS be 17 characters before being returned
        if len(mac) != 17:
            mac = None

    return mac


def send_wol(mac_address):
    """
    Send the WOL "magic" packet to power a TV on.


    :param mac_address: MAC address of the TV
    :type mac_address: `str`
    :return: `None`
    :rtype: `None`
    """
    split_mac = mac_address.split(':')
    hex_mac = list(int(h, 16) for h in split_mac)
    hex_mac = struct.pack('BBBBBB', *hex_mac)

    # create the magic packet from MAC address
    packet = b'\xff' * 6 + (hex_mac * 16)

    for ip in adapter_addresses.get_adapter_ips():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.debug('WOL: ' + repr(packet))
        try:
            sock.bind((ip, 0))
            for _ in range(5):
                sock.sendto(packet, ('255.255.255.255', 9))
                sock.sendto(packet, ('255.255.255.255', 7))
                sock.sendto(packet, ('255.255.255.255', 0))
        except socket.error:
            pass

        sock.close()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    try:
        # noinspection PyCompatibility
        entered_ip = raw_input('Enter IP address:')
    except NameError:
        entered_ip = input('Enter IP address:')

    returned_mac = get_mac_address(entered_ip)
    print('Found MAC:', returned_mac)

    if returned_mac is not None:
        try:
            # noinspection PyCompatibility
            answer = raw_input('Send WOL packet (Y/N)?')
        except NameError:
            answer = input('Send WOL packet (Y/N)?')

        if answer.lower() == 'y':
            send_wol(returned_mac)
