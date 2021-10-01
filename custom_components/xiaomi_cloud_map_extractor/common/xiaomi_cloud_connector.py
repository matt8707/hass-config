import base64
import hashlib
import hmac
import json
import logging
import os
import random
import time
from typing import Optional

import requests

from custom_components.xiaomi_cloud_map_extractor.const import *

_LOGGER = logging.getLogger(__name__)


# noinspection PyBroadException
class XiaomiCloudConnector:

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._agent = self.generate_agent()
        self._device_id = self.generate_device_id()
        self._session = requests.session()
        self._sign = None
        self._ssecurity = None
        self._userId = None
        self._cUserId = None
        self._passToken = None
        self._location = None
        self._code = None
        self._serviceToken = None

    def login_step_1(self):
        url = "https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true"
        headers = {
            "User-Agent": self._agent,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        cookies = {
            "userId": self._username
        }
        try:
            response = self._session.get(url, headers=headers, cookies=cookies, timeout=10)
        except:
            response = None
        successful = response is not None and response.status_code == 200 and "_sign" in self.to_json(response.text)
        if successful:
            self._sign = self.to_json(response.text)["_sign"]
        return successful

    def login_step_2(self):
        url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
        headers = {
            "User-Agent": self._agent,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        fields = {
            "sid": "xiaomiio",
            "hash": hashlib.md5(str.encode(self._password)).hexdigest().upper(),
            "callback": "https://sts.api.io.mi.com/sts",
            "qs": "%3Fsid%3Dxiaomiio%26_json%3Dtrue",
            "user": self._username,
            "_sign": self._sign,
            "_json": "true"
        }
        try:
            response = self._session.post(url, headers=headers, params=fields, timeout=10)
        except:
            response = None
        successful = response is not None and response.status_code == 200
        if successful:
            json_resp = self.to_json(response.text)
            successful = "ssecurity" in json_resp and len(str(json_resp["ssecurity"])) > 4
            if successful:
                self._ssecurity = json_resp["ssecurity"]
                self._userId = json_resp["userId"]
                self._cUserId = json_resp["cUserId"]
                self._passToken = json_resp["passToken"]
                self._location = json_resp["location"]
                self._code = json_resp["code"]
            else:
                if "notificationUrl" in json_resp:
                    _LOGGER.error(
                        "Additional authentication required. " +
                        "Open following URL using device that has the same public IP, " +
                        "as your Home Assistant instance: %s ",
                        json_resp["notificationUrl"])
                    successful = None

        return successful

    def login_step_3(self):
        headers = {
            "User-Agent": self._agent,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = self._session.get(self._location, headers=headers, timeout=10)
        except:
            response = None
        successful = response is not None and response.status_code == 200 and "serviceToken" in response.cookies
        if successful:
            self._serviceToken = response.cookies.get("serviceToken")
        return successful

    def login(self):
        self._session.close()
        self._session = requests.session()
        self._agent = self.generate_agent()
        self._device_id = self.generate_device_id()
        self._session.cookies.set("sdkVersion", "accountsdk-18.8.15", domain="mi.com")
        self._session.cookies.set("sdkVersion", "accountsdk-18.8.15", domain="xiaomi.com")
        self._session.cookies.set("deviceId", self._device_id, domain="mi.com")
        self._session.cookies.set("deviceId", self._device_id, domain="xiaomi.com")
        return self.login_step_1() and self.login_step_2() and self.login_step_3()

    def get_raw_map_data(self, map_url) -> Optional[bytes]:
        if map_url is not None:
            try:
                response = self._session.get(map_url, timeout=10)
            except:
                response = None
            if response is not None and response.status_code == 200:
                return response.content
        return None

    def get_device_details(self, token, country):
        countries_to_check = CONF_AVAILABLE_COUNTRIES
        if country is not None:
            countries_to_check = [country]
        for country in countries_to_check:
            devices = self.get_devices(country)
            if devices is None:
                continue
            found = list(filter(lambda d: str(d["token"]).casefold() == str(token).casefold(),
                                devices["result"]["list"]))
            if len(found) > 0:
                user_id = found[0]["uid"]
                device_id = found[0]["did"]
                model = found[0]["model"]
                return country, user_id, device_id, model
        return None, None, None, None

    def get_devices(self, country):
        url = self.get_api_url(country) + "/home/device_list"
        params = {
            "data": '{"getVirtualModel":false,"getHuamiDevices":0}'
        }
        return self.execute_api_call(url, params)

    def execute_api_call(self, url, params):
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": self._agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "x-xiaomi-protocal-flag-cli": "PROTOCAL-HTTP2"
        }
        cookies = {
            "userId": str(self._userId),
            "yetAnotherServiceToken": str(self._serviceToken),
            "serviceToken": str(self._serviceToken),
            "locale": "en_GB",
            "timezone": "GMT+02:00",
            "is_daylight": "1",
            "dst_offset": "3600000",
            "channel": "MI_APP_STORE"
        }
        millis = round(time.time() * 1000)
        nonce = self.generate_nonce(millis)
        signed_nonce = self.signed_nonce(nonce)
        signature = self.generate_signature(url.replace("/app", ""), signed_nonce, nonce, params)
        fields = {
            "signature": signature,
            "_nonce": nonce,
            "data": params["data"]
        }
        try:
            response = self._session.post(url, headers=headers, cookies=cookies, params=fields, timeout=10)
        except:
            response = None
        if response is not None and response.status_code == 200:
            return response.json()
        return None

    def get_api_url(self, country):
        return "https://" + ("" if country == "cn" else (country + ".")) + "api.io.mi.com/app"

    def signed_nonce(self, nonce):
        hash_object = hashlib.sha256(base64.b64decode(self._ssecurity) + base64.b64decode(nonce))
        return base64.b64encode(hash_object.digest()).decode('utf-8')

    @staticmethod
    def generate_nonce(millis):
        nonce_bytes = os.urandom(8) + (int(millis / 60000)).to_bytes(4, byteorder='big')
        return base64.b64encode(nonce_bytes).decode()

    @staticmethod
    def generate_agent():
        agent_id = "".join(map(lambda i: chr(i), [random.randint(65, 69) for _ in range(13)]))
        return f"Android-7.1.1-1.0.0-ONEPLUS A3010-136-{agent_id} APP/xiaomi.smarthome APPV/62830"

    @staticmethod
    def generate_device_id():
        return "".join(map(lambda i: chr(i), [random.randint(97, 122) for _ in range(6)]))

    @staticmethod
    def generate_signature(url, signed_nonce, nonce, params):
        signature_params = [url.split("com")[1], signed_nonce, nonce]
        for k, v in params.items():
            signature_params.append(f"{k}={v}")
        signature_string = "&".join(signature_params)
        signature = hmac.new(base64.b64decode(signed_nonce), msg=signature_string.encode(), digestmod=hashlib.sha256)
        return base64.b64encode(signature.digest()).decode()

    @staticmethod
    def to_json(response_text):
        return json.loads(response_text.replace("&&&START&&&", ""))
