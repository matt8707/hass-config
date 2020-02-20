import sys
import json
import logging

import aiohttp
import xmltodict

from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import *

_LOGGER = logging.getLogger(__name__)


class HPPrinterAPI:
    def __init__(self, hass, host, port=80, is_ssl=False, data_type=None, reader=None):
        self._hass = hass
        self._host = host
        self._port = port
        self._protocol = "https" if is_ssl else "http"
        self._data_type = data_type
        self._data = None
        self._reader = reader
        self._session = None

        self._url = f'{self._protocol}://{self._host}:{self._port}/DevMgmt/{self._data_type}.xml'

        self.initialize()

    @property
    def data(self):
        return self._data

    def initialize(self):
        try:
            self._session = async_create_clientsession(hass=self._hass)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f"Failed to initialize BlueIris API, error: {ex}, line: {line_number}")

    async def get_data(self, store=None):
        try:
            self._data = None

            _LOGGER.debug(f"Updating {self._data_type} from {self._host}")

            if self._reader is None:
                printer_data = await self.async_get(store)
            else:
                printer_data = self._reader(self._data_type)

            result = {}

            if printer_data is not None:
                for root_key in printer_data:
                    root_item = printer_data[root_key]

                    item = self.extract_data(root_item, root_key)

                    if item is not None:
                        result[root_key] = item

                self._data = result

                if store is not None:
                    json_data = json.dumps(self._data)

                    store(f"{self._data_type}.json", json_data)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to update data ({self._data_type}) and parse it, Error: {ex}, Line: {line_number}')

        return self._data

    async def async_get(self, store=None):
        result = None

        try:
            _LOGGER.debug(f"Retrieving {self._data_type} from {self._host}")

            async with self._session.get(self._url, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()

                content = await response.text()

                if store is not None:
                    store(f"{self._data_type}.xml", content)

                for ns in NAMESPACES_TO_REMOVE:
                    content = content.replace(f'{ns}:', '')

                json_data = xmltodict.parse(content)

                result = json_data

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.info(f'Cannot retrieve data ({self._data_type}) from printer, Error: {ex}, Line: {line_number}')

        return result

    def extract_data(self, data_item, data_item_key):
        try:
            ignore = data_item_key in IGNORE_ITEMS
            is_default_array = data_item_key in ARRAY_AS_DEFAULT

            if ignore:
                return None

            elif isinstance(data_item, dict):
                return self.extract_ordered_dictionary(data_item, data_item_key)

            elif isinstance(data_item, list) and not is_default_array:
                return self.extract_array(data_item, data_item_key)

            else:
                return data_item
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to extract {data_item_key} of {data_item}, Error: {ex}, Line: {line_number}')

    def extract_ordered_dictionary(self, data_item, item_key):
        try:
            result = {}

            for data_item_key in data_item:
                next_item = data_item[data_item_key]

                item = self.extract_data(next_item, data_item_key)

                if item is not None:
                    result[data_item_key] = item

            return result
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(f'Failed to extract from dictionary {item_key} of {data_item}, {error_details}')

    def extract_array(self, data_item, item_key):
        try:
            result = {}
            keys = ARRAY_KEYS.get(item_key, [])
            index = 0

            for current_item in data_item:
                next_item_key = item_key
                item = {}
                for key in current_item:
                    next_item = current_item[key]

                    item_data = self.extract_data(next_item, key)

                    if item_data is not None:
                        item[key] = item_data

                        if key in keys:
                            next_item_key = f'{next_item_key}_{item[key]}'

                if len(keys) == 0:
                    next_item_key = f'{next_item_key}_{index}'

                result[next_item_key] = item

                index += 1

            return result
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to extract from array {item_key} of {data_item}, Error: {ex}, Line: {line_number}')

    @staticmethod
    def clean_parameter(data_item, data_key, default_value="N/A"):
        result = data_item.get(data_key, {})

        if not isinstance(result, str):
            result = result.get("#text", 0)

        if not isinstance(result, str):
            result = default_value

        return result


class ConsumableConfigDynPrinterDataAPI(HPPrinterAPI):
    def __init__(self, hass, host, port=80, is_ssl=False, reader=None):
        data_type = "ConsumableConfigDyn"

        super().__init__(hass, host, port, is_ssl, data_type, reader)


class ProductUsageDynPrinterDataAPI(HPPrinterAPI):
    def __init__(self, hass, host, port=80, is_ssl=False, reader=None):
        data_type = "ProductUsageDyn"

        super().__init__(hass, host, port, is_ssl, data_type, reader)


class ProductStatusDynDataAPI(HPPrinterAPI):
    def __init__(self, hass, host, port=80, is_ssl=False, reader=None):
        data_type = "ProductStatusDyn"

        super().__init__(hass, host, port, is_ssl, data_type, reader)


class ProductConfigDynDataAPI(HPPrinterAPI):
    def __init__(self, hass, host, port=80, is_ssl=False, reader=None):
        data_type = "ProductConfigDyn"

        super().__init__(hass, host, port, is_ssl, data_type, reader)
