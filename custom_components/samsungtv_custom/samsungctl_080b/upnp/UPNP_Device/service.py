# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
import os
from lxml import etree
from .data_type import StateVariable
from .action import Action
from .icon import Icon
from .xmlns import strip_xmlns

try:
    # noinspection PyCompatibility
    from urlparse import urlparse
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import urlparse

import logging

logger = logging.getLogger(__name__)


class Service(object):

    def __init__(
        self,
        parent,
        url,
        location,
        service,
        control_url,
        node=None,
        dump=''
    ):

        self._parent = parent
        self.state_variables = {}
        self._actions = {}
        self._node = node
        self.url = url
        self._icons = {}

        parsed = urlparse(url)
        self.ip_address = parsed.hostname

        if node is not None:
            icons = node.find('iconList')

            if icons is None:
                icons = []

            for icon in icons:
                icon = Icon(self, url, icon)
                self._icons[icon.__name__] = icon

        self.service = service

        self.__name__ = service.split(':')[-2]

        location = location.replace(url, '')
        location = location.replace('//', '/')

        if not location.startswith('/') and not url.endswith('/'):
            location = '/' + location

        logger.debug(
            self.ip_address +
            ' <-- (' +
            url + location +
            ') ""'
        )

        response = requests.get(url + location)

        logger.debug(
            self.ip_address +
            ' --> (' +
            url + location +
            ') ' +
            response.content.decode('utf-8')
        )

        if dump:
            path = location
            if path.startswith('/'):
                path = path[1:]
            if '/' in path:
                path, file_name = path.rsplit('/', 1)
                path = os.path.join(dump, path)
            else:
                file_name = path
                path = dump

            if not os.path.exists(path):
                os.makedirs(path)

            if not file_name.endswith('.xml'):
                file_name += '.xml'

            with open(os.path.join(path, file_name), 'w') as f:
                f.write(response.content.decode('utf-8'))

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
        actions = root.find('actionList')
        if actions is None:
            actions = []

        state_variables = root.find('serviceStateTable')
        if state_variables is None:
            state_variables = []

        for state_variable in state_variables:
            state_variable = StateVariable(state_variable)
            self.state_variables[state_variable.name] = state_variable

        for action in actions:
            action = Action(
                self,
                action,
                self.state_variables,
                service,
                url + control_url
            )

            self._actions[action.__name__] = action

    @property
    def methods(self):
        return list(self._actions.values())[:]

    @property
    def access_point(self):
        return self._parent.access_point + '.' + self.__name__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self._actions:
            return self._actions[item]

        if self._node is not None:
            if item in self._icons:
                return self._icons[item]

            if item in self.__class__.__dict__:
                if hasattr(self.__class__.__dict__[item], 'fget'):
                    return self.__class__.__dict__[item].fget(self)

            value = self._node.find(item)
            if value is not None:
                return value.text

        raise AttributeError(item)

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            methods=list(method.as_dict for method in self.methods),
            icons=list(icon.as_dict for icon in self.icons)
        )

        if self._node is not None:
            for node in self._node:
                if node.text.strip() and node.text != '/':
                    res[node.tag] = node.text
        return res

    def __str__(self, indent=''):
        actions = ''

        for action in self._actions.values():
            actions += action.__str__(indent + '    ')

        if not actions:
            actions += indent + '    None'

        if self._node is None:

            output = TEMPLATE.format(
                indent=indent,
                access_point=self.access_point,
                service=self.service,
                name=self.__name__,
                actions=actions
            )
            return output

        icons = ''
        for icon in self.icons:
            icons += icon.__str__(indent=indent + '    ') + '\n'

        if not icons:
            icons = indent + '    None'

        output = TEMPLATE.format(
            indent=indent,
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
            icons=icons,
            access_point=self.access_point,
            service=self.service,
            name=self.__name__,
            actions=actions.rstrip() + '\n'
        )

        return output

    def _get_xml_text(self, tag):
        value = self._node.find(tag)
        if value is not None:
            value = value.text

        return value

    @property
    def hardware_id(self):
        value = self._get_xml_text('X_hardwareId')
        if value is not None:
            value = value.replace('&amp;', '&')

        return value

    @property
    def device_category(self):
        value = self._get_xml_text('X_deviceCategory')
        return value

    @property
    def device_subcategory(self):
        value = self._get_xml_text('X_deviceCategory')
        return value

    @property
    def icons(self):
        return list(self._icons.values())[:]

    @property
    def device_type(self):
        return self._get_xml_text('deviceType')

    @property
    def presentation_url(self):
        value = self._get_xml_text('presentationURL')
        if value is not None:
            return self.url + value

    @property
    def friendly_name(self):
        return self._get_xml_text('friendlyName')

    @property
    def manufacturer(self):
        return self._get_xml_text('manufacturer')

    @property
    def manufacturer_url(self):
        return self._get_xml_text('manufacturerURL')

    @property
    def model_description(self):
        return self._get_xml_text('modelDescription')

    @property
    def model_name(self):
        return self._get_xml_text('modelName')

    @property
    def model_number(self):
        return self._get_xml_text('modelNumber')

    @property
    def model_url(self):
        return self._get_xml_text('modelURL')

    @property
    def serial_number(self):
        return self._get_xml_text('serialNumber')

    @property
    def udn(self):
        return self._get_xml_text('UDN')

    @property
    def upc(self):
        return self._get_xml_text('UPC')


TEMPLATE = '''{indent}Service name: {name}
{indent}Service class: {service}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}Methods:
{actions}
'''

TEMPLATE2 = '''{indent}Service name: {name}
{indent}Service class: {service}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}Manufacturer:         {manufacturer}
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
{indent}--------------------------------------------------------
{indent}Icons
{indent}--------------------------------------------------------
{icons}
{indent}Methods:
{actions}
'''
