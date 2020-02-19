# -*- coding: utf-8 -*-

import socket
import logging
from errno import ENOPROTOOPT
import time
import threading
from .upnp_class import UPNPObject

SSDP_PORT = 1900
SSDP_ADDR = '239.255.255.250'


def listen(timeout, log_level=None):
    logger = logging.getLogger('UPNP_Devices')
    logger.setLevel(logging.NOTSET)
    if log_level is not None:
        logger.setLevel(log_level)

    threads = []
    event = threading.Event()
    found = []
    found_event = threading.Event()

    def do(lcl_address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except socket.error as err:
                # RHEL6 defines SO_REUSEPORT but it doesn't work
                if err.errno == ENOPROTOOPT:
                    pass
                else:
                    raise err

        addr = socket.inet_aton(SSDP_ADDR)
        interface = socket.inet_aton(lcl_address)
        cmd = socket.IP_ADD_MEMBERSHIP
        sock.setsockopt(socket.IPPROTO_IP, cmd, addr + interface)
        sock.bind((lcl_address, SSDP_PORT))
        sock.settimeout(1)

        logger.debug('SSDP bound on address ' + lcl_address)

        start = time.time()

        while time.time() - start < timeout:
            try:
                data, addr = sock.recvfrom(1024)
                if data:
                    host, port = addr
                    logger.debug('SSDP data: %s --> %s', host, data)

                    try:
                        header, payload = data.decode().split('\r\n\r\n')[:2]
                    except ValueError as err:
                        logger.error(err)
                        continue

                    lines = header.split('\r\n')
                    cmd = lines[0].split(' ')
                    lines = map(lambda x: x.replace(': ', ':', 1), lines[1:])
                    lines = filter(lambda x: len(x) > 0, lines)

                    headers = [x.split(':', 1) for x in lines]
                    headers = dict(map(lambda x: (x[0].lower(), x[1]), headers))

                    logger.debug('SSDP command %s %s - from %s:%d', cmd[0], cmd[1], host, port)
                    logger.debug('with headers: %s.', headers)

                    if cmd[0] == 'M-SEARCH' and cmd[1] == '*':
                        logger.debug('M-SEARCH *')
                    elif cmd[0] == 'NOTIFY' and cmd[1] == '*':

                        addr = addr[0]

                        start = data.lower().find(b'nt:')

                        if start > -1:
                            start += 3
                            nt = data[start:]
                            nt = nt[:nt.find(b'\n')].strip()
                        else:
                            continue

                        logger.debug('SSDP: %s found nt: %s', addr, nt)

                        if nt != b'upnp:rootdevice':
                            continue

                        start = data.lower().find(b'st:')

                        if start > -1:
                            start += 3
                            st = data[start:]
                            st = st[:st.find(b'\n')].strip()
                        else:
                            continue

                        start = data.lower().find(b'location:')

                        if start > -1:
                            start += 9
                            location = data[start:]
                            location = location[:location.find(b'\n')].strip()
                        else:
                            continue


                        logger.debug('SSDP: %s found st: %s', addr, st)
                        logger.debug('SSDP: %s found location: %s', addr, location)
                        found.append(UPNPObject(addr, {st: location}))
                        found_event.set()

                    else:
                        logger.debug('Unknown SSDP command %s %s', cmd[0], cmd[1])

            except socket.timeout:
                continue
        try:
            sock.close()
        except socket.error:
            pass

        found_event.set()

        threads.remove(threading.current_thread())
        if not threads:
            event.set()
            found_event.set()

    for local_address in get_local_addresses():
        t = threading.Thread(target=do, args=(local_address,))
        t.daemon = True
        threads += [t]
        t.start()

    while not event.isSet():
        found_event.wait()
        found_event.clear()
        while found:
            yield found.pop(0)
