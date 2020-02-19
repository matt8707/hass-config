import base64
import logging
import socket
import time

from . import exceptions


class RemoteLegacy():
    """Object for remote control connection."""

    def __init__(self, config):
        if not config["port"]:
            config["port"] = 55000

        """Make a new connection."""
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if config["timeout"]:
            self.connection.settimeout(config["timeout"])

        self.connection.connect((config["host"], config["port"]))

        payload = b"\x64\x00" \
                  + self._serialize_string(config["description"]) \
                  + self._serialize_string(config["id"]) \
                  + self._serialize_string(config["name"])
        packet = b"\x00\x00\x00" + self._serialize_string(payload, True)

        logging.info("Sending handshake.")
        self.connection.send(packet)
        self._read_response(True)

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

        payload = b"\x00\x00\x00" + self._serialize_string(key)
        packet = b"\x00\x00\x00" + self._serialize_string(payload, True)

        logging.info("Sending control command: %s", key)
        self.connection.send(packet)
        self._read_response()
        time.sleep(self._key_interval)

    _key_interval = 0.2

    def _read_response(self, first_time=False):
        header = self.connection.recv(3)
        tv_name_len = int.from_bytes(header[1:3],
                                     byteorder="little")
        tv_name = self.connection.recv(tv_name_len)

        if first_time:
            logging.debug("Connected to '%s'.", tv_name.decode())

        response_len = int.from_bytes(self.connection.recv(2),
                                      byteorder="little")
        response = self.connection.recv(response_len)

        if len(response) == 0:
            self.close()
            raise exceptions.ConnectionClosed()

        if response == b"\x64\x00\x01\x00":
            logging.debug("Access granted.")
            return
        elif response == b"\x64\x00\x00\x00":
            raise exceptions.AccessDenied()
        elif response[0:1] == b"\x0a":
            if first_time:
                logging.warning("Waiting for authorization...")
            return self._read_response()
        elif response[0:1] == b"\x65":
            logging.warning("Authorization cancelled.")
            raise exceptions.AccessDenied()
        elif response == b"\x00\x00\x00\x00":
            logging.debug("Control accepted.")
            return

        raise exceptions.UnhandledResponse(response)

    @staticmethod
    def _serialize_string(string, raw=False):
        if isinstance(string, str):
            string = str.encode(string)

        if not raw:
            string = base64.b64encode(string)

        return bytes([len(string)]) + b"\x00" + string
