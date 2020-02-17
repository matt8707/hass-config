"""Define constants for the Docker Monitor component."""
from datetime import timedelta

DOMAIN = 'docker_monitor'

PLATFORMS = [
    'sensor',
    'switch'
]
EVENT_CONTAINER = 'container_event'

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)

CONF_URL = 'url'
CONF_CONTAINERS = 'containers'
CONF_CONTAINER_SWITCH = 'switch'

CONF_MONITOR_UTILISATION_VERSION = 'version'
CONF_MONITOR_UTILISATION_CONTAINERS_TOTAL = 'containers_total'
CONF_MONITOR_UTILISATION_CONTAINERS_PAUSED = 'containers_paused'
CONF_MONITOR_UTILISATION_CONTAINERS_RUNNING = 'containers_running'
CONF_MONITOR_UTILISATION_CONTAINERS_STOPPED = 'containers_stopped'
CONF_MONITOR_UTILISATION_IMAGES_TOTAL = 'images_total'

CONF_MONITOR_CONTAINER_STATUS = 'status'
CONF_MONITOR_CONTAINER_UPTIME = 'uptime'
CONF_MONITOR_CONTAINER_IMAGE = 'image'
CONF_MONITOR_CONTAINER_CPU_PERCENTAGE = 'cpu_percentage_usage'
CONF_MONITOR_CONTAINER_MEMORY_USAGE = 'memory_usage'
CONF_MONITOR_CONTAINER_MEMORY_PERCENTAGE = 'memory_percentage_usage'
CONF_MONITOR_CONTAINER_NETWORK_TOTAL_UP = 'network_total_up'
CONF_MONITOR_CONTAINER_NETWORK_TOTAL_DOWN = 'network_total_down'

CONF_MONITOR_UTILISATION_CONDITIONS = {
    CONF_MONITOR_UTILISATION_VERSION:
        ['Version', None, 'mdi:information-outline', None],
    CONF_MONITOR_UTILISATION_CONTAINERS_TOTAL:
        ['Containers Total', None, 'mdi:docker', None],
    CONF_MONITOR_UTILISATION_CONTAINERS_PAUSED:
        ['Containers Paused', None, 'mdi:docker', None],
    CONF_MONITOR_UTILISATION_CONTAINERS_RUNNING:
        ['Containers Running', None, 'mdi:docker', None],
    CONF_MONITOR_UTILISATION_CONTAINERS_STOPPED:
        ['Containers Stopped', None, 'mdi:docker', None],
    CONF_MONITOR_UTILISATION_IMAGES_TOTAL:
        ['Images Total', None, 'mdi:information-outline', None],
}

CONF_MONITOR_CONTAINER_CONDITIONS = {
    CONF_MONITOR_CONTAINER_STATUS:
        ['Status', None, 'mdi:checkbox-marked-circle-outline', None],
    CONF_MONITOR_CONTAINER_UPTIME:
        ['Up Time', '', 'mdi:clock', 'timestamp'],
    CONF_MONITOR_CONTAINER_IMAGE:
        ['Image', None, 'mdi:information-outline', None],
    CONF_MONITOR_CONTAINER_CPU_PERCENTAGE:
        ['CPU use', '%', 'mdi:chip', None],
    CONF_MONITOR_CONTAINER_MEMORY_USAGE:
        ['Memory use', 'MB', 'mdi:memory', None],
    CONF_MONITOR_CONTAINER_MEMORY_PERCENTAGE:
        ['Memory use (percent)', '%', 'mdi:memory', None],
    CONF_MONITOR_CONTAINER_NETWORK_TOTAL_UP:
        ['Network total Up', 'MB', 'mdi:upload', None],
    CONF_MONITOR_CONTAINER_NETWORK_TOTAL_DOWN:
        ['Network total Down', 'MB', 'mdi:download', None],
}

ATTR_CREATED = 'Created'
ATTR_IMAGE = 'Image'
ATTR_MEMORY_LIMIT = 'Memory_limit'
ATTR_ONLINE_CPUS = 'Online_CPUs'
ATTR_STARTED_AT = 'Started_at'
ATTR_VERSION_API = 'Api_version'
ATTR_VERSION_ARCH = 'Architecture'
ATTR_VERSION_OS = 'Os'

CONF_ATTRIBUTION = 'Data provided by Docker'

VERSION_INFO = 'info'
VERSION_INFO_VERSION = 'version'
VERSION_INFO_API_VERSION = 'api_version'
VERSION_INFO_OS = 'os'
VERSION_INFO_ARCHITECTURE = 'arch'
VERSION_INFO_KERNEL = 'kernel'
VERSION_INFO_CONTAINERS_TOTAL = 'containers_total'
VERSION_INFO_CONTAINERS_PAUSED = 'containers_paused'
VERSION_INFO_CONTAINERS_RUNNING = 'containers_running'
VERSION_INFO_CONTAINERS_STOPPED = 'containers_stopped'
VERSION_INFO_IMAGES = 'images_total'
VERSION_INFO_MEMTOTAL = 'memory_total'

CONTAINER_INFO = 'info'
CONTAINER_INFO_ID = 'id'
CONTAINER_INFO_IMAGE = 'image'
CONTAINER_INFO_STATUS = 'status'
CONTAINER_INFO_CREATED = 'created'
CONTAINER_INFO_STARTED = 'started'
CONTAINER_INFO_NETWORKMODE = 'networkmode'

EVENT_INFO_CONTAINER = 'Container'
EVENT_INFO_IMAGE = 'Image'
EVENT_INFO_STATUS = 'Status'
EVENT_INFO_ID = 'Id'

ICON_SWITCH = 'mdi:docker'

PRECISION = 2
