# -*- coding: utf-8 -*-

import requests
from xml.dom.minidom import Document
from lxml import etree
from .xmlns import ENVELOPE_XMLNS, strip_xmlns

import logging

logger = logging.getLogger(__name__)


class Action(object):

    def __init__(self, parent, node, state_variables, service, control_url):
        self.__parent = parent
        self.params = []
        self.ret_vals = []
        self.service = service
        self.control_url = control_url

        self.__name__ = node.find('name').text

        logger.debug(
            parent.ip_address +
            ' -- (action) ' +
            self.__name__
        )

        logger.debug(
            parent.ip_address +
            ' -- (control url) ' +
            control_url
        )

        logger.debug(
            parent.ip_address +
            ' -- (service) ' +
            service

        )

        for arguments in node:
            if arguments.tag != 'argumentList':
                continue
            for argument in arguments:
                name = argument.find('name').text
                direction = argument.find('direction').text
                variable = argument.find('relatedStateVariable').text
                variable = state_variables[variable](name, direction)

                if direction == 'in':
                    logger.debug(
                        parent.ip_address +
                        ' -- (' +
                        self.__name__ +
                        ') parameter added ' +
                        name
                    )
                    self.params += [variable]
                else:
                    logger.debug(
                        parent.ip_address +
                        ' -- (' +
                        self.__name__ +
                        ') return value added ' +
                        name
                    )

                    self.ret_vals += [variable]

                logger.debug(
                    name + ': data type - ' + str(variable.py_data_type)
                )

    def __call__(self, *args, **kwargs):

        total_params = len(list(kwargs.keys())) + len(args)

        if len(self.params) < total_params:
            raise RuntimeError(
                'To many parameters specified for UPNP funcion {0}.\n'
                'Allowed parameters are {1}'.format(
                    self.__name__,
                    ', '.join(param.__name__ for param in self.params)
                )
            )

        for i, arg in enumerate(args):
            try:
                kwargs[self.params[i].__name__] = arg
            except IndexError:
                for param in self.params:
                    print(param.__name__)
                raise

        doc = Document()

        envelope = doc.createElementNS('', 's:Envelope')
        envelope.setAttribute(
            'xmlns:s',
            ENVELOPE_XMLNS
        )
        envelope.setAttribute(
            's:encodingStyle',
            'http://schemas.xmlsoap.org/soap/encoding/'
        )

        body = doc.createElementNS('', 's:Body')

        fn = doc.createElementNS('', self.__name__)
        fn.setAttribute('xmlns:u', self.service)

        for param in self.params:
            if param.__name__ not in kwargs:
                value = param(None)
            else:
                value = param(kwargs[param.__name__])

            tmp_node = doc.createElement(param.__name__)
            tmp_text_node = doc.createTextNode(str(value))
            tmp_node.appendChild(tmp_text_node)
            fn.appendChild(tmp_node)

        body.appendChild(fn)
        envelope.appendChild(body)
        doc.appendChild(envelope)
        pure_xml = doc.toxml()

        header = {
            'SOAPAction':   '"{service}#{method}"'.format(
                service=self.service,
                method=self.__name__
            ),
            'Content-Type': 'text/xml'
        }

        logger.debug(
            self.__parent.ip_address +
            ' <-- (' +
            self.control_url +
            ') header: ' +
            str(header) +
            ' body: ' +
            pure_xml
        )
        try:
            response = requests.post(
                self.control_url,
                data=pure_xml,
                headers=header
            )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout
        ):
            return [None] * len(self.ret_vals)

        logger.debug(
            self.__parent.ip_address +
            ' --> (' +
            self.control_url +
            ') ' +
            response.content.decode('utf-8')
        )

        try:
            envelope = etree.fromstring(response.content.decode('utf-8'))
        except etree.ParseError:
            return [None] * len(self.ret_vals)
        except ValueError:
            try:
                envelope = etree.fromstring(response.content)
            except etree.ParseError:
                return [None] * len(self.ret_vals)

        envelope = strip_xmlns(envelope)

        body = envelope.find('Body')

        return_value = []

        if body is not None:

            response = body.find(self.__name__ + 'Response')
            if response is not None:
                for ret_val in self.ret_vals:
                    value = response.find(ret_val.__name__)
                    if value is None:
                        value = ret_val(None)
                    else:
                        value = ret_val(value.text)

                    return_value += [value]

        if not return_value and self.ret_vals:
            for val in self.ret_vals:
                return_value += [val(None)]

        return return_value

    @property
    def as_dict(self):
        res = dict(
            name=self.__name__,
            params=list(param.as_dict for param in self.params),
            ret_vals=list(ret_val.as_dict for ret_val in self.ret_vals)
        )
        return res

    @property
    def access_point(self):
        return self.__parent.access_point + '.' + self.__name__

    def __str__(self, indent=''):
        if self.params:
            param_names = ', '.join(param.__name__ for param in self.params)
            params = '\n'

            for param in self.params:
                params += param.__str__(indent=indent + '    ') + '\n'

        else:
            params = 'None\n\n'
            param_names = ''

        if self.ret_vals:
            ret_val_names = (
                ', '.join(ret_val.__name__ for ret_val in self.ret_vals)
            ) + ' = '
            ret_vals = '\n'

            for val in self.ret_vals:
                ret_vals += val.__str__(indent=indent + '    ') + '\n'

        else:
            ret_vals = 'None\n\n'
            ret_val_names = ''

        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            access_point=self.access_point,
            params=params,
            ret_vals=ret_vals,
            param_names=param_names,
            ret_val_names=ret_val_names
        )

        return output


TEMPLATE = '''{indent}Method name: {name}
{indent}Access point: {access_point}
{indent}Call: {ret_val_names}{access_point}({param_names})
{indent}----------------------------------------------
{indent}    Parameters: {params}{indent}    Return Values: {ret_vals}'''
