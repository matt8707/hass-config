# -*- coding: utf-8 -*-

from __future__ import print_function
import base64
import logging
import threading
import ssl
import websocket
import requests
import time
import json
from . import art_mode
from . import application
from . import websocket_base
from .utils import LogIt, LogItWithReturn

logger = logging.getLogger(__name__)
#
#
# URL_FORMAT = "ws://{}:{}/api/v2/channels/samsung.tv.display?name={}"
# SSL_URL_FORMAT = "wss://{}:{}/api/v2/channels/samsung.tv.display?name={}"
#
# URL_FORMAT = "ws://{}:{}/api/v2/channels/samsung.tv.channel?name={}"
# SSL_URL_FORMAT = "wss://{}:{}/api/v2/channels/samsung.tv.channel?name={}"

URL_FORMAT = "ws://{0}:{1}/api/v2/channels/samsung.remote.control?name={2}"
SSL_URL_FORMAT = "wss://{0}:{1}/api/v2/channels/samsung.remote.control?name={2}"


# noinspection PyAbstractClass
class RemoteWebsocket(websocket_base.WebSocketBase):
    """Object for remote control connection."""

    @LogIt
    def __init__(self, config):
        self.receive_lock = threading.Lock()
        self.send_event = threading.Event()
        self._cec = None
        self._art_mode = None
        self._app_websocket = None
        websocket_base.WebSocketBase.__init__(self, config)

    @property
    @LogItWithReturn
    def has_ssl(self):
        try:
            logger.debug(
                self.config.host +
                ' <-- http://{0}:8001/api/v2/'.format(self.config.host)
            )
            response = requests.get(
                'http://{0}:8001/api/v2/'.format(self.config.host),
                timeout=3
            )
            logger.debug(
                self.config.host +
                ' --> ' +
                response.content.decode('utf-8')
            )
            return (
                json.loads(
                    response.content.decode('utf-8')
                )['device']['TokenAuthSupport'] == 'true'
            )
        except (ValueError, KeyError):
            return False
        except (requests.HTTPError, requests.exceptions.ConnectTimeout):
            return None

    @LogIt
    def open(self):
        def do():
            if self.config.port == 8002:
                if self.config.token:
                    token = "&token=" + str(self.config.token)
                else:
                    token = ''

                sslopt = {"cert_reqs": ssl.CERT_NONE}
                url = SSL_URL_FORMAT.format(
                    self.config.host,
                    self.config.port,
                    self._serialize_string(self.config.name)
                ) + token
            else:
                sslopt = {}
                url = URL_FORMAT.format(
                    self.config.host,
                    self.config.port,
                    self._serialize_string(self.config.name)
                )

            auth_event = threading.Event()
            unauth_event = threading.Event()

            @LogIt
            def unauthorized_callback(_):
                unauth_event.set()
                auth_event.set()

            @LogItWithReturn
            def auth_callback(data):
                if 'data' in data and 'token' in data["data"]:
                    self.config.token = data['data']["token"]

                    logger.debug(
                        self.config.host +
                        ' -- (token) ' +
                        str(self.config.token)
                    )

                self.config.paired = True

                if self.config.path:
                    self.config.save()

                logger.debug(
                    self.config.host +
                    ' -- access granted'
                )
                auth_event.set()

            del self._registered_callbacks[:]

            self.register_receive_callback(
                auth_callback,
                'event',
                'ms.channel.connect'
            )

            self.register_receive_callback(
                unauthorized_callback,
                'event',
                'ms.channel.unauthorized'
            )

            logger.debug(
                self.config.host +
                ' <-- websocket url: ' +
                url +
                ' - ssl options:' +
                str(sslopt)
            )

            if self._thread is None:
                self._thread = threading.Thread(target=self.loop)
                self._thread.start()

            # noinspection PyPep8,PyBroadException
            try:
                self.sock = websocket.create_connection(url, sslopt=sslopt)
            except:
                if not self.config.paired:
                    raise RuntimeError('Unable to connect to the TV')

                return False

            auth_event.wait(30.0)

            self.unregister_receive_callback(
                unauthorized_callback,
                'event',
                'ms.channel.unauthorized'
            )
            self.unregister_receive_callback(
                auth_callback,
                'event',
                'ms.channel.connect'
            )

            if auth_event.isSet() and not unauth_event.is_set():
                # self._app_websocket = application.AppWebsocket(self.config)

                if self._art_mode is not None:
                    self._art_mode.open()

                return True

            if self.config.port == 8001:
                logger.debug(
                    self.config.host +
                    ' -- trying SSL connection.'
                )
                self.config.port = 8002

                res = do()

                if not res:
                    self.config.port = 8001

                return res

            if self.config.token is not None:
                saved_token = self.config.token
                self.config.token = None

                res = do()

                if not res:
                    self.config.token = saved_token
                    raise RuntimeError(
                        'Auth Error: invalid token - '
                        'create a new pairing to the TV.'
                    )
                else:
                    logger.info(
                        self.config.host +
                        ' -- new token: ' +
                        str(self.config.token) +
                        ' old token: ' +
                        str(saved_token)
                    )
                    return res

            raise RuntimeError('Unknown Auth Failure: \n' + str(self.config))

        with self._auth_lock:
            if self.sock is not None:
                return True

            return do()

    @LogIt
    def send(self, method, **params):
        if self.sock is None:
            logger.info(
                self.config.host +
                ' -- is the TV on?!?'
            )
            return False

        with self._send_lock:

            payload = dict(
                method=method,
                params=params
            )
            logger.debug(
                self.config.host +
                ' <-- ' +
                str(payload)
            )

            # noinspection PyPep8,PyBroadException
            try:
                self.sock.send(json.dumps(payload))
                self.send_event.wait(0.3)
                return True
            except:
                return False

    def _send_key(self, key, cmd='Click'):
        """
        Send a control command.
        cmd can be one of the following
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"Click", "Press" or "Release",
                "DataOfCmd":"KEY_*",
                "Option":"false",
                "TypeOfRemote":"SendRemoteKey"
            }
        }

        """
        params = dict(
            Cmd=cmd,
            DataOfCmd=key,
            Option="false",
            TypeOfRemote="SendRemoteKey"
        )

        self.send("ms.remote.control", **params)

    _key_interval = 0.5

    @LogItWithReturn
    def get_application(self, pattern):
        for app in self.applications:
            if pattern in (app.app_id, app.name):
                return app

    @property
    @LogItWithReturn
    def applications(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "data":"",
                "event":"ed.edenApp.get",
                "to":"host",
            }
        }
        {
            "method":"ms.channel.emit",
            "params":{
                "data":"",
                "event":"ed.installedApp.get",
                "to":"host",
            }
        }

        """
        eden_event = threading.Event()
        installed_event = threading.Event()

        eden_data = []
        installed_data = []

        @LogIt
        def eden_app_get(data):
            if 'data' in data:
                eden_data.extend(data['data']['data'])
            eden_event.set()

        @LogIt
        def installed_app_get(data):
            if 'data' in data:
                installed_data.extend(data['data']['data'])
            installed_event.set()

        self.register_receive_callback(
            eden_app_get,
            'event',
            'ed.edenApp.get'
        )
        # self._app_websocket.register_receive_callback(
        #     eden_app_get,
        #     'event',
        #     'ed.edenApp.get'
        # )
        self.register_receive_callback(
            installed_app_get,
            'event',
            'ed.installedApp.get'
        )
        # self._app_websocket.register_receive_callback(
        #     installed_app_get,
        #     'event',
        #     'ed.installedApp.get'
        # )

        for event in ['ed.edenApp.get', 'ed.installedApp.get']:
            params = dict(
                data='',
                event=event,
                to='host'
            )

            self.send('ms.channel.emit', **params)

        eden_event.wait(30.0)
        installed_event.wait(30.0)

        self.unregister_receive_callback(
            eden_app_get,
            'event',
            'ed.edenApp.get'
        )

        # self._app_websocket.unregister_receive_callback(
        #     eden_app_get,
        #     'event',
        #     'ed.edenApp.get'
        # )
        self.unregister_receive_callback(
            installed_app_get,
            'event',
            'ed.installedApp.get'
        )
        # self._app_websocket.unregister_receive_callback(
        #     installed_app_get,
        #     'event',
        #     'ed.installedApp.get'
        # )

        if not eden_event.isSet():
            logger.debug(
                self.config.host +
                ' -- (ed.edenApp.get) timed out'
            )

        if not installed_event.isSet():
            logger.debug(
                self.config.host +
                ' -- (ed.installedApp.get) timed out'
            )

        if eden_data and installed_data:
            updated_apps = []

            for eden_app in eden_data[:]:
                for installed_app in installed_data[:]:
                    if eden_app['appId'] == installed_app['appId']:
                        installed_data.remove(installed_app)
                        eden_data.remove(eden_app)
                        eden_app.update(installed_app)
                        updated_apps += [eden_app]
                        break
        else:
            updated_apps = []

        updated_apps += eden_data + installed_data

        for app in updated_apps[:]:
            updated_apps.remove(app)
            updated_apps += [application.Application(self, **app)]

        return updated_apps

    @property
    def art_mode(self):
        if self._art_mode is None:
            self._art_mode = art_mode.ArtMode(self.config)

        return self._art_mode

    @LogIt
    def on_message(self, message):
        response = json.loads(message)

        for callback, key, data in self._registered_callbacks[:]:
            if key in response and (data is None or response[key] == data):
                self._registered_callbacks.remove([callback, key, data])
                callback(response)
                break
        else:
            if 'params' in response and 'event' in response['params']:
                event = response['params']['event']

                if event == 'd2d_service_message':
                    data = json.loads(response['params']['data'])

                    if 'event' in data:
                        for callback, key, _ in self._registered_callbacks[:]:
                            if key == data['event']:
                                self._registered_callbacks.remove(
                                    [callback, key, None]
                                )
                                callback(data)
                                break

    def run_browser(self, url):
        params = dict(
            data=dict(
                appId='org.tizen.browser',
                action_type='NATIVE_LAUNCH',
                metaTag=url
            ),
            event='ed.apps.launch',
            to='host'
        )

        self.send('ms.channel.emit', **params)

    @LogIt
    def input_text(self, text):
        """
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":base64.b64encode,
                "TypeOfRemote":"SendInputString",
                "DataOfCmd":"base64",
            }
        }
        """

        params = dict(
            Cmd=self._serialize_string(text),
            TypeOfRemote="SendInputString",
            DataOfCmd="base64"
        )

        self.send('ms.remote.control', **params)

    @LogIt
    def start_voice_recognition(self):
        """Activates voice recognition.

        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"Press",
                "TypeOfRemote":"SendRemoteKey",
                "DataOfCmd":"KEY_BT_VOICE",
                "Option":"false"
            }
        }

        """
        event = threading.Event()

        def voice_callback(_):
            event.set()

        self.register_receive_callback(
            voice_callback,
            'event',
            'ms.voiceApp.standby'
        )

        params = dict(
            Cmd='Press',
            DataOfCmd='KEY_BT_VOICE',
            Option="false",
            TypeOfRemote="SendRemoteKey"
        )

        self.send("ms.remote.control", **params)

        event.wait(2.0)
        self.unregister_receive_callback(
            voice_callback,
            'event',
            'ms.voiceApp.standby'
        )

        if not event.isSet():
            logger.debug(
                self.config.host +
                ' -- (ms.voiceApp.standby) timed out'
            )

    @LogIt
    def stop_voice_recognition(self):
        """Activates voice recognition.
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"Release",
                "TypeOfRemote":"SendRemoteKey",
                "DataOfCmd":"KEY_BT_VOICE",
                "Option":"false"
            }
        }
        """

        event = threading.Event()

        def voice_callback(_):
            event.set()

        self.register_receive_callback(
            voice_callback,
            'event',
            'ms.voiceApp.hide'
        )

        params = dict(
            Cmd='Release',
            DataOfCmd='KEY_BT_VOICE',
            Option="false",
            TypeOfRemote="SendRemoteKey"
        )

        self.send("ms.remote.control", **params)

        event.wait(2.0)
        self.unregister_receive_callback(
            voice_callback,
            'event',
            'ms.voiceApp.hide'
        )
        if not event.isSet():
            logger.debug(
                self.config.host +
                ' -- (ms.voiceApp.hide) timed out'
            )

    @staticmethod
    def _serialize_string(string):
        if isinstance(string, str):
            string = str.encode(string)

        return base64.b64encode(string).decode("utf-8")

    @property
    @LogItWithReturn
    def mouse(self):
        return Mouse(self)


class Mouse(object):

    @LogIt
    def __init__(self, remote):
        self._remote = remote
        self._is_running = False
        self._commands = []
        self._ime_start_event = threading.Event()
        self._ime_update_event = threading.Event()
        self._touch_enable_event = threading.Event()
        self._send_event = threading.Event()

    @property
    @LogItWithReturn
    def is_running(self):
        return self._is_running

    @LogIt
    def clear(self):
        if not self.is_running:
            del self._commands[:]

    @LogIt
    def _send(self, cmd, **kwargs):
        """Send a control command."""
        if not self.is_running:
            params = dict(
                Cmd=cmd,
                TypeOfRemote="ProcessMouseDevice"
            )
            params.update(kwargs)

            payload = dict(
                method="ms.remote.control",
                params=params
            )

            self._commands += [payload]

    @LogIt
    def left_click(self):
        """
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"LeftClick",
                "TypeOfRemote":"ProcessMouseDevice"
            }
        }
        """
        self._send('LeftClick')

    @LogIt
    def right_click(self):
        """
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"RightClick",
                "TypeOfRemote":"ProcessMouseDevice"
            }
        }
        """
        self._send('RightClick')

    @LogIt
    def move(self, x, y):
        """
        {
            "method":"ms.remote.control",
            "params":{
                "Cmd":"Move",
                "x": 0,
                "y": 0,
                "Time": time.time,
                "TypeOfRemote":"ProcessMouseDevice"
            }
        }
        """
        position = dict(
            x=x,
            y=y,
            Time=str(time.time())
        )

        self._send('Move', Position=position)

    @LogIt
    def add_wait(self, wait):
        if self._is_running:
            self._commands += [wait]

    @LogIt
    def stop(self):
        if self.is_running:
            self._send_event.set()
            self._ime_start_event.set()
            self._ime_update_event.set()
            self._touch_enable_event.set()

    @LogIt
    def run(self):
        if not self.is_running:
            self._send_event.clear()
            self._ime_start_event.clear()
            self._ime_update_event.clear()
            self._touch_enable_event.clear()

            self._is_running = True

            @LogIt
            def ime_start(_):
                self._ime_start_event.set()

            @LogIt
            def ime_update(_):
                self._ime_update_event.set()

            @LogIt
            def touch_enable(_):
                self._touch_enable_event.set()

            self._remote.register_receive_callback(
                ime_start,
                'event',
                'ms.remote.imeStart'
            )

            self._remote.register_receive_callback(
                ime_update,
                'event',
                'ms.remote.imeUpdate'
            )

            self._remote.register_receive_callback(
                touch_enable,
                'event',
                'ms.remote.touchEnable'
            )

            for payload in self._commands:
                if isinstance(payload, (float, int)):
                    self._send_event.wait(payload)
                    if self._send_event.isSet():
                        self._is_running = False
                        return
                else:
                    self._remote.send(**payload)

                self._ime_start_event.wait(len(self._commands))
                self._ime_update_event.wait(len(self._commands))
                self._touch_enable_event.wait(len(self._commands))

                self._remote.unregister_receive_callback(
                    ime_start,
                    'event',
                    'ms.remote.imeStart'
                )

                self._remote.unregister_receive_callback(
                    ime_update,
                    'event',
                    'ms.remote.imeUpdate'
                )

                self._remote.unregister_receive_callback(
                    touch_enable,
                    'event',
                    'ms.remote.touchEnable'
                )

                self._is_running = False
