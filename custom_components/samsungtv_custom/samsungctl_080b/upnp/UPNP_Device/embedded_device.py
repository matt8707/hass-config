# -*- coding: utf-8 -*-
try:
    from .icon import Icon
    from .service import Service
except ImportError:
    from icon import Icon
    from service import Service

import logging

logger = logging.getLogger(__name__)


class EmbeddedDevice(object):

    def __init__(self, url, node=None, parent=None, dump=''):
        self.__parent = parent
        self.__services = {}
        self.__devices = {}
        self.__icons = {}

        icons = node.find('iconList')
        if icons is None:
            icons = []
        services = node.find('serviceList')
        if services is None:
            services = []
        devices = node.find('deviceList')
        if devices is None:
            devices = []

        self.__node = node

        for icon in icons:
            icon = Icon(self, url, icon)
            self.__icons[icon.__name__] = icon

        for service in services:
            scpdurl = service.find('SCPDURL').text.replace(url, '')
            control_url = service.find('controlURL').text.replace(url, '')
            service_id = service.find('serviceId').text
            service_type = service.find('serviceType').text

            service = Service(
                self,
                url,
                scpdurl,
                service_type,
                control_url,
                dump=dump
            )

            name = service_id.split(':')[-1]
            service.__name__ = name
            self.__services[name] = service

        for device in devices:
            device = EmbeddedDevice(
                url,
                node=device,
                parent=self,
                dump=dump
            )

            self.__devices[device.__name__] = device

        self.url = url
        self.__name__ = self.friendly_name.replace(' ', '_').replace('-', '')

    def __str__(self, indent='  '):
        icons = ''
        for icon in self.icons:
            icons += icon.__str__(indent=indent + '    ')

        services = ''
        for service in self.services:
            services += service.__str__(indent=indent + '    ')

        devices = ''
        for device in self.devices:
            devices += device.__str__(indent=indent + '    ')

        output = TEMPLATE.format(
            indent=indent,
            access_point=self.access_point,
            friendly_name=self.friendly_name,
            manufacturer=self.manufacturer,
            manufacturer_url=self.manufacturer_url,
            model_description=self.model_description,
            model_name=self.model_name,
            model_number=self.model_number,
            model_url=self.model_url,
            serial_number=self.serial_number,
            presentation_url=self.presentation_url,
            device_type=self.device_type,
            hardware_id=self.hardware_id,
            device_category=self.device_category,
            device_subcategory=self.device_subcategory,
            udn=self.udn,
            upc=self.upc,
        )

        if icons:
            output += indent + 'Icons:\n' + icons
        else:
            output += indent + 'Icons: None\n'

        if services:
            output += indent + 'Services:\n' + services
        else:
            output += indent + 'Services: None\n'

        if devices:
            output += indent + 'Devices:\n' + devices
        else:
            output += indent + 'Devices: None\n'

        return output

    @property
    def access_point(self):
        if self.__parent is not None:
            return self.__parent.access_point + '.' + self.__name__
        else:
            return self.__name__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if self.__node is not None:
            if item in self.__services:
                return self.__services[item]
            if item in self.__devices:
                return self.__devices[item]
            if item in self.__icons:
                return self.__icons[item]

            node = self.__node.find(item)
            if node is not None:
                return node.text

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            icons=list(icon.as_dict for icon in self.icons),
            services=list(service.as_dict for service in self.services),
            devices=list(device.as_dict for device in self.devices)
        )

        if self.__node is not None:
            for node in self.__node:
                if node.text.strip() and node.text != '/':
                    res[node.tag] = node.text
        return res

    def __get_xml_text(self, tag):
        value = self.__node.find(tag)
        if value is not None:
            value = value.text

        return value

    @property
    def hardware_id(self):
        value = self.__get_xml_text('X_hardwareId')
        if value is not None:
            value = value.text.replace('&amp;', '&')

        return value

    @property
    def device_category(self):
        value = self.__get_xml_text('X_deviceCategory')
        if value is not None:
            value = value.text

        return value

    @property
    def device_subcategory(self):
        value = self.__get_xml_text('X_deviceCategory')
        if value is not None:
            value = value.text

        return value

    @property
    def icons(self):
        return list(self.__icons.values())[:]

    @property
    def devices(self):
        return list(self.__devices.values())[:]

    @property
    def services(self):
        return list(self.__services.values())[:]

    @property
    def device_type(self):
        return self.__get_xml_text('deviceType')

    @property
    def presentation_url(self):
        value = self.__get_xml_text('presentationURL')
        if value is not None:
            return self.url + value

    @property
    def friendly_name(self):
        return self.__get_xml_text('friendlyName')

    @property
    def manufacturer(self):
        return self.__get_xml_text('manufacturer')

    @property
    def manufacturer_url(self):
        return self.__get_xml_text('manufacturerURL')

    @property
    def model_description(self):
        return self.__get_xml_text('modelDescription')

    @property
    def model_name(self):
        return self.__get_xml_text('modelName')

    @property
    def model_number(self):
        return self.__get_xml_text('modelNumber')

    @property
    def model_url(self):
        return self.__get_xml_text('modelURL')

    @property
    def serial_number(self):
        return self.__get_xml_text('serialNumber')

    @property
    def udn(self):
        return self.__get_xml_text('UDN')

    @property
    def upc(self):
        return self.__get_xml_text('UPC')


TEMPLATE = '''
{indent}{friendly_name}
{indent}{manufacturer}
{indent}Access point: {access_point}
{indent}========================================================
{indent}Manufacturer URL:     {manufacturer_url}
{indent}Model Description:    {model_description}
{indent}Model Name:           {model_name}
{indent}Model Number:         {model_number}
{indent}Model URL:            {model_url}
{indent}Serial Number:        {serial_number}
{indent}Device Type:          {device_type}
{indent}Hardware ID:          {hardware_id}
{indent}Device Category:      {device_category}
{indent}Device Subcategory:   {device_subcategory}
{indent}Presentation URL:     {presentation_url}
{indent}UDN:                  {udn}
{indent}UPC:                  {upc}
'''
