from asyncio import sleep
import json
import logging
import sys
from typing import Optional

import aiohttp
import xmltodict

from homeassistant.helpers.aiohttp_client import async_create_clientsession

from . import LoginError
from ..helpers.const import *
from ..managers.configuration_manager import ConfigManager
from ..models.config_data import ConfigData

_LOGGER = logging.getLogger(__name__)


class HPPrinterAPI:
    def __init__(self, hass, config_manager: ConfigManager, data_type=None):
        self._config_manager = config_manager

        self._hass = hass
        self._data_type = data_type
        self._data = None
        self._session = None

        self.initialize()

    @property
    def data(self):
        return self._data

    @property
    def config_data(self) -> Optional[ConfigData]:
        if self._config_manager is not None:
            return self._config_manager.data

        return None

    @property
    def url(self):
        config_data = self.config_data

        url = f"{config_data.protocol}://{config_data.host}:{config_data.port}/DevMgmt/{self._data_type}.xml"

        return url

    def initialize(self):
        try:
            self._session = async_create_clientsession(
                hass=self._hass, auto_cleanup=True
            )

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to initialize Printer API, error: {ex}, line: {line_number}"
            )

    async def terminate(self):
        try:
            if self._session is not None and not self._session.closed:
                await self._session.close()

                await sleep(3)

                self._session = None

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to terminate Printer API, error: {ex}, line: {line_number}"
            )

    async def get_data(self):
        try:
            self._data = None

            _LOGGER.debug(f"Updating {self._data_type} from {self.config_data.host}")

            file_reader = self.config_data.file_reader

            if file_reader is None:
                printer_data = await self.async_get()
            else:
                printer_data = file_reader(self._data_type)

            result = {}

            if printer_data is not None:
                for root_key in printer_data:
                    root_item = printer_data[root_key]

                    item = self.extract_data(root_item, root_key)

                    if item is not None:
                        result[root_key] = item

                self._data = result

                json_data = json.dumps(self._data)

                self.save_file("json", json_data)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to update data ({self._data_type}) and parse it, Error: {ex}, Line: {line_number}"
            )

        return self._data

    def save_file(self, extension, content, file_name: Optional[str] = None):
        if self.config_data.should_store:
            if file_name is None:
                file_name = self._data_type

            with open(f"{self.config_data.name}-{file_name}.{extension}", "w") as file:
                file.write(content)

    async def async_get(self, throw_exception: bool = False):
        result = None
        status_code = 400

        try:
            _LOGGER.debug(f"Retrieving {self._data_type} from {self.config_data.host}")

            async with self._session.get(
                self.url, ssl=False, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                status_code = response.status
                response.raise_for_status()

                content = await response.text()

                self.save_file("xml", content)

                for ns in NAMESPACES_TO_REMOVE:
                    content = content.replace(f"{ns}:", "")

                json_data = xmltodict.parse(content)

                result = json_data

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.info(
                f"Cannot retrieve data ({self._data_type}) from printer, Error: {ex}, Line: {line_number}"
            )

        if throw_exception and status_code > 399:
            raise LoginError(status_code)

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

            _LOGGER.error(
                f"Failed to extract {data_item_key} of {data_item}, Error: {ex}, Line: {line_number}"
            )

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

            _LOGGER.error(
                f"Failed to extract from dictionary {item_key} of {data_item}, {error_details}"
            )

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
                            next_item_key = f"{next_item_key}_{item[key]}"

                if len(keys) == 0:
                    next_item_key = f"{next_item_key}_{index}"

                result[next_item_key] = item

                index += 1

            return result
        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to extract from array {item_key} of {data_item}, Error: {ex}, Line: {line_number}"
            )

    @staticmethod
    def clean_parameter(data_item, data_key, default_value="N/A"):
        result = data_item.get(data_key, {})

        if not isinstance(result, str):
            result = result.get("#text", 0)

        if not isinstance(result, str):
            result = default_value

        return result


class ConsumableConfigDynPrinterDataAPI(HPPrinterAPI):
    def __init__(self, hass, config_manager: ConfigManager):
        data_type = "ConsumableConfigDyn"

        super().__init__(hass, config_manager, data_type)


class ProductUsageDynPrinterDataAPI(HPPrinterAPI):
    def __init__(self, hass, config_manager: ConfigManager):
        data_type = "ProductUsageDyn"

        super().__init__(hass, config_manager, data_type)


class ProductStatusDynDataAPI(HPPrinterAPI):
    def __init__(self, hass, config_manager: ConfigManager):
        data_type = "ProductStatusDyn"

        super().__init__(hass, config_manager, data_type)


class ProductConfigDynDataAPI(HPPrinterAPI):
    def __init__(self, hass, config_manager: ConfigManager):
        data_type = "ProductConfigDyn"

        super().__init__(hass, config_manager, data_type)
