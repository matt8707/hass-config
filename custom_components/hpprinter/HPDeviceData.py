from .HPPrinterAPI import *

_LOGGER = logging.getLogger(__name__)


class HPDeviceData:
    def __init__(self, hass, host, name, reader=None):
        self._usage_data_manager = ProductUsageDynPrinterDataAPI(hass, host, reader=reader)
        self._consumable_data_manager = ConsumableConfigDynPrinterDataAPI(hass, host, reader=reader)
        self._product_config_manager = ProductConfigDynDataAPI(hass, host, reader=reader)

        self._hass = hass
        self._name = name
        self._host = host

        self._usage_data = None
        self._consumable_data = None
        self._product_config_data = None

        self._device_data = {
            "Name": name,
            HP_DEVICE_IS_ONLINE: False
        }

    def update(self):
        data = self.get_data()

        return data

    async def get_data(self, store=None):
        try:
            self._usage_data = await self._usage_data_manager.get_data(store)
            self._consumable_data = await self._consumable_data_manager.get_data(store)
            self._product_config_data = await self._product_config_manager.get_data(store)

            data_list = [self._usage_data, self._consumable_data, self._product_config_data]
            is_online = True

            for item in data_list:
                if item is None:
                    is_online = False
                    break

            if is_online:
                self.set_usage_data()
                self.set_consumable_data()
                self.set_product_config_data()

            self._device_data[HP_DEVICE_IS_ONLINE] = is_online

            if store is not None:
                json_data = json.dumps(self._device_data)

                store("final.json", json_data)

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(f'Failed to update data ({self._name} @{self._host}) and parse it, {error_details}')

        return self._device_data

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

            _LOGGER.error(f'Failed to parse consumable data ({self._name} @{self._host}), {error_details}')

    def set_product_config_data(self):
        try:
            if self._product_config_data is not None:
                root = self._product_config_data.get("ProductConfigDyn", {})
                product_information = root.get("ProductInformation", {})
                self._device_data[ENTITY_MODEL] = product_information.get("MakeAndModel")

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to parse usage data ({self._name} @{self._host}), Error: {ex}, Line: {line_number}')

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

            _LOGGER.error(f'Failed to parse usage data ({self._name} @{self._host}), Error: {ex}, Line: {line_number}')

    def set_printer_usage_data(self, printer_data):
        try:
            total_printed_pages = self.clean_parameter(printer_data, "TotalImpressions", "0")

            color_printed_pages = self.clean_parameter(printer_data, "ColorImpressions")
            monochrome_printed_pages = self.clean_parameter(printer_data, "MonochromeImpressions")

            printer_jams = self.clean_parameter(printer_data, "Jams")
            if printer_jams == "N/A":
                printer_jams = self.clean_parameter(printer_data, "JamEvents", "0")

            cancelled_print_jobs_number = self.clean_parameter(printer_data, "TotalFrontPanelCancelPresses")

            self._device_data[HP_DEVICE_PRINTER] = {
                HP_DEVICE_PRINTER_STATE: total_printed_pages,
                "Color": color_printed_pages,
                "Monochrome": monochrome_printed_pages,
                "Jams": printer_jams,
                "Cancelled": cancelled_print_jobs_number,
            }

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            _LOGGER.error(f'Failed to set printer data ({self._name} @{self._host}), Error: {ex}, Line: {line_number}')

    def set_scanner_usage_data(self, scanner_data):
        try:
            scan_images_count = self.clean_parameter(scanner_data, "ScanImages")
            adf_images_count = self.clean_parameter(scanner_data, "AdfImages")
            duplex_sheets_count = self.clean_parameter(scanner_data, "DuplexSheets")
            flatbed_images = self.clean_parameter(scanner_data, "FlatbedImages")
            scanner_jams = self.clean_parameter(scanner_data, "JamEvents", "0")
            scanner_mispick = self.clean_parameter(scanner_data, "MispickEvents", "0")

            if scan_images_count == 'N/A':
                new_scan_images_count = 0

                if adf_images_count != "N/A" and int(adf_images_count) > 0:
                    new_scan_images_count = int(adf_images_count)

                if flatbed_images != "N/A" and int(flatbed_images) > 0:
                    new_scan_images_count = new_scan_images_count + int(flatbed_images)

                scan_images_count = new_scan_images_count

            self._device_data[HP_DEVICE_SCANNER] = {
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

            _LOGGER.error(f'Failed to set scanner data ({self._name} @{self._host}), Error: {ex}, Line: {line_number}')

    def set_printer_consumable_usage_data(self, printer_consumable_data):
        try:
            color = self.clean_parameter(printer_consumable_data, "MarkerColor")
            head_type = self.clean_parameter(printer_consumable_data, "ConsumableTypeEnum").capitalize()
            station = self.clean_parameter(printer_consumable_data, "ConsumableStation")

            cartridge_key = f"{head_type} {color}"

            should_create_cartridges = False
            should_create_cartridge = False

            cartridges = self._device_data.get(HP_DEVICE_CARTRIDGES)
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
                self._device_data[HP_DEVICE_CARTRIDGES] = cartridges

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno
            error_details = f"Error: {ex}, Line: {line_number}"

            _LOGGER.error(f'Failed to set printer consumable usage data ({self._name} @{self._host}), {error_details}')

    def set_printer_consumable_data(self, printer_consumable_data):
        try:
            consumable_label_code = self.clean_parameter(printer_consumable_data, "ConsumableLabelCode")
            head_type = self.clean_parameter(printer_consumable_data, "ConsumableTypeEnum").capitalize()
            product_number = self.clean_parameter(printer_consumable_data, "ProductNumber")
            serial_number = self.clean_parameter(printer_consumable_data, "SerialNumber")
            remaining = self.clean_parameter(printer_consumable_data, "ConsumablePercentageLevelRemaining", "0")

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
                color = HP_INK_MAPPING.get(consumable_label_code, consumable_label_code)

                if color == consumable_label_code:
                    _LOGGER.warning(f"Head type {head_type} color mapping for {consumable_label_code} not available")

            cartridge_key = f"{head_type} {color}"

            should_create_cartridges = False
            should_create_cartridge = False

            cartridges = self._device_data.get(HP_DEVICE_CARTRIDGES)
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
                self._device_data[HP_DEVICE_CARTRIDGES] = cartridges

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            line_number = tb.tb_lineno

            error_details = f"Error: {str(ex)}, Line: {line_number}"

            _LOGGER.error(f'Failed to set printer consumable data ({self._name} @{self._host}), {error_details}')

    @staticmethod
    def clean_parameter(data_item, data_key, default_value="N/A"):
        result = data_item.get(data_key, {})

        if not isinstance(result, str):
            result = result.get("#text", 0)

        if not isinstance(result, str):
            result = default_value

        return result
