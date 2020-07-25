from custom_components.hpprinter.api.HPPrinterAPI import *

from ..models.config_data import ConfigData
from .storage_manager import StorageManager

_LOGGER = logging.getLogger(__name__)


class HPDeviceData:
    device_data: dict

    def __init__(self, hass, config_manager: ConfigManager):
        self._hass = hass
        self._config_manager = config_manager

        self._storage_manager = StorageManager(self._hass, self._config_manager)

        self._usage_data_manager = ProductUsageDynPrinterDataAPI(
            hass, self._config_manager
        )
        self._consumable_data_manager = ConsumableConfigDynPrinterDataAPI(
            hass, self._config_manager
        )
        self._product_config_manager = ProductConfigDynDataAPI(
            hass, self._config_manager
        )
        self._product_status_manager = ProductStatusDynDataAPI(
            hass, self._config_manager
        )

        self._usage_data = None
        self._consumable_data = None
        self._product_config_data = None
        self._product_status_data = None
        self.device_data = {}

    @property
    def config_data(self) -> ConfigData:
        return self._config_manager.data

    @property
    def name(self):
        return self.config_data.name

    @property
    def host(self):
        return self.config_data.host

    async def initialize(self):
        _LOGGER.debug("Initialize")

        self.device_data = await self._storage_manager.async_load_from_store()

        if self.device_data is None:
            self.device_data = {}

        self.device_data[PRINTER_CURRENT_STATUS] = PRINTER_STATUS[""]
        self.device_data[HP_DEVICE_IS_ONLINE] = False

    async def terminate(self):
        await self._usage_data_manager.terminate()
        await self._consumable_data_manager.terminate()
        await self._product_config_manager.terminate()
        await self._product_status_manager.terminate()

    async def update(self):
        try:
            self.device_data["Name"] = self.config_data.name

            self._usage_data = await self._usage_data_manager.get_data()
            self._consumable_data = await self._consumable_data_manager.get_data()
            self._product_config_data = await self._product_config_manager.get_data()
            self._product_status_data = await self._product_status_manager.get_data()

            data_list = [
                self._usage_data,
                self._consumable_data,
                self._product_config_data,
                self._product_status_data,
            ]

            is_online = True

            for item in data_list:
                if item is None:
                    is_online = False
                    break

            if is_online:
                self.set_usage_data()
                self.set_consumable_data()
                self.set_product_config_data()
                self.set_product_status_data()
            else:
                self.device_data[PRINTER_CURRENT_STATUS] = PRINTER_STATUS[""]

            self.device_data[HP_DEVICE_IS_ONLINE] = is_online

            if is_online:
                await self._storage_manager.async_save_to_store(self.device_data)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(
                f"Failed to update data ({self.name} @{self.host}) and parse it, {error_details}"
            )

    def set_consumable_data(self):
        try:
            if self._consumable_data is not None:
                root = self._consumable_data.get("ConsumableConfigDyn", {})
                consumables_info = root.get("ConsumableInfo", [])

                if "ConsumableLabelCode" in consumables_info:
                    self.set_printer_consumable_data(consumables_info)
                else:
                    for consumable_key in consumables_info:
                        consumable = consumables_info[consumable_key]

                        self.set_printer_consumable_data(consumable)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(
                f"Failed to parse consumable data ({self.name} @{self.host}), {error_details}"
            )

    def set_product_config_data(self):
        try:
            if self._product_config_data is not None:
                root = self._product_config_data.get("ProductConfigDyn", {})
                product_information = root.get("ProductInformation", {})
                self.device_data[ENTITY_MODEL] = product_information.get("MakeAndModel")

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to parse usage data ({self.name} @{self.host}), Error: {ex}, Line: {line_number}"
            )

    def set_product_status_data(self):
        try:
            if self._product_status_data is not None:
                root = self._product_status_data.get("ProductStatusDyn", {})
                status = root.get("Status", [])
                printer_status = ""

                if "StatusCategory" in status:
                    printer_status = self.clean_parameter(status, "StatusCategory")
                else:
                    for item in status:
                        status_item = status[item]
                        if "LocString" not in status_item:
                            printer_status = self.clean_parameter(
                                status_item, "StatusCategory"
                            )

                self.device_data[PRINTER_CURRENT_STATUS] = PRINTER_STATUS.get(
                    printer_status, printer_status
                )

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to parse usage data ({self.name} @{self.host}), Error: {ex}, Line: {line_number}"
            )

    def set_usage_data(self):
        try:
            if self._usage_data is not None:
                root = self._usage_data.get("ProductUsageDyn", {})
                printer_data = root.get("PrinterSubunit")
                scanner_data = root.get("ScannerEngineSubunit")
                consumables_data = root.get("ConsumableSubunit")

                if printer_data is not None:
                    self.set_printer_usage_data(printer_data)

                if scanner_data is not None:
                    self.set_scanner_usage_data(scanner_data)

                if consumables_data is not None:
                    printer_consumables = consumables_data.get("Consumable")

                    if printer_consumables is not None:
                        if "ConsumableStation" in printer_consumables:
                            self.set_printer_consumable_usage_data(printer_consumables)
                        else:
                            for key in printer_consumables:
                                consumable = printer_consumables.get(key)

                                if consumable is not None:
                                    self.set_printer_consumable_usage_data(consumable)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to parse usage data ({self.name} @{self.host}), Error: {ex}, Line: {line_number}"
            )

    def set_printer_usage_data(self, printer_data):
        try:
            total_printed_pages = self.clean_parameter(
                printer_data, "TotalImpressions", "0"
            )

            color_printed_pages = self.clean_parameter(printer_data, "ColorImpressions")
            monochrome_printed_pages = self.clean_parameter(
                printer_data, "MonochromeImpressions"
            )

            printer_jams = self.clean_parameter(printer_data, "Jams")
            if printer_jams == NOT_AVAILABLE:
                printer_jams = self.clean_parameter(printer_data, "JamEvents", "0")

            cancelled_print_jobs_number = self.clean_parameter(
                printer_data, "TotalFrontPanelCancelPresses"
            )

            self.device_data[HP_DEVICE_PRINTER] = {
                HP_DEVICE_PRINTER_STATE: total_printed_pages,
                "Color": color_printed_pages,
                "Monochrome": monochrome_printed_pages,
                "Jams": printer_jams,
                "Cancelled": cancelled_print_jobs_number,
            }

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to set printer data ({self.name} @{self.host}), Error: {ex}, Line: {line_number}"
            )

    def set_scanner_usage_data(self, scanner_data):
        try:
            scan_images_count = self.clean_parameter(scanner_data, "ScanImages")
            adf_images_count = self.clean_parameter(scanner_data, "AdfImages")
            duplex_sheets_count = self.clean_parameter(scanner_data, "DuplexSheets")
            flatbed_images = self.clean_parameter(scanner_data, "FlatbedImages")
            scanner_jams = self.clean_parameter(scanner_data, "JamEvents", "0")
            scanner_mispick = self.clean_parameter(scanner_data, "MispickEvents", "0")

            if scan_images_count == NOT_AVAILABLE:
                new_scan_images_count = 0

                if adf_images_count != NOT_AVAILABLE and int(adf_images_count) > 0:
                    new_scan_images_count = int(adf_images_count)

                if flatbed_images != NOT_AVAILABLE and int(flatbed_images) > 0:
                    new_scan_images_count = new_scan_images_count + int(flatbed_images)

                scan_images_count = new_scan_images_count

            self.device_data[HP_DEVICE_SCANNER] = {
                HP_DEVICE_SCANNER_STATE: scan_images_count,
                "ADF": adf_images_count,
                "Duplex": duplex_sheets_count,
                "Flatbed": flatbed_images,
                "Jams": scanner_jams,
                "Mispick": scanner_mispick,
            }

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(
                f"Failed to set scanner data ({self.name} @{self.host}), Error: {ex}, Line: {line_number}"
            )

    def set_printer_consumable_usage_data(self, printer_consumable_data):
        try:
            color = self.clean_parameter(printer_consumable_data, "MarkerColor")
            head_type = self.clean_parameter(
                printer_consumable_data, "ConsumableTypeEnum"
            ).capitalize()
            station = self.clean_parameter(printer_consumable_data, "ConsumableStation")

            if NOT_AVAILABLE in head_type.upper() or NOT_AVAILABLE in color:
                _LOGGER.info(f"Skipped setting using data for {head_type} {color}")

                return

            cartridge_key = f"{head_type} {color}"

            should_create_cartridges = False
            should_create_cartridge = False

            cartridges = self.device_data.get(HP_DEVICE_CARTRIDGES)
            if cartridges is None:
                cartridges = {}
                should_create_cartridges = True

            cartridge = cartridges.get(cartridge_key)

            if cartridge is None:
                cartridge = {}
                should_create_cartridge = True

            cartridge["Color"] = color
            cartridge["Type"] = head_type
            cartridge["Station"] = station

            if should_create_cartridge:
                cartridges[cartridge_key] = cartridge

            if should_create_cartridges:
                self.device_data[HP_DEVICE_CARTRIDGES] = cartridges

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(
                f"Failed to set printer consumable usage data ({self.name} @{self.host}), {error_details}"
            )

    def set_printer_consumable_data(self, printer_consumable_data):
        try:
            consumable_label_code = self.clean_parameter(
                printer_consumable_data, "ConsumableLabelCode"
            )
            head_type = self.clean_parameter(
                printer_consumable_data, "ConsumableTypeEnum"
            ).capitalize()
            product_number = self.clean_parameter(
                printer_consumable_data, "ProductNumber"
            )
            serial_number = self.clean_parameter(
                printer_consumable_data, "SerialNumber"
            )
            remaining = self.clean_parameter(
                printer_consumable_data, "ConsumablePercentageLevelRemaining", "0"
            )

            installation = printer_consumable_data.get("Installation", {})
            installation_data = self.clean_parameter(installation, "Date")

            manufacturer = printer_consumable_data.get("Manufacturer", {})
            manufactured_by = self.clean_parameter(manufacturer, "Name").rstrip()
            manufactured_at = self.clean_parameter(manufacturer, "Date")

            warranty = printer_consumable_data.get("Warranty", {})
            expiration_date = self.clean_parameter(warranty, "ExpirationDate")

            if head_type == HP_HEAD_TYPE_PRINT_HEAD:
                color = consumable_label_code
            else:
                color_map = []

                if consumable_label_code == HP_ORGANIC_PHOTO_CONDUCTOR:
                    color = HP_ORGANIC_PHOTO_CONDUCTOR_NAME
                else:
                    for color_letter in consumable_label_code:
                        mapped_color = HP_INK_MAPPING.get(color_letter, color_letter)

                        color_map.append(mapped_color)

                    color = "".join(color_map)

                    if color == consumable_label_code:
                        _LOGGER.warning(
                            f"Head type {head_type} color mapping for {consumable_label_code} not available"
                        )

            if NOT_AVAILABLE in head_type.upper() or NOT_AVAILABLE in color:
                _LOGGER.info(f"Skipped setting {head_type} {color}")

                return

            cartridge_key = f"{head_type} {color}"

            should_create_cartridges = False
            should_create_cartridge = False

            cartridges = self.device_data.get(HP_DEVICE_CARTRIDGES)
            if cartridges is None:
                cartridges = {}
                should_create_cartridges = True

            cartridge = cartridges.get(cartridge_key)

            if cartridge is None:
                cartridge = {}
                should_create_cartridge = True

            if head_type == HP_HEAD_TYPE_PRINT_HEAD:
                cartridge["Color"] = color
                cartridge["Type"] = head_type

            else:
                cartridge["Product Number"] = product_number
                cartridge["Serial Number"] = serial_number
                cartridge["Manufactured By"] = manufactured_by
                cartridge["Manufactured At"] = manufactured_at
                cartridge["Warranty Expiration Date"] = expiration_date

            cartridge["Installed At"] = installation_data
            cartridge[HP_DEVICE_CARTRIDGE_STATE] = remaining

            if should_create_cartridge:
                cartridges[cartridge_key] = cartridge

            if should_create_cartridges:
                self.device_data[HP_DEVICE_CARTRIDGES] = cartridges

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            error_details = f"Error: {str(ex)}, Line: {line_number}"

            _LOGGER.error(
                f"Failed to set printer consumable data ({self.name} @{self.host}), {error_details}"
            )

    @staticmethod
    def clean_parameter(data_item, data_key, default_value=NOT_AVAILABLE):
        if data_item is None:
            result = default_value
        else:
            result = data_item.get(data_key, {})

        if not isinstance(result, str):
            result = result.get("#text", 0)

        if not isinstance(result, str):
            result = default_value

        return result
