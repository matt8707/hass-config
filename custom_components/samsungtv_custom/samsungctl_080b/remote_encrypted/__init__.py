# -*- coding: utf-8 -*-
"""
The code for the encrypted websocket connection is a modified version of the
SmartCrypto library that was modified by eclair4151.
I want to thank eclair4151 for writing the code that allows the samsungctl
library to support H and J (2014, 2015) model TV's

https://github.com/eclair4151/SmartCrypto
"""


from __future__ import print_function
import requests
import time
import websocket
import threading
import json
from lxml import etree
import logging
import traceback

from . import crypto # NOQA
from .aes import AES # NOQA
from .. import websocket_base # NOQA
from ..upnp.UPNP_Device.xmlns import strip_xmlns # NOQA
from ..utils import LogIt, LogItWithReturn # NOQA

logger = logging.getLogger('samsungctl')


class URL(object):

    def __init__(self, config):
        self.config = config

    @property
    def base_url(self):
        return 'http://{0}'.format(self.config.host)

    @property
    def full_url(self):
        return "{0}:{1}".format(self.base_url, self.config.port)

    @property
    @LogItWithReturn
    def request(self):
        return (
            '{0}/ws/pairing?'
            'step={{0}}&'
            'app_id=12345&'
            'device_id=7e509404-9d7c-46b4-8f6a-e2a9668ad184'.format(
                self.full_url,
                # self.config.app_id,
                # self.config.id
            )
        )

    @property
    @LogItWithReturn
    def step1(self):
        return self.request.format(0) + "&type=1"

    @property
    @LogItWithReturn
    def step2(self):
        return self.request.format(1)

    @property
    @LogItWithReturn
    def step3(self):
        return self.request.format(2)

    @property
    @LogItWithReturn
    def step4(self):
        millis = int(round(time.time() * 1000))
        return '{0}:8000/socket.io/1/?t={1}'.format(self.base_url, millis)

    @property
    @LogItWithReturn
    def websocket(self):

        logger.debug(
            self.config.host +
            ' <-- (' +
            self.step4 +
            ') ""'
        )

        try:
            websocket_response = requests.get(self.step4, timeout=3)
        except (requests.HTTPError, requests.exceptions.ConnectTimeout):
            logger.info(
                self.config.model +
                ' -- unable to open connection.. Is the TV on?!?'
            )
            return None

        logger.debug(
            self.config.host +
            ' --> (' +
            self.step4 +
            ') ' +
            websocket_response.content.decode('utf-8')
        )

        websocket_url = (
            'ws://{0}:8000/socket.io/1/websocket/{1}'.format(
                self.config.host,
                websocket_response.text.split(':')[0]
            )
        )

        logger.debug(
            self.config.host +
            ' -- (websocket url)' +
            websocket_url
        )

        return websocket_url

    @property
    @LogItWithReturn
    def cloud_pin_page(self):
        return "{0}/ws/apps/CloudPINPage".format(self.full_url)


# noinspection PyAbstractClass
class RemoteEncrypted(websocket_base.WebSocketBase):

    @LogIt
    def __init__(self, config):
        self.url = URL(config)
        self.current_session_id = None
        self.aes = None

        websocket_base.WebSocketBase.__init__(self, config)

    @LogItWithReturn
    def open(self):
        with self._auth_lock:
            if self._thread is None:
                self._thread = threading.Thread(target=self.loop)
                self._thread.start()

            if self.sock is not None:
                return True

            del self._registered_callbacks[:]

            if self.config.token is None:
                if self.check_pin_page():
                    logger.debug(
                        self.config.host +
                        ' -- showing pin page'
                    )
                    self.show_pin_page()
                else:
                    logger.debug(
                        self.config.host +
                        ' -- pin page already displayed'
                    )
                try:
                    while not self.config.paired:
                        tv_pin = self.config.get_pin()
                        if tv_pin is False:
                            logger.error(
                                self.config.host +
                                '-- pin retry limit reached.'
                            )
                            self.is_powering_on = False
                            return False

                        if tv_pin is None:
                            continue

                        logger.info(
                            self.config.host +
                            ' -- (pin) ' +
                            tv_pin
                        )

                        self.first_step_of_pairing()
                        output, last_request_id = self.hello_exchange(tv_pin)
                        if output:
                            logger.info(
                                self.config.host +
                                ' -- pin accepted'
                            )

                            aes_key = crypto.bytes2str(output['ctx'])
                            logger.debug(
                                self.config.host +
                                ' -- (aes_key) ' +
                                aes_key.upper()
                            )

                            sk_prime = output['SKPrime']
                            logger.debug(
                                self.config.host +
                                ' -- (sk prime) ' +
                                repr(sk_prime)
                            )

                            current_session_id = self.acknowledge_exchange(
                                last_request_id,
                                sk_prime
                            )

                            self.config.token = (
                                aes_key.upper() + ':' + str(current_session_id)
                            )
                            logger.debug(
                                self.config.host +
                                ' -- (token) ' +
                                self.config.token
                            )

                            logger.info(
                                self.config.host +
                                ' -- authorization successful.'
                            )

                            self.config.paired = True
                            if self.config.path:
                                self.config.save()

                        else:
                            logger.info(
                                self.config.host +
                                ' -- pin incorrect.\nplease try again...'
                            )
                finally:
                    self.close_pin_page()

            if self.config.token is None:
                raise RuntimeError('Unknown Authentication Error')

            aes_key, current_session_id = self.config.token.rsplit(':', 1)
            self.current_session_id = int(current_session_id)

            if self.aes is None:
                self.aes = AES(aes_key)

            websocket_url = self.url.websocket
            if websocket_url is None:
                return False

            # noinspection PyPep8,PyBroadException

            try:
                self.sock = websocket.create_connection(websocket_url)
            except:
                return False

            return True

    @LogIt
    def show_pin_page(self):
        logger.debug(
            self.config.host +
            ' <-- (' +
            self.url.cloud_pin_page +
            ') "pin4"'
        )

        response = requests.post(self.url.cloud_pin_page, "pin4")

        logger.debug(
            self.config.host +
            ' --> (' +
            self.url.cloud_pin_page +
            ') ' +
            response.content.decode('utf-8')
        )

    @LogItWithReturn
    def check_pin_page(self):
        logger.debug(
            self.config.host +
            ' <-- (' +
            self.url.cloud_pin_page +
            ') ""'
        )

        response = requests.get(self.url.cloud_pin_page, timeout=3)

        logger.debug(
            self.config.host +
            ' --> (' +
            self.url.cloud_pin_page +
            ') ' +
            response.content.decode('utf-8')
        )

        try:
            root = etree.fromstring(response.content)
        except etree.LxmlSyntaxError:
            return False

        root = strip_xmlns(root)

        state = root.find('state')
        if state is not None:
            logger.debug(
                self.config.host +
                ' --> (pin display state)' +
                state.text
            )
            if state.text == 'stopped':
                return True

        return False

    @LogIt
    def first_step_of_pairing(self):
        logger.debug(
            self.config.host +
            ' <-- (' +
            self.url.step1 +
            ') ""'
        )

        response = requests.get(self.url.step1)
        logger.debug(
            self.config.host +
            ' --> (' +
            self.url.step1 +
            ') ' +
            response.content.decode('utf-8')
        )

    @LogItWithReturn
    def hello_exchange(self, pin):
        hello_output = crypto.generate_server_hello('654321', pin)

        logger.debug(
            self.config.host +
            ' -- (hello output) ' +
            str(hello_output)
        )

        if not hello_output:
            return {}

        content = dict(
            auth_Data=dict(
                auth_type='SPC',
                GeneratorServerHello=crypto.bytes2str(
                    hello_output['serverHello']
                ).upper()
            )
        )

        logger.debug(
            self.config.host +
            ' <-- (' +
            self.url.step2 +
            ') ' +
            str(content)
        )

        response = requests.post(self.url.step2, json=content)
        logger.debug(
            self.config.host +
            ' --> (' +
            self.url.step2 +
            ') ' +
            response.content.decode('utf-8')
        )

        try:
            auth_data = json.loads(response.json()['auth_data'])
            client_hello = auth_data['GeneratorClientHello']
            request_id = auth_data['request_id']
        except (ValueError, KeyError):
            return {}

        client_response = crypto.parse_client_hello(
            client_hello,
            # hello_output['hash'],
            hello_output['AES_key'],
            '654321'
        )

        logger.debug(
            self.config.host +
            ' -- (hello_exchange) ' +
            str(client_response)
        )

        return client_response, int(request_id)

    @LogItWithReturn
    def acknowledge_exchange(self, last_request_id, sk_prime):
        server_ack_message = crypto.generate_server_acknowledge(sk_prime)
        content = dict(
            auth_Data=dict(
                auth_type='SPC',
                request_id=str(last_request_id),
                ServerAckMsg=server_ack_message
            )
        )

        logger.debug(
            self.config.host +
            ' <-- (' +
            self.url.step3 +
            ') ' +
            str(content)
        )

        response = requests.post(self.url.step3, json=content)

        logger.debug(
            self.config.host +
            ' --> (' +
            self.url.step3 +
            ') ' +
            response.content.decode('utf-8')
        )

        if "secure-mode" in response.content.decode('utf-8'):
            self.is_powering_on = False
            raise RuntimeError(
                "TODO: Implement handling of encryption flag!!!!"
            )

        try:
            auth_data = json.loads(response.json()['auth_data'])
            client_ack = auth_data['ClientAckMsg']
            session_id = auth_data['session_id']
        except (ValueError, KeyError):
            self.is_powering_on = False
            raise RuntimeError(
                "Unable to get session_id and/or ClientAckMsg!!!"
            )

        logger.debug(
            self.config.host +
            ' -- (session id) ' +
            session_id
        )

        if not crypto.parse_client_acknowledge(client_ack, sk_prime):
            self.is_powering_on = False
            raise RuntimeError("Parse client ack message failed.")

        return session_id

    @LogIt
    def close_pin_page(self):
        requests.delete(self.url.cloud_pin_page + '/run')
        return False

    def on_message(self, response):
        # noinspection PyPep8,PyBroadException
        try:
            response = self.aes.decrypt(response)
        except:
            pass

        logger.debug(
            self.config.host +
            ' --> ' +
            repr(response)
        )

        for callback, key, data in self._registered_callbacks[:]:
            if key == response:
                self._registered_callbacks.remove(
                    [callback, key, data]
                )
                callback(response)
                break

        if response.startswith('5::/com.samsung.companion'):
            response = response.replace('5::/com.samsung.companion:', '')
            response = json.loads(response)
            if response['name'] == 'receiveCommon':
                args = eval(response['args'])
                args = ''.join(hex(itm)[2:].zfill(2) for itm in args)
                response = json.loads(self.aes.decrypt(args))

                for callback, key, data in self._registered_callbacks[:]:
                    if (
                        key in response and
                        (data is None or response[key] == data)
                    ):
                        self._registered_callbacks.remove(
                            [callback, key, data]
                        )
                        callback(response)
                        break

    def _send_key(self, command):
        with self._send_lock:
            command = dict(
                method="POST",
                body=dict(
                    plugin="RemoteControl",
                    param1="uuid:12345",
                    param2="Click",
                    param3=command,
                    param4=False,
                    api="SendRemoteKey",
                    version="1.000"
                )
            )

            command_bytes = self.aes.encrypt(json.dumps(command))

            if isinstance(command_bytes, str):
                int_array = list(str(ord(x)) for x in command_bytes)
            else:
                int_array = list(map(str, command_bytes))

            res = dict(
                name="callCommon",
                args=[
                    dict(
                        Session_Id=self.current_session_id,
                        body='[' + (','.join(int_array)) + ']'
                    )
                ]
            )

            packet = '5::/com.samsung.companion:' + json.dumps(res)

            logger.debug(
                self.config.host +
                ' <-- "1::/com.samsung.companion"'
            )
            # noinspection PyPep8,PyBroadException
            try:
                event = threading.Event()

                def callback(_):
                    event.set()

                self.register_receive_callback(
                    callback,
                    '1::/com.samsung.companion',
                    None
                )
                self.register_receive_callback(
                    callback,
                    '1::',
                    None
                )

                self.sock.send(
                    '1::/com.samsung.companion'
                )
                event.wait(2.0)

                self.unregister_receive_callback(
                    callback,
                    '1::/com.samsung.companion',
                    None
                )
                self.unregister_receive_callback(
                    callback,
                    '1::',
                    None
                )

                if not event.isSet():
                    logger.debug(
                        self.config.host +
                        ' -- remote key send failure 1::/com.samsung.companion'
                    )
                    return

                event.clear()

                logger.debug(
                    self.config.host +
                    ' <-- ' +
                    repr(packet)
                )

                result = []

                def callback(response):
                    if (
                        'api' in response and
                        response['api'] == 'SendRemoteKey'
                    ):
                        result.append(response['result'])
                        event.set()

                self.register_receive_callback(
                    callback,
                    'plugin',
                    'RemoteControl'
                )

                self.sock.send(packet)

                event.wait(2.0)

                self.unregister_receive_callback(
                    callback,
                    'plugin',
                    'RemoteControl'
                )

                if event.isSet() and result[0] in (1, '1'):
                    return True

                return False

            except:
                traceback.print_exc()
                return False
