# -*- coding: utf-8 -*-

import requests
import os
from lxml import etree
try:
    # noinspection PyCompatibility
    from urlparse import urlparse
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import urlparse

try:
    from .xmlns import strip_xmlns
    from .service import Service
    from .embedded_device import EmbeddedDevice
    from .instance_singleton import InstanceSingleton
except ImportError:
    from xmlns import strip_xmlns
    from service import Service
    from embedded_device import EmbeddedDevice
    from instance_singleton import InstanceSingleton

import logging

logger = logging.getLogger(__name__)


class UPNPObject(object):

    def __init__(self, ip, locations, dump='', load_on_startup=True):
        self.ip_address = ip
        self._devices = {}
        self._services = {}
        self.__name__ = self.__class__.__name__
        if load_on_startup:
            self.build(ip, locations, dump)

    def build(self, ip_address, locations, dump=''):
        self._devices.clear()
        self._services.clear()
        self.ip_address = ip_address

        for location in locations:
            parsed = urlparse(location)
            url = '{0}://{1}:{2}/'.format(
                parsed.scheme,
                parsed.hostname,
                parsed.port
            )

            logger.debug(
                self.ip_address +
                ' <-- (' +
                location +
                ') ""'
            )
            response = requests.get(location)

            logger.debug(
                self.ip_address +
                ' --> (' +
                location +
                ') ' +
                response.content.decode('utf-8')
            )

            path = parsed.path
            if path.startswith('/'):
                path = path[1:]

            if '/' in path:
                path, file_name = path.rsplit('/', 1)
            else:
                file_name = path
                path = ''

            if not file_name.endswith('.xml'):
                file_name += '.xml'

            if dump:
                content = response.content.decode('utf-8')
                if path:
                    output = os.path.join(dump, path)

                    if not os.path.exists(output):
                        os.makedirs(output)
                else:
                    output = dump

                indent_count = 0

                for line in content.split('\n'):
                    for char in list(line):
                        if not line:
                            continue

                        if char != ' ' and not indent_count:
                            break
                        if char == ' ':
                            indent_count += 1
                        else:
                            if indent_count != 2:
                                indent_count = 0
                            break
                    if indent_count:
                        break

                with open(os.path.join(output, file_name), 'w') as f:
                    for line in content.split('\n'):
                        if not line.strip():
                            continue
                        line = line.replace('\t', '    ')
                        if indent_count:
                            count = 0
                            for char in list(line):
                                if char != ' ':
                                    break
                                count += 1
                            line = '    ' * (count / 2) + line.strip()
                        f.write(line + '\n')

            try:
                root = etree.fromstring(response.content.decode('utf-8'))
            except etree.XMLSyntaxError:
                return
            except ValueError:
                try:
                    root = etree.fromstring(response.content)
                except etree.XMLSyntaxError:
                    return

            root = strip_xmlns(root)
            node = root.find('device')
            if node is None:
                services = []
                devices = []

            else:
                services = node.find('serviceList')

                if services is None:
                    services = []

                devices = node.find('deviceList')
                if devices is None:
                    devices = []

            for service in services:
                scpdurl = service.find('SCPDURL').text.replace(url, '')

                if '/' not in scpdurl and path and path not in scpdurl:
                    scpdurl = path + '/' + scpdurl

                control_url = service.find('controlURL').text
                if control_url is None:
                    if scpdurl.endswith('.xml'):
                        control_url = scpdurl.rsplit('/', 1)[0]
                        if control_url == scpdurl:
                            control_url = ''
                    else:
                        control_url = scpdurl
                else:
                    control_url = control_url.replace(url, '')

                if control_url.startswith('/'):
                    control_url = control_url[1:]

                if scpdurl.startswith('/'):
                    scpdurl = scpdurl[1:]

                service_id = service.find('serviceId').text
                service_type = service.find('serviceType').text

                service = Service(
                    self,
                    url,
                    scpdurl,
                    service_type,
                    control_url,
                    node,
                    dump=dump
                )
                name = service_id.split(':')[-1]
                service.__name__ = name
                self._services[name] = service

            for device in devices:
                device = EmbeddedDevice(
                    url,
                    node=device,
                    parent=self,
                    dump=dump
                )
                self._devices[device.__name__] = device

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self._devices:
            return self._devices[item]

        if item in self._services:
            return self._services[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    @property
    def as_dict(self):
        res = dict(
            services=list(service.as_dict for service in self.services),
            devices=list(device.as_dict for device in self.devices)
        )
        return res

    @property
    def access_point(self):
        return self.__class__.__name__

    @property
    def services(self):
        return list(self._services.values())[:]

    @property
    def devices(self):
        return list(self._devices.values())[:]

    def __str__(self):
        output = '\n\n' + str(self.__name__) + '\n'
        output += 'IP Address: ' + self.ip_address + '\n'
        output += '==============================================\n'

        if self.services:
            output += 'Services:\n'
            for cls in self.services:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Services: None\n'

        if self.devices:
            output += 'Devices:\n'
            for cls in self.devices:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Devices: None\n'

        return output
