# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
import atexit
import socket
import json
import threading
import logging
from lxml import etree
from .UPNP_Device.xmlns import strip_xmlns
from .UPNP_Device import adapter_addresses
from ..config import Config
from .. import wake_on_lan


logger = logging.getLogger(__name__)


IPV4_MCAST_GRP = "239.255.255.250"

IPV4_SSDP = '''\
M-SEARCH * HTTP/1.1\r
ST: {0}\r
MAN: "ssdp:discover"\r
HOST: 239.255.255.250:1900\r
MX: 1\r
Content-Length: 0\r
\r
'''

SERVICES = (
    'urn:schemas-upnp-org:device:MediaRenderer:1',
    'urn:samsung.com:device:IPControlServer:1',
    'urn:dial-multiscreen-org:device:dialreceiver:1',
    'urn:samsung.com:device:MainTVServer2:1',
    'urn:samsung.com:device:RemoteControlReceiver:1',
)

SSDP_DEBUG = False


def convert_ssdp_response(packet, _):
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

    return packet


def get_mac(host):
    try:
        res = requests.get(
            'http://{0}:8001/api/v2/'.format(host),
            timeout=3
        )
        res = res.json()['device']
        if res['networkType'] == 'wired':
            return wake_on_lan.get_mac_address(host)
        else:
            return res['wifiMac'].upper()
    except (
        ValueError,
        KeyError,
        requests.HTTPError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ConnectionError
    ):
        return wake_on_lan.get_mac_address(host)


def websocket(host):
    return 'websocket', 8001, None, get_mac(host)


def encrypted(host):
    return 'encrypted', 8080, '12345', get_mac(host)


def legacy(host):
    return (
        'legacy',
        55000,
        None,
        wake_on_lan.get_mac_address(host)
    )


CONNECTION_TYPES = {
    (
        'urn:schemas-upnp-org:device:MediaRenderer:1',
        'urn:samsung.com:device:IPControlServer:1',
        'urn:dial-multiscreen-org:device:dialreceiver:1'
    ): websocket,

    (
        'urn:samsung.com:device:RemoteControlReceiver:1',
        'urn:dial-multiscreen-org:device:dialreceiver:1',
        'urn:schemas-upnp-org:device:MediaRenderer:1'
    ): websocket,

    (
        'urn:samsung.com:device:MainTVServer2:1',
        'urn:samsung.com:device:RemoteControlReceiver:1',
        'urn:schemas-upnp-org:device:MediaRenderer:1',
        'urn:dial-multiscreen-org:device:dialreceiver:1'
    ): encrypted,

    (
        'urn:schemas-upnp-org:device:MediaRenderer:1',
        'urn:samsung.com:device:MainTVServer2:1',
        'urn:samsung.com:device:RemoteControlReceiver:1'
    ): legacy
}


class UPNPDiscoverSocket(threading.Thread):

    def __init__(self, parent, local_address):
        self._timeout = 5.0
        self._local_address = local_address
        self._parent = parent
        self._event = threading.Event()
        self._found = {}
        self._program_powered_off = {}
        self._program_powered_on = {}
        self._powering_off = {}
        self._powered_off = {}
        self._powered_on = {}
        self.sock = self._create_socket()
        threading.Thread.__init__(self)

    def _create_socket(self):
        sock = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP
        )
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((self._local_address, 0))
            return sock
        except socket.error:
            try:
                sock.close()
            except socket.error:
                pass

            return None

    def start(self):
        if self.sock is not None:
            threading.Thread.start(self)

    def is_on(self, uuid):
        if uuid in self._found:
            if uuid in self._powered_on:
                return self._powered_on[uuid]

            if uuid in self._powering_off:
                return self._powering_off[uuid]

    @property
    def powered_on(self):
        return (
            list(self._powered_on.values())[:]
        )

    @property
    def powered_off(self):
        return (
            list(
                self._found[uuid] for uuid in self._found.keys()
                if uuid not in self._powered_on.keys()
            )
        )

    @property
    def discovered(self):
        return list(self._found.values())[:]

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        if self.sock is not None:
            if SSDP_DEBUG:
                logger.debug(
                    'SSDP: %s -- new timeout %s',
                    self._local_address,
                    timeout
                )
            self.sock.settimeout(timeout)

    def run(self):

        while not self._event.isSet():
            self.sock.settimeout(self._timeout)

            for service in SERVICES:
                packet = IPV4_SSDP.format(service)
                if SSDP_DEBUG:
                    logger.debug(
                        'SSDP: %s - %s\n%s',
                        self._local_address,
                        IPV4_MCAST_GRP,
                        packet
                    )

                try:
                    self.sock.sendto(
                        packet.encode('utf-8'),
                        (IPV4_MCAST_GRP, 1900)
                    )
                except socket.error:
                    try:
                        self.sock.close()
                    except socket.error:
                        pass
                    self.sock = None
                    return

            found_packets = {}
            try:
                while not self._event.isSet():
                    data, (connected_ip, _) = self.sock.recvfrom(1024)

                    if data:
                        packet = convert_ssdp_response(data, connected_ip)

                        if (
                            packet['TYPE'] != 'response' or
                            'LOCATION' not in packet
                        ):
                            continue

                        if (
                            packet['LOCATION'].count('/') == 2 and
                            packet['LOCATION'].startswith('http')
                        ):
                            continue

                        if SSDP_DEBUG:
                            logger.debug(
                                connected_ip +
                                ' --> ' +
                                self._local_address +
                                ' (SSDP) ' +
                                json.dumps(packet, indent=4)
                            )

                        if connected_ip not in found_packets:
                            found_packets[connected_ip] = set()

                        found_packets[connected_ip].add(
                            (packet['ST'], packet['LOCATION'])
                        )

            except socket.timeout:
                try:
                    self.sock.close()
                except socket.error:
                    pass

                self.sock = self._create_socket()

                if found_packets:
                    if SSDP_DEBUG:
                        logger.debug(found_packets)
                        powered_on = []

                        for host, packet in found_packets.items():
                            if self._event.isSet():
                                return

                            upnp_locations = list(
                                location for _, location in packet
                            )

                            for service, location in packet:
                                if service == SERVICES[0]:
                                    break
                            else:
                                continue

                            if SSDP_DEBUG:
                                logger.debug(
                                    host +
                                    ' <-- (' +
                                    location +
                                    ') ""'
                                )
                            try:
                                response = requests.get(location, timeout=2)
                            except (
                                requests.ConnectionError,
                                requests.ConnectTimeout
                            ):
                                continue

                            if SSDP_DEBUG:
                                logger.debug(
                                    host +
                                    ' --> (' +
                                    location +
                                    ') ' +
                                    response.content.decode('utf-8')
                                )

                            try:
                                root = etree.fromstring(
                                    response.content.decode('utf-8'))
                            except etree.ParseError:
                                continue
                            except ValueError:
                                try:
                                    root = etree.fromstring(response.content)
                                except etree.ParseError:
                                    continue

                            root = strip_xmlns(root)
                            node = root.find('device')

                            if node is None:
                                continue

                            description = node.find('modelDescription')
                            if (
                                description is None or
                                'Samsung' not in description.text or
                                'TV' not in description.text
                            ):
                                continue

                            model = node.find('modelName')
                            if model is None:
                                continue

                            model = model.text

                            uuid = node.find('UDN')

                            if uuid is None or not uuid.text:
                                continue

                            uuid = uuid.text.split(':')[-1]

                            if uuid in self._found:
                                config = self._found[uuid]
                                config.host = host
                                config.upnp_locations = upnp_locations
                            else:
                                product_cap = node.find('ProductCap')
                                if product_cap is None:
                                    years = dict(
                                        A=2008,
                                        B=2009,
                                        C=2010,
                                        D=2011,
                                        E=2012,
                                        F=2013,
                                        H=2014,
                                        J=2015
                                    )
                                    year = years[model[4].upper()]
                                else:
                                    product_cap = product_cap.text.split(',')

                                    for item in product_cap:
                                        if (
                                            item.upper().startswith('Y') and
                                            len(item) == 5 and
                                            item[1:].isdigit()
                                        ):
                                            year = int(item[1:])
                                            break
                                    else:
                                        year = None

                                if year is None:
                                    services = list(
                                        service for service, _ in packet)

                                    conn_items = CONNECTION_TYPES.items()
                                    for found_services, method in conn_items:
                                        for found_service in found_services:
                                            if found_service not in services:
                                                break
                                        else:
                                            method, port, app_id, mac = (
                                                method(host)
                                            )
                                            break
                                    else:
                                        continue

                                elif year <= 2013:
                                    method, port, app_id, mac = legacy(host)
                                elif year <= 2015:
                                    method, port, app_id, mac = encrypted(host)
                                else:
                                    method, port, app_id, mac = websocket(host)

                                if mac is None:
                                    logger.warning(
                                        'Unable to acquire TV\'s mac address'
                                    )
                                config = Config(
                                    host=host,
                                    method=method,
                                    upnp_locations=upnp_locations,
                                    model=model,
                                    uuid=uuid,
                                    mac=mac,
                                    app_id=app_id,
                                    port=port,
                                )
                                logger.debug(
                                    'Discovered TV:' +
                                    ' UUID - ' +
                                    uuid +
                                    ' IP - ' +
                                    host
                                )

                                self._parent.callback(config, None)

                            self._found[uuid] = config
                            self._powered_on[uuid] = config

                            self._parent.callback(config, state=True)
                            powered_on += [uuid]

                        for uuid, config in list(self._found.items())[:]:
                            if uuid not in powered_on:
                                if uuid in self._powered_on:
                                    del self._powered_on[uuid]

                                self._parent.callback(
                                    config,
                                    state=False
                                )

                else:
                    self._event.wait(2.0)

                if SSDP_DEBUG:
                    logger.debug(
                        self._local_address +
                        ' -- (SSDP) loop restart'
                    )
            except socket.error:
                break

        try:
            self.sock.close()
        except socket.error:
            pass

        self.sock = None

    def stop(self):
        if self.sock is not None:
            self._event.set()
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except socket.error:
                pass

            self.join(2.0)


class Discover(object):

    def __init__(self):
        self._callbacks = []
        self._threads = []

    @property
    def logging(self):
        return SSDP_DEBUG

    @logging.setter
    def logging(self, value):
        global SSDP_DEBUG
        SSDP_DEBUG = value

    def start(self):
        if not self.is_running:
            for adapter_ip in adapter_addresses.get_adapter_ips():
                thread = UPNPDiscoverSocket(self, adapter_ip)
                self._threads += [thread]
                thread.start()

        atexit.register(self.stop)

    def is_on(self, uuid):
        for thread in self._threads:
            config = thread.is_on(uuid)
            if config is not None:
                return config

    def stop(self):
        del self._callbacks[:]

        while self._threads:
            thread = self._threads.pop(0)
            thread.stop()

        try:
            # noinspection PyUnresolvedReferences
            atexit.unregister(self.stop)
        except (NameError, AttributeError):
            pass

    def register_callback(self, callback, uuid=None):
        global SSDP_DEBUG
        self._callbacks += [(callback, uuid)]

        if not self.is_running:
            if logger.getEffectiveLevel() == logging.DEBUG:
                SSDP_DEBUG = True

            self.start()

        for thread in self._threads:
            if uuid is None:
                for config in thread.discovered:
                    callback(config)
            else:
                for config in thread.powered_on:
                    if config.uuid == uuid:
                        callback(config, True)

                for config in thread.powered_off:
                    if config.uuid == uuid:
                        callback(config, False)

    def unregister_callback(self, callback, uuid=None):
        if (callback, uuid) in self._callbacks:
            self._callbacks.remove((callback, uuid))

        if not self._callbacks:
            self.stop()

    @property
    def discovered(self):
        res = []

        for thread in self._threads:
            res += thread.discovered

        return res

    def callback(self, config, state=None):
        for callback, uuid in self._callbacks:
            if uuid is None and state is None:
                callback(config)
            elif (
                uuid is not None and
                uuid == config.uuid and
                state is not None
            ):
                callback(config, state)

    @property
    def is_running(self):
        return len(self._threads) > 0


auto_discover = Discover()


def discover(host=None, timeout=8):

    if timeout < 8:
        timeout = 8
    event = threading.Event()

    def discover_callback(config):
        configs.append(config)

    configs = []
    auto_discover.register_callback(discover_callback)
    event.wait(timeout)
    auto_discover.unregister_callback(discover_callback)

    if host:
        for config in configs:
            if config.host == host:
                return [config]
        return []

    return configs
