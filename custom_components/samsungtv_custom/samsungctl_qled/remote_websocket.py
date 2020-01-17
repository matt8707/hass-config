import base64
import json
import logging
import socket
import time
import os
import ssl

from . import exceptions


URL_FORMAT = "ws://{}:{}/api/v2/channels/samsung.remote.control?name={}"
SSL_URL_FORMAT = "wss://{}:{}/api/v2/channels/samsung.remote.control?name={}"


class RemoteWebsocket():
    """Object for remote control connection."""

    def __init__(self, config):
        import websocket
        self.token_file = os.path.dirname(os.path.realpath(__file__)) + "/token.txt"

        if not config["port"]:
            config["port"] = 8001

        if config["timeout"] == 0:
            config["timeout"] = None

        if config["port"] == 8001:
            url = URL_FORMAT.format(config["host"], config["port"],
                        self._serialize_string(config["name"]))

            self.connection = websocket.create_connection(url, config["timeout"])
        elif config["port"] == 8002:
            url = SSL_URL_FORMAT.format(config["host"], config["port"],
                                        self._serialize_string(config["name"]))
            if os.path.isfile(self.token_file):
                with open(self.token_file, "r") as token_file:
                    url += "&token=" + token_file.readline()
            self.connection = websocket.create_connection(url, config["timeout"], sslopt={"cert_reqs": ssl.CERT_NONE})

        self._read_response()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.debug("Connection closed.")

    def control(self, key):
        """Send a control command."""
        if not self.connection:
            raise exceptions.ConnectionClosed()

        payload = json.dumps({
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        })

        logging.info("Sending control command: %s", key)
        self.connection.send(payload)
        time.sleep(self._key_interval)

    _key_interval = 0.2

    def _read_response(self):
        response = self.connection.recv()
        response = json.loads(response)

        if 'data' in response and 'token' in response["data"]:
            with open(self.token_file, "w") as token_file:
                token_file.write(response['data']["token"])

        if response["event"] != "ms.channel.connect":
            self.close()
            raise exceptions.UnhandledResponse(response)

        logging.debug("Access granted.")

    @staticmethod
    def _serialize_string(string):
        if isinstance(string, str):
            string = str.encode(string)

        return base64.b64encode(string).decode("utf-8")

    def get_installed_apps(self):
        """Send a control command."""
        if not self.connection:
            raise exceptions.ConnectionClosed()

        payload = json.dumps({
            "method": "ms.channel.emit",
            "params": {
                "data": "",
                "event": "ed.installedApp.get",
                # "event": "ed.edenApp.get",
                "to": "host"
            }
        })

        logging.info("Asking for installed apps.")
        self.connection.send(payload)
        data = json.loads(self.connection.recv())
        installed_apps = []
        for app in data['data']['data']:
            installed_apps.append([app['name'], app['appId']])
        return installed_apps
