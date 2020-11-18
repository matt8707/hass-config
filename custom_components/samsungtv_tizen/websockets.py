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
import requests
from . import exceptions
from . import shortcuts

_LOGGING = logging.getLogger(__name__)


class SamsungTVWS:
    _URL_FORMAT = 'ws://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}'
    _SSL_URL_FORMAT = 'wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}&token={token}'
    _REST_URL_FORMAT = 'http://{host}:8001/api/v2/{append}'

    def __init__(self, host, token=None, token_file=None, port=8001, timeout=None, key_press_delay=1,
                 name='SamsungTvRemote', app_list=None):
        self.host = host
        self.token = token
        self.token_file = token_file
        self._app_list = app_list
        self.port = port
        self.timeout = None if timeout == 0 else timeout
        self.key_press_delay = key_press_delay
        self.name = name
        self.connection = None

    def __enter__(self):
        return self

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

    def _format_rest_url(self, append=''):
        params = {
            'host': self.host,
            'append': append,
        }

        return self._REST_URL_FORMAT.format(**params)

    def _get_token(self):
        if self.token_file is not None:
            try:
                with open(self.token_file, 'r') as token_file:
                    return token_file.readline()
            except:
                return ''
        else:
            return self.token

    def _set_token(self, token):
        _LOGGING.info('New token %s', token)
        if self.token_file is not None:
            _LOGGING.debug('Save token to file', token)
            with open(self.token_file, 'w') as token_file:
                token_file.write(token)
        else:
            self.token = token

    def _ws_send(self, command, key_press_delay=None):
        if self.connection is None:
            self.open()

        payload = json.dumps(command)
        self.connection.send(payload)

        if key_press_delay is None:
            time.sleep(self.key_press_delay)
        else:
            time.sleep(key_press_delay)

    def _rest_request(self, target, method='GET'):
        url = self._format_rest_url(target)
        try:
            if method == 'POST':
                return requests.post(url, timeout=self.timeout)
            elif method == 'PUT':
                return requests.put(url, timeout=self.timeout)
            elif method == 'DELETE':
                return requests.delete(url, timeout=self.timeout)
            else:
                return requests.get(url, timeout=self.timeout)
        except requests.ConnectionError:
            raise exceptions.HttpApiError('TV unreachable or feature not supported on this model.')

    def _process_api_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            _LOGGING.debug('Failed to parse response from TV. response text: %s', response)
            raise exceptions.ResponseError('Failed to parse response from TV. Maybe feature not supported on this model')

    def open(self):
        is_ssl = self._is_ssl_connection()
        url = self._format_websocket_url(is_ssl)
        sslopt = {'cert_reqs': ssl.CERT_NONE} if is_ssl else {}

        _LOGGING.debug('WS url %s', url)
        self.connection = websocket.create_connection(
            url,
            self.timeout,
            sslopt=sslopt
        )

        completed = False

        try:
            response = self._process_api_response(self.connection.recv())
        except:
            response = False

        if response and response.get("event", "") == "ms.channel.connect":
            conn_data = response.get("data")
            completed = True
            token = conn_data.get("token")
            if token:
                _LOGGING.debug("Got token %s", token)
                self._set_token(token)

        if not completed:
            # For correct auth
            self.timeout = 45
            self.close()
            raise exceptions.ConnectionFailure(response)

    def close(self):
        if self.connection:
            self.connection.close()

        self.connection = None
        _LOGGING.debug('Connection closed.')

    def send_key(self, key, key_press_delay=None, cmd='Click'):
        _LOGGING.debug('Sending key %s', key)
        self._ws_send(
            {
                'method': 'ms.remote.control',
                'params': {
                    'Cmd': cmd,
                    'DataOfCmd': key,
                    'Option': 'false',
                    'TypeOfRemote': 'SendRemoteKey'
                }
            },
            key_press_delay
        )

    def hold_key(self, key, seconds):
        self.send_key(key, cmd='Press')
        time.sleep(seconds)
        self.send_key(key, cmd='Release')

    def move_cursor(self, x, y, duration=0):
        self._ws_send(
            {
                'method': 'ms.remote.control',
                'params': {
                    'Cmd': 'Move',
                    'Position': {
                        'x': x,
                        'y': y,
                        'Time': str(duration)
                    },
                    'TypeOfRemote': 'ProcessMouseDevice'
                }
            },
            key_press_delay=0
        )

    def run_app(self, app_id, app_type='DEEP_LINK', meta_tag=''):
        _LOGGING.debug('Sending run app app_id: %s app_type: %s meta_tag: %s', app_id, app_type, meta_tag)
        self._ws_send({
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

    def open_browser(self, url):
        _LOGGING.debug('Opening url in browser %s', url)
        self.run_app(
            'org.tizen.browser',
            'NATIVE_LAUNCH',
            url
        )

    def app_list(self):
        _LOGGING.debug('Get app list')
        self._ws_send({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.installedApp.get',
                'to': 'host'
            }
        })

        response = self._process_api_response(self.connection.recv())
        if response.get('data') and response.get('data').get('data'):
            return response.get('data').get('data')
        else:
            return response

    def rest_device_info(self):
        _LOGGING.debug('Get device info via rest api')
        response = self._rest_request('')
        return self._process_api_response(response.text)

    def rest_app_status(self, app_id):
        _LOGGING.debug('Get app %s status via rest api', app_id)
        response = self._rest_request('applications/' + app_id)
        return self._process_api_response(response.text)

    def rest_app_run(self, app_id):
        _LOGGING.debug('Run app %s via rest api', app_id)
        response = self._rest_request('applications/' + app_id, 'POST')
        return self._process_api_response(response.text)

    def rest_app_close(self, app_id):
        _LOGGING.debug('Close app %s via rest api', app_id)
        response = self._rest_request('applications/' + app_id, 'DELETE')
        return self._process_api_response(response.text)

    def rest_app_install(self, app_id):
        _LOGGING.debug('Install app %s via rest api', app_id)
        response = self._rest_request('applications/' + app_id, 'PUT')
        return self._process_api_response(response.text)

    def shortcuts(self):
        return shortcuts.SamsungTVShortcuts(self)
