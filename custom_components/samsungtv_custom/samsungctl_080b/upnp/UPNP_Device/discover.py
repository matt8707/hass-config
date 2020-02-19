# -*- coding: utf-8 -*-

from __future__ import print_function
import socket
import threading
import sys
import os
import logging
import json

from . import adapter_addresses

logger = logging.getLogger(__name__)

if sys.platform.startswith('win'):
    IPPROTO_IPV6 = 41
else:
    IPPROTO_IPV6 = getattr(socket, 'IPPROTO_IPV6')

IPV4_MCAST_GRP = "239.255.255.250"
IPV6_MCAST_GRP = "[ff02::c]"

IPV4_SSDP = '''\
M-SEARCH * HTTP/1.1\r
ST: {0}\r
MAN: "ssdp:discover"\r
HOST: 239.255.255.250:1900\r
MX: 1\r
Content-Length: 0\r
\r
'''

IPV6_SSDP = '''\
M-SEARCH * HTTP/1.1\r
ST: {0}\r
MAN: "ssdp:discover"\r
HOST: [ff02::c]:1900\r
MX: 1\r
Content-Length: 0\r
\r
'''


def discover(
    timeout=5,
    log_level=None,
    search_ips=(),
    dump='',
    services=('upnp:rootdevice',)
):
    adapter_ips = list(adapter_addresses.get_adapter_ips())

    if dump and not os.path.exists(dump):
        os.makedirs(dump)

    if log_level is not None:
        logging.basicConfig(format="%(message)s", level=log_level)
        if log_level is not None:
            logger.setLevel(log_level)

    found = {}
    found_event = threading.Event()
    threads = []

    def convert_ssdp_response(packet, addr):
        packet_type, packet = packet.decode('utf-8').split('\n', 1)
        if '200 OK' in packet_type:
            packet_type = 'response'
        elif 'MSEARCH' in packet_type:
            packet_type = 'search'
        elif 'NOTIFY' in packet_type:
            packet_type = 'notify'
        else:
            packet_type = 'unknown'

        packet = dict(
            (
                line.split(':', 1)[0].strip().upper(),
                line.split(':', 1)[1].strip()
            ) for line in packet.split('\n') if line.strip()
        )

        packet['TYPE'] = packet_type

        if dump:
            with open(os.path.join(dump, 'SSDP.log'), 'a') as f:
                f.write(json.dumps(packet, indent=4) + '\n')

        logger.debug('SSDP: inbound packet for IP ' + addr)
        logger.debug(json.dumps(packet, indent=4))

        return packet

    def send_to(destination, t_out=5):
        # try:
        #     network = ipaddress.ip_network(destination.decode('utf-8'))
        # except:
        #     network = ipaddress.ip_network(destination)
        # if isinstance(network, ipaddress.IPv6Network):
        #     mcast = IPV6_MCAST_GRP
        #     ssdp_packet = IPV6_SSDP
        #     sock = socket.socket(
        #         family=socket.AF_INET6,
        #         type=socket.SOCK_DGRAM,
        #         proto=socket.IPPROTO_IP
        #     )
        #     sock.setsockopt(IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)
        #
        # else:
        mcast = IPV4_MCAST_GRP
        ssdp_packet = IPV4_SSDP
        sock = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP
        )
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if destination in adapter_ips:
            try:
                sock.bind((destination, 0))
            except socket.error:
                sock.close()
                raise

            destination = mcast

        sock.settimeout(t_out)

        for service in services:
            packet = ssdp_packet.format(service)
            logger.debug(
                'SSDP: %s\n%s',
                destination,
                packet
            )

            sock.sendto(packet.encode('utf-8'), (destination, 1900))

        return sock

    def do(local_address, target_ips):
        # noinspection PyPep8,PyBroadException
        try:
            sock = send_to(local_address)
        except:
            threads.remove(threading.current_thread())

            if not threads:
                found_event.set()

            return

        for target_ip in target_ips:
            found[target_ip] = set()
            trd = threading.Thread(target=found_thread, args=(target_ip,))
            trd.daemon = True
            threads.append(trd)
            trd.start()
        try:
            while True:
                data, addr = sock.recvfrom(1024)

                if target_ips and addr[0] not in target_ips:
                    continue

                packet = convert_ssdp_response(data, addr[0])

                if packet['TYPE'] != 'response' or 'LOCATION' not in packet:
                    continue

                if addr[0] not in found:
                    found[addr[0]] = set()
                    trd = threading.Thread(
                        target=found_thread,
                        args=(addr[0],)
                    )
                    trd.daemon = True
                    threads.append(trd)
                    trd.start()

                found[addr[0]].add((packet['ST'], packet['LOCATION']))

        except socket.timeout:
            pass

        except socket.error:
            import traceback

            logger.debug(traceback.format_exc())

        try:
            sock.close()
        except socket.error:
            pass

        threads.remove(threading.current_thread())

        if not threads:
            found_event.set()

    def found_thread(ip_addr):
        try:
            sock = send_to(ip_addr, timeout)
        except OSError:
            threads.remove(threading.current_thread())

            if not threads:
                found_event.set()
            return

        try:
            while True:
                data, addr = sock.recvfrom(1024)
                packet = convert_ssdp_response(data, addr[0])

                if packet['TYPE'] != 'response' or 'LOCATION' not in packet:
                    continue

                if (
                    packet['LOCATION'].count('/') == 2 and
                    packet['LOCATION'].startswith('http')
                ):
                    continue

                found[addr[0]].add((packet['ST'], packet['LOCATION']))

        except socket.error:
            pass

        threads.remove(threading.current_thread())

        if not threads:
            found_event.set()

    for adapter_ip in adapter_ips:
        t = threading.Thread(
            target=do,
            args=(adapter_ip, search_ips)
        )
        t.daemon = True
        threads += [t]
        t.start()

    found_event.wait()

    for ip, locations in found.items():
        locations = list(loc for loc in locations)
        if not locations:
            continue

        yield ip, locations


if __name__ == '__main__':
    from upnp_class import UPNPObject

    from logging import NullHandler

    logger.addHandler(NullHandler())

    for device_ip, locs in discover(5, logging.DEBUG):
        print(UPNPObject(device_ip, locs))
