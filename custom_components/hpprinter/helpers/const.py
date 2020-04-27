from homeassistant.components.binary_sensor import DOMAIN as DOMAIN_BINARY_SENSOR
from homeassistant.components.sensor import DOMAIN as DOMAIN_SENSOR

MANUFACTURER = "HP"
DEFAULT_NAME = "HP Printer"
DOMAIN = "hpprinter"
DATA_HP_PRINTER = f"data_{DOMAIN}"
SIGNAL_UPDATE_HP_PRINTER = f"updates_{DOMAIN}"
NOTIFICATION_ID = f"{DOMAIN}_notification"
NOTIFICATION_TITLE = f"{DEFAULT_NAME} Setup"

SENSOR_ENTITY_ID = "sensor.{}_{}"
BINARY_SENSOR_ENTITY_ID = "binary_sensor.{}_{}"

NAMESPACES_TO_REMOVE = [
    "ccdyn",
    "ad",
    "dd",
    "dd2",
    "pudyn",
    "psdyn",
    "xsd",
    "pscat",
    "locid",
    "prdcfgdyn2",
    "prdcfgdyn",
]

CONF_STORE_DATA = "store_data"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_LOG_LEVEL = "log_level"

ENTITY_ICON = "icon"
ENTITY_STATE = "state"
ENTITY_ATTRIBUTES = "attributes"
ENTITY_NAME = "name"
ENTITY_MODEL = "model"
ENTITY_MODEL_FAMILY = "model-family"
ENTITY_DEVICE_NAME = "device-name"
ENTITY_UNIQUE_ID = "unique-id"

ENTITY_STATUS = "entity-status"
ENTITY_STATUS_EMPTY = None
ENTITY_STATUS_READY = f"{ENTITY_STATUS}-ready"
ENTITY_STATUS_CREATED = f"{ENTITY_STATUS}-created"
ENTITY_STATUS_MODIFIED = f"{ENTITY_STATUS}-modified"
ENTITY_STATUS_IGNORE = f"{ENTITY_STATUS}-ignore"
ENTITY_STATUS_CANCELLED = f"{ENTITY_STATUS}-cancelled"

PRINTER_CURRENT_STATUS = "status"
PRINTER_SENSOR = "Printer"

INK_ICON = "mdi:cup-water"
PAGES_ICON = "mdi:book-open-page-variant"
SCANNER_ICON = "mdi:scanner"

PROTOCOLS = {True: "https", False: "http"}

IGNORE_ITEMS = [
    "@xsi:schemaLocation",
    "@xmlns:xsd",
    "@xmlns:dd",
    "@xmlns:dd2",
    "@xmlns:ccdyn",
    "@xmlns:xsi",
    "@xmlns:pudyn",
    "@xmlns:ad",
    "@xmlns:psdyn",
    "@xmlns:pscat",
    "@xmlns:locid",
    "@xmlns:locid",
    "@xmlns:prdcfgdyn",
    "@xmlns:prdcfgdyn2",
    "@xmlns:pudyn",
    "PECounter",
]

ARRAY_KEYS = {
    "UsageByMedia": [],
    "SupportedConsumable": ["ConsumableTypeEnum", "ConsumableLabelCode"],
    "SupportedConsumableInfo": ["ConsumableUsageType"],
    "EmailAlertCategories": ["AlertCategory"],
}

ARRAY_AS_DEFAULT = [
    "AlertDetailsUserAction",
    "ConsumableStateAction",
    "AlertCategory",
    "ResourceURI",
    "Language",
    "AutoOnEvent",
    "DaysOfWeek",
]

HP_DEVICE_CONNECTIVITY = "Connectivity"
HP_DEVICE_STATUS = "Status"
HP_DEVICE_PRINTER = "Printer"
HP_DEVICE_SCANNER = "Scanner"
HP_DEVICE_CARTRIDGES = "Cartridges"

HP_DEVICE_PRINTER_STATE = "Total"
HP_DEVICE_SCANNER_STATE = "Total"
HP_DEVICE_CARTRIDGE_STATE = "Remaining"

HP_DEVICE_IS_ONLINE = "IsOnline"

HP_HEAD_TYPE_INK = "ink"
HP_HEAD_TYPE_PRINT_HEAD = "printhead"

HP_INK_MAPPING = {"C": "Cyan", "Y": "Yellow", "M": "Magenta", "K": "Black"}

SIGNAL_UPDATE_BINARY_SENSOR = f"{DEFAULT_NAME}_{DOMAIN_BINARY_SENSOR}_SIGNLE_UPDATE"
SIGNAL_UPDATE_SENSOR = f"{DEFAULT_NAME}_{DOMAIN_SENSOR}_SIGNLE_UPDATE"

SIGNALS = {
    DOMAIN_BINARY_SENSOR: SIGNAL_UPDATE_BINARY_SENSOR,
    DOMAIN_SENSOR: SIGNAL_UPDATE_SENSOR,
}

LOG_LEVEL_DEFAULT = "Default"
LOG_LEVEL_DEBUG = "Debug"
LOG_LEVEL_INFO = "Info"
LOG_LEVEL_WARNING = "Warning"
LOG_LEVEL_ERROR = "Error"

LOG_LEVELS = [
    LOG_LEVEL_DEFAULT,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
]

PRINTER_STATUS = {
    "ready": "On",
    "scanProcessing": "Scanning",
    "copying": "Copying",
    "processing": "Printing",
    "cancelJob": "Cancelling Job",
    "inPowerSave": "Idle",
    "": "Off",
}
