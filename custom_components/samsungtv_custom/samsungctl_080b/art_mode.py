# -*- coding: utf-8 -*-

from __future__ import print_function
import threading
import logging
import json
from .utils import LogIt
from .websocket_base import AuxWebsocketBase

logger = logging.getLogger(__name__)


URL_FORMAT = "ws://{}:{}/api/v2/channels/com.samsung.art-app?name={}"
SSL_URL_FORMAT = "wss://{}:{}/api/v2/channels/com.samsung.art-app?name={}"


class ArtMode(AuxWebsocketBase):

    def __init__(self, config):
        AuxWebsocketBase.__init__(self, config, URL_FORMAT, SSL_URL_FORMAT)

    def is_supported(self):
        return self.sock is not None

    @LogIt
    def on_message(self, message):
        response = json.loads(message)

        logger.debug(
            self.config.host,
            ' <---- art_mode: ' +
            json.dumps(response, indent=4)
        )

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
                        if data['event'] == 'go_to_standby':
                            print(json.dumps(data, indent=4))
                        elif data['event'] == 'wakeup':
                            print(json.dumps(data, indent=4))
                        elif data['event'] == 'art_mode_changed':
                            print(json.dumps(data, indent=4))

                        for callback, key, _ in self._registered_callbacks[:]:
                            if key == data['event']:
                                self._registered_callbacks.remove(
                                    [callback, key, None]
                                )
                                callback(data)
                                break

    def _build_art_app_request(self, request, value=None):
        if value is None:
            data = dict(
                request=request,
                id=self._id
            )
        else:
            data = dict(
                request=request,
                value=value,
                id=self._id
            )

        return dict(
            clientIp=self._client_ip,
            data=json.dumps(data),
            deviceName=self._device_name,
            event='art_app_request',
            to='host'
        )

    @property
    def motion_timer(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":\"get_motion_timer\",
                    \"id\":\"30852acd-1b7d-4496-8bef-53e1178fa839\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_motion_timer')

        response = []
        event = threading.Event()

        def motion_timer_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"259320d8-f368-48a4-bf03-789f24a22c0f\",
                        \"event\":\"motion_timer\",
                        \"value\":\"30\",
                        \"valid_values\":\"[\\\"off\\\",\\\"15\\\",\\\"30\\\",\\\"60\\\",\\\"120\\\",\\\"240\\\"]\\n\",
                        \"target_client_id\":\"84b12082-5f28-461e-8e81-b98ad1c1ffa\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"84b12082-5f28-461e-8e81-b98ad1c1ffa"
                }
            }
            """

            valid_values = []

            for item in data['valid_values']:
                if item.isdigit():
                    item = int(item)
                valid_values += [item]

            if data['value'].isdigit():
                data['value'] = int(data['value'])

            response.append(
                dict(
                    value=int(data['value']),
                    valid_values=valid_values[:]

                )
            )

            event.set()

        self.register_receive_callback(
            motion_timer_callback,
            'motion_timer',
            None
        )

        sent = self.send('ms.channel.emit', **params)

        if sent:
            event.wait(2.0)

        self.unregister_receive_callback(
            motion_timer_callback,
            'motion_timer',
            None
        )

        if sent:
            if not event.isSet():
                logging.debug(
                    self.config.host +
                    ' -- (get_motion_timer) timed out'
                )
            else:
                return response[0]

    @motion_timer.setter
    def motion_timer(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"off\",
                    \"request\":\"set_motion_timer\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        if value != 'off':
            value = int(value)

        res = self.motion_timer

        if res and value in res['valid_values']:
            params = self._build_art_app_request(
                'set_motion_timer',
                str(value)
            )

            self.send('ms.channel.emit', **params)

    @property
    def motion_sensitivity(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":\"get_motion_sensitivity\",
                    \"id\":\"30852acd-1b7d-4496-8bef-53e1178fa839\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_motion_sensitivity')

        response = []
        event = threading.Event()

        def motion_sensitivity_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"259320d8-f368-48a4-bf03-789f24a22c0f\",
                        \"event\":\"motion_sensitivity\",
                        \"value\":\"2\",
                        \"min\":\"1\",
                        \"max\":\"3\",
                        \"target_client_id\":\"84b12082-5f28-461e-8e81-b98ad1c1ffa\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"84b12082-5f28-461e-8e81-b98ad1c1ffa"
                }
            }
            """
            response.append(
                dict(
                    value=int(data['value']),
                    min=int(data['min']),
                    max=int(data['max'])
                )
            )

            event.set()

        self.register_receive_callback(
            motion_sensitivity_callback,
            'motion_sensitivity',
            None
        )

        sent = self.send('ms.channel.emit', **params)

        if sent:
            event.wait(2.0)

        self.unregister_receive_callback(
            motion_sensitivity_callback,
            'motion_sensitivity',
            None
        )

        if sent:
            if not event.isSet():
                logging.debug(
                    self.config.host +
                    ' -- (get_motion_sensitivity) timed out'
                )
            else:
                return response[0]

    @motion_sensitivity.setter
    def motion_sensitivity(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"2\",
                    \"request\":\"set_motion_sensitivity\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """
        value = int(value)

        res = self.motion_sensitivity
        if res and res['min'] <= value <= res['max']:
            params = self._build_art_app_request(
                'set_motion_sensitivity',
                str(value)
            )

            self.send('ms.channel.emit', **params)

    @property
    def color_temperature(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":\"get_color_temperature\",
                    \"id\":\"30852acd-1b7d-4496-8bef-53e1178fa839\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_color_temperature')

        response = []
        event = threading.Event()

        def color_temperature_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"259320d8-f368-48a4-bf03-789f24a22c0f\",
                        \"event\":\"color_temperature\",
                        \"value\":\"2\",
                        \"min\":\"1\",
                        \"max\":\"3\",
                        \"target_client_id\":\"84b12082-5f28-461e-8e81-b98ad1c1ffa\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"84b12082-5f28-461e-8e81-b98ad1c1ffa"
                }
            }
            """
            response.append(
                dict(
                    value=int(data['value']),
                    min=int(data['min']),
                    max=int(data['max'])
                )
            )

            event.set()

        self.register_receive_callback(
            color_temperature_callback,
            'color_temperature',
            None
        )

        sent = self.send('ms.channel.emit', **params)

        if sent:
            event.wait(2.0)

        self.unregister_receive_callback(
            color_temperature_callback,
            'color_temperature',
            None
        )

        if sent:
            if not event.isSet():
                logging.debug(
                    self.config.host +
                    ' -- (get_color_temperature) timed out'
                )
            else:
                return response[0]

    @color_temperature.setter
    def color_temperature(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"2\",
                    \"request\":\"set_color_temperature\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """
        value = int(value)

        res = self.color_temperature
        if res and res['min'] <= value <= res['max']:
            params = self._build_art_app_request(
                'set_color_temperature',
                str(value)
            )

            self.send('ms.channel.emit', **params)

    @property
    def brightness(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":\"get_brightness\",
                    \"id\":\"30852acd-1b7d-4496-8bef-53e1178fa839\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_brightness')

        response = []
        event = threading.Event()

        def brightness_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"259320d8-f368-48a4-bf03-789f24a22c0f\",
                        \"event\":\"brightness\",
                        \"value\":\"2\",
                        \"min\":\"1\",
                        \"max\":\"3\",
                        \"target_client_id\":\"84b12082-5f28-461e-8e81-b98ad1c1ffa\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"84b12082-5f28-461e-8e81-b98ad1c1ffa"
                }
            }
            """
            response.append(
                dict(
                    value=int(data['value']),
                    min=int(data['min']),
                    max=int(data['max'])
                )
            )

            event.set()

        self.register_receive_callback(
            brightness_callback,
            'brightness',
            None
        )

        sent = self.send('ms.channel.emit', **params)
        if sent:
            event.wait(2.0)

        self.unregister_receive_callback(
            brightness_callback,
            'brightness',
            None
        )

        if sent:
            if not event.isSet():
                logger.debug('get_brightness: timed out')
            else:
                return response[0]

    @brightness.setter
    def brightness(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"2\",
                    \"request\":\"set_brightness\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """
        value = int(value)

        res = self.brightness
        if res and res['min'] <= value <= res['max']:
            params = self._build_art_app_request(
                'set_brightness',
                str(value)
            )

            self.send('ms.channel.emit', **params)

    @property
    def brightness_sensor(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":\"get_brightness_sensor_setting\",
                    \"id\":\"713fe2f1-2848-4161-b04c-18dd6753ecaf\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_brightness_sensor_setting')

        response = []
        event = threading.Event()

        def brightness_sensor_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"713fe2f1-2848-4161-b04c-18dd6753ecaf\",
                        \"event\":\"brightness_sensor_setting\",
                        \"value\":\"off\",
                        \"target_client_id\":\"de34a6-2b5f-46a0-ad19-f1a3d56167\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"de34a6-2b5f-46a0-ad19-f1a3d56167"
                }
            }
            """

            if data['value'] == 'on':
                response.append(True)
            else:
                response.append(False)

            event.set()

        self.register_receive_callback(
            brightness_sensor_callback,
            'brightness_sensor_setting',
            None
        )

        sent = self.send('ms.channel.emit', **params)
        if sent:
            event.wait(2.0)

        self.unregister_receive_callback(
            brightness_sensor_callback,
            'brightness_sensor_setting',
            None
        )

        if sent:
            if not event.isSet():
                logging.debug(
                    self.config.host +
                    ' -- (get_brightness_sensor_setting) timed out'
                )
            else:
                return response[0]

    @brightness_sensor.setter
    def brightness_sensor(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"on\",
                    \"request\":\"set_brightness_sensor_setting\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request(
            'set_brightness_sensor_setting',
            'on' if value else 'off'
        )

        self.send('ms.channel.emit', **params)

    @property
    def artmode(self):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"request\":
                    \"get_artmode_status\",
                    \"id\":\"30852acd-1b7d-4496-8bef-53e1178fa839\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request('get_artmode_status')

        response = []
        event = threading.Event()

        def artmode_callback(data):
            """
            {
                "method":"ms.channel.emit",
                "params":{
                    "clientIp":"127.0.0.1",
                    "data":"{
                        \"id\":\"259320d8-f368-48a4-bf03-789f24a22c0f\",
                        \"event\":\"artmode_status\",
                        \"value\":\"off\",
                        \"target_client_id\":\"84b12082-5f28-461e-8e81-b98ad1c1ffa\"
                    }",
                    "deviceName":"Smart Device",
                    "event":"d2d_service_message",
                    "to":"84b12082-5f28-461e-8e81-b98ad1c1ffa"
                }
            }
            """

            if data['value'] == 'on':
                response.append(True)
            else:
                response.append(False)

            event.set()

        self.register_receive_callback(
            artmode_callback,
            'artmode_status',
            None
        )

        sent = self.send('ms.channel.emit', **params)

        if sent:
            event.wait(3.0)

        self.unregister_receive_callback(
            artmode_callback,
            'artmode_status',
            None
        )

        if sent:
            if not event.isSet():
                logger.debug(
                    self.config.host +
                    ' -- (get_artmode_status) timed out'
                )
            else:
                return response[0]


    @artmode.setter
    def artmode(self, value):
        """
        {
            "method":"ms.channel.emit",
            "params":{
                "clientIp":"192.168.1.20",
                "data":"{
                    \"id\":\"545fc0c1-bd9b-48f5-8444-02f9c519aaec\",
                    \"value\":\"on\",
                    \"request\":\"set_artmode_status\"
                }",
                "deviceName":"W1Bob25lXWlQaG9uZQ==",
                "event":"art_app_request",
                "to":"host"
            }
        }
        """

        params = self._build_art_app_request(
            'set_artmode_status',
            'on' if value else 'off'
        )

        self.send('ms.channel.emit', **params)

