"""
SamsungTVWS - Samsung Smart TV WS API wrapper

Copyright (C) 2019 Xchwarze

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA  02110-1335  USA

"""
import base64
import json
import logging
import time
import ssl
import websocket
from . import shortcuts
import xml.etree.ElementTree as ET
import requests

class SamsungTVWS:
    _URL_FORMAT = 'ws://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}'
    _SSL_URL_FORMAT = 'wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}&token={token}'

    def __init__(self, host, token=None, token_file=None, port=8001, timeout=None, key_press_delay=1, name='SamsungTvRemote', app_list=None):
        self.host = host
        self._app_list = app_list
        self.token = token
        self.token_file = token_file
        self.port = port
        self.timeout = None if timeout == 0 else timeout
        self.key_press_delay = key_press_delay
        self.name = name
        self.connection = None
        self.mute = False
        self.volume = 0

    def __exit__(self, type, value, traceback):
        self.close()

    def _serialize_string(self, string):
        if isinstance(string, str):
            string = str.encode(string)

        return base64.b64encode(string).decode('utf-8')

    def _is_ssl_connection(self):
        return self.port == 8002

    def _format_websocket_url(self, is_ssl=False):
        params = {
            'host': self.host,
            'port': self.port,
            'name': self._serialize_string(self.name),
            'token': self._get_token(),
        }

        if is_ssl:
            return self._SSL_URL_FORMAT.format(**params)
        else:
            return self._URL_FORMAT.format(**params)

    def _get_token(self):
        if self.token_file is not None:
            try :
                with open(self.token_file, 'r') as token_file:
                    return token_file.readline()
            except:
                return ''
        else:
            return self.token

    def _set_token(self, token):
        if self.token_file is not None:
            with open(self.token_file, 'w') as token_file:
                token_file.write(token)
        else:
            logging.info('New token %s', token)

    def _ws_send(self, payload):
        if self.connection is None:
            self.open()

        self.connection.send(payload)
        time.sleep(self.key_press_delay)

    def open(self):
        is_ssl = self._is_ssl_connection()
        url = self._format_websocket_url(is_ssl)
        sslopt = {'cert_reqs': ssl.CERT_NONE} if is_ssl else {}

        logging.debug('WS url %s', url)

        self.connection = websocket.create_connection(
            url,
            self.timeout,
            sslopt=sslopt
        )

        response = json.loads(self.connection.recv())

        if response.get('data') and response.get('data').get('token'):
            token = response.get('data').get('token')
            self._set_token(token)

        if response['event'] != 'ms.channel.connect':
            self.close()
            raise Exception(response)

    def close(self):
        if self.connection:
            self.connection.close()

        self.connection = None
        logging.debug('Connection closed.')

    def send_key(self, key):
        payload = json.dumps({
            'method': 'ms.remote.control',
            'params': {
                'Cmd': 'Click',
                'DataOfCmd': key,
                'Option': 'false',
                'TypeOfRemote': 'SendRemoteKey'
            }
        })

        logging.info('Sending key %s', key)
        self._ws_send(payload)

    def run_app(self, app_id, app_type='DEEP_LINK', meta_tag=''):
        payload = json.dumps({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.apps.launch',
                'to': 'host',
                'data': {
                    # action_type: NATIVE_LAUNCH / DEEP_LINK
                    # app_type == 2 ? 'DEEP_LINK' : 'NATIVE_LAUNCH',
                    'action_type': app_type,
                    'appId': app_id,
                    'metaTag': meta_tag
                }
            }
        })

        logging.info('Sending run app app_id: %s app_type: %s meta_tag: %s', app_id, app_type, meta_tag)
        self._ws_send(payload)

    def open_browser(self, url):
        logging.info('Opening url in browser %s', url)
        self.run_app(
            'org.tizen.browser',
            'NATIVE_LAUNCH',
            url
        )

    def app_list(self):
        payload = json.dumps({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.installedApp.get',
                'to': 'host'
            }
        })

        logging.info('Get app list')
        self._ws_send(payload)
        response = json.loads(self.connection.recv())
        if response.get('data') and response.get('data').get('data'):
            return response.get('data').get('data')
        else:
            return response

    def shortcuts(self):
        return shortcuts.SamsungTVShortcuts(self)

    def SOAPrequest(self, action, arguments, protocole):
        headers = {'SOAPAction': '"urn:schemas-upnp-org:service:{protocole}:1#{action}"'.format(action=action, protocole=protocole), 'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="utf-8"?>
                <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:{action} xmlns:u="urn:schemas-upnp-org:service:{protocole}:1">
                        <InstanceID>0</InstanceID>
                        {arguments}
                    </u:{action}>
                    </s:Body>
                </s:Envelope>""".format(action=action, arguments=arguments, protocole=protocole)
        response = None
        try:
            response = requests.post("http://{host}:9197/upnp/control/{protocole}1".format(host=self.host, protocole=protocole), data=body, headers=headers, timeout=0.1)
            response = response.content
        except:
            pass
        return response

    def get_volume(self):
        response = self.SOAPrequest('GetVolume', "<Channel>Master</Channel>", 'RenderingControl')
        if response is not None:
            volume_xml = response.decode('utf8')
            tree = ET.fromstring(volume_xml)
            for elem in tree.iter(tag='CurrentVolume'):
                self.volume = elem.text
        return self.volume

    def get_running_app(self):

        if self._app_list is not None:

            for app in self._app_list:

                r = None

                try:
                    r = requests.get('http://{host}:8001/api/v2/applications/{value}'.format(host=self.host, value=self._app_list[app]), timeout=0.5)
                except requests.exceptions.RequestException as e:
                    pass

                if r is not None:
                    data = r.text
                    if data is not None:
                        root = json.loads(data.encode('UTF-8'))
                        if 'visible' in root:
                            if root['visible']:
                                return app

        return 'TV/HDMI'

    def set_volume(self, volume):
        self.SOAPrequest('SetVolume', "<Channel>Master</Channel><DesiredVolume>{}</DesiredVolume>".format(volume), 'RenderingControl')

    def get_mute(self):
        response = self.SOAPrequest('GetMute', "<Channel>Master</Channel>", 'RenderingControl')
        if response is not None:
            # mute_xml = response.decode('utf8')
            tree = ET.fromstring(response.decode('utf8'))
            mute = 0
            for elem in tree.iter(tag='CurrentMute'):
                mute = elem.text
            if (int(mute) == 0):
                self.mute = False
            else:
                self.mute = True
        return self.mute

    def set_current_media(self, url):
        """ Set media to playback and play it."""
        try:
            self.SOAPrequest('SetAVTransportURI', "<CurrentURI>{url}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>".format(url=url), 'AVTransport')
            self.SOAPrequest('Play', "<Speed>1</Speed>", 'AVTransport')
        except Exception:
            pass

    def play(self):
        """ Play media that was already set as current."""
        try:
            self.SOAPrequest('Play', "<Speed>1</Speed>", 'AVTransport')
        except Exception:
            pass
