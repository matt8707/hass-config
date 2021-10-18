"""
Platform that supports scanning iCloud.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.icloud/


Special Note: I want to thank Walt Howd, (iCloud2 fame) who inspired me to
    tackle this project. I also want to give a shout out to Kovács Bálint,
    Budapest, Hungary who wrote the Python WazeRouteCalculator and some
    awesome HA guys (Petro31, scop, tsvi, troykellt, balloob, Myrddyn1,
    mountainsandcode,  diraimondo, fabaff, squirtbrnr, and mhhbob) who
    gave me the idea of using Waze in iCloud3.
                ...Gary Cobb aka GeeksterGary, Vero Beach, Florida, USA

Thanks to all
"""

#pylint: disable=bad-whitespace, bad-indentation
#pylint: disable=bad-continuation, import-error, invalid-name, bare-except
#pylint: disable=too-many-arguments, too-many-statements, too-many-branches
#pylint: disable=too-many-locals, too-many-return-statements
#pylint: disable=unused-argument, unused-variable
#pylint: disable=too-many-instance-attributes, too-many-lines

VERSION = '2.4.6'

'''
v2.4.6 (10/11/2021)
1. Changed the icon for zones from mdi:cellphone-iphone to mdi:cellphone because of Home Assistant mdi update.
2. Changed the sensor state values for Travel Time, Distance, Next Update Time, etc. from an empty field to a value to address a Lovelace display change. The fields that were empty were not alligned with the field next to them. Travel Time will now display 0 min when in a zone. Other fields will display '___' when empty.

v2.4.5 (10/5/2021)
1. Fixed a problem where the Waze Route Calculator was being disabled and the distance method-calc was being used. I think the problem started when the WazeRouteCalculator module in the Home Assistant standard Python library was updated.

v2.4.4 (9/25/2021)
1. Coordindated update with pyicloud_ic3.py to support Apple iCloud url changes to access iCloud+ for location & device info for Find-my-Friends tracking method.

v2.4.3a (9/2/2021)
1. An undefined variable 'invalid_code_text' was displayed after entering an invalid iCloud account verification code or taking to long to enter it. This has been corrected.

V2.4.3 (7/30/2001)
1. Added sensor '[devicename]_travel_time_min' -- This is the unformatted waze travel time in minutes. It can be included or excluded using the 'mtim' code.

v2.4.2 (4/20/2021)
1. Added AU to the list of valid Waze regions.

v2.4.1 (4/19/2021)
1. Fixed a bug where the create_sensor was not creating any sensors and the exclude_sensor was not excluding the specified sensors.
2. Fixed coding spelling error bugs related to iCloud 2fa reauthorization requests and determining if a beta version of the the Event Log needed updated when iCloud3 was starting.
'''

#Symbols = •▶¦▶ ●►◄ ▬ ▲▼◀▶ oPhone=►▶►

import logging
import os
import sys
import shutil
import time
import datetime
import json
import voluptuous as vol
from collections import OrderedDict
from re import match

import homeassistant.util.yaml.loader as yaml_loader

from   homeassistant.const                import CONF_USERNAME, CONF_PASSWORD
from   homeassistant.helpers.event        import track_utc_time_change
import homeassistant.helpers.config_validation as cv
from   homeassistant.util                 import slugify
import homeassistant.util.dt              as dt_util
from   homeassistant.util.location        import distance
from   homeassistant.components.device_tracker import (
                PLATFORM_SCHEMA, DOMAIN, ATTR_ATTRIBUTES)
#from   homeassistant.components.device_tracker import DeviceScanner

_LOGGER = logging.getLogger(__name__)

#Changes in device_tracker entities are not supported in HA v0.94 and
#legacy code is being used for the DeviceScanner. Try to import from the
#.legacy directory and retry from the normal directory if the .legacy
#directory does not exist.
#try:
#    from homeassistant.components.device_tracker.legacy import DeviceScanner
#    HA_DEVICE_TRACKER_LEGACY_MODE = True
#except ImportError:
#    from homeassistant.components.device_tracker import DeviceScanner

HA_DEVICE_TRACKER_LEGACY_MODE = False

#Vailidate that Waze is available and can be used
try:
    from .waze_route_calc_ic3 import WazeRouteCalculator, WRCError
    WAZE_IMPORT_SUCCESSFUL = True
except ImportError:
    WAZE_IMPORT_SUCCESSFUL = False
    pass

try:
    from .pyicloud_ic3 import PyiCloudService
    from .pyicloud_ic3 import (
            PyiCloudFailedLoginException,
            PyiCloudNoDevicesException,
            PyiCloudServiceNotActivatedException,
            PyiCloudAPIResponseException,
            PyiCloud2SARequiredException,
            )
    PYICLOUD_IC3_IMPORT_SUCCESSFUL = True
except ImportError:
    PYICLOUD_IC3_IMPORT_SUCCESSFUL = False
    pass

DEBUG_TRACE_CONTROL_FLAG = False

HA_ENTITY_REGISTRY_FILE_NAME    ='/config/.storage/core.entity_registry'
ENTITY_REGISTRY_FILE_KEY        = 'core.entity_registry'
DEFAULT_CONFIG_IC3_FILE_NAME    = '/config/config_ic3.yaml'
STORAGE_KEY_ICLOUD              = 'icloud'
STORAGE_KEY_ENTITY_REGISTRY     = 'core.entity_registry'
STORAGE_VERSION                 = 1
STORAGE_DIR                     = ".storage"

CONF_ACCOUNT_NAME               = 'account_name'
CONF_GROUP                      = 'group'
CONF_NAME                       = 'name'
CONF_TRACKING_METHOD            = 'tracking_method'
CONF_IOSAPP_REQUEST_LOC_MAX_CNT = 'iosapp_request_loc_max_cnt'
CONF_TRACK_DEVICES              = 'track_devices'
CONF_DEVICES                    = 'devices'
CONF_UNIT_OF_MEASUREMENT        = 'unit_of_measurement'
CONF_TIME_FORMAT                = 'time_format'
CONF_INTERVAL                   = 'interval'
CONF_BASE_ZONE                  = 'base_zone'
CONF_INZONE_INTERVAL            = 'inzone_interval'
CONF_INZONE_INTERVALS           = 'inzone_intervals'
CONF_DISPLAY_ZONE_FORMAT        = 'display_zone_format'
CONF_CENTER_IN_ZONE             = 'center_in_zone'
CONF_STATIONARY_STILL_TIME      = 'stationary_still_time'
CONF_STATIONARY_INZONE_INTERVAL = 'stationary_inzone_interval'
CONF_STATIONARY_ZONE_OFFSET     = 'stationary_zone_offset'
CONF_MAX_INTERVAL               = 'max_interval'
CONF_TRAVEL_TIME_FACTOR         = 'travel_time_factor'
CONF_GPS_ACCURACY_THRESHOLD     = 'gps_accuracy_threshold'
CONF_OLD_LOCATION_THRESHOLD     = 'old_location_threshold'
CONF_IGNORE_GPS_ACC_INZONE      = 'ignore_gps_accuracy_inzone'
CONF_HIDE_GPS_COORDINATES       = 'hide_gps_coordinates'
CONF_WAZE_REGION                = 'waze_region'
CONF_WAZE_MAX_DISTANCE          = 'waze_max_distance'
CONF_WAZE_MIN_DISTANCE          = 'waze_min_distance'
CONF_WAZE_REALTIME              = 'waze_realtime'
CONF_DISTANCE_METHOD            = 'distance_method'
CONF_COMMAND                    = 'command'
CONF_CREATE_SENSORS             = 'create_sensors'
CONF_EXCLUDE_SENSORS            = 'exclude_sensors'
CONF_ENTITY_REGISTRY_FILE       = 'entity_registry_file_name'
CONF_LOG_LEVEL                  = 'log_level'
CONF_CONFIG_IC3_FILE_NAME       = 'config_ic3_file_name'
CONF_LEGACY_MODE                = 'legacy_mode'
CONF_EVENT_LOG_CARD_DIRECTORY   = 'event_log_card_directory'
CONF_EVENT_LOG_CARD_FILENAME    = 'event_log_card_filename'
CONF_DISPLAY_TEXT_AS            = 'display_text_as'
CONF_TEST_PARAMETER             = 'test_parameter'
CONF_ZONE                       = 'zone'

#devices_schema parameters
CONF_DEVICENAME                 = 'device_name'
CONF_TRACK_FROM_ZONE            = 'track_from_zone'
CONF_IOSAPP_SUFFIX              = 'iosapp_suffix'
CONF_IOSAPP_ENTITY              = 'iosapp_entity'
CONF_NOIOSAPP                   = 'noiosapp'
CONF_NO_IOSAPP                  = 'no_iosapp'
CONF_IOSAPP_INSTALLED           = 'iosapp_installed'
CONF_PICTURE                    = 'picture'
CONF_EMAIL                      = 'email'
CONF_CONFIG                     = 'config'
CONF_SOURCE                     = 'source'
CONF_DEVICE_TYPE                = 'device_type'

# entity attributes (iCloud FmF & FamShr)
ATTR_ICLOUD_TIMESTAMP           = 'timeStamp'
ATTR_ICLOUD_HORIZONTAL_ACCURACY = 'horizontalAccuracy'
ATTR_ICLOUD_VERTICAL_ACCURACY   = 'verticalAccuracy'
ATTR_ICLOUD_BATTERY_STATUS      = 'batteryStatus'
ATTR_ICLOUD_BATTERY_LEVEL       = 'batteryLevel'
ATTR_ICLOUD_DEVICE_CLASS        = 'deviceClass'
ATTR_ICLOUD_DEVICE_STATUS       = 'deviceStatus'
ATTR_ICLOUD_LOW_POWER_MODE      = 'lowPowerMode'

# device data attributes
ATTR_LOCATION                   = 'location'
ATTR_ATTRIBUTES                 = 'attributes'
ATTR_RADIUS                     = 'radius'
ATTR_FRIENDLY_NAME              = 'friendly_name'
ATTR_NAME                       = 'name'
ATTR_DEVICE_CLASS               = 'device_class'

# entity attributes
ATTR_ZONE                       = 'zone'
ATTR_ZONE_TIMESTAMP             = 'zone_timestamp'
ATTR_LAST_ZONE                  = 'last_zone'
ATTR_GROUP                      = 'group'
ATTR_TIMESTAMP                  = 'timestamp'
ATTR_TIMESTAMP_SECS             = 'timestamp_secs'
ATTR_TIMESTAMP_TIME             = 'timestamp_time'
ATTR_AGE                        = 'age'
ATTR_TRIGGER                    = 'trigger'
ATTR_BATTERY                    = 'battery'
ATTR_BATTERY_LEVEL              = 'battery_level'
ATTR_BATTERY_STATUS             = 'battery_status'
ATTR_INTERVAL                   = 'interval'
ATTR_ZONE_DISTANCE              = 'zone_distance'
ATTR_CALC_DISTANCE              = 'calc_distance'
ATTR_WAZE_DISTANCE              = 'waze_distance'
ATTR_WAZE_TIME                  = 'travel_time'
ATTR_WAZE_TIME_MIN              = 'travel_time_min'
ATTR_DIR_OF_TRAVEL              = 'dir_of_travel'
ATTR_TRAVEL_DISTANCE            = 'travel_distance'
ATTR_DEVICE_STATUS              = 'device_status'
ATTR_LOW_POWER_MODE             = 'low_power_mode'
ATTR_TRACKING                   = 'tracking'
ATTR_DEVICENAME_IOSAPP          = 'iosapp_device'
ATTR_AUTHENTICATED              = 'authenticated'
ATTR_LAST_UPDATE_TIME           = 'last_update'
ATTR_NEXT_UPDATE_TIME           = 'next_update'
ATTR_LAST_LOCATED               = 'last_located'
ATTR_INFO                       = 'info'
ATTR_GPS_ACCURACY               = 'gps_accuracy'
ATTR_GPS                        = 'gps'
ATTR_LATITUDE                   = 'latitude'
ATTR_LONGITUDE                  = 'longitude'
ATTR_POLL_COUNT                 = 'poll_count'
ATTR_ICLOUD3_VERSION            = 'icloud3_version'
ATTR_VERT_ACCURACY              = 'vertical_accuracy'
ATTR_ALTITUDE                   = 'altitude'
ATTR_BADGE                      = 'badge'
ATTR_EVENT_LOG                  = 'event_log'
ATTR_PICTURE                    = 'entity_picture'

#General constants
HOME                            = 'home'
NOT_HOME                        = 'not_home'
NOT_SET                         = 'not_set'
STATIONARY                      = 'stationary'
AWAY_FROM                       = 'AwayFrom'
AWAY                            = 'Away'
PAUSED                          = 'Paused'
PAUSED_CAPS                     = 'PAUSED'
UNKNOWN                         = 'Unknown'
NEVER                           = 'Never'
ERROR                           = 'Error'
TIMESTAMP_ZERO                  = '0000-00-00 00:00:00'
HHMMSS_ZERO                     = '00:00:00'
HIGH_INTEGER                    = 9999999999
UTC_TIME                        = True
LOCAL_TIME                      = False
NUMERIC                         = True
NEW_LINE                        = '\n'
WAZE                            = 'waze'
CALC                            = 'calc'

IPHONE                          = 'iphone'
IPAD                            = 'ipad'
IPOD                            = 'ipod'
WATCH                           = 'watch'

SENSOR_EVENT_LOG_ENTITY = 'sensor.icloud3_event_log'

DEVICE_ATTRS_BASE = {
         ATTR_LATITUDE: 0,
         ATTR_LONGITUDE: 0,
         ATTR_BATTERY: 0,
         ATTR_BATTERY_LEVEL: 0,
         ATTR_BATTERY_STATUS: '',
         ATTR_GPS_ACCURACY: 0,
         ATTR_VERT_ACCURACY: 0,
         ATTR_TIMESTAMP: TIMESTAMP_ZERO,
         ATTR_ICLOUD_TIMESTAMP: HHMMSS_ZERO,
         ATTR_TRIGGER: '',
         ATTR_DEVICE_STATUS: UNKNOWN,
         ATTR_LOW_POWER_MODE: '',
         }

INITIAL_LOCATION_DATA  = {
        ATTR_NAME: '',
        ATTR_DEVICE_CLASS: 'iPhone',
        ATTR_BATTERY_LEVEL: 0,
        ATTR_BATTERY_STATUS: UNKNOWN,
        ATTR_DEVICE_STATUS: UNKNOWN,
        ATTR_LOW_POWER_MODE: False,
        ATTR_TIMESTAMP_SECS: 0,
        ATTR_TIMESTAMP_TIME: HHMMSS_ZERO,
        ATTR_AGE: HIGH_INTEGER,
        ATTR_LATITUDE: 0.0,
        ATTR_LONGITUDE: 0.0,
        ATTR_ALTITUDE: 0.0,
        ATTR_GPS_ACCURACY: 0,
        ATTR_VERT_ACCURACY: 0,
        }
        #ATTR_ISOLD: False,

TRACE_ATTRS_BASE = {
        ATTR_NAME: '',
        ATTR_ZONE: '',
        ATTR_LAST_ZONE: '',
        ATTR_ZONE_TIMESTAMP: '',
        ATTR_LATITUDE: 0,
        ATTR_LONGITUDE: 0,
        ATTR_TRIGGER: '',
        ATTR_TIMESTAMP: TIMESTAMP_ZERO,
        ATTR_ZONE_DISTANCE: 0,
        ATTR_INTERVAL: 0,
        ATTR_DIR_OF_TRAVEL: '',
        ATTR_TRAVEL_DISTANCE: 0,
        ATTR_WAZE_DISTANCE: ' ',
        ATTR_CALC_DISTANCE: 0,
        ATTR_LAST_LOCATED: '',
        ATTR_LAST_UPDATE_TIME: '',
        ATTR_NEXT_UPDATE_TIME: '',
        ATTR_POLL_COUNT: '',
        ATTR_INFO: '',
        ATTR_BATTERY: 0,
        ATTR_BATTERY_LEVEL: 0,
        ATTR_GPS: 0,
        ATTR_GPS_ACCURACY: 0,
        ATTR_VERT_ACCURACY: 0,
        }

TRACE_ICLOUD_ATTRS_BASE = {
        CONF_NAME: '',
        ATTR_ICLOUD_DEVICE_STATUS: '',
        ATTR_LATITUDE: 0,
        ATTR_LONGITUDE: 0,
        ATTR_ICLOUD_TIMESTAMP: 0,
        ATTR_ICLOUD_HORIZONTAL_ACCURACY: 0,
        ATTR_ICLOUD_VERTICAL_ACCURACY: 0,
        'positionType': 'Wifi',
        }
        #ATTR_ISOLD: False,

SENSOR_DEVICE_ATTRS = [
        'zone',
        'last_zone',
        'base_zone',
        'zone_name',
        'zone_title',
        'zone_fname',
        'last_zone_name',
        'last_zone_title',
        'last_zone_fname',
        'zone_timestamp',
        'zone_distance',
        'calc_distance',
        'waze_distance',
        'travel_time',
        'travel_time_min',
        'dir_of_travel',
        'interval',
        'info',
        'last_located',
        'last_update',
        'next_update',
        'poll_count',
        'travel_distance',
        'trigger',
        'battery',
        'battery_status',
        'gps_accuracy',
        'vertical accuracy',
        'badge',
        'name',
        ]

SENSOR_ATTR_FORMAT = {
        'zone_distance': 'dist',
        'calc_distance': 'dist',
        'waze_distance': 'diststr',
        'travel_distance': 'dist',
        'battery': '%',
        'dir_of_travel': 'title',
        'altitude': 'm-ft',
        'badge': 'badge',
        ATTR_LAST_LOCATED: 'timestamp-time',
        ATTR_LAST_UPDATE_TIME: 'timestamp-time',
        ATTR_NEXT_UPDATE_TIME: 'timestamp-time',
        ATTR_WAZE_TIME: 'min',
        ATTR_WAZE_TIME_MIN: 'min',
        }

#---- iPhone Device Tracker Attribute Templates -----
SENSOR_ATTR_FNAME = {
        'zone': 'Zone',
        'last_zone': 'Last Zone',
        'zone_name': 'Zone Name',
        'zone_title': 'Zone Title',
        'zone_fname': 'Zone Fname',
        'last_zone_name': 'Last Zone Name',
        'last_zone_title': 'Last Zone Title',
        'last_zone_fname': 'Last Zone Fname',
        'zone_timestamp': 'Zone Timestamp',
        'base_zone': 'Base Zone',
        'zone_distance': 'Zone Distance',
        'calc_distance': 'Calc Dist',
        'waze_distance': 'Waze Dist',
        'travel_time': 'Travel Time',
        'travel_time_min': 'Travel Time',
        'dir_of_travel': 'Direction',
        'interval': 'Interval',
        'info': 'Info',
        'last_located': 'Last Located',
        'last_update': 'Last Update',
        'next_update': 'Next Update',
        'poll_count': 'Poll Count',
        'travel_distance': 'Travel Dist',
        'trigger': 'Trigger',
        'battery': 'Battery',
        'battery_status': 'Battery Status',
        'gps_accuracy': 'GPS Accuracy',
        'vertical_accuracy': 'Vertical Accuracy',
        'badge': 'Badge',
        'name': 'Name',
        }
SENSOR_ATTR_ZONE_FNAME = {
        'zone_name': 'Zone Name',
        'zone_title': 'Zone Title',
        'zone_fname': 'Zone Fname',
        'last_zone_name': 'Last Zone Name',
        'last_zone_title': 'Last Zone Title',
        'last_zone_fname': 'Last Zone Fname',
}

SENSOR_ATTR_ICON = {
        'zone': 'mdi:cellphone',
        'last_zone': 'mdi:map-clock-outline',
        'base_zone': 'mdi:map-clock',
        'zone_timestamp': 'mdi:clock-in',
        'zone_distance': 'mdi:map-marker-distance',
        'calc_distance': 'mdi:map-marker-distance',
        'waze_distance': 'mdi:map-marker-distance',
        'travel_time': 'mdi:clock-outline',
        'travel_time_min': 'mdi:clock-outline',
        'dir_of_travel': 'mdi:compass-outline',
        'interval': 'mdi:clock-start',
        'info': 'mdi:information-outline',
        'last_located': 'mdi:history',
        'last_update': 'mdi:history',
        'next_update': 'mdi:update',
        'poll_count': 'mdi:counter',
        'travel_distance': 'mdi:map-marker-distance',
        'trigger': 'mdi:flash-outline',
        'battery': 'mdi:battery-outline',
        'battery_status': 'mdi:battery-outline',
        'gps_accuracy': 'mdi:map-marker-radius',
        'altitude': 'mdi:image-filter-hdr',
        'vertical_accuracy': 'mdi:map-marker-radius',
        'badge': 'mdi:shield-account',
        'name': 'mdi:account',
        'entity_log': 'mdi:format-list-checkbox',
        }

SENSOR_ID_NAME_LIST = {
        'zon': 'zone',
        'lzon': 'last_zone',
        'bzon': 'base_zone',
        'zonn': 'zone_name',
        'zont': 'zone_title',
        'zonfn': 'zone_fname',
        'lzonn': 'last_zone_name',
        'lzont': 'last_zone_title',
        'lzonfn': 'last_zone_fname',
        'zonts': 'zone_timestamp',
        'zdis': 'zone_distance',
        'cdis': 'calc_distance',
        'wdis': 'waze_distance',
        'tdis': 'travel_distance',
        'ttim': 'travel_time',
        'mtim': 'travel_time_min',
        'dir': 'dir_of_travel',
        'intvl':  'interval',
        'lloc': 'last_located',
        'lupdt': 'last_update',
        'nupdt': 'next_update',
        'cnt': 'poll_count',
        'info': 'info',
        'trig': 'trigger',
        'bat': 'battery',
        'batstat': 'battery_status',
        'alt': 'altitude',
        'gpsacc': 'gps_accuracy',
        'vacc': 'vertical_accuracy',
        'badge': 'badge',
        'name': 'name',
        }

ATTR_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
APPLE_DEVICE_TYPES    = [IPHONE, IPAD, IPOD, WATCH, 'iwatch', 'icloud',
                         'iPhone', 'iPad', 'iPod', 'Watch', 'iWatch', 'iCloud']
FMF_FAMSHR_LOCATION_FIELDS = ['altitude', 'latitude', 'longitude', 'timestamp',
                       'horizontalAccuracy', 'verticalAccuracy', ATTR_ICLOUD_BATTERY_STATUS]

#Convert zone/state value to display value
ZONE_TO_DISPLAY_BASE = {
        None: "not_home",
        "not_home": "Away",
        "not_set": "NotSet",
        "away": "Away",
        "stationary": "Stationary",
        "nearzone": "NearZone",
        "near_zone": "NearZone",
        }
#Convert state non-fname value to internal zone/state value
STATE_TO_ZONE_BASE = {
        "NotSet": "not_set",
        "Away": "not_home",
        "away": "not_home",
        "NotHome": "not_home",
        "nothome": "not_home",
        "Stationary": "stationary",
        "stationary": "stationary",
        "NearZone": "nearzone",
        "NearZone": "near_zone",
        }

#icloud_update commands
CMD_ERROR    = 1
CMD_INTERVAL = 2
CMD_PAUSE    = 3
CMD_RESUME   = 4
CMD_WAZE     = 5
CMD_LOCATION = 6

#Other constants
IOSAPP_DT_ENTITY = True
ICLOUD_DT_ENTITY = False
ICLOUD_LOCATION_DATA_ERROR = False

STATIONARY_LAT_90       = 90
STATIONARY_LONG_180     = 180
STAT_ZONE_NEW_LOCATION  = True
STAT_ZONE_MOVE_TO_BASE  = False
STATIONARY_ZONE_1KM_LAT = 0.008983      #Subtract/add from home zone latitude to make stat zone location
STATIONARY_ZONE_1KM_LONG= 0.010094
EVLOG_RECDS_PER_DEVICE  = 2000          #Used to calculate the max recds to store
EVENT_LOG_CLEAR_SECS    = 600           #Clear event log data interval
EVENT_LOG_CLEAR_CNT     = 15            #Number of recds to display when clearing event log
ICLOUD3_ERROR_MSG       = "ICLOUD3 ERROR-SEE EVENT LOG"

#Devicename config parameter file extraction
DI_DEVICENAME           = 0
DI_DEVICE_TYPE          = 1
DI_NAME                 = 2
DI_EMAIL                = 3
DI_BADGE_PICTURE        = 4
DI_IOSAPP_ENTITY        = 5
DI_IOSAPP_SUFFIX        = 6
DI_ZONES                = 7

#Waze status codes
WAZE_REGIONS      = ['US', 'NA', 'EU', 'IL', 'AU']
WAZE_USED         = 0
WAZE_NOT_USED     = 1
WAZE_PAUSED       = 2
WAZE_OUT_OF_RANGE = 3
WAZE_NO_DATA      = 4

#Interval range table used for setting the interval based on a retry count
#The key is starting retry count range, the value is the interval (in minutes)
#poor_location_gps cnt, icloud_authentication cnt (default)
POOR_LOC_GPS_CNT       = 1.1
AUTH_ERROR_CNT         = 1.2
RETRY_INTERVAL_RANGE_1 = {0:.25, 4:1, 8:5,  12:30, 16:60, 20:120, 22:240, 24:-240}
#request iosapp location retry cnt
IOSAPP_REQUEST_LOC_CNT = 2.1
RETRY_INTERVAL_RANGE_2 = {0:.5,  4:2, 8:30, 12:60, 14:120, 16:180, 18:240, 20:-240}

#Used by the 'update_method' in the polling_5_sec loop
IOSAPP_UPDATE     = "IOSAPP"
ICLOUD_UPDATE     = "ICLOUD"

#The event_log lovelace card will display the event in a special color if
#the text starts with a special character:
#^1^ - LightSeaGreen
#^2^ - BlueViolet
#^3^ - OrangeRed
#^4^ - DeepPink
#^5^ - MediumVioletRed
#^6^ - --dark-primary-color
EVLOG_NOTICE      = "^2^"
EVLOG_ERROR       = "^3^"
EVLOG_ALERT       = "^4^"
EVLOG_DEBUG       = "^6^"
CRLF_DOT          = 'CRLF• '
CRLF_CHK          = 'CRLF✓ '


#tracking_method config parameter being used
ICLOUD            = 'icloud'    #iCloud Location Services (FmF & FamShr)
FMF               = 'fmf'       #Find My Friends
FAMSHR            = 'famshr'    #Family Sharing
IOSAPP            = 'iosapp'    #HA IOS App v1.5x or v2.x
IOSAPP1           = 'iosapp1'   #HA IOS App v1.5x only
FMF_FAMSHR        = [FMF, FAMSHR, ICLOUD]
IOSAPP_IOSAPP1    = [IOSAPP, IOSAPP1]

#TRK_METHOD_NAME = {
#        FMF: 'Find My Friends',
#        FAMSHR: 'Family Sharing',
#        IOSAPP: 'iOS App',
#        IOSAPP1: 'iOS App v1',
#        }
TRK_METHOD_SHORT_NAME = {
        FMF: 'FmF',
        FAMSHR: 'FamShr',
        IOSAPP: 'iOSApp',
        IOSAPP1: 'iOSApp1',
        }
DEVICE_TYPE_FNAME = {
        IPHONE: 'iPhone',
        'phone': 'iPhone',
        IPAD: 'iPad',
        'iwatch': 'iWatch',
        WATCH: 'Watch',
        IPOD: 'iPod',
        }

#iOS App Triggers defined in \iOS/Shared/Location/LocatioTrigger.swift
BACKGROUND_FETCH          = 'Background Fetch'
BKGND_FETCH               = 'Bkgnd Fetch'
GEOGRAPHIC_REGION_ENTERED = 'Geographic Region Entered'
GEOGRAPHIC_REGION_EXITED  = 'Geographic Region Exited'
IBEACON_REGION_ENTERED    = 'iBeacon Region Entered'
IBEACON_REGION_EXITED     = 'iBeacon Region Exited'
REGION_ENTERED            = 'Region Entered'
REGION_EXITED             = 'Region Exited'
INITIAL                   = 'Initial'
MANUAL                    = 'Manual'
LAUNCH                    = "Launch",
SIGNIFICANT_LOC_CHANGE    = 'Significant Location Change'
SIGNIFICANT_LOC_UPDATE    = 'Significant Location Update'
SIG_LOC_CHANGE            = 'Sig Loc Change'
PUSH_NOTIFICATION         = 'Push Notification'
REQUEST_IOSAPP_LOC        = 'Request iOSApp Loc'
IOSAPP_LOC_CHANGE         = "iOSApp Loc Change"

#Trigger is converted to abbreviation after getting last_update_trigger
IOS_TRIGGER_ABBREVIATIONS = {
        GEOGRAPHIC_REGION_ENTERED: REGION_ENTERED,
        GEOGRAPHIC_REGION_EXITED: REGION_EXITED,
        IBEACON_REGION_ENTERED: REGION_ENTERED,
        IBEACON_REGION_EXITED: REGION_EXITED,
        SIGNIFICANT_LOC_CHANGE: SIG_LOC_CHANGE,
        SIGNIFICANT_LOC_UPDATE: SIG_LOC_CHANGE,
        PUSH_NOTIFICATION: REQUEST_IOSAPP_LOC,
        BACKGROUND_FETCH: BKGND_FETCH,
        }
IOS_TRIGGERS_VERIFY_LOCATION = [
        INITIAL,
        LAUNCH,
        MANUAL,
        IOSAPP_LOC_CHANGE,
        BKGND_FETCH,
        SIG_LOC_CHANGE,
        REQUEST_IOSAPP_LOC,
        ]
IOS_TRIGGERS_ENTER = [
        REGION_ENTERED,
        'Test Entered',
        ]
IOS_TRIGGERS_EXIT = [
        REGION_EXITED,
        'Test Exited'
        ]
IOS_TRIGGERS_ENTER_EXIT = [
        REGION_ENTERED,
        REGION_EXITED,
        ]

#Lists to hold the group names, group objects and iCloud device configuration
#The ICLOUD3_GROUPS is filled in on each platform load, the GROUP_OBJS is
#filled in after the polling timer is setup.
ICLOUD3_GROUPS     = []
ICLOUD3_GROUP_OBJS = {}
ICLOUD3_TRACKED_DEVICES = {}
'''
DEVICE_STATUS_SET = [
        'deviceModel', 'rawDeviceModel', 'deviceStatus',
        'batteryStatus', 'batteryLevel', 'id', 'lowPowerMode',
        'deviceDisplayName', 'name', 'fmlyShare',
        'location',
        'locationCapable', 'locationEnabled', 'isLocating',
        'remoteLock', 'activationLocked', 'lockedTimestamp',
        'lostModeCapable', 'lostModeEnabled', 'locFoundEnabled',
        'lostDevice', 'lostTimestamp',
        'remoteWipe', 'wipeInProgress', 'wipedTimestamp',
        'isMac']
'''
#Default values are ["batteryLevel", "deviceDisplayName", "deviceStatus", "name"]
DEVICE_STATUS_SET = [
        ATTR_ICLOUD_DEVICE_CLASS,
        ATTR_ICLOUD_BATTERY_STATUS,
        ATTR_ICLOUD_LOW_POWER_MODE,
        ATTR_LOCATION
        ]
DEVICE_STATUS_CODES = {
        '200': 'online',
        '201': 'offline',
        '203': 'pending',
        '204': 'unregistered',
        '0': ''
        }
DEVICE_STATUS_ONLINE = ['online', 'pending', 'unknown', 'Unknown', '']

#-----►►Test configuration parameters ----------
VALID_CONF_DEVICES_ITEMS = [CONF_DEVICENAME, CONF_EMAIL, CONF_PICTURE, CONF_NAME, CONF_INZONE_INTERVAL,
                            CONF_TRACK_FROM_ZONE, CONF_IOSAPP_SUFFIX, CONF_IOSAPP_ENTITY,
                            CONF_IOSAPP_INSTALLED, CONF_NOIOSAPP, CONF_NO_IOSAPP]

SERVICE_SCHEMA = vol.Schema({
    vol.Optional(CONF_GROUP):  cv.string,
    vol.Optional(CONF_DEVICENAME): cv.slugify,
    vol.Optional(CONF_INTERVAL): cv.slugify,
    vol.Optional(CONF_COMMAND): cv.string
    })

#Parameters for devices to be tracked
DEVICES_SCHEMA = vol.Schema({
    vol.Optional(CONF_DEVICENAME): cv.string,
    vol.Optional(CONF_EMAIL): cv.string,
    vol.Optional(CONF_DEVICE_TYPE): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_TRACK_FROM_ZONE): cv.string,
    vol.Optional(CONF_PICTURE): cv.string,
    vol.Optional(CONF_IOSAPP_ENTITY): cv.string,
    vol.Optional(CONF_IOSAPP_SUFFIX): cv.string,
    vol.Optional(CONF_INZONE_INTERVAL): cv.string,
    vol.Optional(CONF_NOIOSAPP): cv.boolean,
    vol.Optional(CONF_NO_IOSAPP): cv.boolean,
    vol.Optional(CONF_IOSAPP_INSTALLED): cv.boolean,
    })

#Parameters for devices to be tracked
INZONE_INTERVALS_SCHEMA = vol.Schema({
    vol.Optional(CONF_INZONE_INTERVAL): cv.string,
    vol.Optional(IPHONE): cv.string,
    vol.Optional(IPAD): cv.string,
    vol.Optional(IPOD): cv.string,
    vol.Optional(WATCH): cv.string,
    vol.Optional(CONF_NO_IOSAPP): cv.string,
    })

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=''): cv.string,
    vol.Optional(CONF_GROUP, default=''): cv.string,
    vol.Optional(CONF_TRACKING_METHOD, default=ICLOUD): cv.slugify,
    vol.Optional(CONF_IOSAPP_REQUEST_LOC_MAX_CNT, default=HIGH_INTEGER): cv.string,
    vol.Optional(CONF_ENTITY_REGISTRY_FILE): cv.string,
    vol.Optional(CONF_CONFIG_IC3_FILE_NAME, default=''): cv.string,
    vol.Optional(CONF_EVENT_LOG_CARD_DIRECTORY, default='www/custom_cards'): cv.string,
    vol.Optional(CONF_EVENT_LOG_CARD_FILENAME, default='icloud3-event-log-card.js'): cv.string,
    vol.Optional(CONF_LEGACY_MODE, default=False): cv.boolean,
    vol.Optional(CONF_DISPLAY_TEXT_AS, default=[]): vol.All(cv.ensure_list, [cv.string]),

    #-----►►General Attributes ----------
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default='mi'): cv.slugify,
    vol.Optional(CONF_TIME_FORMAT, default=12): cv.positive_int,
    vol.Optional(CONF_INZONE_INTERVAL, default='2 hrs'): cv.string,
    vol.Optional(CONF_INZONE_INTERVALS, default=[]): vol.All(cv.ensure_list, [INZONE_INTERVALS_SCHEMA]),
    vol.Optional(CONF_DISPLAY_ZONE_FORMAT, default=CONF_NAME): cv.string,
    vol.Optional(CONF_CENTER_IN_ZONE, default=False): cv.boolean,
    vol.Optional(CONF_MAX_INTERVAL, default='4 hrs'): cv.string,
    vol.Optional(CONF_TRAVEL_TIME_FACTOR, default=.60): cv.small_float,
    vol.Optional(CONF_GPS_ACCURACY_THRESHOLD, default=100): cv.positive_int,
    vol.Optional(CONF_OLD_LOCATION_THRESHOLD, default='3 min'): cv.string,
    vol.Optional(CONF_IGNORE_GPS_ACC_INZONE, default=False): cv.boolean,
    vol.Optional(CONF_HIDE_GPS_COORDINATES, default=False): cv.boolean,
    vol.Optional(CONF_LOG_LEVEL, default=''): cv.string,

    #-----►►Filter, Include, Exclude Devices ----------
    vol.Optional(CONF_TRACK_DEVICES, default=[]): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_DEVICES, default=[]): vol.All(cv.ensure_list, [DEVICES_SCHEMA]),

    #-----►►Waze Attributes ----------
    vol.Optional(CONF_DISTANCE_METHOD, default=WAZE): cv.string,
    vol.Optional(CONF_WAZE_REGION, default='US'): cv.string,
    vol.Optional(CONF_WAZE_MAX_DISTANCE, default=1000): cv.positive_int,
    vol.Optional(CONF_WAZE_MIN_DISTANCE, default=1): cv.positive_int,
    vol.Optional(CONF_WAZE_REALTIME, default=False): cv.boolean,

    #-----►►Other Attributes ----------
    vol.Optional(CONF_STATIONARY_INZONE_INTERVAL, default='30 min'): cv.string,
    vol.Optional(CONF_STATIONARY_STILL_TIME, default='8 min'): cv.string,
    vol.Optional(CONF_STATIONARY_ZONE_OFFSET, default='1,0'): cv.string,
    vol.Optional(CONF_CREATE_SENSORS, default=[]): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_EXCLUDE_SENSORS, default=[]): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_COMMAND): cv.string,
})

DEFAULT_CONFIG_VALUES = {
    CONF_UNIT_OF_MEASUREMENT: 'mi',
    CONF_TIME_FORMAT: 12,
    CONF_INZONE_INTERVAL: '2 hrs',
    CONF_INZONE_INTERVALS : [],
    CONF_DISPLAY_ZONE_FORMAT: CONF_NAME,
    CONF_CENTER_IN_ZONE: False,
    CONF_MAX_INTERVAL: '4 hrs',
    CONF_TRAVEL_TIME_FACTOR: .60,
    CONF_GPS_ACCURACY_THRESHOLD: 100,
    CONF_OLD_LOCATION_THRESHOLD: '3 min',
    CONF_IGNORE_GPS_ACC_INZONE: False,
    CONF_HIDE_GPS_COORDINATES: False,
    CONF_TRACK_DEVICES: [],
    CONF_DEVICES: [],
    CONF_DISTANCE_METHOD: WAZE,
    CONF_LEGACY_MODE: False,
    CONF_WAZE_REGION: 'US',
    CONF_WAZE_MAX_DISTANCE: 1000,
    CONF_WAZE_MIN_DISTANCE: 1,
    CONF_WAZE_REALTIME: False,
    CONF_STATIONARY_STILL_TIME: '8 min',
    CONF_STATIONARY_ZONE_OFFSET: '1, 0',
    CONF_STATIONARY_INZONE_INTERVAL: '30 min',

    CONF_LOG_LEVEL: '',
    CONF_EVENT_LOG_CARD_DIRECTORY: 'www/custom_cards',
    CONF_EVENT_LOG_CARD_FILENAME: 'icloud3-event-log-card.js',
    CONF_DISPLAY_TEXT_AS: [],
    }

VALIDATE_PARAMETER_LIST = {
    CONF_UNIT_OF_MEASUREMENT: ['mi', 'km'],
    CONF_TIME_FORMAT: [12, 24],
    CONF_DISPLAY_ZONE_FORMAT: ['zone', 'name', 'fname', 'title'],
    CONF_DISTANCE_METHOD: ['waze', 'calc'],
    CONF_WAZE_REGION: ['US', 'NA', 'EU', 'IS', 'AU', 'us', 'na', 'eu', 'is', 'au'],
    CONF_DISPLAY_ZONE_FORMAT: ['zone', 'name', 'fname', 'title'],
}
VALIDATE_PARAMETER_TRUE_FALSE = [
    CONF_CENTER_IN_ZONE,
    CONF_IGNORE_GPS_ACC_INZONE,
    CONF_HIDE_GPS_COORDINATES,
    CONF_WAZE_REALTIME,
    CONF_LEGACY_MODE,
]
VALIDATE_PARAMETER_NUMBER = [
    CONF_TRAVEL_TIME_FACTOR,
    CONF_GPS_ACCURACY_THRESHOLD,
    CONF_WAZE_MAX_DISTANCE,
    CONF_WAZE_MIN_DISTANCE,
]
VALIDATE_PARAMETER_TIME = [
    CONF_INZONE_INTERVAL,
    CONF_MAX_INTERVAL,
    CONF_STATIONARY_STILL_TIME,
    CONF_STATIONARY_INZONE_INTERVAL,
    CONF_OLD_LOCATION_THRESHOLD,
]

#config_ic3.yaml parameter validation items
LIST = 1
TIME = 2
NUMBER = 3
TRUE_FALSE = 4
VALID_TIME_TYPES = ['sec', 'secs', 'min', 'mins', 'hr', 'hrs']

#==============================================================================
#
#   SYSTEM LEVEL FUNCTIONS
#
#==============================================================================
def _combine_lists(parm_lists):
    '''
    Take a list of lists and return a single list of all of the items.
        [['a,b,c'],['d,e,f']] --> ['a','b','c','d','e','f']
    '''
    new_list = []
    for lists in parm_lists:
        lists_items = lists.split(',')
        for lists_item in lists_items:
            new_list.append(lists_item)

    return new_list

#--------------------------------------------------------------------
def _test(parm1, parm2):
    return f"{parm1}-{parm2}"

#--------------------------------------------------------------------
def TRACE(desc, v1='+++', v2='', v3='', v4='', v5=''):
    '''
    Display a message or variable in the HA log file
    '''
    if desc != '':
        if v1 == '+++':
            value_str = f"►TRACE►► {desc}"
        else:
            value_str = (f"►TRACE►► {desc} = |{v1}|-|{v2}|-"
                         f"|{v3}|-|{v4}|-|{v5}|")
        _LOGGER.info(value_str)

#--------------------------------------------------------------------
def instr(string, find_string):
    if find_string is None:
        return False
    else:
        return str(string).find(find_string) >= 0

#--------------------------------------------------------------------
def isnumber(string):

    try:
        test_number = float(string)

        return True
    except:
        return False

#--------------------------------------------------------------------
def inlist(string, list_items):
    for item in list_items:
        if str(string).find(item) >= 0:
            return True

    return False

#--------------------------------------------------------------------
def format_gps(latitude, longitude, accuracy, latitude_to=None, longitude_to=None):
    '''Format the GPS string for logs & messages'''

    if longitude is None or latitude is None:
        gps_text = UNKNOWN
    else:
        accuracy_text = (f"/{accuracy}m)") if accuracy > 0 else ")"
        gps_to_text   = (f" to ({round(latitude_to, 6)}, {round(longitude_to, 6)})") if latitude_to else ""
        gps_text      = f"({round(latitude, 6)}, {round(longitude, 6)}{accuracy_text}{gps_to_text}"
    return gps_text
#==============================================================================
#
#   CREATE THE ICLOUD3 DEVICE TRACKER PLATFORM
#
#==============================================================================
def setup_scanner(hass, config: dict, see, discovery_info=None):

    #Table with all the parameters specified in the configuration.yaml file. These items
    #will be updated with the parameters in the config_ic3.yaml file and then validated
    #by parameter type. Invalid parameters will be replaced with the default value and an
    #error message will be displayed in the Event Log.
    config_parameter = {}
    config_parameter[CONF_USERNAME]                 = config.get(CONF_USERNAME)
    config_parameter[CONF_PASSWORD]                 = config.get(CONF_PASSWORD)
    config_parameter[CONF_GROUP]                    = config.get(CONF_GROUP)
    config_parameter[CONF_ENTITY_REGISTRY_FILE]     = config.get(CONF_ENTITY_REGISTRY_FILE)
    config_parameter[CONF_CONFIG_IC3_FILE_NAME]     = config.get(CONF_CONFIG_IC3_FILE_NAME)
    config_parameter[CONF_EVENT_LOG_CARD_DIRECTORY] = config.get(CONF_EVENT_LOG_CARD_DIRECTORY)
    config_parameter[CONF_EVENT_LOG_CARD_FILENAME]  = config.get(CONF_EVENT_LOG_CARD_FILENAME)
    config_parameter[CONF_TRACK_DEVICES]            = config.get(CONF_TRACK_DEVICES) or []
    config_parameter[CONF_DEVICES]                  = config.get(CONF_DEVICES) or []
    config_parameter[CONF_DISPLAY_TEXT_AS]          = config.get(CONF_DISPLAY_TEXT_AS)
    config_parameter[CONF_TRACKING_METHOD]          = config.get(CONF_TRACKING_METHOD)
    config_parameter[CONF_CREATE_SENSORS]           = config.get(CONF_CREATE_SENSORS)
    config_parameter[CONF_EXCLUDE_SENSORS]          = config.get(CONF_EXCLUDE_SENSORS)
    config_parameter[CONF_UNIT_OF_MEASUREMENT]      = config.get(CONF_UNIT_OF_MEASUREMENT)
    config_parameter[CONF_TIME_FORMAT]              = config.get(CONF_TIME_FORMAT)
    config_parameter[CONF_INZONE_INTERVAL]          = config.get(CONF_INZONE_INTERVAL)
    config_parameter[CONF_INZONE_INTERVALS]         = config.get(CONF_INZONE_INTERVALS)
    config_parameter[CONF_DISPLAY_ZONE_FORMAT]      = config.get(CONF_DISPLAY_ZONE_FORMAT)
    config_parameter[CONF_CENTER_IN_ZONE]           = config.get(CONF_CENTER_IN_ZONE)
    config_parameter[CONF_MAX_INTERVAL]             = config.get(CONF_MAX_INTERVAL)
    config_parameter[CONF_TRAVEL_TIME_FACTOR]       = config.get(CONF_TRAVEL_TIME_FACTOR)
    config_parameter[CONF_GPS_ACCURACY_THRESHOLD]   = config.get(CONF_GPS_ACCURACY_THRESHOLD)
    config_parameter[CONF_OLD_LOCATION_THRESHOLD]   = config.get(CONF_OLD_LOCATION_THRESHOLD)
    config_parameter[CONF_IGNORE_GPS_ACC_INZONE]    = config.get(CONF_IGNORE_GPS_ACC_INZONE)
    config_parameter[CONF_HIDE_GPS_COORDINATES]     = config.get(CONF_HIDE_GPS_COORDINATES)
    config_parameter[CONF_DISTANCE_METHOD]          = config.get(CONF_DISTANCE_METHOD).lower()
    config_parameter[CONF_LEGACY_MODE]              = config.get(CONF_LEGACY_MODE)
    config_parameter[CONF_WAZE_REGION]              = config.get(CONF_WAZE_REGION).upper()
    config_parameter[CONF_WAZE_MAX_DISTANCE]        = config.get(CONF_WAZE_MAX_DISTANCE)
    config_parameter[CONF_WAZE_MIN_DISTANCE]        = config.get(CONF_WAZE_MIN_DISTANCE)
    config_parameter[CONF_WAZE_REALTIME]            = config.get(CONF_WAZE_REALTIME)
    config_parameter[CONF_STATIONARY_STILL_TIME]    = config.get(CONF_STATIONARY_STILL_TIME)
    config_parameter[CONF_STATIONARY_ZONE_OFFSET]   = config.get(CONF_STATIONARY_ZONE_OFFSET)
    config_parameter[CONF_STATIONARY_INZONE_INTERVAL] = config.get(CONF_STATIONARY_INZONE_INTERVAL)
    config_parameter[CONF_LOG_LEVEL]                = config.get(CONF_LOG_LEVEL)
    config_parameter[CONF_IOSAPP_REQUEST_LOC_MAX_CNT] = config.get(CONF_IOSAPP_REQUEST_LOC_MAX_CNT)

    #make sure the same group is not specified in more than one platform. If so,
    #append with a number
    username = config.get(CONF_USERNAME)
    if username in ICLOUD3_GROUPS:
        username = f"{username}{len(ICLOUD3_GROUPS)+1}"

    ICLOUD3_GROUPS.append(username)
    ICLOUD3_TRACKED_DEVICES[username] = username

    log_msg =(f"Setting up iCloud3 v{VERSION} device tracker for User: {username}")
    if HA_DEVICE_TRACKER_LEGACY_MODE:
        log_msg = (f"{log_msg}, using device_tracker.legacy code")
    _LOGGER.info(log_msg)

#---------------------------------------------
    ICLOUD3_GROUP_OBJS[username] = Icloud3(hass, see,  config_parameter)


#--------------------------------------------------------------------

    def _icloud3_update_service(call):
        """Call the update function of an iCloud group."""

        groups     = call.data.get(CONF_GROUP, ICLOUD3_GROUP_OBJS)
        devicename = call.data.get(CONF_DEVICENAME)
        command    = call.data.get(CONF_COMMAND)

        for group in groups:
            if group in ICLOUD3_GROUP_OBJS:
                ICLOUD3_GROUP_OBJS[group]._icloud3_update_service_handler(
                                    group, devicename, command)

    hass.services.register(DOMAIN, 'icloud3_update',
                _icloud3_update_service, schema=SERVICE_SCHEMA)


#--------------------------------------------------------------------
    def _icloud3_restart_service(call):
        """Reset an iCloud group."""

        groups = call.data.get(CONF_GROUP, ICLOUD3_GROUP_OBJS)
        for group in groups:
            if group in ICLOUD3_GROUP_OBJS:
                ICLOUD3_GROUP_OBJS[group]._start_icloud3()

    hass.services.register(DOMAIN, 'icloud3_restart',
                _icloud3_restart_service, schema=SERVICE_SCHEMA)

#--------------------------------------------------------------------
    def _icloud3_setinterval_service(call):
        """Call the setinterval function of an iCloud group."""

        groups     = call.data.get(CONF_GROUP, ICLOUD3_GROUP_OBJS)
        interval   = call.data.get(CONF_INTERVAL)
        devicename = call.data.get(CONF_DEVICENAME)

        for group in groups:
            if group in ICLOUD3_GROUP_OBJS:
                ICLOUD3_GROUP_OBJS[group]._icloud3_setinterval_service_handlerl(
                                    group, interval, devicename)

    hass.services.register(DOMAIN, 'icloud3_set_interval',
                _icloud3_setinterval_service, schema=SERVICE_SCHEMA)

#--------------------------------------------------------------------
    def _icloud3_find_iphone_alert_service(call):
        """Call the find_iphone_alert to play a sound on the phone"""

        groups     = call.data.get(CONF_GROUP, ICLOUD3_GROUP_OBJS)
        devicename = call.data.get(CONF_DEVICENAME)

        for group in groups:
            if group in ICLOUD3_GROUP_OBJS:
                ICLOUD3_GROUP_OBJS[group]._icloud3_find_iphone_alert_service_handlert(
                                    group, devicename)

    hass.services.register(DOMAIN, 'icloud3_find_iphone_alert',
                _icloud3_find_iphone_alert_service, schema=SERVICE_SCHEMA)

    # Tells the bootstrapper that the component was successfully initialized
    return True


#====================================================================
class Icloud3:#(DeviceScanner):
    """Representation of an iCloud3 platform"""

    def __init__(self, hass, see,  config_parameter):

        self.config_parameter   = config_parameter

        """Initialize the iCloud3 device tracker."""
        self.hass_configurator_request_id    = {}

        self.hass                         = hass
        self.see                          = see
        self.polling_5_sec_loop_running   = False
        self.api                          = None
        self.WazeRouteCalc                = None        # WazeRouteCalculator object
        self.base_zone                    = HOME
        self.verification_inprocess_flag  = False
        self.verification_code            = None
        self.trusted_device               = None
        self.trusted_device_id            = None
        self.trusted_devices              = None
        self.start_icloud3_request_flag   = False
        self.start_icloud3_inprocess_flag = False
        self.authenticated_time           = 0
        self.log_eventlog_flag            = False
        self.log_debug_flag               = False
        self.log_rawdata_flag             = False
        self.log_debug_flag_restart       = None
        self.log_rawdata_flag_restart     = None

        self.attributes_initialized_flag  = False
        self.e_seconds_local_offset_secs  = 0
        self.display_text_as_list         = {}

        #initialize variables configuration.yaml parameters
        self._set_data_fields_from_config_parameter_dictionary()
        self._initialize_debug_control(self.log_level)
        self._setup_tracking_method(self.tracking_method_config)

        #define & initialize fields
        self._define_zone_fields()
        self._define_event_log_fields()
        self._define_usage_counters()
        self._define_iosapp_message_fields()
        self.last_config_ic3_items = []

        #add HA event that will call the _polling_loop_5_sec_icloud function
        #on a 5-second interval. The interval is offset by 1-second for each
        #group to avoid update conflicts.
        self.start_icloud3_initial_load_flag = True
        self._start_icloud3()

        self.start_icloud3_initial_load_flag = False
#--------------------------------------------------------------------
    def _start_icloud3(self):
        """
        Start iCloud3, Define all variables & tables, Initialize devices
        """

        #check to see if restart is in process
        if self.start_icloud3_inprocess_flag:
            return

        try:
            self.start_timer = time.time()

            self.start_icloud3_inprocess_flag = True
            self.start_icloud3_request_flag   = False
            self.initial_locate_complete_flag = False
            self.startup_log_msgs             = ''
            self.startup_log_msgs_prefix      = ''
            devicename = ''

            self._define_device_fields()
            self._define_device_status_fields()
            self._define_device_tracking_fields()
            self._define_zone_fields()
            self._define_device_zone_fields()
            self._define_tracking_control_fields()
            self._define_sensor_fields(self.start_icloud3_initial_load_flag)

            event_msg = (f"^^^Initializing iCloud3 v{VERSION} > "
                         f"{dt_util.now().strftime('%A, %b %d')}")
            self._save_event_halog_info("*", event_msg)

            self.startup_log_msgs_prefix = NEW_LINE
            self._check_ic3_event_log_file_version()
            self._check_ic3_update_2sa_to_2fa()
            self._initialize_zone_tables_step_1()
            self._get_config_ic3_parameters()

            #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            self._display_info_status_msg("", "Stage 1-Initial Config Setup")
            event_msg = (f"Stage 1 > Prepare iCloud3 for {self.username}")
            self._save_event_halog_info("*", event_msg)

            self._validate_config_parameters()
            self._set_data_fields_from_config_parameter_dictionary()
            self._initialize_debug_control(self.log_level)

            self._setup_tracking_method(self.tracking_method_config)
            self._initialize_zone_tables_step_2()
            self._initialize_um_formats(self.unit_of_measurement)
            self._define_stationary_zone_fields(self.stationary_inzone_interval_str,
                        self.stationary_still_time_str)

            self._display_info_status_msg("", "Initializing Waze Route Tracker")
            self._initialize_waze_fields(self.waze_region, self.waze_min_distance,
                        self.waze_max_distance, self.waze_realtime)

            for devicename_cnt in self.count_update_iosapp:
                self._display_usage_counts(devicename_cnt)

            for item in self.display_text_as:
                if instr(item, '>'):
                    from_to_text = item.split(">")
                    self.display_text_as_list[from_to_text[0].strip()] = from_to_text[1].strip()

        except Exception as err:
            _LOGGER.exception(err)

        try:
            self.startup_log_msgs_prefix = NEW_LINE
            self._update_sensor_ic3_event_log("")

            #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            event_msg = (f"Stage 2 > Set up tracked device parameters")
            self._save_event_halog_info("*", event_msg)

            self._display_info_status_msg("", "Setting up Tracked Devices")
            self._set_track_devices_fields_from_config_parms()

            self.this_update_secs     = self._time_now_secs()
            self.icloud3_started_secs = self.this_update_secs

            if self.CONF_TRK_METHOD_FMF_FAMSHR:
                event_msg = (f"Stage 2a > Authenticate iCloud Account, List Trackable Devices")
                self._save_event_halog_info("*", event_msg)
                self._display_info_status_msg("", "Authenticating iCloud Account")
                self._pyicloud_initialize_device_api()

                if self.api:
                    self._setup_tracked_devices_for_fmf()
                    self._setup_tracked_devices_for_famshr()
                    self._tune_tracked_devices_fmf_famshr()

                elif self.CONF_TRK_METHOD_FMF_FAMSHR:
                    event_msg = (f"iCloud3 Error > iCloud Account Authentication needed > "
                                f"Will use iOS App Tracking Method until the iCloud "
                                f"account is authentication is complete. See the HA "
                                f"Notification area to continue. iCloud3 will then be restarted.")
                    self._save_event_halog_info("*", event_msg)

            if self.TRK_METHOD_IOSAPP:
                if self.CONF_TRK_METHOD_FMF_FAMSHR:
                    event_msg = (f"{EVLOG_ALERT}iCloud Alert > FmF or FamShr Tracking Method is disabled until "
                                 f"Verification has been completed. iOS App Trackimg Method "
                                 f"wil be used.")
                    self._save_event_halog_info("*", event_msg)
                event_msg = (f"Stage 2b > Setup iOS App Tracking Method")
                self._save_event_halog_info("*", event_msg)
                self._setup_tracked_devices_for_iosapp()

        except Exception as err:
            _LOGGER.exception(err)

        try:
            self.startup_log_msgs_prefix = NEW_LINE
            self._update_sensor_ic3_event_log("")

            #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            event_msg = (f"Stage 3 > Identify iOS App entities, Verify tracked devices")
            self._save_event_halog_info("*", event_msg)

            iosapp_entities    = self._get_entity_registry_entities('mobile_app', 'device_tracker')
            if iosapp_entities == []:
                event_msg = (f"iCloud3 Alert > No mobile_app device_tracker entities "
                            f"were found in the HA Entity Registry. The iOSApp "
                            f"will not be monitored for any device.")
                self._save_event("*", event_msg)
            else:
                notify_devicenames = self._get_mobile_app_notify_devicenames()

            self.track_devicename_list = ""
            for devicename in self.devicename_verified:
                error_log_msg = None
                self._display_info_status_msg(devicename, "Verifing Device")
                #Devicename config parameter is OK, now check to make sure the
                #entity for device name has been setup by iosapp correctly.
                #If the devicename is valid, it will be tracked
                self._initialize_iosapp_message_fields(devicename)

                if iosapp_entities == []:
                    self.iosapp_monitor_dev_trk_flag[devicename] = False

                if self.devicename_verified.get(devicename):
                    self.tracked_devices.append(devicename)

                    self.track_devicename_list += (f"{CRLF_DOT}{devicename} > {self.fname.get(devicename)}, ")
                    self.attr_tracking_msg     += (f"{devicename}")

                    if self.iosapp_monitor_dev_trk_flag.get(devicename):
                        self._setup_monitored_iosapp_entities(devicename, iosapp_entities,
                                notify_devicenames, self.devicename_iosapp_suffix.get(devicename))
                        suffix = self.devicename_iosapp_entity.get(devicename).replace(devicename, '')
                        self.track_devicename_list += (f"iOSAppSuffix-{suffix}, ")
                        self.attr_tracking_msg     += (f"/{suffix}")
                    else:
                        self.track_devicename_list += ("iOSApp-NotMonitored, ")

                    self.track_devicename_list += (f"TrkMethod-{self._format_tracking_method(devicename)}")
                    self.attr_tracking_msg     += (f" ({self._format_tracking_method(devicename)}), ")

                    event_msg = (f"Verified Device > {self._format_fname_devicename(devicename)}")
                    self._save_event_halog_info("*", event_msg)
                    self._display_info_status_msg(devicename, "Verified Device")

                    if self.iosapp_monitor_dev_trk_flag.get(devicename):
                        event_msg = (f"iOS App monitored > {self._format_fname_devicename(devicename)} >"
                                     f"{CRLF_DOT}device_tracker.{self.devicename_iosapp_entity.get(devicename)}"
                                     f"{CRLF_DOT}sensor.{self.iosapp_last_trigger_entity.get(devicename)}")
                        self._save_event_halog_info("*", event_msg)

                        event_msg = (f"iOS App location requests sent to > {self._format_fname_devicename(devicename)} > "
                                     f"{self._format_list(self.notify_iosapp_entity.get(devicename))}")
                        self._save_event_halog_info("*", event_msg)

                        db=(f"1290 {devicename} {self.notify_iosapp_entity=}")
                        self._save_event_halog_info("*", db)

                        #Send a message to all devices during startup
                        if self.broadcast_msg != '':
                            self._send_message_to_device(devicename, self.broadcast_msg)
                    else:
                        event_msg = (f"iOS App not monitored > {self._format_fname_devicename(devicename)}")
                        self._save_event_halog_info("*", event_msg)

                #If the devicename is not valid & verified, it will not be tracked
                else:
                    if self.TRK_METHOD_FMF_FAMSHR:
                        event_msg = (f"iCloud3 Error for {self._format_fname_devicename(devicename)}/{devicename} > "
                            f"The iCloud Account for {self.username} did not return any "
                            f"device information for this device."
                            f"CRLF{'-'*25}"
                            f"CRLF 1. Restart iCloud3 on the Event_log screen or restart HA."
                            f"CRLF 2. Verify the devicename on the `devices/device_name: {devicename}` "
                            f"parameter if the error persists."
                            f"CRLF 3. Refresh the Event Log in your browser to refresh the list of devices.")
                        self._save_event_halog_error("*", event_msg)

                    event_msg = (f"Not Tracking Device > "
                        f"{self._format_fname_devicename(devicename)}")
                    self._save_event_halog_info("*", event_msg)

            self.attr_tracking_msg = self.attr_tracking_msg[:-2]

            #Reset msg sent to all devices during startup
            self.broadcast_msg = ''

            #Now that the devices have been set up, finish setting up
            #the Event Log Sensor
            self._setup_event_log_base_attrs(self.start_icloud3_initial_load_flag)
            self._setup_sensors_custom_list(self.start_icloud3_initial_load_flag)
            self._display_info_status_msg(devicename, "Define Sensors")

            #nothing to do if no devices to track
            if self.track_devicename_list == '':
                event_msg = (f"iCloud3 Error for {self.username} > Setup aborted, no devices to track. "
                    f"Verify the devicename on the `devices/device_name: [devicename]` parameters. "
                    f"They must be the same as `Settings > General > About > Name` "
                    f"on the phones being tracked.")
                self._save_event_halog_error("*", event_msg)

                self._update_sensor_ic3_event_log("*")
                self.start_icloud3_inprocess_flag = False
                return False

            event_msg = (f"Tracking Devices > {self.track_devicename_list}")
            self._save_event_halog_info("*", event_msg)

            self.startup_log_msgs_prefix = NEW_LINE
            self._update_sensor_ic3_event_log("*")

            #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            event_msg = (f"Stage 4 > Configure tracked devices")
            self._save_event_halog_info("*", event_msg)

            for devicename in self.tracked_devices:
                event_msg = (f"Configuring Device > {self._format_fname_devicename(devicename)}")

                if self.track_from_zones.get(devicename) != [HOME]:
                    track_from_zones = self.track_from_zones.get(devicename)
                    track_from_zones = ', '.join(track_from_zones)
                    event_msg += (f"{CRLF_DOT}Track from zones > {track_from_zones}")

                event_msg += self._display_info_status_msg(devicename, "Initialize Tracking Fields")
                self._initialize_device_status_fields(devicename)
                self._initialize_device_tracking_fields(devicename)
                self._initialize_usage_counters(devicename, self.start_icloud3_initial_load_flag)
                event_msg += self._display_info_status_msg(devicename, "Initialize Zones")
                self._initialize_device_zone_fields(devicename)
                event_msg += self._display_info_status_msg(devicename,
                            f"Initialize Stationary Zone > {self._format_zone_name(devicename, STATIONARY)}")
                self._update_stationary_zone(
                        devicename,
                        self.stat_zone_base_lat,
                        self.stat_zone_base_long,
                        STAT_ZONE_MOVE_TO_BASE)

                #Initialize the new attributes
                event_msg += self._display_info_status_msg(devicename, "Update HA Device Entities")

                iosapp_data_flag = False
                if self.iosapp_monitor_dev_trk_flag.get(devicename):
                    iosapp_state, iosapp_dev_attrs, iosapp_data_flag = \
                        self._get_iosapp_device_tracker_state_attributes(
                                devicename, HOME, {})

                if iosapp_data_flag:
                    initial_lat  = iosapp_dev_attrs[ATTR_LATITUDE]
                    initial_long = iosapp_dev_attrs[ATTR_LONGITUDE]
                else:
                    initial_lat  = self.zone_home_lat
                    initial_long = self.zone_home_long

                kwargs = self._setup_base_kwargs(
                        devicename,
                        initial_lat,
                        initial_long,
                        0, 0)

                attrs  = self._initialize_attrs(devicename)
                self._update_device_attributes(devicename, kwargs, attrs, '_start_icloud3')

                if devicename not in self.sensor_prefix_name:
                    event_msg += self._setup_sensor_base_attrs(devicename)
                    event_msg += self._display_info_status_msg(devicename, "Initialize Sensor Fields")
                    self._update_device_sensors(devicename, kwargs)
                    self._update_device_sensors(devicename, attrs)

                self._save_event_halog_info("*", event_msg)

            self._display_info_status_msg(devicename, "Initialize Event Log")
            self._save_event_halog_info("*", "Initialize Event Log Sensor")

        except Exception as err:
            _LOGGER.exception(err)

        for devicename in self.tracked_devices:
            if self.log_debug_flag or self.log_eventlog_flag:
                self._display_usage_counts(devicename, force_display=(not self.start_icloud3_initial_load_flag))

        self.startup_log_msgs_prefix = NEW_LINE
        self._update_sensor_ic3_event_log("*")
        event_msg = (f"^^^Initializing iCloud3 v{VERSION} > Complete, "
                     f"Took {round(time.time()-self.start_timer, 2)} sec")
        self._save_event_halog_info("*", event_msg)
        self._display_info_status_msg(devicename, "Setup Complete, Locating Device")
        self._update_sensor_ic3_event_log("*")
        #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

        self.start_icloud3_inprocess_flag = False

        if self.log_debug_flag is False:
            self.startup_log_msgs = (NEW_LINE + '-'*55 +
                                    self.startup_log_msgs.replace("CRLF", NEW_LINE) +
                                    NEW_LINE + '-'*55)
            _LOGGER.info(self.startup_log_msgs)
        self.startup_log_msgs = ''

        if self.polling_5_sec_loop_running is False:
            self.polling_5_sec_loop_running = True
            track_utc_time_change(self.hass, self._polling_loop_5_sec_device,
                    second=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

        return True

#########################################################
#
#   This function is called every 5 seconds by HA. Cycle through all
#   of the iCloud devices to see if any of the ones being tracked need
#   to be updated. If so, we might as well update the information for
#   all of the devices being tracked since PyiCloud gets data for
#   every device in the account
#
#########################################################
    def _polling_loop_5_sec_device(self, now):
        try:
            fct_name = "_polling_loop_5_sec_device"

            if self.start_icloud3_request_flag:    #via service call
                self._start_icloud3()

            if (self.any_device_being_updated_flag
                    or self.start_icloud3_inprocess_flag):
                return

        except Exception as err:
            _LOGGER.exception(err)
            return

        self.this_update_secs = self._time_now_secs()
        self.this_update_time = dt_util.now().strftime('%H:%M:%S')
        this_minute           = int(dt_util.now().strftime('%M'))
        this_5sec_loop_second = int(dt_util.now().strftime('%S'))

        #Reset counts on new day, check for daylight saving time new offset
        if self.this_update_time.endswith(':00:00'):
            self._timer_tasks_every_hour()

        if self.this_update_time == HHMMSS_ZERO:
            self._timer_tasks_midnight()

        elif self.this_update_time == '01:00:00':
            self._timer_tasks_1am()

        #Test code to check ios monitor, display it every minute
        #if self.this_update_time.endswith(':00'):
        #    self.last_iosapp_msg['gary_iphone'] = ""

        try:
            if self.this_update_secs >= self.event_log_clear_secs and \
                        self.log_debug_flag is False:
                self._update_sensor_ic3_event_log('clear_log_items')

            if self.this_update_secs >= self.authentication_error_retry_secs:
                self._pyicloud_authenticate_account()

            for devicename in self.tracked_devices:
                devicename_zone = self._format_devicename_zone(devicename, HOME)

                if self._is_device_paused(devicename):
                    continue

                update_method = None
                self.state_change_flag[devicename] = False

                #if self.state_last_poll.get(devicename) == NOT_SET:
                #    self._display_info_status_msg(devicename, "Getting Initial Device State/Triggers")

                #get tracked_device (device_tracker.<devicename>) state & attributes
                #icloud & ios app v1 use this entity
                ic3_entity_id  = self.device_tracker_entity_ic3.get(devicename)
                ic3dev_state  = self._get_state(ic3_entity_id)

                #Will be not_set with a last_poll value if the iosapp has not be set up
                if (ic3dev_state == NOT_SET
                        and self.state_last_poll.get(devicename) != NOT_SET):
                    event_msg = "iOSApp state will be updated after iOSApp starts"
                    self._save_event(devicename,event_msg)
                    continue

                #Extract only attrs needed to update the device
                ic3dev_attrs          = self._get_device_attributes(ic3_entity_id)
                ic3dev_attrs_avail    = {k: v for k, v in ic3dev_attrs.items() if k in DEVICE_ATTRS_BASE}
                ic3dev_data           = {**DEVICE_ATTRS_BASE, **ic3dev_attrs_avail}

                ic3dev_latitude       = ic3dev_data[ATTR_LATITUDE]
                ic3dev_longitude      = ic3dev_data[ATTR_LONGITUDE]
                ic3dev_gps_accuracy   = ic3dev_data[ATTR_GPS_ACCURACY]
                ic3dev_battery        = ic3dev_data[ATTR_BATTERY_LEVEL]
                ic3dev_trigger        = ic3dev_data[ATTR_TRIGGER]
                ic3dev_timestamp_secs = self._timestamp_to_secs(ic3dev_data[ATTR_TIMESTAMP])
                iosapp_state          = ic3dev_state
                iosapp_dev_attrs      = {ATTR_LATITUDE: ic3dev_latitude,
                                         ATTR_LONGITUDE: ic3dev_longitude,
                                         ATTR_GPS_ACCURACY: ic3dev_gps_accuracy,
                                         ATTR_BATTERY_LEVEL: ic3dev_battery}

                #iosapp uses the device_tracker.<devicename>_# entity for
                #location info and sensor.<devicename>_last_update_trigger entity
                #for trigger info. Get location data and trigger.
                #Use the trigger/timestamp if timestamp is newer than current
                #location timestamp.

                update_reason      = ""
                ios_update_reason  = ""
                update_via_iosapp_flag = False
                last_located_secs_plus_5 = self.last_located_secs.get(devicename) + 5
                if self.iosapp_monitor_dev_trk_flag.get(devicename):
                    iosapp_state, iosapp_dev_attrs, iosapp_data_flag = \
                            self._get_iosapp_device_tracker_state_attributes(
                                    devicename, iosapp_state, iosapp_dev_attrs)

                    if iosapp_data_flag is False and self.iosapp_monitor_error_cnt.get(devicename) > 120:
                        self.iosapp_monitor_error_cnt[devicename] = 0
                        event_msg = (f"iOS App data not available, iCloud data used")
                        self._save_event(devicename, event_msg)

                    entity_id = self.device_tracker_entity_iosapp.get(devicename)
                    iosapp_state_changed_time, iosapp_state_changed_secs, iosapp_state_changed_timestamp, \
                            iosapp_state_age_secs, iosapp_state_age_str = \
                            self._get_entity_last_changed_time(entity_id, devicename)

                    iosapp_trigger, iosapp_trigger_changed_time, iosapp_trigger_changed_secs, \
                            iosapp_trigger_age_secs,  iosapp_trigger_age_str = \
                            self._get_iosapp_device_sensor_trigger(devicename)

                    iosapp_data_msg = "" if iosapp_data_flag else "(Using iC3 data) "
                    iosapp_msg = (f"iOSApp Monitor {iosapp_data_msg}> "
                                  f"Trigger-{iosapp_trigger}@{iosapp_trigger_changed_time} (%tage ago), "
                                  f"State-{iosapp_state}@{iosapp_state_changed_time} (%sage ago), "
                                  f"GPS-{format_gps(iosapp_dev_attrs[ATTR_LATITUDE], iosapp_dev_attrs[ATTR_LONGITUDE], iosapp_dev_attrs[ATTR_GPS_ACCURACY])}, "
                                  f"LastiC3UpdtTime-{self.last_update_time.get(devicename_zone)}, ")

                    #Initialize if first time through
                    if self.last_iosapp_trigger.get(devicename) == '':
                        self.last_iosapp_state[devicename]                = iosapp_state
                        self.last_iosapp_state_changed_time[devicename]   = iosapp_state_changed_time
                        self.last_iosapp_state_changed_secs[devicename]   = iosapp_state_changed_secs
                        self.last_iosapp_trigger[devicename]              = iosapp_trigger
                        self.last_iosapp_trigger_changed_time[devicename] = iosapp_trigger_changed_time
                        self.last_iosapp_trigger_changed_secs[devicename] = iosapp_trigger_changed_secs

                        if self.TRK_METHOD_IOSAPP:
                            update_via_iosapp_flag = True
                            ios_update_reason = "Initial Locate"

                    if iosapp_data_flag is False:
                        update_via_iosapp_flag = False
                        ios_update_reason = "No data received from the iOS App, using iC3 data"

                    elif (iosapp_state == NOT_SET
                            and self.iosapp_request_loc_retry_cnt.get(devicename) == 0):
                        update_via_iosapp_flag = True
                        ios_update_reason = "Reinitialize iOSApp location"

                    elif (instr(iosapp_state, STATIONARY)
                            and iosapp_dev_attrs[ATTR_LATITUDE]  == self.stat_zone_base_lat
                            and iosapp_dev_attrs[ATTR_LONGITUDE] == self.stat_zone_base_long):
                        ios_update_reason = "Stat Zone Base Locatioon"

                    #State changed
                    elif iosapp_state != self.last_iosapp_state.get(devicename):
                        update_via_iosapp_flag = True
                        ios_update_reason = (f"State Change-{iosapp_state}")

                    #trigger time is after last locate
                    #elif iosapp_trigger_changed_secs > (self.last_located_secs.get(devicename) + 5):
                    elif iosapp_trigger_changed_secs > last_located_secs_plus_5:
                        update_via_iosapp_flag = True
                        ios_update_reason  = (f"Trigger Change-{iosapp_trigger}")

                    #State changed more than 5-secs after last locate
                    #elif iosapp_state_changed_secs > (self.last_located_secs.get(devicename) + 5):
                    elif iosapp_state_changed_secs > last_located_secs_plus_5:
                        update_via_iosapp_flag = True
                        iosapp_trigger = "iOSApp Loc Update"
                        iosapp_trigger_changed_secs = iosapp_state_changed_secs
                        ios_update_reason = (f"iOSApp Loc Update@{iosapp_state_changed_time}")

                    #Prevent duplicate update if State & Trigger changed at the same time
                    #and state change was handled on last cycle
                    elif (iosapp_trigger_changed_secs == iosapp_state_changed_secs
                            or iosapp_trigger_changed_secs <= last_located_secs_plus_5):
                           # or iosapp_trigger_changed_secs <= (self.last_located_secs.get(devicename) + 5)):
                        self.last_iosapp_trigger[devicename] = iosapp_trigger
                        ios_update_reason  = "Already Processed"

                    #Trigger changed more than 5-secs after last trigger
                    elif (iosapp_trigger_changed_secs > (self.last_iosapp_trigger_changed_secs.get(devicename) + 5)):
                        update_via_iosapp_flag = True
                        ios_update_reason = (f"Trigger Time@{self._secs_to_time(iosapp_trigger_changed_secs)}")

                    #Bypass if trigger contains ic3 date stamp suffix (@hhmmss)
                    elif instr(iosapp_trigger, '@'):
                        ios_update_reason = "Trigger Already Processed"

                    #elif iosapp_trigger_changed_secs <= (self.last_located_secs.get(devicename) + 5):
                    elif iosapp_trigger_changed_secs <= last_located_secs_plus_5:
                        ios_update_reason  = "Trigger Before Last Locate"

                    else:
                        ios_update_reason  = "Failed Update Tests"

                    iosapp_msg += (f"WillUpdate-{update_via_iosapp_flag}")

                    #Show iOS App monitor every half hour
                    if self.this_update_time.endswith(':00:00') or self.this_update_time.endswith(':30:00'):
                        self.last_iosapp_msg[devicename] = ""

                    if (iosapp_msg != self.last_iosapp_msg.get(devicename)):
                        self.last_iosapp_msg[devicename] = iosapp_msg

                        iosapp_msg = iosapp_msg.replace("%tage", iosapp_trigger_age_str)
                        iosapp_msg = iosapp_msg.replace("%sage", iosapp_state_age_str)
                        iosapp_msg += (f", {ios_update_reason}")
                        self._log_debug_msg(devicename, iosapp_msg)
                        self._evlog_debug_msg(devicename, iosapp_msg)

                    #This devicename is entering a zone also assigned to another device. The ios app
                    #will move issue a Region Entered trigger and the state is the other devicename's
                    #stat zone name. Create this device's stat zone at the current location to get the
                    #zone tables in sync. Must do this before processing the state/trigger change or
                    #this devicename will use this trigger to start a timer rather than moving it ineo
                    #the stat zone.
                    if update_via_iosapp_flag:
                        if (iosapp_trigger in IOS_TRIGGERS_ENTER):
                            if (instr(iosapp_state, STATIONARY)
                                    and instr(iosapp_state, devicename) is False
                                    and self.in_stationary_zone_flag.get(devicename) is False):

                                event_msg = (f"Stationary Zone Entered > iOS App used another device's "
                                            f"Stationary Zone, changed {iosapp_state} to "
                                            f"{self._format_zone_name(devicename, STATIONARY)}")
                                self._save_event(devicename, event_msg)

                                latitude  = self.zone_lat.get(iosapp_state)
                                longitude = self.zone_long.get(iosapp_state)

                                self._update_stationary_zone(
                                        devicename,
                                        latitude,
                                        longitude,
                                        STAT_ZONE_NEW_LOCATION, 'poll 5-EnterTrigger')

                                iosapp_state = self._format_zone_name(devicename, STATIONARY)

                        elif (iosapp_trigger in IOS_TRIGGERS_EXIT):
                            if (self.in_stationary_zone_flag.get(devicename)):
                                self._update_stationary_zone(
                                        devicename,
                                        self.stat_zone_base_lat,
                                        self.stat_zone_base_long,
                                        STAT_ZONE_MOVE_TO_BASE, 'poll 5-ExitTrigger')

                    if instr(iosapp_state, STATIONARY):
                            iosapp_state = STATIONARY

                    #----------------------------------------------------------------------------
                    ic3dev_battery                = self._get_attr(iosapp_dev_attrs, ATTR_BATTERY_LEVEL, NUMERIC)
                    self.last_battery[devicename] = ic3dev_battery

                    if update_via_iosapp_flag:
                        iosapp_trigger_age_secs         = self._secs_since(iosapp_trigger_changed_secs)
                        age                             = iosapp_trigger_changed_secs - self.this_update_secs
                        ic3dev_state                    = iosapp_state
                        ic3dev_latitude                 = iosapp_dev_attrs[ATTR_LATITUDE]
                        ic3dev_longitude                = iosapp_dev_attrs[ATTR_LONGITUDE]
                        ic3dev_gps_accuracy             = iosapp_dev_attrs[ATTR_GPS_ACCURACY]
                        ic3dev_trigger                  = iosapp_trigger
                        ic3dev_timestamp_secs           = iosapp_trigger_changed_secs
                        ic3dev_data[ATTR_LATITUDE]      = ic3dev_latitude
                        ic3dev_data[ATTR_LONGITUDE]     = ic3dev_longitude
                        ic3dev_data[ATTR_TIMESTAMP]     = iosapp_state_changed_timestamp
                        ic3dev_data[ATTR_GPS_ACCURACY]  = ic3dev_gps_accuracy
                        ic3dev_data[ATTR_BATTERY_LEVEL] = ic3dev_battery
                        ic3dev_data[ATTR_ALTITUDE]      = self._get_attr(iosapp_dev_attrs, ATTR_ALTITUDE, NUMERIC)
                        ic3dev_data[ATTR_VERT_ACCURACY] = self._get_attr(iosapp_dev_attrs, ATTR_VERT_ACCURACY, NUMERIC)

                        self.last_iosapp_state[devicename]                = iosapp_state
                        self.last_iosapp_state_changed_time[devicename]   = iosapp_state_changed_time
                        self.last_iosapp_state_changed_secs[devicename]   = iosapp_state_changed_secs
                        self.last_iosapp_trigger[devicename]              = iosapp_trigger
                        self.last_iosapp_trigger_changed_time[devicename] = iosapp_trigger_changed_time
                        self.last_iosapp_trigger_changed_secs[devicename] = iosapp_trigger_changed_secs

                    #Check ios app for activity every 6-hours
                    #Issue ios app Location update 15-min before 6-hour alert
                    elif (self.this_update_time in ['23:45:00', '05:45:00', '11:45:00', '17:45:00']
                            and iosapp_state_age_secs > 20700
                            and iosapp_trigger_age_secs > 20700):
                        self._iosapp_request_loc_update(devicename)

                    #No activity, display Alert msg in Event Log
                    elif (self.this_update_time in ['00:00:00', '06:00:00', '12:00:00', '18:00:00']
                            and iosapp_state_age_secs > 21600
                            and iosapp_trigger_age_secs > 21600):
                        event_msg = (f"{EVLOG_NOTICE}iOS App Alert > No iOS App updates for more than 6 hours > "
                                    f"Device-{self.device_tracker_entity_iosapp.get(devicename)}, "
                                    f"LastTrigger-{iosapp_trigger}@{iosapp_trigger_changed_time} ({iosapp_trigger_age_str}), "
                                    f"LastState-{iosapp_state}@{iosapp_state_changed_time} ({iosapp_state_age_str})")
                        self._save_event_halog_info(devicename, event_msg)
                        event_msg = (f"Last iOS App update from {self.device_tracker_entity_iosapp.get(devicename)}"
                                    f"—{iosapp_trigger_age_str} ago")
                        self._display_info_status_msg(devicename, event_msg)

                zone          = self._format_zone_name(devicename, ic3dev_state)
                event_msg     = ""
                update_reason = ""

                dist_from_zone_m = self._zone_distance_m(
                            devicename,
                            zone,
                            ic3dev_latitude,
                            ic3dev_longitude)

                dist_from_home_m = self._zone_distance_m(
                            devicename,
                            HOME,
                            ic3dev_latitude,
                            ic3dev_longitude)

                zone_radius_m = self.zone_radius_m.get(
                            zone,
                            self.zone_radius_m.get(HOME))
                zone_radius_accuracy_m = zone_radius_m + self.gps_accuracy_threshold

                if (self.TRK_METHOD_IOSAPP and self.zone_current.get(devicename) == ''):
                    update_method = IOSAPP_UPDATE
                    update_reason = "Initial Locate"

                #device_tracker.see svc call from automation wipes out
                #latitude and longitude. Reset via icloud update.
                elif ic3dev_latitude == 0:
                    update_method  = ICLOUD_UPDATE
                    update_reason  = (f"GPS=(0, 0) {self.state_last_poll.get(devicename)}/{ic3dev_state}")
                    ic3dev_trigger = "RefreshLocation"
                    device_offline_msg = (f"May be Offline, No Location "
                                         f"(#{self.poor_location_gps_cnt.get(devicename)})")
                    self._display_info_status_msg(devicename, device_offline_msg)
                    self._save_event(devicename,device_offline_msg)

                #Update the device if it wasn't completed last time.
                elif (self.state_last_poll.get(devicename) == NOT_SET
                        and self.next_update_secs.get(devicename_zone) < self.this_update_secs):
                    update_method  = ICLOUD_UPDATE
                    ic3dev_trigger = update_reason = "Initial Locate"
                    self._display_info_status_msg(devicename, "Locating Device via iCloud")

                #If the state changed since last time and it was a trigger
                #related to another Stationary Zone, discard it.
                elif (ic3dev_state != self.state_last_poll.get(devicename)
                        and ic3dev_state != STATIONARY
                        and instr(ic3dev_state, STATIONARY)
                        and instr(ic3dev_state, devicename) is False):
                    update_method = None
                    update_reason = "Other Device StatZone"
                    event_msg     = (f"Discarded > Another device's Stationary Zone trigger detected, "
                                    f"Zone-{ic3dev_state}")
                    self._save_event(devicename, event_msg)

                elif (self.stat_zone_timer.get(devicename, 0) > 0
                        and self.this_update_secs >= self.stat_zone_timer.get(devicename)
                        and self.poor_location_gps_cnt.get(devicename) == 0):
                    event_msg = (f"Move into Stationary Zone Timer reached > {devicename}, "
                                 f"Expired-{self._secs_to_time(self.stat_zone_timer.get(devicename, -1))}")
                    self._save_event(devicename, event_msg)

                    update_method  = ICLOUD_UPDATE
                    ic3dev_trigger = "MoveIntoStatZone"
                    update_reason  = "Move into Stat Zone "

                #The state can be changed via device_tracker.see service call
                #with a different location_name in an automation or by an
                #ios app notification that a zone is entered or exited. If
                #by the ios app, the trigger is 'Geographic Region Exited' or
                #'Geographic Region Entered'. In iosapp 2.0, the state is
                #changed without a trigger being posted and will be picked
                #up here anyway.
                elif (ic3dev_state != self.state_last_poll.get(devicename)
                        and ic3dev_timestamp_secs > last_located_secs_plus_5):
                    self.count_state_changed[devicename] += 1
                    self.state_change_flag[devicename] = True
                    update_method = IOSAPP_UPDATE
                    update_reason = "State Change"
                    event_msg     = (f"iOSApp State Change detected > "
                                    f"{self.state_last_poll.get(devicename)} to {ic3dev_state}")
                    self._save_event(devicename, event_msg)

                elif (ic3dev_trigger != self.trigger.get(devicename)
                        and instr(iosapp_state, STATIONARY)
                        and iosapp_dev_attrs[ATTR_LATITUDE] == self.stat_zone_base_lat
                        and iosapp_dev_attrs[ATTR_LONGITUDE] == self.stat_zone_base_long):
                    update_method = ICLOUD_UPDATE
                    update_reason = "Verify Location"
                    event_msg     = (f"Discarded > Entering Stationary Base Zone")
                    self._save_event(devicename, event_msg)

                elif (ic3dev_trigger != self.trigger.get(devicename)
                        and ic3dev_timestamp_secs > last_located_secs_plus_5):
                    update_method = IOSAPP_UPDATE
                    self.count_trigger_changed[devicename] += 1
                    update_reason = "Trigger Change"
                    event_msg     = (f"iOSApp Trigger Change detected > {ic3dev_trigger}")
                    self._save_event(devicename, event_msg)

                #If iOS App tracking and next update time reached and message not sent, request location. iOS App should respond within 20-seconds and create a Location Request
                #trigger. Do this 4-times and then display message and wait.
                elif (self.TRK_METHOD_IOSAPP
                        and self._is_next_update_time_reached_devicename(devicename)):
                    self._iosapp_request_loc_update(devicename)

                else:
                    update_reason = f"OlderTrigger-{ic3dev_trigger}"

                if (self.TRK_METHOD_IOSAPP
                        and update_method == ICLOUD_UPDATE):
                    update_method = IOSAPP_UPDATE

                #Update because of state or trigger change.
                #Accept the location data as it was sent by ios if the trigger
                #is for zone enter, exit, manual or push notification,
                #or if the last trigger was already handled by ic3 ( an '@hhmmss'
                #was added to it.
                #If the trigger was sometning else (Significant Location Change,
                #Background Fetch, etc, check to make sure it is not old or
                #has poor gps info.
                if (update_method == IOSAPP_UPDATE
                        or update_method == ICLOUD_UPDATE and self.TRK_METHOD_IOSAPP):
                    self.iosapp_request_loc_sent_flag[devicename] = False

                    #If exit trigger flag is not set, set it now if Exiting zone
                    #If already set, leave it alone and reset when enter Zone (v2.1x)
                    if  self.got_exit_trigger_flag.get(devicename) is False:
                        self.got_exit_trigger_flag[devicename] = (ic3dev_trigger in IOS_TRIGGERS_EXIT)

                    if ic3dev_trigger in IOS_TRIGGERS_ENTER:
                        if (zone in self.zone_lat
                                and dist_from_zone_m > self.zone_radius_m.get(zone)*2
                                and dist_from_zone_m < HIGH_INTEGER):
                            event_msg = (f"Enter Zone Trigger Conflict Moving into Zone > "
                                f"Zone-{zone}, Distance-{dist_from_zone_m}m, "
                                f"ZoneVerifyDist-{self.zone_radius_m.get(zone)*2}m, "
                                f"GPS-{format_gps(ic3dev_latitude, ic3dev_longitude, ic3dev_gps_accuracy)}")
                            self._save_event_halog_info(devicename, event_msg)

                            ic3dev_latitude             = self.zone_lat.get(zone)
                            ic3dev_longitude            = self.zone_long.get(zone)
                            ic3dev_data[ATTR_LATITUDE]  = ic3dev_latitude
                            ic3dev_data[ATTR_LONGITUDE] = ic3dev_longitude

                    #RegionExit trigger overrules old location, gps accuracy and other checks
                    elif (ic3dev_trigger in IOS_TRIGGERS_EXIT
                            and ic3dev_timestamp_secs > last_located_secs_plus_5):
                        update_method = IOSAPP_UPDATE
                        update_reason = "Region Exit"

                    #Check info if Background Fetch, Significant Location Update,
                    #Push, Manual, Initial
                    #elif (ic3dev_trigger in IOS_TRIGGERS_VERIFY_LOCATION):
                    #If not an enter/exit trigger, verify the location
                    elif (ic3dev_trigger not in IOS_TRIGGERS_ENTER_EXIT):
                        poor_location_gps_flag, discard_reason = self._check_poor_location_gps(
                                devicename,
                                ic3dev_timestamp_secs,
                                ic3dev_gps_accuracy)

                        #If old location, discard
                        if poor_location_gps_flag:
                            event_msg = (f"Old Location or Poor GPS "
                                    f"(#{self.poor_location_gps_cnt.get(devicename)}) > "
                                    f"LocTime-{self._format_time_age(ic3dev_timestamp_secs)}, "
                                    f"GPS-{format_gps(ic3dev_latitude, ic3dev_longitude, ic3dev_gps_accuracy)}, "
                                    f"OldLocThreshold-{self._secs_to_time_str(self.old_location_secs.get(devicename))}")

                            self._save_event(devicename, event_msg)
                            update_method = ICLOUD_UPDATE
                            update_reason = "OldLoc PoorGPS"

                        #If got these triggers and not old location check a few
                        #other things
                        else:
                            update_reason = (f"{ic3dev_trigger}")
                            self.last_iosapp_trigger[devicename] = ic3dev_trigger

                            #if the zone is a stationary zone and no exit trigger,
                            #the zones in the ios app may not be current.
                            if (dist_from_zone_m >= zone_radius_m * 2
                                    and instr(zone, STATIONARY)
                                    and instr(self.zone_last.get(devicename), STATIONARY)):
                                event_msg = ("Outside Stationary Zone without "
                                    "Exit Trigger > iOS App Zone info may need to be reloaded. "
                                    "Check `iOS App Configuration > Location` screen for stat zones. "
                                    "Force close iOS App and reload if necessary. "
                                    f"Zone-{zone}, "
                                    f"Distance-{self._format_dist_m(dist_from_zone_m)}, "
                                    f"StatZoneTestDist-{zone_radius_m * 2}m")
                                #self._save_event_halog_info(devicename, event_msg)

                                self.iosapp_stat_zone_action_msg_cnt[devicename] += 1
                                if self.iosapp_stat_zone_action_msg_cnt.get(devicename) < 5:
                                    message = {
                                        "title": "iCloud3/iOSApp Zone Action Needed",
                                        "message": event_msg,
                                        "data": {"subtitle": "Stationary Zone Exit "\
                                            "Trigger was not recieved"}}
                                    self._send_message_to_device(devicename, message)

                            #Check to see if currently in a zone. If so, check the zone distance.
                            #If new location is outside of the zone and inside radius*4, discard
                            #by treating it as poor GPS
                            if self._is_inzone_zonename(zone):
                                outside_no_exit_trigger_flag, info_msg = \
                                    self._is_outside_zone_no_exit(devicename, zone, ic3dev_trigger,
                                            ic3dev_latitude, ic3dev_longitude)
                                if outside_no_exit_trigger_flag:
                                    update_method     = None
                                    ios_update_reason = None
                                    self._save_event_halog_info(devicename, info_msg)

                            #update via icloud to verify location if less than home_radius*10
                            elif (dist_from_zone_m <= zone_radius_m * 10
                                    and self.TRK_METHOD_FMF_FAMSHR):
                                event_msg = (f"Verify Location Needed > "
                                    f"Zone-{zone}, "
                                    f"Distance-{self._format_dist_m(dist_from_zone_m)}m, "
                                    f"ZoneVerifyDist-{self._format_dist_m(zone_radius_m*10)}m, "
                                    f"GPS-{format_gps(ic3dev_latitude, ic3dev_longitude, ic3dev_gps_accuracy)}")
                                self._save_event_halog_info(devicename, event_msg)
                                update_method = ICLOUD_UPDATE
                                update_reason = "Verify Location"
                            else:
                                pass
                    else:
                        pass

                    if (ic3dev_data[ATTR_LATITUDE] is None or ic3dev_data[ATTR_LONGITUDE] is None):
                        update_method = ICLOUD_UPDATE

                device_monitor_msg = (f"Device Monitor > UpdateMethod-{update_method}, "
                             f"UpdateReason-{update_reason}, "
                             f"State-{ic3dev_state}, "
                             f"Trigger-{ic3dev_trigger}, "
                             f"LastLoc-{self._secs_to_time(ic3dev_timestamp_secs)}, "
                             f"Zone-{zone}, "
                             f"HomeDist-{self._format_dist_m(dist_from_home_m)}, "
                             f"inZone-{self._is_inzone_zonename(zone)}, "
                             f"GPS-{format_gps(ic3dev_latitude, ic3dev_longitude, ic3dev_gps_accuracy)}, "
                             f"StateThisPoll-{ic3dev_state}, "
                             f"StateLastPoll-{self.state_last_poll.get(devicename)}")
                if self.last_device_monitor_msg.get(devicename) != device_monitor_msg:
                    self._evlog_debug_msg(devicename, device_monitor_msg)
                    self.last_device_monitor_msg[devicename] = device_monitor_msg

                if (self._device_offline(devicename)
                        or self.state_this_poll == NOT_SET):
                    device_offline_msg = (f"May be Offline, Never Located "
                                         f"(#{self.poor_location_gps_cnt.get(devicename)})")
                    self._display_info_status_msg(devicename, device_offline_msg)

                #Save trigger and time for cycle even if trigger was discarded.
                self.trigger[devicename]           = ic3dev_trigger
                self.last_located_secs[devicename] = ic3dev_timestamp_secs

                if update_method == ICLOUD_UPDATE:
                    if self.TRK_METHOD_FMF_FAMSHR:
                        self._update_device_icloud(update_reason, devicename)

                    elif self.TRK_METHOD_IOSAPP:
                        update_method = IOSAPP_UPDATE
                        self.iosapp_request_loc_sent_flag[devicename] = False

                if update_method == IOSAPP_UPDATE:
                    self.state_this_poll[devicename]    = ic3dev_state
                    self.iosapp_update_flag[devicename] = True

                    update_method = self._update_device_iosapp(devicename, update_reason, ic3dev_data)

                    #Retry with iCloud of an error or no data
                    if (update_method == ICLOUD_UPDATE
                            and self.TRK_METHOD_FMF_FAMSHR):
                        self._update_device_icloud(update_reason, devicename)

                self.any_device_being_updated_flag = False

                #If less than 90 secs to the next update for any devicename:zone, display time to
                #the next update in the NextUpdt time field, e.g, 1m05s or 0m15s.
                if devicename in self.track_from_zones:
                    for zone in self.track_from_zones.get(devicename):
                        devicename_zone = self._format_devicename_zone(devicename, zone)
                        if devicename_zone in self.next_update_secs:
                            age_secs = self._secs_to(self.next_update_secs.get(devicename_zone))
                            self._display_time_till_update_info_msg(devicename_zone, age_secs)


                #if update_method is not None:
                if update_method:
                    self.device_being_updated_flag[devicename] = False
                    self.state_change_flag[devicename]         = False
                    self.update_in_process_flag                = False

            #End devicename in self.tracked_devices loop

        except Exception as err:
            _LOGGER.exception(err)
            log_msg = (f"Device Update Error, Error-{ValueError}")
            self._log_error_msg(log_msg)

        self.update_in_process_flag     = False

        #Cycle thru all devices and check to see if devices next update time
        #will occur in 5-secs. If so, request a location update now so it
        #it might be current on the next update.
        if ((this_5sec_loop_second % 15) == 10) and self.TRK_METHOD_FMF_FAMSHR:
            self._polling_loop_10_sec_loc_prefetch(now)

        #Cycle thru all devices and check to see if devices need to be
        #updated via every 15 seconds
        if ((this_5sec_loop_second % 15) == 0) and self.TRK_METHOD_FMF_FAMSHR:
            self._polling_loop_15_sec_icloud(now)

        #Refresh the Event Log after completing the first locate, display info
        #for the first devicename
        if self.tracked_devices:
            devicename = self.tracked_devices[0]
            if (self.initial_locate_complete_flag is False
                    and self.state_this_poll.get(devicename, NOT_SET) != NOT_SET):
                self.initial_locate_complete_flag = True
                self._update_sensor_ic3_event_log(devicename)

#--------------------------------------------------------------------
    def _retry_update(self, devicename):
        #This flag will be 'true' if the last update for this device
        #was not completed. Do another update now.
        self.device_being_updated_retry_cnt[devicename] = 0
        while (self.device_being_updated_flag.get(devicename)
                and self.device_being_updated_retry_cnt.get(devicename) < 4):
            self.device_being_updated_retry_cnt[devicename] += 1

            log_msg = (f"{self._format_fname_devtype(devicename)} "
                f"Retrying Update, Update was not completed in last cycle, "
                f"Retry #{self.device_being_updated_retry_cnt.get(devicename)}")
            self._save_event_halog_info(devicename, log_msg)

            self.device_being_updated_flag[devicename] = True

            self._wait_if_update_in_process()
            update_reason = (f"Retry Update #{self.device_being_updated_retry_cnt.get(devicename)}")

            self._update_device_icloud(update_reason, devicename)

#########################################################
#
#   This function is called every 10 seconds. Cycle through all
#   of the devices to see if any of the ones being tracked will
#   be updated on the 15-sec polling loop in 5-secs. If so, request a
#   location update now so it might be current when the device
#   is updated.
#
#########################################################
    def _polling_loop_10_sec_loc_prefetch(self, now):

        try:
            if self.next_update_secs is None:
                return

            for devicename_zone in self.next_update_secs:
                devicename = devicename_zone.split(':')[0]
                if self.state_this_poll.get(devicename) == NOT_SET:
                    continue
                elif self._is_device_paused(devicename):
                    continue

                time_till_update = self.next_update_secs.get(devicename_zone) - \
                        self.this_update_secs
                location_data = self.location_data.get(devicename)

                if time_till_update <= 10:
                    location_data = self.location_data.get(devicename)
                    location_age  = self._secs_since(location_data[ATTR_TIMESTAMP_SECS])
                    self.location_data[devicename][ATTR_AGE] = location_age

                    if location_age > 15:
                        if self.TRK_METHOD_FMF_FAMSHR:
                            self._refresh_pyicloud_devices_location_data(location_age, devicename)

                        elif self.TRK_METHOD_IOSAPP:
                            self._iosapp_request_loc_update(devicename)
                    break

        except Exception as err:
            _LOGGER.exception(err)

        return

#########################################################
#
#   Update the device on a state or trigger change was recieved from the ios app
#     ●►●◄►●▬▲▼◀►►●◀ oPhone=►▶
#########################################################
    def _update_device_iosapp(self, devicename, update_reason, ic3dev_data):
        """
        Update the devices location using data from the iOS App
        """

        if self.start_icloud3_inprocess_flag:
            return

        fct_name = "_update_device_ios_trigger"

        self.any_device_being_updated_flag = True
        return_code = IOSAPP_UPDATE

        self.iosapp_request_loc_retry_cnt[devicename] = 0
        self.iosapp_request_loc_sent_secs[devicename] = 0
        self.iosapp_request_loc_sent_flag[devicename] = False

        try:
            devicename_zone = self._format_devicename_zone(devicename, HOME)

            if self._is_device_paused(devicename):
                self._save_event(devicename,"update_iosapp, paused")
                return
            elif ATTR_LATITUDE not in ic3dev_data or ATTR_LONGITUDE not in ic3dev_data:
                self._save_event(devicename,f"update_iosapp, ic3_dev_data={ic3dev_data}")
                return
            elif ic3dev_data[ATTR_LATITUDE] is None or ic3dev_data[ATTR_LONGITUDE] is None:
                self._save_event(devicename,f"update_iosapp, lat=None, ic3_dev_data={ic3dev_data}")
                return

            self._log_start_finish_update_banner('▼▼▼', devicename, "iOSApp", update_reason)
            self._trace_device_attributes(devicename, 'IC3DEV_DATA', fct_name, ic3dev_data)
            event_msg = (f"iOS App update started ({update_reason.split('@')[0]})")
            self._save_event(devicename, event_msg)

            self.update_timer[devicename] = time.time()

            entity_id      = self.device_tracker_entity_ic3.get(devicename)
            state          = self._get_state(entity_id)
            latitude       = ic3dev_data[ATTR_LATITUDE]
            longitude      = ic3dev_data[ATTR_LONGITUDE]
            timestamp_secs = self._timestamp_to_secs(ic3dev_data[ATTR_TIMESTAMP])
            timestamp      = self._timestamp_to_time(ic3dev_data[ATTR_TIMESTAMP])
            timestamp      = self.this_update_time if timestamp == HHMMSS_ZERO else timestamp
            gps_accuracy   = ic3dev_data[ATTR_GPS_ACCURACY]
            battery        = ic3dev_data[ATTR_BATTERY_LEVEL]
            battery_status = ic3dev_data[ATTR_BATTERY_STATUS]
            device_status  = ic3dev_data[ATTR_DEVICE_STATUS]
            low_power_mode = ic3dev_data[ATTR_LOW_POWER_MODE]
            altitude       = self._get_attr(ic3dev_data, ATTR_ALTITUDE, NUMERIC)
            vertical_accuracy = self._get_attr(ic3dev_data, ATTR_VERT_ACCURACY, NUMERIC)

            #Save data in common device data field - self.location_data
            location_data                      = {}
            location_data[ATTR_NAME]           = self.fname.get(devicename)
            location_data[ATTR_DEVICE_CLASS]   = self.device_type.get(devicename, '')
            location_data[ATTR_BATTERY_LEVEL]  = battery
            location_data[ATTR_BATTERY_STATUS] = battery_status
            location_data[ATTR_DEVICE_STATUS]  = DEVICE_STATUS_CODES.get(device_status, "")
            location_data[ATTR_LOW_POWER_MODE] = low_power_mode
            location_data[ATTR_TIMESTAMP_SECS] = timestamp_secs
            location_data[ATTR_TIMESTAMP_TIME] = self._secs_to_time(timestamp_secs)
            location_data[ATTR_AGE]            = self._secs_since(timestamp_secs)
            location_data[ATTR_LATITUDE]       = latitude
            location_data[ATTR_LONGITUDE]      = longitude
            location_data[ATTR_ALTITUDE]       = altitude
            location_data[ATTR_GPS_ACCURACY]   = gps_accuracy
            location_data[ATTR_VERT_ACCURACY]  = vertical_accuracy

            self.location_data[devicename]     = location_data

            #location_isold_attr = False
            poor_location_gps_flag = False
            self.poor_location_gps_cnt[devicename] = 0
            self.poor_location_gps_msg[devicename] = False
            self.poor_gps_flag[devicename]         = False
            self.device_status[devicename]         = device_status

            attrs = {}

            #--------------------------------------------------------
            try:
                if self.device_being_updated_flag.get(devicename):
                    info_msg = "Last update not completed, retrying"
                else:
                    info_msg = "Updating"
                info_msg = (f"{info_msg} {self.fname.get(devicename)}")

                self._display_info_status_msg(devicename, info_msg)
                self.device_being_updated_flag[devicename] = True

            except Exception as err:
                _LOGGER.exception(err)
                attrs = self._internal_error_msg(fct_name, err, 'UpdateAttrs1')

            try:
                for zone in self.track_from_zones.get(devicename):
                    #If the state changed, only process the zone that changed
                    #to avoid delays caused calculating travel time by other zones
                    if (self.state_change_flag.get(devicename)
                            and self.state_this_poll.get(devicename) != zone
                            and zone != HOME):
                        continue

                    #discard trigger if outsize zone with no exit trigger
                    if self._is_inzone_zonename(zone):
                        discard_flag, discard_msg = \
                            self._is_outside_zone_no_exit(devicename, zone, '',
                                    latitude, longitude)

                        if discard_flag:
                            self._save_event(devicename, discard_msg)
                            continue

                    self._set_base_zone_name_lat_long_radius(zone)
                    self._log_start_finish_update_banner('▼-▼', devicename, "iOSApp", zone)

                    attrs = self._determine_interval(
                        devicename,
                        latitude,
                        longitude,
                        battery,
                        gps_accuracy,
                        poor_location_gps_flag,
                        self.last_located_secs.get(devicename),
                        timestamp,
                        "iOSApp")

                    if attrs != {}:
                        self._update_device_sensors(devicename, attrs)
                    self._log_start_finish_update_banner('▲-▲', devicename,  "iOSApp", zone)

            except Exception as err:
                attrs = self._internal_error_msg(fct_name, err, 'DetInterval')
                self.any_device_being_updated_flag = False
                return ICLOUD_UPDATE

            try:
                #attrs should not be empty, but catch it and do an icloud update
                #if it is and no data is available. Exit without resetting
                #device_being_update_flag so an icloud update will be done.
                if attrs == {} and self.TRK_METHOD_FMF_FAMSHR:
                    self.any_device_being_updated_flag = False
                    self.iosapp_request_loc_sent_secs[devicename] = 0

                    event_msg = ("iOS update was not completed, "
                        f"will retry with {self._format_tracking_method(devicename)}")
                    self._save_event_halog_debug(devicename, event_msg)

                    return ICLOUD_UPDATE

                #Note: Final prep and update device attributes via
                #device_tracker.see. The gps location, battery, and
                #gps accuracy are not part of the attrs variable and are
                #reformatted into device attributes by 'See'. The gps
                #location goes to 'See' as a "(latitude, longitude)" pair.
                #'See' converts them to ATTR_LATITUDE and ATTR_LONGITUDE
                #and discards the 'gps' item.

                log_msg = (f"LOCATION ATTRIBUTES, State-{self.state_last_poll.get(devicename)}, "
                           f"Attrs-{attrs}")
                self._log_debug_msg(devicename, log_msg)

                #If location is empty or trying to set to the Stationary Base Zone Location,
                #discard the update and try again in 15-sec
                check_gps = self._update_last_latitude_longitude(
                        devicename,
                        latitude,
                        longitude,
                        (f"iOSApp-{update_reason}"))

                if check_gps is False:
                    self.any_device_being_updated_flag = False
                    return ICLOUD_UPDATE

                self.count_update_iosapp[devicename] += 1
                self.last_battery[devicename]      = battery
                self.last_gps_accuracy[devicename] = gps_accuracy
                self.last_located_time[devicename] = self._time_to_12hrtime(timestamp)

                if altitude is None:
                    altitude = 0

                attrs[ATTR_LAST_LOCATED]   = self._secs_to_timestamp(timestamp_secs)
                attrs[ATTR_DEVICE_STATUS]  = self.device_status.get(devicename)
                attrs[ATTR_LOW_POWER_MODE] = low_power_mode
                attrs[ATTR_BATTERY]        = battery
                attrs[ATTR_BATTERY_STATUS] = battery_status
                attrs[ATTR_ALTITUDE]       = round(altitude, 2)
                attrs[ATTR_VERT_ACCURACY]  = vertical_accuracy
                attrs[ATTR_POLL_COUNT]     = self._format_poll_count(devicename)

            except Exception as err:
                _LOGGER.exception(err)

            try:
                kwargs = self._setup_base_kwargs(
                    devicename,
                    latitude,
                    longitude,
                    battery,
                    gps_accuracy)

                self._update_device_attributes(devicename, kwargs, attrs, 'Final Update')
                self._update_device_sensors(devicename, kwargs)
                self._update_device_sensors(devicename, attrs)
                self._update_stationary_zone_location(devicename)

                self.seen_this_device_flag[devicename]     = True
                self.device_being_updated_flag[devicename] = False

            except Exception as err:
                _LOGGER.exception(err)
                log_msg = (f"{self._format_fname_devtype(devicename)} "
                           f"Error Updating Device, {err}")
                self._log_error_msg(log_msg)
                return_code = ICLOUD_UPDATE

            try:
                event_msg = (f"IOS App update complete")
                self._save_event(devicename, event_msg)

                self._log_start_finish_update_banner('▲▲▲', devicename,  "iOSApp", update_reason)

                entity_id = self.device_tracker_entity_ic3.get(devicename)
                ic3dev_attrs = self._get_device_attributes(entity_id)

                return_code = IOSAPP_UPDATE

            except KeyError as err:
                self._internal_error_msg(fct_name, err, 'iosUpdateMsg')
                return_code = ICLOUD_UPDATE

        except Exception as err:
            _LOGGER.exception(err)
            self._internal_error_msg(fct_name, err, 'OverallUpdate')
            self.device_being_updated_flag[devicename] = False
            return_code = ICLOUD_UPDATE

        self.any_device_being_updated_flag = False

        return return_code

#########################################################
#
#   Using the iosapp tracking method or iCloud is disabled
#   so trigger the osapp to send a
#   location transaction
#
#########################################################
    def _iosapp_request_loc_update(self, devicename, reissue_msg=""):
        '''
        Send location request to phone. Check to see if one has been sent but not responded to
        and, if true, set interval based on the retry count.
        '''

        try:
            #Save initial sent time if not sent before, otherwise increase retry cnt and
            #set new interval time
            if self.iosapp_request_loc_sent_flag.get(devicename) is False:
                self.iosapp_request_loc_sent_secs[devicename] = self.this_update_secs
                self.iosapp_request_loc_retry_cnt[devicename] = 0
            else:
                self.iosapp_request_loc_retry_cnt[devicename] += 1

            location_age = self.location_data.get(devicename)[ATTR_AGE]

            event_msg = (f"Requesting iOSApp Location #{self.iosapp_request_loc_retry_cnt.get(devicename)} > "
                         f"LastLocTime-")
            if location_age > 604800:
                event_msg += (f"Never (Initial Locate)")
            else:
                event_msg += (f"{self._format_time_age(self.location_data.get(devicename)[ATTR_TIMESTAMP_SECS])}")

            if self.iosapp_request_loc_retry_cnt.get(devicename) > 0:
                event_msg += (f", LastRequested-{self._format_time_age(self.iosapp_request_loc_sent_secs.get(devicename))}")

                if self.iosapp_request_loc_retry_cnt.get(devicename) > 10:
                    event_msg += ", May be offline/asleep"

                self._determine_interval_after_error(
                    devicename,
                    event_msg,
                    counter=IOSAPP_REQUEST_LOC_CNT)

            self.iosapp_request_loc_sent_flag[devicename] = True
            self.iosapp_request_loc_cnt[devicename] += 1

            message = {"message": "request_location_update"}
            return_code = self._send_message_to_device(devicename, message)

            #self.hass.async_create_task(
            #    self.hass.services.async_call('notify',  entity_id, service_data))

            self._save_event_halog_info(devicename, event_msg)

            if return_code:
                attrs = {}
                attrs[ATTR_POLL_COUNT] = self._format_poll_count(devicename)
                attrs[ATTR_INFO] = event_msg
                self._update_device_sensors(devicename, attrs)
            else:
                event_msg = f"{EVLOG_NOTICE}{event_msg} > Failed to send message"
                self._save_event_halog_info(devicename, event_msg)

        except Exception as err:
            _LOGGER.exception(err)
            error_msg = (f"iCloud3 Error > An error occurred sending a location request > "
                         f"Device-{self.notify_iosapp_entity.get(devicename)}, Error-{err}")
            self._save_event_halog_error(devicename, error_msg)


#########################################################
#
#   This function is called every 15 seconds. Cycle through all
#   of the iCloud devices to see if any of the ones being tracked need
#   to be updated. If so, we might as well update the information for
#   all of the devices being tracked since PyiCloud gets data for
#   every device in the account.
#
#########################################################
    def _polling_loop_15_sec_icloud(self, now):
        """Called every 15-sec to check iCloud update"""

        if self.any_device_being_updated_flag:
            return
        elif self.TRK_METHOD_IOSAPP:
            return

        fct_name = "_polling_loop_15_sec_icloud"

        self.this_update_secs = self._time_now_secs()
        this_update_time = dt_util.now().strftime(self.um_time_strfmt)

        try:
            for devicename in self.tracked_devices:
                update_reason = "Location Update"
                devicename_zone = self._format_devicename_zone(devicename, HOME)
                update_via_other_devicename = None

                if (devicename_zone not in self.next_update_secs
                        or devicename_zone not in self.next_update_time):
                    continue
                elif self._is_device_paused(devicename):
                    continue
                elif (self.state_this_poll.get(devicename) == NOT_SET
                        and self.next_update_secs.get(devicename_zone) > self.this_update_secs):
                    continue

                self.iosapp_update_flag[devicename] = False
                update_method = None
                event_msg = ""

                # If the state changed since last poll, force an update
                # This can be done via device_tracker.see service call
                # with a different location_name in an automation or
                # from entering a zone via the IOS App.
                entity_id = self.device_tracker_entity_ic3.get(devicename)
                state     = self._get_state(entity_id)

                if state != self.state_last_poll.get(devicename):
                    update_method = ICLOUD_UPDATE
                    update_reason = "State Change"
                    event_msg     = (f"State Change detected for {devicename} > "
                                     f"{self.state_last_poll.get(devicename)} to "
                                     f"{state}")
                    self._save_event_halog_info(devicename, event_msg)

                if update_method == ICLOUD_UPDATE:
                    if 'nearzone' in state:
                        state = 'near_zone'

                    self.state_this_poll[devicename] = state
                    self.next_update_secs[devicename_zone] = 0

                    attrs  = {}
                    attrs[ATTR_INTERVAL]           = '0 sec'
                    attrs[ATTR_NEXT_UPDATE_TIME]   = TIMESTAMP_ZERO
                    self._update_device_sensors(devicename, attrs)

                #This flag will be 'true' if the last update for this device
                #was not completed. Do another update now.
                if (self.device_being_updated_flag.get(devicename)
                        and self.device_being_updated_retry_cnt.get(devicename) > 4):
                    self.device_being_updated_flag[devicename] = False
                    self.device_being_updated_retry_cnt[devicename] = 0

                    log_msg = (f"{self._format_fname_devtype(devicename)} Cancelled update retry")
                    self._log_info_msg(log_msg)

                if self._is_in_zone_and_before_next_update(devicename):
                    continue

                elif self.device_being_updated_flag.get(devicename):
                    update_method = ICLOUD_UPDATE
                    self.device_being_updated_retry_cnt[devicename] += 1

                    update_reason = "Retry Last Update"
                    event_msg     = (f"{self._format_tracking_method(devicename)} update not completed, retrying")
                    self._save_event_halog_info(devicename, event_msg)

                elif self.next_update_secs.get(devicename_zone) == 0:
                    update_method = ICLOUD_UPDATE
                    update_reason = "State Change/Resume"
                    event_msg     = "State Change or Resume Polling Requested"
                    self._save_event(devicename, event_msg)

                else:
                    update_via_other_devicename = self._is_next_update_time_reached()
                    if (update_via_other_devicename != devicename
                            and self.poor_location_gps_cnt.get(devicename) > 0
                            and self.next_update_secs.get(devicename_zone) > self.this_update_secs):
                        pass

                    elif update_via_other_devicename:
                        retry_suffix = "" if self.poor_location_gps_cnt.get(devicename) == 0 else " (Retry)"
                        update_method = ICLOUD_UPDATE
                        update_reason = f"Next Update Time reached{retry_suffix}"
                        self.trigger[devicename] = f"NextUpdateTime{retry_suffix}"
                        event_msg = (f"{update_reason} > {update_via_other_devicename}")
                        self._save_event(devicename, event_msg)

                    elif update_method == ICLOUD_UPDATE:
                        retry_suffix = "" if self.poor_location_gps_cnt.get(devicename) == 0 else " (Retry)"
                        event_msg = (f"Next Update Time reached{retry_suffix} > {devicename}")
                        self._save_event(devicename, event_msg)

                if update_method == ICLOUD_UPDATE:
                    self._wait_if_update_in_process()
                    self.update_in_process_flag = True

                    if self._is_authentication_2fa_code_needed():
                        #Only display error once
                        if instr(self.info_notification, "ICLOUD"):
                            self.update_in_process_flag = False
                            return

                        self.info_notification = (f"THE ICLOUD 2FA CODE IS NEEDED TO VERIFY "
                                                    f"THE ACCOUNT FOR {self.username}")
                        for devicename in self.tracked_devices:
                            self._display_info_status_msg(devicename, self.info_notification)

                            log_msg = (f"iCloud3 Error > The iCloud 2fa code for account "
                                    f"{self.username} needs to be verified. Use the HA "
                                    f"Notifications area on the HA Sidebar at the bottom "
                                    f"the HA main screen.")
                            self._save_event_halog_error(devicename, log_msg)

                            if self.api.requires_2fa:
                                self._icloud_2fa1_show_verification_code_entry_form()
                        return

                    self._update_device_icloud(update_reason, update_via_other_devicename)

                self.update_in_process_flag = False

        except Exception as err:       #ValueError:
            _LOGGER.exception(err)

            try:
                log_msg = ("iCloud/FmF API Error, will reauthenticate and retry")
                self._log_error_msg(log_msg)

                self._pyicloud_authenticate_account()

                self.authenticated_time = time.time()
                self._update_device_icloud('iCloud/FmF Reauth', update_via_other_devicename)    #Retry update devices

                self.update_in_process_flag = False

            except Exception as err:       #ValueError:
                _LOGGER.exception(err)


#########################################################
#
#   Cycle through all iCloud devices and update the information for the devices
#   being tracked
#     ●►●◄►●▬▲▼◀►►●◀ oPhone=►▶
#########################################################
    def _update_device_icloud(self, update_reason='Check iCloud',
            arg_devicename=None, arg_via_other_devicename=None):

        """
        Request device information from iCloud (if needed) and update
        device_tracker information.

        arg_devicename -
                None     = Update all devices
                Not None = Update specified device
        arg_other-devicename -
                None     = Update all devices
                Not None = One device in the list reached the next update time.
                           Do not update another device that now has poor location
                           gps after all the results have been determined if
                           their update time has not been reached.

        """

        if self.TRK_METHOD_IOSAPP:
            return
        elif (self.start_icloud3_inprocess_flag and update_reason != 'Initial Locate'):
            return
        elif self.any_device_being_updated_flag:
            return
        fct_name = "_update_device_icloud"

        self.any_device_being_updated_flag = True
        self.base_zone                     = HOME

        try:
            for devicename in self.tracked_devices:
                zone    = self.zone_current.get(devicename)
                devicename_home_zone = self._format_devicename_zone(devicename)

                if arg_devicename and devicename != arg_devicename:
                    continue
                elif (devicename_home_zone not in self.next_update_secs
                        or devicename_home_zone not in self.next_update_time):
                    continue
                elif self._is_device_paused(devicename):
                    continue
                elif (update_reason == 'Initial Locate'
                        and (self.poor_location_gps_cnt.get(devicename) > 35
                            or self.count_discarded_update.get(devicename) > 125)):
                    continue
                elif (self.state_this_poll.get(devicename) == NOT_SET
                        and self.next_update_secs.get(devicename_home_zone) > self.this_update_secs):
                    continue

                #If the device is in a zone, and was in the same zone on the
                #last poll of another device on the account and this device
                #update time has not been reached, do not update device
                #information. Do this in case this device currently has bad gps
                #and really doesn't need to be polled at this time anyway.
                #If the iOS App triggered the update and it was not done by the
                #iosapp_update routine, do one now anyway.
                if (self._is_in_zone_and_before_next_update(devicename)
                        and arg_devicename is None):
                    continue

                event_msg = (f"{self._format_tracking_method(devicename)} update started ({update_reason.split('@')[0]})")
                self._save_event_halog_debug(devicename, event_msg)

                self._log_start_finish_update_banner('▼▼▼', devicename, "iCloud", update_reason)

                self.update_timer[devicename] = time.time()
                self.iosapp_request_loc_sent_secs[devicename] = 0
                do_not_update_flag = False
                location_time      = 0

                #Updating device info. Get data from FmF or FamShr and update
                #if self.TRK_METHOD_FMF:
                if self._devicename_fmf(devicename):
                    valid_data_flag = self._get_fmf_data(devicename)

                elif self._devicename_famshr(devicename):
                    valid_data_flag = self._get_famshr_data(devicename)

                #An error ocurred accessing the iCloud account. This can be a
                #Authentication error or an error retrieving the loction data
                #if ic3dev_data[0] is False:
                if valid_data_flag == ICLOUD_LOCATION_DATA_ERROR:
                    self.icloud_acct_auth_error_cnt += 1
                    self._determine_interval_after_error(
                        devicename,
                        "iCloud Offline (Authentication or Location Error)",
                        counter=AUTH_ERROR_CNT)

                    if (self.interval_seconds.get(devicename) != 15
                            and self.icloud_acct_auth_error_cnt > 2):
                        log_msg = ("iCloud3 Error > An error occurred accessing "
                            f"the iCloud account {self.username} for {devicename}. "
                            "This can be an account "
                            "authentication issue or no location data is "
                            "available. Retrying at next update time. "
                            f"Retry #{self.icloud_acct_auth_error_cnt}")
                        self._save_event_halog_error("*", log_msg)
                        if self.icloud_acct_auth_error_cnt > 6:
                            self._pause_device(devicename)
                            self.icloud_acct_auth_error_cnt = 0

                    if self.icloud_acct_auth_error_cnt > 20:
                        self._setup_tracking_method(IOSAPP)
                        log_msg = ("iCloud3 Error > More than 20 iCloud Authentication "
                            "errors. Resetting to use tracking_method <iosapp>. "
                            "Restart iCloud3 at a later time to see if iCloud "
                            "Loction Services is available.")
                        self._save_event_halog_error("*", log_msg)

                    break
                else:
                    self.icloud_acct_auth_error_cnt = 0

                #icloud data overrules device data which may be stale
                location_data = self.location_data.get(devicename)
                latitude      = location_data[ATTR_LATITUDE]
                longitude     = location_data[ATTR_LONGITUDE]
                gps_accuracy  = 0
                poor_location_gps_flag = False

                if latitude != 0 and longitude != 0:
                    timestamp_secs      = location_data[ATTR_TIMESTAMP_SECS]
                    last_located_secs   = location_data[ATTR_TIMESTAMP_SECS]
                    location_time       = location_data[ATTR_TIMESTAMP_TIME]
                    location_age        = self._secs_since(timestamp_secs)
                    battery             = location_data[ATTR_BATTERY_LEVEL]
                    battery_status      = location_data[ATTR_BATTERY_STATUS]
                    device_status       = location_data[ATTR_DEVICE_STATUS]
                    low_power_mode      = location_data[ATTR_LOW_POWER_MODE]
                    altitude            = location_data[ATTR_ALTITUDE]
                    gps_accuracy        = location_data[ATTR_GPS_ACCURACY]
                    vertical_accuracy   = location_data[ATTR_VERT_ACCURACY]

                    self.location_data[devicename][ATTR_BATTERY_LEVEL] = battery
                    self.last_located_secs[devicename] = last_located_secs
                    self.location_data[devicename][ATTR_AGE] = location_age
                    self.device_status[devicename]     = device_status

                    poor_location_gps_flag, discard_reason = self._check_poor_location_gps(
                            devicename,
                            last_located_secs,
                            gps_accuracy)

                #Discard if no location coordinates
                if latitude == 0 or longitude == 0:
                    location_time = NEVER
                    location_age  = HIGH_INTEGER
                    self.poor_location_gps_cnt[devicename] += 1
                    poor_location_flag = True
                    discard_reason     = (f"No location data "
                                          f"(#{self.poor_location_gps_cnt.get(devicename)})")
                    device_offline_msg = (f"May be Offline, No Location "
                                         f"(#{self.poor_location_gps_cnt.get(devicename)})")
                    info_msg           = discard_reason
                    do_not_update_flag = True

                #Check to see if currently in a zone. If so, check the zone distance.
                #If new location is outside of the zone and inside radius*4, discard
                #by treating it as poor GPS
                elif (self._isnot_inzone_zonename(zone)
                        or self.state_this_poll.get(devicename) == NOT_SET):
                    outside_no_exit_trigger_flag = False
                    info_msg= ''
                else:
                    outside_no_exit_trigger_flag, info_msg = \
                        self._is_outside_zone_no_exit(devicename, zone, '',
                                latitude, longitude)

                if self.icloud_acct_auth_error_cnt > 0:
                    event_msg = (f"iCloud Authentication Problem (#{self.icloud_acct_auth_error_cnt}) > "
                                 f"Location data may be old")
                    self._save_event(devicename, event_msg)

                if do_not_update_flag:
                    pass

                #Ignore old location when in a zone and ignore=True
                #let normal next time update check process
                elif (poor_location_gps_flag
                        and self._is_inzone(devicename)
                        and self.ignore_gps_accuracy_inzone_flag):
                    self.poor_location_gps_cnt[devicename] -= 1
                    location_age_str = "" if location_time == NEVER else (f" ({self._format_age(location_age)})")
                    event_msg = (f"Poor Loc/GPS Accuracy exception (will process) > "
                                 f"IgnoreInzoneAccuracy=True, InzoneFlag=True, "
                                 f"NextUpdate-{self.next_update_time.get(self._format_devicename_zone(devicename))}, "
                                 f"(Not reached), "
                                 f"GPS-{format_gps(latitude, longitude, gps_accuracy)}, "
                                 f"LocationTime-{location_time}{location_age_str}")
                    self._save_event(devicename, event_msg)

                elif self._device_offline(devicename):
                    do_not_update_flag = True
                    info_msg = "Device Offline"
                    event_msg = (f"Device Status Exception, Tracking may be delayed > {devicename} "
                                 f"Status-{self.device_status.get(devicename)}")
                    self._save_event(devicename, event_msg)

                #Outside zone, no exit trigger check
                elif outside_no_exit_trigger_flag:
                    self.poor_gps_flag[devicename] = True
                    self.poor_location_gps_cnt[devicename] += 1
                    do_not_update_flag = True

                #Discard if location is old or poor gps
                elif poor_location_gps_flag:
                    info_msg = (f"{discard_reason}")
                    do_not_update_flag = True

                #discard if outside home zone and less than zone_radius+self.gps_accuracy_threshold due to gps errors
                dist_from_home_m = self._calc_distance_m(latitude, longitude,
                                            self.zone_home_lat, self.zone_home_long)

                if do_not_update_flag:
                    self._determine_interval_after_error(devicename, info_msg, gps_accuracy=gps_accuracy)

                    location_age_str = "" if location_time == NEVER else (f" ({self._format_age(location_age)})")
                    event_msg = (f"Discarded > {info_msg} > "
                                 f"GPS-{format_gps(latitude, longitude, gps_accuracy)}, "
                                 f"Located-{location_time}{location_age_str}, "
                                 f"NextUpdate-{self.next_update_time.get(self._format_devicename_zone(devicename))}, "
                                 f"OldLocThreshold-{self._secs_to_time_str(self.old_location_secs.get(devicename))}")
                    if self._device_offline(devicename):
                        event_msg += (f", DeviceStatus-{self.device_status.get(devicename)}")
                    #self._save_event(devicename, event_msg)

                    self._log_start_finish_update_banner('▲▲▲', devicename, "iCloud", update_reason)
                    continue

                #--------------------------------------------------------
                try:
                    if self.device_being_updated_flag.get(devicename):
                        info_msg  = "Retrying > Last update not completed"
                        event_msg = info_msg
                    else:
                        info_msg = "Updating"
                        event_msg = (f"Located Device > GPS-{format_gps(latitude, longitude, gps_accuracy)}, "
                            f"LocTime-{location_time} ({self._format_age(location_age)})")
                    #        f"LocTime-{location_time} ({self._format_age(location_age)})")
                    info_msg = f"{info_msg} {self.fname.get(devicename)}"
                    self._display_info_status_msg(devicename, info_msg)
                    self._save_event(devicename, event_msg)

                    #set device being updated flag. This is checked in the
                    #'_polling_loop_15_sec_icloud' loop to make sure the last update
                    #completed successfully (Waze has a compile error bug that will
                    #kill update and everything will sit there until the next poll.
                    #if this is still set in '_polling_loop_15_sec_icloud', repoll
                    #immediately!!!
                    self.device_being_updated_flag[devicename] = True

                except Exception as err:
                    attrs = self._internal_error_msg(fct_name, err, 'UpdateAttrs1')

                try:
                    for zone in self.track_from_zones.get(devicename):
                        self._set_base_zone_name_lat_long_radius(zone)

                        self._log_start_finish_update_banner('▼-▼', devicename,
                                self._format_tracking_method(devicename), zone)
                        self.location_data[devicename][ATTR_BATTERY_LEVEL] = battery
                        attrs = self._determine_interval(
                                    devicename,
                                    latitude,
                                    longitude,
                                    battery,
                                    gps_accuracy,
                                    poor_location_gps_flag,
                                    last_located_secs,
                                    location_time,
                                    "icld")
                        if attrs != {}:
                            self._update_device_sensors(devicename, attrs)

                        self._log_start_finish_update_banner('▲-▲', devicename,
                            self._format_tracking_method(devicename), zone)

                except Exception as err:
                    attrs = self._internal_error_msg(fct_name, err, 'DetInterval')
                    continue

                try:
                    #Note: Final prep and update device attributes via
                    #device_tracker.see. The gps location, battery, and
                    #gps accuracy are not part of the attrs variable and are
                    #reformatted into device attributes by 'See'. The gps
                    #location goes to 'See' as a "(latitude, longitude)" pair.
                    #'See' converts them to ATTR_LATITUDE and ATTR_LONGITUDE
                    #and discards the 'gps' item.
                    log_msg = (f"LOCATION ATTRIBUTES, "
                               f"State-{self.state_last_poll.get(devicename)}, "
                               f"Attrs-{attrs}")
                    self._log_debug_msg(devicename, log_msg)

                    self.count_update_icloud[devicename] += 1
                    if not poor_location_gps_flag:
                        self._update_last_latitude_longitude(
                                devicename, latitude, longitude,
                                (f"iCloud-{update_reason}"))

                    if altitude is None:
                        altitude = -2

                    #attrs[ATTR_DEVICE_STATUS]  = device_status
                    attrs[ATTR_DEVICE_STATUS]  = self.device_status.get(devicename)
                    attrs[ATTR_LOW_POWER_MODE] = low_power_mode
                    attrs[ATTR_BATTERY]        = battery
                    attrs[ATTR_BATTERY_STATUS] = battery_status
                    attrs[ATTR_ALTITUDE]       = round(altitude, 2)
                    attrs[ATTR_VERT_ACCURACY]  = vertical_accuracy
                    attrs[ATTR_POLL_COUNT]     = self._format_poll_count(devicename)
                    attrs[ATTR_AUTHENTICATED]  = self._secs_to_timestamp(self.authenticated_time)

                except Exception as err:
                    attrs = self._internal_error_msg(fct_name, err, 'SetAttrs')

                try:
                    kwargs = self._setup_base_kwargs(devicename,
                        latitude, longitude, battery, gps_accuracy)

                    self._update_device_attributes(devicename, kwargs, attrs, 'Final Update')
                    self._update_device_sensors(devicename, kwargs)
                    self._update_device_sensors(devicename, attrs)
                    self._update_stationary_zone_location(devicename)

                    self.seen_this_device_flag[devicename]     = True
                    self.device_being_updated_flag[devicename] = False

                except Exception as err:
                    log_msg = (f"{self._format_fname_devtype(devicename)} Error Updating Device, {err}")
                    self._log_error_msg(log_msg)

                    _LOGGER.exception(err)

                try:
                    event_msg = (f"{self._format_tracking_method(devicename)} update completed")
                    self._save_event(devicename, event_msg)

                    self._log_start_finish_update_banner('▲▲▲', devicename, "iCloud", update_reason)

                except KeyError as err:
                    self._internal_error_msg(fct_name, err, 'icloudUpdateMsg')

        except Exception as err:
            _LOGGER.exception(err)
            self._internal_error_msg(fct_name, err, 'OverallUpdate')
            self.device_being_updated_flag[devicename] = False

        self.any_device_being_updated_flag = False

#########################################################
#
#   Get iCloud device & location info when using the
#   FmF (Find-my-Friends / Find Me) tracking method.
#
#########################################################
    def _get_fmf_data(self, devicename):
        '''
        Get the location data from Find My Friends.

        location_data-{
            'locationStatus': None,
            'location': {
                'isInaccurate': False,
                'altitude': 0.0,
                'address': {'formattedAddressLines': ['123 Main St',
                    'Your City, NY', 'United States'],
                    'country': 'United States',
                    'streetName': 'Main St,
                    'streetAddress': '123 Main St',
                    'countryCode': 'US',
                    'locality': 'Your City',
                    'stateCode': 'NY',
                    'administrativeArea': 'New York'},
                'locSource': None,
                'latitude': 12.34567890,
                'floorLevel': 0,
                'horizontalAccuracy': 65.0,
                'labels': [{'id': '79f8e34c-d577-46b4-a6d43a7b891eca843',
                    'latitude': 12.34567890,
                    'longitude': -45.67890123,
                    'info': None,
                    'label': '_$!<home>!$_',
                    'type': 'friend'}],
                'tempLangForAddrAndPremises': None,
                'verticalAccuracy': 0.0,
                ATTR_ICLOUD_BATTERY_STATUS: None,
                'locationId': 'a6b0ee1d-be34-578a-0d45-5432c5753d3f',
                'locationTimestamp': 0,
                'longitude': -45.67890123,
                'timestamp': 1562512615222},
            'id': 'NDM0NTU2NzE3',
            'status': None}
        '''

        fct_name = "_get_fmf_data"
        from .pyicloud_ic3 import PyiCloudNoDevicesException

        log_msg = (f"= = = Prep Data From FmF = = = (Now-{self.this_update_secs})")
        self._log_debug_msg(devicename, log_msg)

        try:
            self._display_info_status_msg(devicename, "Getting iCloud Location")
            location_data = self.location_data.get(devicename)
            location_age = location_data[ATTR_AGE]

            log_msg = (f"LOCATION DATA-{location_data})")
            self._log_debug_msg(devicename, log_msg)

            if location_age > self.old_location_secs.get(devicename):
                if self._refresh_pyicloud_devices_location_data(location_age, devicename):
                    self._display_info_status_msg(devicename, "Location Data Old, Refreshing")
                    location_data = self.location_data.get(devicename)

                    evlog_msg = (f"Refreshed FmF iCloud location data")
                    self._evlog_debug_msg(devicename, evlog_msg)
                else:
                    self._display_info_status_msg(devicename, "No iCloud Location Available")
                    if self.icloud_acct_auth_error_cnt > 3:
                        self._log_error_msg(f"iCloud3 Error > No Location Data "
                                           f"Returned for {devicename}")
                    return ICLOUD_LOCATION_DATA_ERROR

            if self._device_online(devicename):
                self._display_info_status_msg(devicename, "iCloud Location Data Available")

            return True

        except Exception as err:
            _LOGGER.exception(err)
            self._log_error_msg("General iCloud Location Data Error")
            return ICLOUD_LOCATION_DATA_ERROR

#########################################################
#
#   Get iCloud device & location info when using the
#   FamShr (Family Sharing) tracking method.
#
#########################################################
    def _get_famshr_data(self, devicename):
        '''
        Extract the data needed to determine location, direction, interval,
        etc. from the iCloud data set.

        Sample data set is:
            {'isOld': False, 'isInaccurate': False, 'altitude': 0.0, 'positionType': 'Wifi',
            'latitude': 27.72690098883266, 'floorLevel': 0, 'horizontalAccuracy': 65.0,
            'locationType': '', 'timeStamp': 1587306847548, 'locationFinished': True,
            'verticalAccuracy': 0.0, 'longitude': -80.3905776599289}
        '''

        fct_name = "_get_famshr_data"

        log_msg = (f"= = = Prep Data From FamShr = = = (Now-{self.this_update_secs})")
        self._log_debug_msg(devicename, log_msg)

        try:
            self._display_info_status_msg(devicename, "Getting iCloud Location")
            location_data = self.location_data.get(devicename)
            location_age  = location_data[ATTR_AGE]

            log_msg = (f"LOCATION DATA-{location_data})")
            self._log_debug_msg(devicename, log_msg)


            if location_age > self.old_location_secs.get(devicename):
                if self._refresh_pyicloud_devices_location_data(location_age, devicename):
                    self._display_info_status_msg(devicename, "Location Data Old, Refreshing")
                    location_data = self.location_data.get(devicename)

                    evlog_msg = (f"Refreshed FamShr iCloud location data")
                    self._evlog_debug_msg(devicename, evlog_msg)
                else:
                    self._display_info_status_msg(devicename, "No iCloud Location Available")
                    if self.icloud_acct_auth_error_cnt > 3:
                        self._log_error_msg(f"iCloud3 Error > No Location Data "
                                           f"Returned for {devicename}")
                    return ICLOUD_LOCATION_DATA_ERROR
            self._display_info_status_msg(devicename, "iCloud Location Data Available")
            return True

        except Exception as err:
            _LOGGER.exception(err)
            self._log_error_msg("General iCloud FamShr Location Data Error")
            return ICLOUD_LOCATION_DATA_ERROR

#----------------------------------------------------------------------------
    def _refresh_pyicloud_devices_location_data(self, location_age, arg_devicename):
        '''
        Authenticate pyicloud & refresh device & location data. This calls the
        function to update 'self.location_data' for each device being tracked.

        Return: True if device data was updated successfully
                False if api error or no device data returned
        '''

        try:
            event_msg=(f"Requesting New iCloud Location > LastLocTime-")
            if location_age > 604800:
                event_msg += (f"Never (Initial Locate)")
            else:
                event_msg += (f"{self._format_time_age(self.location_data.get(arg_devicename)[ATTR_TIMESTAMP_SECS])}")
            self._save_event_halog_info(arg_devicename, event_msg)

            exit_get_data_loop = False
            authenticated_pyicloud_flag = False
            self.count_pyicloud_location_update += 1
            pyicloud_start_call_time = time.time()

            while exit_get_data_loop is False:
                try:
                    if self.api is None:
                        return False

                    log_msg = (f"UPDATE LOC DEV TRK METHOD > {self.devicename_tracking_method}")
                    self._log_debug_msg(arg_devicename, log_msg)
                    log_msg = (f"UPDATE LOC DEVICE ID > {self.devicename_by_device_id}")
                    self._log_debug_msg(arg_devicename, log_msg)

                    if self._devicename_fmf(arg_devicename):
                        devices_data = self.api.friends.refresh_client()
                        if devices_data:
                            for location in devices_data['locations']:
                                if ATTR_LOCATION in location:
                                    device_id  = location['id']
                                    devicename = self.devicename_by_device_id.get(device_id, None)
                                    log_msg = (f"UPDATE LOC DATA (FAMSHR) > {devicename}, "
                                                f"id-{device_id} from-{arg_devicename}")
                                    self._log_debug_msg(arg_devicename, log_msg)
                                    if devicename:
                                        self._update_location_data(devicename, location)

                    elif self._devicename_famshr(arg_devicename):
                        device_id = self.devicename_device_id.get(arg_devicename)
                        devices_data = self.api.devices.response["content"]
                        if devices_data:
                            for device_data in devices_data:
                                if device_data:
                                    device_id  = device_data['id']
                                    devicename = self.devicename_by_device_id.get(device_id, None)
                                    log_msg = (f"UPDATE LOC DATA (FAMSHR) > {devicename}, name-{device_data[ATTR_NAME]}, "
                                                f"id-{device_id} from-{arg_devicename}")
                                    self._log_debug_msg(arg_devicename, log_msg)
                                    if devicename:
                                        self._update_location_data(devicename, device_data)

                except PyiCloud2SARequiredException as err:
                    if authenticated_pyicloud_flag:
                        return False

                    authenticated_pyicloud_flag = True
                    self._pyicloud_authenticate_account(devicename=arg_devicename)

                except PyiCloudAPIResponseException as err:
                    if authenticated_pyicloud_flag:
                        return False

                    authenticated_pyicloud_flag = True
                    self._pyicloud_authenticate_account(devicename=arg_devicename)

                except Exception as err:
                    _LOGGER.exception(err)

                else:
                    exit_get_data_loop = True

            self._check_authentication_message(arg_devicename)

            update_took_time = time.time() - pyicloud_start_call_time
            self.time_pyicloud_calls += update_took_time


            return True

        except Exception as err:
            _LOGGER.exception(err)

        return False

#----------------------------------------------------------------------------
    def _update_location_data(self, devicename, device_data):
        '''
        Extract the location_data dictionary table from the device
        data returned from pyicloud for the devicename device. This data is used to
        determine the update interval, accuracy, location, etc.
        '''
        try:
            if device_data is None:
                return False
            elif ATTR_LOCATION not in device_data:
                return False
            elif device_data[ATTR_LOCATION] == {}:
                return
            elif device_data[ATTR_LOCATION] is None:
                return
            elif self._is_device_paused(devicename):
                return

            self._log_rawdata("update_location_data (device_data)", device_data)

            try:
                timestamp_field = ATTR_TIMESTAMP if self._devicename_fmf(devicename) else ATTR_ICLOUD_TIMESTAMP
                timestamp_secs  = device_data[ATTR_LOCATION][timestamp_field] / 1000
                last_loc_timestamp_secs = self.location_data.get(devicename)[ATTR_TIMESTAMP_SECS]
                if timestamp_secs < last_loc_timestamp_secs:
                    location_age = self._secs_since(timestamp_secs)
                    event_msg = (f"Discarded Update > This Update Request Returned Older Location > "
                                 f"CurrentLocation-{self._format_time_age(last_loc_timestamp_secs)}), "
                                 f"RequestReturned-{self._format_time_age(timestamp_secs)}")
                    self._save_event_halog_debug(devicename, event_msg)
                    return

            except:
                timestamp_secs = self.location_data.get(devicename)[ATTR_TIMESTAMP_SECS]
                self.location_data[devicename][ATTR_AGE] = self._secs_since(timestamp_secs)
                event_msg = (f"iCloud Locate Exception > Data not returned, "
                            f"LastLocTime-{self._format_time_age(timestamp_secs)}")
                return

            iosapp_battery = self.last_battery.get(devicename, -1)
            icloud_battery = int(device_data.get(ATTR_ICLOUD_BATTERY_LEVEL, 0) * 100)

            location_data                      = {}
            location_data[ATTR_NAME]           = device_data.get(ATTR_NAME, "")
            location_data[ATTR_DEVICE_CLASS]   = device_data.get(ATTR_ICLOUD_DEVICE_CLASS, "")
            location_data[ATTR_BATTERY_LEVEL]  = icloud_battery if icloud_battery > 0 else iosapp_battery
            location_data[ATTR_BATTERY_STATUS] = device_data.get(ATTR_ICLOUD_BATTERY_STATUS, "")

            device_status_code                 = device_data.get(ATTR_ICLOUD_DEVICE_STATUS, 0)
            location_data[ATTR_DEVICE_STATUS]  = DEVICE_STATUS_CODES.get(device_status_code, "")
            location_data[ATTR_LOW_POWER_MODE] = device_data.get(ATTR_ICLOUD_LOW_POWER_MODE, "")

            location                           = device_data[ATTR_LOCATION]
            location_data[ATTR_TIMESTAMP_SECS] = timestamp_secs
            location_data[ATTR_TIMESTAMP_TIME] = self._secs_to_time(timestamp_secs)
            location_data[ATTR_AGE]            = self._secs_since(timestamp_secs)
            location_data[ATTR_LATITUDE]       = location.get(ATTR_LATITUDE, 0)
            location_data[ATTR_LONGITUDE]      = location.get(ATTR_LONGITUDE, 0)
            location_data[ATTR_ALTITUDE]       = round(location.get(ATTR_ALTITUDE, 0), 1)
            #location_data[ATTR_ISOLD]          = location.get(ATTR_ISOLD, False)
            location_data[ATTR_GPS_ACCURACY]   = int(round(location.get(ATTR_ICLOUD_HORIZONTAL_ACCURACY, 0), 0))
            location_data[ATTR_VERT_ACCURACY]  = int(round(location.get(ATTR_ICLOUD_VERTICAL_ACCURACY, 0), 0))

            self.location_data[devicename]     = location_data

            debug_msg = (f"UPDATE LOCATION > LocationTime-{self._format_time_age(location_data[ATTR_TIMESTAMP_SECS])}")
            self._log_debug_msg(devicename, debug_msg)
            self._log_debug_msg(devicename, location_data)

            return True

        except Exception as err:
            _LOGGER.exception(err)

        return False

#########################################################
#
#   Calculate polling interval based on zone, distance from home and
#   battery level. Setup triggers for next poll
#
#########################################################
    def _determine_interval(self, devicename, latitude, longitude,
                    battery, gps_accuracy, poor_location_gps_flag,
                    last_located_secs, location_time,
                    ios_icld = ''):
        """Calculate new interval. Return location based attributes"""

        fct_name = "_determine_interval"

        base_zone_home_flag  = (self.base_zone == HOME)
        devicename_zone = self._format_devicename_zone(devicename)

        try:
            location_data = self._get_distance_data(
                devicename,
                latitude,
                longitude,
                gps_accuracy,
                poor_location_gps_flag)

            log_msg = (f"Location_data-{location_data}")
            self._log_debug_interval_msg(devicename, log_msg)

            #Abort and Retry if Internal Error
            if (location_data[0] == ERROR):
                return location_data[1]     #(attrs)

            self._display_info_status_msg(devicename, "● Calculating Tracking Info ●")

            zone                         = location_data[0]
            dir_of_travel                = location_data[1]
            dist_from_zone_km            = location_data[2]
            dist_from_zone_moved_km      = location_data[3]
            dist_last_poll_moved_km      = location_data[4]
            waze_dist_from_zone_km       = location_data[5]
            calc_dist_from_zone_km       = location_data[6]
            waze_dist_from_zone_moved_km = location_data[7]
            calc_dist_from_zone_moved_km = location_data[8]
            waze_dist_last_poll_moved_km = location_data[9]
            calc_dist_last_poll_moved_km = location_data[10]
            waze_time_from_zone          = location_data[11]
            last_dist_from_zone_km       = location_data[12]
            last_dir_of_travel           = location_data[13]
            dir_of_trav_msg              = location_data[14]
            timestamp                    = location_data[15]

            last_located_secs            = self.last_located_secs.get(devicename)

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetLocation')
            return attrs_msg

        try:
            log_msg = (f"DETERMINE INTERVAL Entered, "
                          "location_data-{location_data}")
            self._log_debug_interval_msg(devicename, log_msg)

    #       The following checks the distance from home and assigns a
    #       polling interval in minutes.  It assumes a varying speed and
    #       is generally set so it will poll one or twice for each distance
    #       group. When it gets real close to home, it switches to once
    #       each 15 seconds so the distance from home will be calculated
    #       more often and can then be used for triggering automations
    #       when you are real close to home. When home is reached,
    #       the distance will be 0.

            waze_time_msg = ''
            try:
                calc_interval = round(self._km_to_mi(dist_from_zone_km) / 1.5) * 60
            except:
                calc_interval = 0

            if self.waze_status == WAZE_USED:
                try:
                    waze_interval = round(waze_time_from_zone * 60 * self.travel_time_factor , 0)
                except:
                    waze_interval = 0

            else:
                waze_interval = 0
            interval = 15
            interval_multiplier = 1
            interval_str = ''

            battery10_flag       = (battery > 0 and battery <= 10)
            battery5_flag        = (battery > 0 and battery <= 5)
            inzone_flag          = (self._is_inzone_zonename(zone))
            not_inzone_flag      = (self._isnot_inzone_zonename(zone))
            was_inzone_flag      = (self._was_inzone(devicename))
            wasnot_inzone_flag   = (self._wasnot_inzone(devicename))
            inzone_home_flag     = (zone == self.base_zone)     #HOME)
            was_inzone_home_flag = \
                (self.state_last_poll.get(devicename) == self.base_zone) #HOME)
            near_zone_flag       = (zone == 'near_zone')

            log_msg =  (f"Zone-{zone} ,IZ-{inzone_flag}, NIZ-{not_inzone_flag}, "
                        f"WIZ-{was_inzone_flag}, WNIZ-{wasnot_inzone_flag}, "
                        f"IZH-{inzone_home_flag}, WIZH-{was_inzone_home_flag}, "
                        f"NZ-{near_zone_flag}")
            self._log_debug_interval_msg(devicename, log_msg)

            interval_method  = ''
            log_msg     = ''
            interval_method_im  = ''
            old_location_secs_msg = ''

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetupZone')
            return attrs_msg

        try:
            if inzone_flag:
                #Reset got zone exit trigger since now in a zone for next
                #exit distance check. Also reset Stat Zone timer and dist moved.
                self.got_exit_trigger_flag[devicename] = False
                self.stat_zone_timer[devicename]       = 0
                self.stat_zone_moved_total[devicename] = 0

            #Note: If state is 'near_zone', it is reset to NOT_HOME when
            #updating the device_tracker state so it will not trigger a state chng
            if self.state_change_flag.get(devicename):
                if inzone_flag:
                    if (STATIONARY in zone):
                        interval = self.stat_zone_inzone_interval
                        interval_method = "1-Stationary"
                        log_msg    = f"Zone-{zone}"

                    #inzone & old location
                    elif poor_location_gps_flag and battery10_flag is False:
                        interval = self._get_interval_for_error_retry_cnt(devicename, POOR_LOC_GPS_CNT)
                        interval_method = '1-OldLocPoorGPS'

                    else:
                        interval = self.inzone_interval_secs.get(devicename)
                        interval_method="1-EnterZone"

                #battery < 5% and near zone
                elif (battery5_flag and dist_from_zone_km <= 1):
                    interval = 15
                    dir_of_travel = 'Battery 5%'
                    interval_method="2-Battery5%"

                #battery < 10%
                elif (battery10_flag):
                    interval = self.stat_zone_inzone_interval
                    dir_of_travel = 'Battery <10%'
                    interval_method="2-Battery10%"

                #entered 'near_zone' zone if close to HOME and last is NOT_HOME
                elif (near_zone_flag and wasnot_inzone_flag and
                        calc_dist_from_zone_km < 2):
                    interval = 15
                    dir_of_travel = 'NearZone'
                    interval_method="2-EnterNearZone"

                #entered 'near_zone' zone if close to HOME and last is NOT_HOME
                elif (near_zone_flag and was_inzone_flag
                        and calc_dist_from_zone_km < 2):
                    interval = 15
                    dir_of_travel = 'NearZone'
                    interval_method="2-EnterNearZone"

                #exited HOME zone
                elif (not_inzone_flag and was_inzone_home_flag):
                    interval = 240
                    dir_of_travel = AWAY_FROM
                    interval_method="2-ExitHomeZone"

                #exited 'other' zone
                elif (not_inzone_flag and was_inzone_flag):
                    interval = 120
                    dir_of_travel = 'left_zone'
                    interval_method="2-ExitZone"

                #entered 'other' zone
                else:
                    interval = 240
                    interval_method="2-ZoneChanged"

                log_msg = (f"Zone-{zone}, Last-{self.state_last_poll.get(devicename)}, "
                           f"This-{self.state_this_poll.get(devicename)}")
                self._log_debug_interval_msg(devicename, log_msg)

            #inzone & poor gps & check gps accuracy when inzone
            elif (self.poor_gps_flag.get(devicename)
                   and inzone_flag
                   and self.check_gps_accuracy_inzone_flag):
                interval = 300      #poor accuracy, try again in 5 minutes
                interval_method = '3-PoorGPSinZone'

            elif self.poor_gps_flag.get(devicename):
                interval = self._get_interval_for_error_retry_cnt(devicename, POOR_LOC_GPS_CNT)
                interval_method = '3-PoorGPS'

            elif self.override_interval_seconds.get(devicename) > 0:
                interval = self.override_interval_seconds.get(devicename)
                interval_method = '3-Override'

            elif (STATIONARY in zone):
                interval = self.stat_zone_inzone_interval
                interval_method = "3-Stationary"
                log_msg = f"Zone-{zone}"

            #battery <= 10% and not near home ==> stationary time
            elif (battery10_flag and dist_from_zone_km > 1):
                interval = self.stat_zone_inzone_interval
                interval_method="3-Battery10%"
                dir_of_travel = "Battery <10%"
                log_msg = (f"Battery-{battery}%")

            elif poor_location_gps_flag:
                interval = self._get_interval_for_error_retry_cnt(devicename, POOR_LOC_GPS_CNT)
                interval_method = '3-OldLocPoorGPS'
                log_msg = f"Cnt-{self.poor_location_gps_cnt.get(devicename)}"

            elif (inzone_home_flag
                    or (dist_from_zone_km < .05
                    and dir_of_travel == 'towards')):
                interval = self.inzone_interval_secs.get(devicename)
                interval_method = '3-InHomeZone'
                log_msg = f"Zone-{zone}"

            elif zone == 'near_zone':
                interval = 15
                interval_method = '3-NearZone'
                log_msg = f"Zone-{zone}, Dir-{dir_of_travel}"

            #in another zone and inzone time > travel time
            elif (inzone_flag
                    and self.inzone_interval_secs.get(devicename) > waze_interval):
                interval = self.inzone_interval_secs.get(devicename)
                interval_method = '3-InZone'
                log_msg = f"Zone-{zone}"

            elif dir_of_travel in ('left_zone', NOT_SET):
                interval = 150
                if inzone_home_flag:
                    dir_of_travel = AWAY_FROM
                else:
                    dir_of_travel = NOT_SET
                interval_method = '3-NeedInfo'
                log_msg = f"ZoneLeft-{zone}"

            elif dist_from_zone_km < 2.5 and self.went_3km.get(devicename):
                interval = 15             #1.5 mi=real close and driving
                interval_method = '3-<2.5km'

            elif dist_from_zone_km < 3.5:      #2 mi=30 sec
                interval = 30
                interval_method = '3-<3.5km'

            elif waze_time_from_zone > 5 and waze_interval > 0:
                interval = waze_interval
                interval_method = '3-WazeTime'
                log_msg = f"TimeFmHome-{waze_time_from_zone}"

            elif dist_from_zone_km < 5:        #3 mi=1 min
                interval = 60
                interval_method = '3-<5km'

            elif dist_from_zone_km < 8:        #5 mi=2 min
                interval = 120
                interval_method = '3-<8km'

            elif dist_from_zone_km < 12:       #7.5 mi=3 min
                interval = 180
                interval_method = '3-<12km'


            elif dist_from_zone_km < 20:       #12 mi=10 min
                interval = 600
                interval_method = '3-<20km'

            elif dist_from_zone_km < 40:       #25 mi=15 min
                interval = 900
                interval_method = '3-<40km'

            elif dist_from_zone_km > 150:      #90 mi=1 hr
                interval = 3600
                interval_method = '3->150km'

            else:
                interval = calc_interval
                interval_method = '3-Calculated'
                log_msg = f"Value-{self._km_to_mi(dist_from_zone_km)}/1.5"

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetInterval')

        try:
            #if haven't moved far for X minutes, put in stationary zone
            #determined in get_dist_data with dir_of_travel
            if dir_of_travel == STATIONARY:
                interval = self.stat_zone_inzone_interval
                interval_method += ",5-Stationary"

                if self.in_stationary_zone_flag.get(devicename) is False:
                    rtn_code = self._update_stationary_zone(
                        devicename,
                        latitude,
                        longitude,
                        STAT_ZONE_NEW_LOCATION, '5-Stationary')

                    self.in_stationary_zone_flag[devicename] = rtn_code
                    if rtn_code:
                        self.zone_current[devicename]   = self._format_zone_name(devicename, STATIONARY)
                        self.zone_timestamp[devicename] = dt_util.now().strftime(self.um_date_time_strfmt)
                        interval_method_im  = "●Set.Stationary.Zone"
                        zone            = STATIONARY
                        dir_of_travel   = 'in_zone'
                        inzone_flag     = True
                        not_inzone_flag = False
                    else:
                        dir_of_travel = NOT_SET

            if (dir_of_travel in ('', AWAY_FROM)
                    and interval < 180
                    and interval > 30):
                interval = 180
                interval_method += ',6-Away(<3min)'

            elif (dir_of_travel == AWAY_FROM
                    and not self.distance_method_waze_flag):
                interval_multiplier = 2    #calc-increase timer
                interval_method += ',6-Away(Calc)'
            elif (dir_of_travel == NOT_SET
                    and interval > 180):
                interval = 180
                interval_method += ',6->180s'

            #15-sec interval (close to zone) and may be going into a stationary zone,
            #increase the interval
            elif (interval == 15
                    and devicename in self.stat_zone_timer
                    and self.this_update_secs >= self.stat_zone_timer.get(devicename)+45):
                interval = 30
                interval_method += ',6-StatTimer+45'

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetStatZone')
            _LOGGER.exception(err)


        try:
            #Turn off waze close to zone flag to use waze after leaving zone
            if inzone_flag:
                self.waze_close_to_zone_pause_flag = False

            #if triggered by ios app (Zone Enter/Exit, Manual, Fetch, etc.)
            #and interval < 3 min, set to 3 min. Leave alone if > 3 min.
            if (self.iosapp_update_flag.get(devicename)
                    and interval < 180
                    and interval > 30
                    and self.override_interval_seconds.get(devicename) == 0):
                interval   = 180
                interval_method += ',7-iosAppTrigger'

            #if changed zones on this poll reset multiplier
            if self.state_change_flag.get(devicename):
                interval_multiplier = 1

            #Check accuracy again to make sure nothing changed, update counter
            if self.poor_gps_flag.get(devicename):
                interval_multiplier = 1

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'ResetStatZone')
            return attrs_msg

        try:
            #Real close, final check to make sure interval is not adjusted
            if (interval <= 60
                    or (battery > 0 and battery <= 33 and interval >= 120)):
                interval_multiplier = 1

            interval     = interval * interval_multiplier
            interval, x  = divmod(interval, 15)
            interval     = interval * 15

            #check for max interval
            if interval > self.max_interval_secs and not_inzone_flag:
                interval_str = (f"{self._secs_to_time_str(self.max_interval_secs)}({self._secs_to_time_str(interval)})")
                interval = self.max_interval_secs
                interval_method += (f",7-Max")
            else:
                interval_str = self._secs_to_time_str(interval)

            interval_debug_msg = (f"●Interval-{interval_str} ({interval_method}, {log_msg}), "
                                  f"●DirOfTrav-{dir_of_trav_msg}, "
                                  f"●State-{self.state_last_poll.get(devicename)}->, "
                                  f"{self.state_this_poll.get(devicename)}, "
                                  f"Zone-{zone}")
            event_msg = (f"Interval basis: {interval_method}, {log_msg}, Direction {dir_of_travel}")
            #self._save_event(devicename, event_msg)

            if interval_multiplier > 1:
                interval_method += (f"x{interval_multiplier}")
                interval_debug_msg = (f"{interval_debug_msg}, "
                                     f"Multiplier-{interval_multiplier} ({interval_method})")

            #check if next update is past midnight (next day), if so, adjust it
            next_poll = round((self.this_update_secs + interval)/15, 0) * 15

            # Update all dates and other fields
            self.next_update_secs[devicename_zone] = next_poll
            self.next_update_time[devicename_zone] = self._secs_to_time(next_poll)
            self.interval_seconds[devicename_zone] = interval
            self.interval_str[devicename_zone]     = interval_str
            self.last_update_secs[devicename_zone] = self.this_update_secs
            self.last_update_time[devicename_zone] = self._time_to_12hrtime(self.this_update_time)

        #--------------------------------------------------------------------------------
            #Calculate the old_location age check based on the direction and if there are
            #multiple zones being tracked from

            zi=self.track_from_zones.get(devicename).index(self.base_zone)
            if zi == 0:
                self.old_location_secs[devicename] = HIGH_INTEGER

            ic3dev_old_location_secs = self.old_location_secs.get(devicename)
            new_old_location_secs    = self._determine_old_location_secs(devicename, zone, interval)
            select=''
            if inzone_flag:
                select='inzone'
                ic3dev_old_location_secs = new_old_location_secs

            #Other base_zones are calculated before home zone, use smallest value
            elif new_old_location_secs < ic3dev_old_location_secs:
                select='ols < self.ols'
                ic3dev_old_location_secs = new_old_location_secs

            elif base_zone_home_flag and ic3dev_old_location_secs == HIGH_INTEGER:
                select='zone-home & HIGH_INTEGER'
                ic3dev_old_location_secs = new_old_location_secs

            self.old_location_secs[devicename] = ic3dev_old_location_secs
            old_location_secs_msg = self._secs_to_time_str(self.old_location_secs.get(devicename))

        #--------------------------------------------------------------------------------
            #if more than 3km(1.8mi) then assume driving, used later above
            if dist_from_zone_km > 3:                # 1.8 mi
                self.went_3km[devicename] = True
            elif dist_from_zone_km < .03:            # home, reset flag
                 self.went_3km[devicename] = False

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetTimes')

        #--------------------------------------------------------------------------------
        try:
            log_msg = (f"►INTERVAL FORMULA, {interval_debug_msg}")
            self._log_debug_interval_msg(devicename, log_msg)

            if self.log_intervalcalc_flag is False:
                interval_debug_msg = ''

            event_msg = (f"Interval Results > "
                f"Interval-{interval_str} ({interval_method}), "
                f"LastUpdate-{self.last_update_time.get(devicename_zone)}, "
                f"NextUpdate-{self.next_update_time.get(devicename_zone)}, "
                f"DistTraveled-{self._format_dist(calc_dist_last_poll_moved_km)}, "
                f"CurrZone-{zone}")
            if self.override_interval_seconds.get(devicename) > 0:
                event_msg += (f", OverrideInterval-{self._secs_to_time_str(self.override_interval_seconds.get(devicename))}")
            self._log_debug_interval_msg(devicename, event_msg)

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'ShowMsgs')


        try:
            #if 'NearZone' zone, do not change the state
            if near_zone_flag:
                zone = NOT_HOME

            log_msg = (f"DIR OF TRAVEL ATTRS, Direction-{dir_of_travel}, "
               f"LastDir-{last_dir_of_travel}, "
               f"Dist-{dist_from_zone_km}, "
               f"LastDist-{last_dist_from_zone_km}, "
               f"SelfDist-{self.zone_dist.get(devicename_zone)}, "
               f"Moved-{dist_from_zone_moved_km},"
               f"WazeMoved-{waze_dist_from_zone_moved_km}")
            self._log_debug_interval_msg(devicename, log_msg)

            #if poor gps and moved less than 1km, redisplay last distances
            if (self.state_change_flag.get(devicename) is False
                    and self.poor_gps_flag.get(devicename)
                    and dist_last_poll_moved_km < 1):
                dist_from_zone_km      = self.zone_dist.get(devicename_zone)
                waze_dist_from_zone_km = self.waze_dist.get(devicename_zone)
                calc_dist_from_zone_km = self.calc_dist.get(devicename_zone)
                waze_time_msg          = self.waze_time.get(devicename_zone)

            else:
                waze_time_msg          = self._format_waze_time_msg(waze_time_from_zone)

                #save for next poll if poor gps
                self.zone_dist[devicename_zone] = dist_from_zone_km
                self.waze_dist[devicename_zone] = waze_dist_from_zone_km
                self.waze_time[devicename_zone] = waze_time_msg
                self.calc_dist[devicename_zone] = calc_dist_from_zone_km

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetDistDir')

        #--------------------------------------------------------------------------------
        try:
            #Save last and new state, set attributes
            #If first time thru, set the last state to the current state
            #so a zone change will not be triggered next time

            if self.state_last_poll.get(devicename) == NOT_SET:
                last_state = zone

            #When put into stationary zone, also set last_poll so it
            #won't trigger again on next cycle as a state change
            elif (instr(zone, STATIONARY)
                    or instr(self.state_this_poll.get(devicename), STATIONARY)):
                zone = STATIONARY
                last_state = STATIONARY

            else:
                last_state = self.state_this_poll.get(devicename)

            #Make sure the new 'last state' value is the internal value for
            #the state (e.g., Away-->not_home) to reduce state change triggers later.
            last_state = STATE_TO_ZONE_BASE.get(last_state, last_state)
            self.state_last_poll[devicename] = last_state

            self.state_this_poll[devicename]   = zone
            self.last_located_time[devicename] = self._time_to_12hrtime(location_time)
            location_age                       = self._secs_since(last_located_secs)
            location_age_str                   = self._format_age(location_age)
            if (poor_location_gps_flag and self.poor_gps_flag.get(devicename) is False):
                location_age_str = (f"Old-{location_age_str}")

            log_msg =  (f"LOCATION TIME-{devicename} location_time-{location_time}, "
                        f"loc_time_secs-{self._secs_to_time(last_located_secs)} ({location_age_str})")
            self._log_debug_msg(devicename, log_msg)

            attrs = {}
            attrs[ATTR_ZONE]              = self.zone_current.get(devicename)
            attrs[ATTR_ZONE_TIMESTAMP]    = str(self.zone_timestamp.get(devicename))
            attrs[ATTR_LAST_ZONE]         = self.zone_last.get(devicename)
            attrs[ATTR_INTERVAL]          = interval_str
            attrs[ATTR_LAST_UPDATE_TIME]  = self._secs_to_timestamp(self.this_update_secs)
            attrs[ATTR_LAST_LOCATED]      = self._secs_to_timestamp(last_located_secs)
            attrs[ATTR_NEXT_UPDATE_TIME]  = self._secs_to_timestamp(next_poll)
            attrs[ATTR_WAZE_TIME]         = 0
            attrs[ATTR_WAZE_TIME_MIN]     = 0
            if self.waze_status == WAZE_USED:
                attrs[ATTR_WAZE_TIME]     = waze_time_msg
                attrs[ATTR_WAZE_TIME_MIN] = waze_time_from_zone
                attrs[ATTR_WAZE_DISTANCE] = self._km_to_mi(waze_dist_from_zone_km)
            elif self.waze_status == WAZE_NOT_USED:
                attrs[ATTR_WAZE_DISTANCE] = 'NotUsed'
            elif self.waze_status == WAZE_NO_DATA:
                attrs[ATTR_WAZE_DISTANCE] = 'NoData'
            elif self.waze_status == WAZE_OUT_OF_RANGE:
                if waze_dist_from_zone_km < 1:
                    attrs[ATTR_WAZE_DISTANCE] = 0
                elif waze_dist_from_zone_km < self.waze_min_distance:
                    attrs[ATTR_WAZE_DISTANCE] = 'DistLow'
                else:
                    attrs[ATTR_WAZE_DISTANCE] = 'DistHigh'
            elif dir_of_travel == 'in_zone':
                attrs[ATTR_WAZE_DISTANCE] = 0
            elif self.waze_status == WAZE_PAUSED:
                attrs[ATTR_WAZE_DISTANCE] = PAUSED
            elif waze_dist_from_zone_km > 0:
                attrs[ATTR_WAZE_TIME]     = waze_time_msg
                attrs[ATTR_WAZE_DISTANCE] = self._km_to_mi(waze_dist_from_zone_km)
            else:
                attrs[ATTR_WAZE_DISTANCE] = 0

            attrs[ATTR_ZONE_DISTANCE]   = self._km_to_mi(dist_from_zone_km)
            attrs[ATTR_CALC_DISTANCE]   = self._km_to_mi(calc_dist_from_zone_km)
            attrs[ATTR_DIR_OF_TRAVEL]   = dir_of_travel
            attrs[ATTR_TRAVEL_DISTANCE] = self._km_to_mi(dist_last_poll_moved_km)

            info_msg = self._format_info_attr(
                    devicename,
                    battery,
                    gps_accuracy,
                    dist_last_poll_moved_km,
                    zone)

            attrs[ATTR_INFO] = interval_debug_msg + info_msg

            #save for event log
            if type(waze_time_msg) != str: waze_time_msg = '0 mi'
            self.last_tavel_time[devicename_zone]   = waze_time_msg
            self.last_distance_str[devicename_zone] = (f"{self._km_to_mi(dist_from_zone_km)} {self.unit_of_measurement}")
            self._trace_device_attributes(devicename, 'RESULTS', fct_name, attrs)

            zone = self.zone_current.get(devicename)

            event_msg = (f"Results: From-{self.zone_to_display.get(self.base_zone)} > CurrZone-"
                         f"{self.zone_to_display.get(zone)}, "
                         f"GPS-{format_gps(latitude, longitude, gps_accuracy)}, "
                         f"Interval-{interval_str} ({interval_method}), ")
            #event_msg +=(f" ({interval_method}), ") if self.log_debug_flag else ", "
            if dist_from_zone_km > 0:
                event_msg +=(f"Dist-{self._km_to_mi(dist_from_zone_km)} {self.unit_of_measurement}, ")
            if waze_time_msg != '0 min':
                event_msg +=(f"TravTime-{waze_time_msg} ({dir_of_travel}), ")
            event_msg += (f"NextUpdt-{self._secs_to_time(next_poll)}, "
                         f"LocationTime-{self._time_to_12hrtime(location_time)} ({location_age_str}), "
                         f"OldLocThreshold-{old_location_secs_msg}")
            if battery10_flag:
                event_msg += (f", Battery-{battery}%")
            if self.stat_zone_timer.get(devicename) > 0:
                event_msg += (f", WillMoveIntoStatZoneAfter-{self._secs_to_time(self.stat_zone_timer.get(devicename))} "
                              f"({self._format_dist(self.stat_zone_moved_total.get(devicename))})")
            self._save_event_halog_info(devicename, event_msg, log_title="")

            return attrs

        except Exception as err:
            attrs_msg = self._internal_error_msg(fct_name, err, 'SetAttrs')
            _LOGGER.exception(err)
            return attrs_msg

#########################################################
#
#   iCloud FmF or FamShr authentication returned an error or no location
#   data is available. Update counter and device attributes and set
#   retry intervals based on current retry count.
#
#########################################################
    def _determine_interval_after_error(self, devicename, info_msg, counter=POOR_LOC_GPS_CNT, gps_accuracy=0):
        '''
        Handle errors where the device can not be or should not be updated with
        the current data. The update will be retried 4 times on a 15 sec interval.
        If the error continues, the interval will increased based on the retry
        count using the following cycles:
            1-4   - 15 sec
            5-8   - 1 min
            9-12  - 5min
            13-16 - 15min
            >16   - 30min

        The following errors use this routine:
            - iCloud Authentication errors
            - FmF location data not available
            - Old location
            - Poor GPS Acuracy
        '''

        fct_name = "_determine_interval_after_error"

        base_zone_home_flag = (self.base_zone == HOME)
        devicename_zone = self._format_devicename_zone(devicename)

        try:
            interval = self._get_interval_for_error_retry_cnt(devicename, counter, pause_control_flag=True)

            if interval < 0:
                self._pause_device(devicename)

                interval      = abs(interval)
                next_poll     = HIGH_INTEGER
                next_updt_str = PAUSED
            else:
                next_poll     = round((self.this_update_secs + interval)/15, 0) * 15
                next_updt_str = self._secs_to_time(next_poll)

            interval_str  = self._secs_to_time_str(interval)
            self.interval_seconds[devicename_zone] = interval
            self.next_update_secs[devicename_zone] = next_poll
            self.next_update_time[devicename_zone] = next_updt_str
            self.last_update_secs[devicename_zone] = self.this_update_secs
            self.last_update_time[devicename_zone] = self._time_to_12hrtime(self.this_update_time)
            self.interval_str[devicename_zone]     = interval_str
            self.count_discarded_update[devicename]  += 1

            attrs = {}
            attrs[ATTR_INTERVAL]          = interval_str
            attrs[ATTR_POLL_COUNT]        = self._format_poll_count(devicename)
            attrs[ATTR_LAST_UPDATE_TIME]  = self._secs_to_timestamp(self.this_update_secs)
            attrs[ATTR_NEXT_UPDATE_TIME]  = self._secs_to_timestamp(next_poll)

            if info_msg.startswith("OldLoc"):
                attrs[ATTR_INFO] = (f"Discarded, {info_msg.split('(')[0]} "
                                    f"(#{self.poor_location_gps_cnt.get(devicename)})")
            else:
                attrs[ATTR_INFO] = (f"● {info_msg} ●")

            this_zone = self.state_this_poll.get(devicename)
            this_zone = self._format_zone_name(devicename, this_zone)
            last_zone = self.state_last_poll.get(devicename)
            last_zone = self._format_zone_name(devicename, last_zone)

            if self._is_inzone(devicename):
                latitude  = self.zone_lat.get(this_zone)
                longitude = self.zone_long.get(this_zone)

            elif self._was_inzone(devicename):
                latitude  = self.zone_lat.get(last_zone)
                longitude = self.zone_long.get(last_zone)
            else:
                latitude  = self.last_lat.get(devicename)
                longitude = self.last_long.get(devicename)

            if latitude is None or longitude is None:
                latitude  = self.last_lat.get(devicename)
                longitude = self.last_long.get(devicename)
            if latitude is None or longitude is None:
                latitude  = self.zone_lat.get(last_zone)
                longitude = self.zone_long.get(last_zone)
            if latitude is None or longitude is None:
                event_msg = "Aborting update, no location data"
                self._save_event_halog_error(devicename,event_msg)
                return

            kwargs = self._setup_base_kwargs(devicename,
                latitude, longitude, 0, 0)

            self._update_device_attributes(devicename, kwargs, attrs, 'DetIntlErrorRetry')
            self._update_device_sensors(devicename, kwargs)
            self._update_device_sensors(devicename, attrs)
            self._update_stationary_zone_location(devicename)

            self.device_being_updated_flag[devicename] = False

            event_msg = (f"Discarded > {info_msg}, "
                         f"OldLocThreshold-{self._secs_to_time_str(self.old_location_secs.get(devicename))}, "
                         f"GPS-{format_gps(latitude, longitude, gps_accuracy)}, "
                         f"NextUpdt-{next_updt_str}, "
                         f"OldLocPoorGpsCnt-#{self.poor_location_gps_cnt.get(devicename)}, "
                         f"DiscardCnt-#{self.count_discarded_update.get(devicename)}")
            if self._device_offline(devicename):
                event_msg += (f", DeviceStatus-{self.device_status.get(devicename)}")
            self._save_event(devicename, event_msg)

            if (self._is_device_paused(devicename)
                    or self.count_discarded_update.get(devicename) > 400):
                self._pause_device(devicename)

                event_msg = (f"{EVLOG_NOTICE}Tracking Paused > Excessive Errors Encountered"
                             f"{CRLF_DOT}Old Location Errors-#{self.poor_location_gps_cnt.get(devicename)}"
                             f"{CRLF_DOT}Discarded Updates-#{self.count_discarded_update.get(devicename)}"
                             f"CRLF{'-'*75}"
                             f"CRLFEvent Log > Actions > Resume Polling to restart")
                self._save_event(devicename, event_msg)

        except Exception as err:
            _LOGGER.exception(err)

#########################################################
#
#   UPDATE DEVICE LOCATION & INFORMATION ATTRIBUTE FUNCTIONS
#
#########################################################
    def _get_distance_data(self, devicename, latitude, longitude,
                                gps_accuracy, poor_location_gps_flag):
        """ Determine the location of the device.
            Returns:
                - zone (current zone from lat & long)
                  set to HOME if distance < home zone radius
                - dist_from_zone_km (mi or km)
                - dist_traveled (since last poll)
                - dir_of_travel (towards, away_from, stationary, in_zone,
                                       left_zone, near_home)
        """

        fct_name = '_get_distance_data'

        try:
            if latitude is None or longitude is None:
                attrs = self._internal_error_msg(fct_name, 'lat/long=None', 'NoLocation')
                return (ERROR, attrs)

            base_zone_home_flag = (self.base_zone == HOME)
            devicename_zone = self._format_devicename_zone(devicename)

            log_msg = ("GET DEVICE DISTANCE DATA Entered")
            self._log_debug_interval_msg(devicename, log_msg)

            last_dir_of_travel     = NOT_SET
            last_dist_from_zone_km = 0
            last_waze_time         = 0
            last_lat               = self.base_zone_lat
            last_long              = self.base_zone_long
            ic3dev_timestamp_secs     = 0

            zone                         = self.base_zone
            calc_dist_from_zone_km       = 0
            calc_dist_last_poll_moved_km = 0
            calc_dist_from_zone_moved_km = 0


            #Get the devicename's icloud3 attributes
            entity_id = self.device_tracker_entity_ic3.get(devicename)
            attrs     = self._get_device_attributes(entity_id)

            self._trace_device_attributes(devicename, 'READ', fct_name, attrs)

        except Exception as err:
            _LOGGER.exception(err)
            error_msg = (f"Entity-{entity_id}, Err-{err}")
            attrs = self._internal_error_msg(fct_name, error_msg, 'GetAttrs')
            return (ERROR, attrs)

        try:
            #Not available if first time after reset
            if self.state_last_poll.get(devicename) != NOT_SET:
                log_msg = ("Distance info available")
                if ATTR_TIMESTAMP in attrs:
                    ic3dev_timestamp_secs = attrs[ATTR_TIMESTAMP]
                    ic3dev_timestamp_secs = self._timestamp_to_time(ic3dev_timestamp_secs)
                else:
                    ic3dev_timestamp_secs = 0

                last_dist_from_zone_km_s = self._get_attr(attrs, ATTR_ZONE_DISTANCE, NUMERIC)
                last_dist_from_zone_km   = last_dist_from_zone_km_s

                last_waze_time        = self._get_attr(attrs, ATTR_WAZE_TIME)
                last_dir_of_travel    = self._get_attr(attrs, ATTR_DIR_OF_TRAVEL)
                last_dir_of_travel    = last_dir_of_travel.replace('*', '', 99)
                last_dir_of_travel    = last_dir_of_travel.replace('?', '', 99)
                last_lat              = self.last_lat.get(devicename)
                last_long             = self.last_long.get(devicename)

            #get last interval
            interval_str = self.interval_str.get(devicename_zone)
            interval     = self._time_str_to_secs(interval_str)

            this_lat  = latitude
            this_long = longitude

        except Exception as err:
            _LOGGER.exception(err)
            attrs = self._internal_error_msg(fct_name, err, 'SetupLocation')
            return (ERROR, attrs)

        try:
            display_zone_msg = (zone == self.track_from_zones.get(devicename)[0])
            zone = self._get_zone(devicename, this_lat, this_long, display_zone_msg)

            log_msg =  (f"LAT-LONG GPS INITIALIZED {zone}, LastDirOfTrav-{last_dir_of_travel}, "
                        f"LastGPS=({last_lat}, {last_long}), ThisGPS=({this_lat}, {this_long}), "
                        f"UsingGPS=({latitude}, {longitude}), GPS.Accur-{gps_accuracy}, "
                        f"GPS.Threshold-{self.gps_accuracy_threshold}")
            self._log_debug_interval_msg(devicename, log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            attrs = self._internal_error_msg(fct_name, err, 'GetCurrZone')
            return (ERROR, attrs)

        try:
            # Get Waze distance & time
            #   Will return [error, 0, 0, 0] if error
            #               [out_of_range, dist, time, info] if
            #                           last_dist_from_zone_km >
            #                           last distance from home
            #               [ok, 0, 0, 0]  if zone=home
            #               [ok, distFmHome, timeFmHome, info] if OK

            calc_dist_from_zone_km       = self._calc_distance_km(this_lat, this_long,
                                            self.base_zone_lat, self.base_zone_long)
            calc_dist_last_poll_moved_km = self._calc_distance_km(last_lat, last_long,
                                            this_lat, this_long)
            calc_dist_from_zone_moved_km= (calc_dist_from_zone_km - last_dist_from_zone_km)
            calc_dist_from_zone_km       = self._round_to_zero(calc_dist_from_zone_km)
            calc_dist_last_poll_moved_km = self._round_to_zero(calc_dist_last_poll_moved_km)
            calc_dist_from_zone_moved_km= self._round_to_zero(calc_dist_from_zone_moved_km)

            if self.distance_method_waze_flag:
                #If waze paused via icloud_command or close to a zone, default to pause
                if self.waze_manual_pause_flag or self.waze_close_to_zone_pause_flag:
                    self.waze_status = WAZE_PAUSED
                else:
                   self.waze_status = WAZE_USED
            else:
                self.waze_status = WAZE_NOT_USED

            log_msg =  (f"Zone-{devicename_zone}, wStatus-{self.waze_status}, "
                        f"calc_dist-{calc_dist_from_zone_km}, wManualPauseFlag-{self.waze_manual_pause_flag}, "
                        f"CloseToZoneFlag-{self.waze_close_to_zone_pause_flag}")
            self._log_debug_interval_msg(devicename, log_msg)

            #Make sure distance and zone are correct for HOME, initialize
            if calc_dist_from_zone_km <= .05 or zone == self.base_zone:
                zone                 = self.base_zone
                calc_dist_from_zone_km       = 0
                calc_dist_last_poll_moved_km = 0
                calc_dist_from_zone_moved_km = 0
                self.waze_status             = WAZE_PAUSED

            #Near zone & towards or in near_zone
            elif (calc_dist_from_zone_km < 1
                    and last_dir_of_travel in ('towards', 'near_zone')):
                self.waze_status = WAZE_PAUSED
                self.waze_close_to_zone_pause_flag = True

                log_msg = "Using Calc Method (near Home & towards or Waze off)"
                self._log_debug_interval_msg(devicename, log_msg)

            #Determine if Waze should be used based on calculated distance
            elif (calc_dist_from_zone_km > self.waze_max_distance
                    or calc_dist_from_zone_km < self.waze_min_distance):
                self.waze_status = WAZE_OUT_OF_RANGE

            #Initialize Waze default fields
            waze_dist_from_zone_km       = calc_dist_from_zone_km
            waze_time_from_zone          = 0
            waze_dist_last_poll_moved_km = calc_dist_last_poll_moved_km
            waze_dist_from_zone_moved_km = calc_dist_from_zone_moved_km
            self.waze_history_data_used_flag[devicename_zone] = False

            #Use Calc if close to home, Waze not accurate when close
            log_msg =  (f"Zone-{devicename_zone}, Status-{self.waze_status}, "
                        f"calc_dist-{calc_dist_from_zone_km}, "
                        f"ManualPauseFlag-{self.waze_manual_pause_flag},"
                        f"CloseToZoneFlag-{self.waze_close_to_zone_pause_flag}")
            self._log_debug_interval_msg(devicename, log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            attrs = self._internal_error_msg(fct_name, err, 'InitializeDist')
            return (ERROR, attrs)

        try:
            if self.waze_status == WAZE_USED:
                try:
                    #See if another device is close with valid Waze data.
                    #If so, use it instead of calling Waze again. event_msg will have
                    #msg for log file if history was used

                    waze_dist_time_info = self._get_waze_from_data_history(
                                                devicename,
                                                calc_dist_from_zone_km,
                                                this_lat,
                                                this_long)

                    #No Waze data from close device. Get it from Waze
                    if waze_dist_time_info is None:
                        waze_dist_time_info = self._get_waze_data(
                                                devicename,
                                                this_lat, this_long,
                                                last_lat, last_long,
                                                zone,
                                                last_dist_from_zone_km)

                    self.waze_status = waze_dist_time_info[0]

                    if self.waze_status == WAZE_USED:
                        waze_dist_from_zone_km       = waze_dist_time_info[1]
                        waze_time_from_zone          = waze_dist_time_info[2]
                        waze_dist_last_poll_moved_km = waze_dist_time_info[3]
                        waze_dist_from_zone_moved_km= round(waze_dist_from_zone_km - last_dist_from_zone_km, 2)
                        waze_time_msg               = self._format_waze_time_msg(waze_time_from_zone)

                        #Save new Waze data or retimestamp data from another
                        #device.
                        if (gps_accuracy <= self.gps_accuracy_threshold
                                and waze_dist_from_zone_km > 0
                                and poor_location_gps_flag is False):
                            self.waze_distance_history[devicename_zone] = \
                                    [self._time_now_secs(),
                                    this_lat,
                                    this_long,
                                    waze_dist_time_info]

                    else:
                        self.waze_distance_history[devicename_zone] = []

                except Exception as err:
                    _LOGGER.exception(err)
                    self.waze_status = WAZE_NO_DATA

        except Exception as err:
            attrs = self._internal_error_msg(fct_name, err, 'WazeNoData')
            self.waze_status = WAZE_NO_DATA

        try:
            #don't reset data if poor gps, use the best we have
            if zone == self.base_zone:
                distance_method         = 'Home/Calc'
                dist_from_zone_km       = 0
                dist_last_poll_moved_km = 0
                dist_from_zone_moved_km = 0
            elif self.waze_status == WAZE_USED:
                distance_method         = WAZE
                dist_from_zone_km       = waze_dist_from_zone_km
                dist_last_poll_moved_km = waze_dist_last_poll_moved_km
                dist_from_zone_moved_km = waze_dist_from_zone_moved_km
            else:
                distance_method         = 'Calc'
                dist_from_zone_km       = calc_dist_from_zone_km
                dist_last_poll_moved_km = calc_dist_last_poll_moved_km
                dist_from_zone_moved_km = calc_dist_from_zone_moved_km

            if dist_from_zone_km > 99: dist_from_zone_km = int(dist_from_zone_km)
            if dist_last_poll_moved_km > 99: dist_last_poll_moved_km = int(dist_last_poll_moved_km)
            if dist_from_zone_moved_km> 99: dist_from_zone_moved_km= int(dist_from_zone_moved_km)

            dist_from_zone_moved_km= self._round_to_zero(dist_from_zone_moved_km)

            log_msg = (f"DISTANCES CALCULATED, "
                       f"Zone-{zone}, Method-{distance_method}, "
                       f"LastDistFmHome-{self._format_dist(last_dist_from_zone_km)}, "
                       f"WazeStatus-{self.waze_status}")
            self._log_debug_interval_msg(devicename, log_msg)
            log_msg = (f"DISTANCES ...Waze, "
                       f"Dist-{self._format_dist(waze_dist_from_zone_km)}, "
                       f"LastPollMoved-{self._format_dist(waze_dist_last_poll_moved_km)}, "
                       f"FmHomeMoved-{self._format_dist(waze_dist_from_zone_moved_km)}, "
                       f"Time-{waze_time_from_zone}, "
                       f"Status-{self.waze_status}")
            self._log_debug_interval_msg(devicename, log_msg)
            log_msg = (f"DISTANCES ...Calc, "
                       f"Dist-{self._format_dist(calc_dist_from_zone_km)}, "
                       f"LastPollMoved-{self._format_dist(calc_dist_last_poll_moved_km)}, "
                       f"FmHomeMoved-{self._format_dist(calc_dist_from_zone_moved_km)}")
            self._log_debug_interval_msg(devicename, log_msg)

            #if didn't move far enough to determine towards or away_from,
            #keep the current distance and add it to the distance on the next
            #poll
            if (dist_from_zone_moved_km> -.3 and dist_from_zone_moved_km< .3):
                dist_from_zone_moved_km+= \
                        self.dist_from_zone_km_small_move_total.get(devicename, 0)
                self.dist_from_zone_km_small_move_total[devicename] = \
                        dist_from_zone_moved_km
            else:
                 self.dist_from_zone_km_small_move_total[devicename] = 0

        except Exception as err:
            _LOGGER.exception(err)
            attrs = self._internal_error_msg(fct_name, err, 'CalcDist')
            return (ERROR, attrs)

        try:
            section = "dir_of_trav"
            dir_of_travel   = ''
            dir_of_trav_msg = ''
            if zone not in (NOT_HOME, 'near_zone'):
                dir_of_travel   = 'in_zone'
                dir_of_trav_msg = (f"Zone-{zone}")

            elif last_dir_of_travel == "in_zone":
                dir_of_travel   = 'left_zone'
                dir_of_trav_msg = (f"LastZone-{last_dir_of_travel}")

            elif dist_from_zone_moved_km<= -.3:            #.18 mi
                dir_of_travel   = 'towards'
                dir_of_trav_msg = (f"Dist-{self._format_dist(dist_from_zone_moved_km)}")

            elif dist_from_zone_moved_km>= .3:             #.18 mi
                dir_of_travel   = AWAY_FROM
                dir_of_trav_msg = (f"Dist-{self._format_dist(dist_from_zone_moved_km)}")

            elif self.poor_gps_flag.get(devicename):
                dir_of_travel   = 'Poor.GPS'
                dir_of_trav_msg = ("Poor.GPS-{gps_accuracy}")

            else:
                #didn't move far enough to tell current direction
                dir_of_travel   = (f"{last_dir_of_travel}?")
                dir_of_trav_msg = (f"Moved-{self._format_dist(dist_last_poll_moved_km)}")

            #If moved more than stationary zone limit (~.06km(200ft)),
            #reset check StatZone still timer and check again next poll
            #Use calc distance rather than waze for better accuracy
            section = "test if home"

            if (calc_dist_from_zone_km > self.stat_min_dist_from_zone_km
                    and zone == NOT_HOME):

                section = "test moved"
                #Reset stationary zone timer
                if (calc_dist_last_poll_moved_km > self.stat_dist_move_limit
                        or devicename not in self.stat_zone_moved_total
                        or self.this_update_secs > self.stat_zone_timer.get(devicename)+120):
                    section = "test moved-reset stat zone "

                    event_msg = (f"Stat Zone > Reset Timer, ")
                    if calc_dist_last_poll_moved_km > self.stat_dist_move_limit:
                        event_msg += (f"MovedOverLimit-{(calc_dist_last_poll_moved_km > self.stat_dist_move_limit)}, ")
                    if devicename not in self.stat_zone_moved_total:
                        event_msg += "Initial Setup, "
                    if (self.this_update_secs > self.stat_zone_timer.get(devicename)+120):
                        event_msg += (f"ResetTimer-{(self.this_update_secs > self.stat_zone_timer.get(devicename)+120)}, ")

                    event_msg += (f"Moved-{self._format_dist(calc_dist_last_poll_moved_km)}, "
                                  f"Timer-{self._secs_to_time(self.stat_zone_timer.get(devicename))}, ")

                    self.stat_zone_moved_total[devicename] = 0
                    self.stat_zone_timer[devicename] = self.this_update_secs + self.stat_zone_still_time

                    event_msg += (f" to {self._secs_to_time(self.stat_zone_timer.get(devicename))}")
                    self._evlog_debug_msg(devicename, event_msg)

                #If moved less than the stationary zone limit, update the
                #distance moved and check to see if now in a stationary zone
                elif devicename in self.stat_zone_moved_total:
                    section = "StatZonePrep"
                    self.stat_zone_moved_total[devicename] += calc_dist_last_poll_moved_km
                    if self.stat_zone_timer.get(devicename) > 0:
                        stat_zone_timer_left       = self.stat_zone_timer.get(devicename) - self.this_update_secs
                    else:
                        stat_zone_timer_left       = HIGH_INTEGER

                    log_msg = (f"Stat Zone Movement > "
                        f"TotalMoved-{self._format_dist(self.stat_zone_moved_total.get(devicename))}, "
                        f"Timer-{self._secs_to_time(self.stat_zone_timer.get(devicename))}, "
                        f"TimerLeft- {stat_zone_timer_left} secs, "
                        f"TimerExpired-{stat_zone_timer_left <= 0}"
                        f"UnderMoveLimit-{self.stat_zone_moved_total.get(devicename) <= self.stat_dist_move_limit}, "
                        f"DistFmZone-{self._format_dist(dist_from_zone_km)}")
                    self._evlog_debug_msg(devicename, log_msg)
                    self._log_debug_msg(devicename, log_msg)
                    section = "CheckNowinzone_stationary"

                    #See if moved less than the stationary zone movement limit
                    #If updating via the ios app and the current state is stationary,
                    #make sure it is kept in the stationary zone
                    if (self.stat_zone_moved_total.get(devicename) <= self.stat_dist_move_limit
                            and stat_zone_timer_left <= 0):
                        dir_of_travel   = STATIONARY
                        dir_of_trav_msg = (f"Age-{self._secs_to(self.stat_zone_timer.get(devicename))}s, "
                                           f"Moved-{self.stat_zone_moved_total.get(devicename)}")
                else:
                    self.stat_zone_moved_total[devicename] = 0

            section = "Finalize"
            dir_of_trav_msg = (f"{dir_of_travel}({dir_of_trav_msg})")
            log_msg = (f"DIR OF TRAVEL DETERMINED, {dir_of_trav_msg}")
            self._log_debug_interval_msg(devicename, log_msg)

            dist_from_zone_km            = self._round_to_zero(dist_from_zone_km)
            dist_from_zone_moved_km      = self._round_to_zero(dist_from_zone_moved_km)
            dist_last_poll_moved_km      = self._round_to_zero(dist_last_poll_moved_km)
            waze_dist_from_zone_km       = self._round_to_zero(waze_dist_from_zone_km)
            calc_dist_from_zone_moved_km = self._round_to_zero(calc_dist_from_zone_moved_km)
            waze_dist_last_poll_moved_km = self._round_to_zero(waze_dist_last_poll_moved_km)
            calc_dist_last_poll_moved_km = self._round_to_zero(calc_dist_last_poll_moved_km)
            last_dist_from_zone_km       = self._round_to_zero(last_dist_from_zone_km)

            log_msg = (f"GET DEVICE DISTANCE DATA Complete, "
                        f"CurrentZone-{zone}, DistFmHome-{dist_from_zone_km}, "
                        f"DistFmHomeMoved-{dist_from_zone_moved_km}, "
                        f"DistLastPollMoved-{dist_last_poll_moved_km}")
            self._log_debug_interval_msg(devicename, log_msg)

            distance_data = (zone,
                             dir_of_travel,
                             dist_from_zone_km,
                             dist_from_zone_moved_km,
                             dist_last_poll_moved_km,
                             waze_dist_from_zone_km,
                             calc_dist_from_zone_km,
                             waze_dist_from_zone_moved_km,
                             calc_dist_from_zone_moved_km,
                             waze_dist_last_poll_moved_km,
                             calc_dist_last_poll_moved_km,
                             waze_time_from_zone,
                             last_dist_from_zone_km,
                             last_dir_of_travel,
                             dir_of_trav_msg,
                             ic3dev_timestamp_secs)

            log_msg = (f"DISTANCE DATA-{devicename}-{distance_data}")
            self._log_debug_msg(devicename, log_msg)
            evlog_msg = (f"Distance Data > DirOfTrav-{dir_of_travel}, "
                         f"LastDirOfTrav-{last_dir_of_travel}, "
                         f"DistFmZone-{self._format_dist(dist_from_zone_km)}, "
                         f"LastDistFmZone-{self._format_dist(last_dist_from_zone_km)}, "
                         f"DistFmZoneMoved-{self._format_dist(dist_from_zone_moved_km)}, "
                         f"DistFmLastPollMoved-{self._format_dist(dist_last_poll_moved_km)}")
            self._evlog_debug_msg(devicename, evlog_msg)

            return  distance_data

        except Exception as err:
           _LOGGER.exception(err)
           attrs = self._internal_error_msg(fct_name+section, err, 'Finalize')
           return (ERROR, attrs)

#--------------------------------------------------------------------------------
    def _determine_old_location_secs(self,devicename, zone, interval):
        """
        Calculate the time between the location timestamp and now (age) a
        location record must be before it is considered old
        """

        old_location_secs = 60
        if self._is_inzone_zonename(zone):
            old_location_secs = interval * .025     #inzone interval --> 2.5%
            if old_location_secs < 90: old_location_secs = 90

        elif interval < 90:
            old_location_secs = 60                  #60 secs if < 1.5 min

        else:
            old_location_secs = interval * .125    #12.5% of the interval

        if old_location_secs < 61:
            old_location_secs = 61
        elif old_location_secs > 600:
            old_location_secs = 600

        #IOS App old location time minimum is 3 min
        if self.TRK_METHOD_IOSAPP and old_location_secs < 180:
            old_location_secs == 180

        if (self.old_location_threshold > 0
                and old_location_secs > self.old_location_threshold):
            old_location_secs = self.old_location_threshold

        return old_location_secs

#########################################################
#
#    DEVICE ATTRIBUTES ROUTINES
#
#########################################################
    def _get_state(self, entity_id):
        """
        Get current state of the device_tracker entity
        (zone's name, actual state (home,  away) or zone's
        friendly name) and return it's zone name
        """

        try:
            entity_state = self.hass.states.get(entity_id).state
            state = self.state_to_zone.get(entity_state, entity_state.lower())

        except Exception as err:
            #When starting iCloud3, the device_tracker for the iosapp might
            #not have been set up yet. Catch the entity_id error here.
            #_LOGGER.exception(err)
            state = NOT_SET

        return state
#--------------------------------------------------------------------
    def _set_state(self, entity_id, state_value, attrs_value):
        """
        General routine for setting the state and attributes of an entity_id
        """

        try:
            self.hass.states.set(entity_id, state_value, attrs_value)

        except Exception as err:
            log_msg = (f"Error updating entity > {entity_id}, StateValue-{state_value}, "
                       f"AttrsValue-{attrs_value}")
            self._log_error_msg(log_msg)
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _get_entity_last_changed_time(self, entity_id, devicename):
        """
        Get entity's last changed time attribute
        Last changed time format '2019-09-09 14:02:45.12345+00:00' (utc value)
        Return time, seconds, timestamp
        """

        try:
            timestamp_utc = str(self.hass.states.get(entity_id).last_changed)

            timestamp_utc = timestamp_utc.split(".")[0]
            secs          = self._timestamp_to_secs(timestamp_utc, UTC_TIME)
            hhmmss        = self._secs_to_time(secs)
            timestamp     = self._secs_to_timestamp(secs)
            age_secs      = self.this_update_secs - secs
            dhms_age_str  = self._secs_to_dhms_str(age_secs)

            return hhmmss, secs, timestamp, age_secs, dhms_age_str

        except Exception as err:
            #_LOGGER.exception(err)
            return '', 0, TIMESTAMP_ZERO, 0, ''
#--------------------------------------------------------------------
    def _get_device_attributes(self, entity_id):
        """ Get attributes of the device """

        try:
            ic3dev_data  = self.hass.states.get(entity_id)
            ic3dev_attrs = ic3dev_data.attributes

            retry_cnt = 0
            while retry_cnt < 10:
                if ic3dev_attrs:
                    break
                retry_cnt += 1
                log_msg = (f"No attribute data returned for {entity_id}. Retrying #{retry_cnt}")
                self._log_debug_msg('*', log_msg)

        except (KeyError, AttributeError):
            ic3dev_attrs = {}
            pass

        except Exception as err:
            _LOGGER.exception(err)
            ic3dev_attrs = {}
            ic3dev_attrs[ATTR_TRIGGER] = (f"Error {err}")

        return dict(ic3dev_attrs)

#--------------------------------------------------------------------
    @staticmethod
    def _get_attr(attributes, attribute_name, numeric = False):
        ''' Get an attribute out of the attrs attributes if it exists'''
        if attribute_name in attributes:
            return attributes[attribute_name]
        elif numeric:
            return 0
        else:
            return ''

#--------------------------------------------------------------------
    def _update_device_attributes(self, devicename, kwargs: str = None,
                        attrs: str = None, fct_name: str = UNKNOWN):
        """
        Update the device and attributes with new information
        On Entry, kwargs = {} or contains the base attributes.

        Trace the interesting attributes if debugging.

        Full set of attributes is:
        'gps': (27.726639, -80.3904565), 'battery': 61, 'gps_accuracy': 65.0
        'dev_id': 'lillian_iphone', 'host_name': 'Lillian',
        'location_name': HOME, 'source_type': 'gps',
        'attributes': {'interval': '2 hrs', 'last_update': '10:55:17',
        'next_update': '12:55:15', 'travel_time': '', 'distance': 0,
        'calc_distance': 0, 'waze_distance': 0, 'dir_of_travel': 'in_zone',
        'travel_distance': 0, 'info': ' ●Battery-61%',
        'group': 'gary_icloud', 'authenticated': '02/22/19 10:55:10',
        'last_located': '10:55:15', 'device_status': 'online',
        ATTR_LOW_POWER_MODE: False, 'battery_status': 'Charging',
        'tracked_devices': 'gary_icloud/gary_iphone,
        gary_icloud/lillian_iphone', 'trigger': 'iCloud',
        'timestamp': '2019-02-22T10:55:17.543', 'poll_count': '1:0:1'}

        {'source_type': 'gps', 'latitude': 27.726639, 'longitude': -80.3904565,
        'gps_accuracy': 65.0, 'battery': 93, 'zone': HOME,
        'last_zone': HOME, 'zone_timestamp': '03/13/19, 9:47:35',
        'trigger': 'iCloud', 'timestamp': '2019-03-13T09:47:35.405',
        'interval': '2 hrs', 'travel_time': '', 'distance': 0,
        'calc_distance': 0, 'waze_distance': '', 'last_located': '9:47:34',
        'last_update': '9:47:35', 'next_update': '11:47:30',
        'poll_count': '1:0:2', 'dir_of_travel': 'in_zone',
        'travel_distance': 0, 'info': ' ●Battery-93%',
        'battery_status': 'NotCharging', 'device_status':
        'online', ATTR_LOW_POWER_MODE: False,
        'authenticated': '03/13/19, 9:47:26',
        'tracked_devices': 'gary_icloud/gary_iphone, gary_icloud/lillian_iphone',
        'group': 'gary_icloud', 'friendly_name': 'Gary',
        'icon': 'mdi:cellphone',
        'entity_picture': '/local/gary-caller_id.png'}
        """

        zone         = self.zone_current.get(devicename)
        ic3dev_state = self.state_this_poll.get(devicename)
        ic3dev_state_fname = ic3dev_state

        #######################################################################
        #The current zone is based on location of the device after it is looked
        #up in the zone tables.
        #The ic3dev_state is from the original trigger value when the poll started.
        #If the device went from one zone to another zone, an enter/exit trigger
        #may not have been issued. If the trigger was the next update time
        #reached, the ic3dev_state and zone many now not match. (v2.0.2)

        if ic3dev_state == NOT_SET or zone == NOT_SET or zone == '':
            pass

        #If ic3dev_state is 'stationary' and in a stationary zone, nothing to do
        elif ic3dev_state == STATIONARY and instr(zone, STATIONARY):
            pass

        #If state is 'stationary' and in another zone, reset the state to the
        #current zone that was based on the device location.
        #If the state is in a zone but not the current zone, change the state
        #to the current zone that was based on the device location.
        elif ((ic3dev_state == STATIONARY
                    and self._is_inzone(zone))
                or (self._is_inzone(ic3dev_state)
                    and self._is_inzone(zone)
                    and ic3dev_state != zone)):
                if self._is_overlapping_zone(ic3dev_state, zone) is False:
                    event_msg = (f"State/Zone mismatch > Resetting iC3 State ({ic3dev_state}) "
                                f"to ({zone})")
                    self._save_event(devicename, event_msg)
                ic3dev_state = zone

        elif ic3dev_state == HOME:
            self.waze_distance_history = {}

        if (ic3dev_state == HOME or ic3dev_state == NOT_HOME):
            pass
        else:
            ic3dev_state_fname = self.zone_to_display.get(ic3dev_state, ic3dev_state)

        #Update the device timestamp
        if not attrs:
            attrs  = {}
        if ATTR_TIMESTAMP in attrs:
            timestamp = attrs[ATTR_TIMESTAMP]
        else:
            timestamp = dt_util.now().strftime(ATTR_TIMESTAMP_FORMAT)[0:19]
            attrs[ATTR_TIMESTAMP] = timestamp

        #Calculate and display how long the update took
        update_took_time =  round(time.time() - self.update_timer.get(devicename), 2)
        if update_took_time > 3 and ATTR_INFO in attrs:
            attrs[ATTR_INFO] = f"{attrs[ATTR_INFO]}  • Took {update_took_time}s"

        attrs[ATTR_NAME]            = self.fname.get(devicename)
        #attrs[ATTR_GROUP]           = self.group
        attrs[ATTR_TRACKING]        = self.attr_tracking_msg
        attrs[ATTR_ICLOUD3_VERSION] = VERSION

        #Add update time to trigger to be able to detect trigger change by iOS App
        #and by iC3.
        new_trigger = (f"{self.trigger.get(devicename)}@").split('@')[0]
        new_trigger = (f"{new_trigger}@{self.last_located_time.get(devicename)}")

        self.trigger[devicename] = new_trigger
        attrs[ATTR_TRIGGER]      = new_trigger

        #Update sensor.<devicename>_last_update_trigger if IOS App detected
        #and iCloud3 has been running for at least 10 secs to let HA &
        #mobile_app start up to avoid error if iC3 loads before the mobile_app

        #Set the gps attribute and update the attributes via self.see
        if kwargs == {} or not kwargs:
            kwargs = self._setup_base_kwargs(
                devicename,
                self.last_lat.get(devicename),
                self.last_long.get(devicename),
                0, 0)

        kwargs['dev_id']        = devicename
        kwargs['host_name']     = self.fname.get(devicename)
        kwargs['location_name'] = ic3dev_state_fname
        kwargs['source_type']   = 'gps'
        kwargs[ATTR_ATTRIBUTES] = attrs
        self.see(**kwargs)

        if ic3dev_state == "Not Set":
            ic3dev_state = "not_set"

        self.state_this_poll[devicename] = ic3dev_state.lower()

        self._trace_device_attributes(devicename, 'WRITE', fct_name, kwargs)

        if timestamp == '':         #Bypass if not initializing
            return

        retry_cnt = 1
        timestamp = timestamp[10:]      #Strip off date

        #Quite often, the attribute update has not actually taken
        #before other code is executed and errors occur.
        #Reread the attributes of the ones just updated to make sure they
        #were updated corectly. Verify by comparing the timestamps. If
        #differet, retry the attribute update. HA runs in multiple threads.
        try:
            entity_id = self.device_tracker_entity_ic3.get(devicename)
            while retry_cnt < 99:
                chk_see_attrs  = self._get_device_attributes(entity_id)
                chk_timestamp  = str(chk_see_attrs.get(ATTR_TIMESTAMP))
                chk_timestamp  = chk_timestamp[10:]

                if timestamp == chk_timestamp:
                    break

                if (retry_cnt % 10) == 0:
                    time.sleep(1)
                retry_cnt += 1

                self.see(**kwargs)

        except Exception as err:
            _LOGGER.exception(err)

        return

#--------------------------------------------------------------------
    def _setup_base_kwargs(self, devicename, latitude, longitude,
            battery, gps_accuracy):

        #check to see if device set up yet
        ic3dev_state = self.state_this_poll.get(devicename)
        zone_name = None

        if latitude == self.zone_home_lat:
            pass
        elif ic3dev_state == NOT_SET:
            zone_name = self.base_zone

        #if in zone, replace lat/long with zone center lat/long
        elif self._is_inzone_zonename(ic3dev_state):
            zone_name = self._format_zone_name(devicename, ic3dev_state)

        debug_msg=(f"SETUP BASE KWARGS zone_name-{zone_name}, inzone-state-{self._is_inzone_zonename(ic3dev_state)}")
        self._log_debug_msg(devicename, debug_msg)

        if zone_name and self._is_inzone_zonename(ic3dev_state):
            zone_lat  = self.zone_lat.get(zone_name)
            zone_long = self.zone_long.get(zone_name)
            zone_dist = self._calc_distance_m(latitude, longitude, zone_lat, zone_long)

            debug_msg=(f"zone_lat/long=({zone_lat}, {zone_long}), "
                    f"lat-long=({latitude}, {longitude}), zone_dist-{zone_dist}, "
                    f"zone-radius-{self.zone_radius_km.get(zone_name, 100)}")
            self._log_debug_msg(devicename, debug_msg)

            #Move center of stationary zone to new location if more than 10m from old loc
            if (instr(zone_name, STATIONARY)
                    and self.in_stationary_zone_flag.get(devicename)
                    and zone_dist > 10):
                self._update_stationary_zone(
                        devicename,
                        latitude,
                        longitude,
                        STAT_ZONE_NEW_LOCATION,'_setup_base_kwargs')

            #inside zone, move to center
            elif (self.center_in_zone_flag
                    and zone_dist <= self.zone_radius_m.get(zone_name, 100)
                    and (latitude != zone_lat or longitude != zone_long)):
                event_msg  = (f"Moving to zone center > {zone_name}, "
                              f"GPS-{format_gps(latitude, longitude, gps_accuracy, zone_lat, zone_long)}, "
                              f"Distance-{self._format_dist_m(zone_dist)}")
                self._save_event(devicename, event_msg)
                self._log_debug_msg(devicename, event_msg)

                latitude  = zone_lat
                longitude = zone_long
                self.last_lat[devicename]  = zone_lat
                self.last_long[devicename] = zone_long

        gps_lat_long           = (latitude, longitude)
        kwargs                 = {}
        kwargs['gps']          = gps_lat_long
        kwargs[ATTR_BATTERY]   = int(battery)
        kwargs[ATTR_GPS_ACCURACY] = gps_accuracy

        return kwargs

#--------------------------------------------------------------------
    def _format_entity_id(self, devicename):
        return (f"{DOMAIN}.{devicename}")

#--------------------------------------------------------------------
    def _format_fname_devtype(self, devicename):
        if devicename == "*":
            return ""
        else:
            return (f"{self.fname.get(devicename, '')} ({self.device_type.get(devicename, '')})")

#--------------------------------------------------------------------
    def _format_fname_devicename(self, devicename):
        if devicename == "*":
            return ""
        else:
            return (f"{self.fname.get(devicename, '')} ({devicename})")

#--------------------------------------------------------------------
    def _format_fname_zone(self, zone):
        return (f"{self.zone_to_display.get(zone, zone.title())}")

#--------------------------------------------------------------------
    def _format_tracking_method(self, devicename):
        return (TRK_METHOD_SHORT_NAME.get(self.devicename_tracking_method.get(devicename)))
#--------------------------------------------------------------------
    def _format_devicename_zone(self, devicename, zone=None):
        if zone is None:
            zone = self.base_zone
        return (f"{devicename}:{zone}")
#--------------------------------------------------------------------
    def _format_list(self, arg_list):
        formatted_list = str(arg_list)
        formatted_list = formatted_list.replace("[", "").replace("]", "")
        formatted_list = formatted_list.replace("{", "").replace("}", "")
        formatted_list = formatted_list.replace("'", "").replace(",", f"{CRLF_DOT}")

        return (f"{CRLF_DOT}{formatted_list}")
#--------------------------------------------------------------------
    def _format_time_age(self, timestamp):
        time_age_str = (f"{self._secs_to_time(timestamp)} "
                        f"({self._secs_to_time_str(self._secs_since(timestamp))} ago)")
        return time_age_str

    def _format_age_ts(self, timestamp):
        return (f"{self._secs_to_time_str(self._secs_since(timestamp))} ago")

    def _format_age(self, secs):
        return (f"{self._secs_to_time_str(secs)} ago")
#--------------------------------------------------------------------
    def _trace_device_attributes(self, devicename, description,
            fct_name, attrs):

        try:
            #Extract only attrs needed to update the device
            if attrs is None:
                return

            attrs_in_attrs = {}
            if (instr(description, "iCloud") or instr(description, "FamShr")):
                attrs_base_elements = TRACE_ICLOUD_ATTRS_BASE
                if ATTR_LOCATION in attrs:
                    attrs_in_attrs  = attrs[ATTR_LOCATION]
            elif 'Zone' in description:
                attrs_base_elements = attrs
            else:
                attrs_base_elements = TRACE_ATTRS_BASE
                if ATTR_ATTRIBUTES in attrs:
                    attrs_in_attrs  = attrs[ATTR_ATTRIBUTES]

            trace_attrs = {k: v for k, v in attrs.items() \
                                       if k in attrs_base_elements}

            trace_attrs_in_attrs = {k: v for k, v in attrs_in_attrs.items() \
                                       if k in attrs_base_elements}

            #trace_attrs = attrs

            ls = self.state_last_poll.get(devicename)
            cs = self.state_this_poll.get(devicename)
            log_msg = (f"{description} Attrs ___ ({fct_name})")
            self._log_debug_msg(devicename, log_msg)

            log_msg = (f"{description} Last State-{ls}, This State-{cs}")
            self._log_debug_msg(devicename, log_msg)

            log_msg = (f"{description} Attrs-{trace_attrs}{trace_attrs_in_attrs}")
            self._log_debug_msg(devicename, log_msg)

            self._log_rawdata(f"iCloud Rawdata - {devicename}--{description}", attrs)


        except Exception as err:
            pass
            #_LOGGER.exception(err)

        return

#--------------------------------------------------------------------
    def _broadcast_message(self, service_data):
        '''Send a message to all devices '''

        for devicename in self.tracked_devices:
            self._send_message_to_device(devicename, service_data)

#--------------------------------------------------------------------
    def _send_message_to_device(self, devicename, service_data):
        '''
        Send a message to the device. An example message is:
            service_data = {
                "title": "iCloud3/iOSApp Zone Action Needed",
                "message": "The iCloud3 Stationary Zone may "\
                    "not be loaded in the iOSApp. Force close "\
                    "the iOSApp from the iOS App Switcher. "\
                    "Then restart the iOSApp to reload the HA zones. "\
                    f"Distance-{dist_from_zone_m} m, "
                    f"StatZoneTestDist-{zone_radius_m * 2} m",
                "data": {"subtitle": "Stationary Zone Exit "\
                    "Trigger was not received"}}
        '''
        try:
            if self.notify_iosapp_entity.get(devicename, None) == None:
                return

            if service_data.get('message') != "request_location_update":
                evlog_msg = (f"{EVLOG_NOTICE}Sending Message to Device > "
                             f"Message-{service_data.get('message')}")
                self._save_event_halog_info(devicename, evlog_msg)

            for notify_devicename in self.notify_iosapp_entity.get(devicename):
                entity_id = (f"mobile_app_{notify_devicename}")
                self.hass.services.call("notify", entity_id, service_data)

            #self.hass.async_create_task(
            #    self.hass.services.async_call('notify', entity_id, service_data))

            return True

        except Exception as err:
            event_msg = (f"iCloud3 Error > An error occurred sending a message to device "
                         f"{notify_devicename} via notify.{entity_id} service. "
                         f"{CRLF_DOT}Message-{str(service_data)}")
            if instr(err, "notify/none"):
                event_msg += "{CRLF_DOT}The devicename can not be found."
                devicename = "*"
            else:
                event_msg += f"{CRLF_DOT}Error-{err}"
            self._save_event_halog_error(devicename, event_msg)

        return False

#--------------------------------------------------------------------
    def _get_iosapp_device_tracker_state_attributes(self, devicename, ic3_state, ic3_dev_attrs):
        '''
        Return the state and attributes of the ios app device tracker.
        The ic3 device tracker state and attributes are returned if
        the ios app data is not available or an error occurs.
        '''
        try:
            entity_id = self.device_tracker_entity_iosapp.get(devicename, None)
            if entity_id:
                iosapp_state     = self._get_state(entity_id)
                iosapp_dev_attrs = self._get_device_attributes(entity_id)

                #iosapp state is the friendly name of the zone, ic3 keeps the state
                #by zone name, not the friendly name. Convert iosapp state back to zone
                #entity name to match ic3 state_this_poll and state_last_poll,
                #state-zone name mismatch errors and state change detected trigger
                #when it really didn't

                if ATTR_LATITUDE in iosapp_dev_attrs:
                    self.iosapp_monitor_error_cnt[devicename] = 0
                    return iosapp_state, iosapp_dev_attrs, True

        except Exception as err:
            if self.start_icloud3_initial_load_flag is False:
                self.iosapp_monitor_error_cnt[devicename] += 1
            #_LOGGER.exception(err)
        return ic3_state, ic3_dev_attrs, False


#--------------------------------------------------------------------
    def _get_iosapp_device_sensor_trigger(self, devicename):

        entity_id = (f"sensor.{self.iosapp_last_trigger_entity.get(devicename)}")

        try:
            if self.iosapp_monitor_dev_trk_flag.get(devicename):
                trigger = self.hass.states.get(entity_id).state

                trigger_time, trigger_time_secs, trigger_timestamp, \
                        trigger_age_secs, trigger_age_str = \
                        self._get_entity_last_changed_time(entity_id, devicename)

                trigger_abbrev = IOS_TRIGGER_ABBREVIATIONS.get(trigger, trigger)

                return (trigger_abbrev, trigger_time, trigger_time_secs,
                            trigger_age_secs, trigger_age_str)

            else:
                return '', TIMESTAMP_ZERO, 0, 0, ''

        except Exception as err:
            #_LOGGER.exception(err)
            return '', TIMESTAMP_ZERO, 0, 0, ''

#--------------------------------------------------------------------
    def _get_iosapp_device_sensor_battery_level(self, devicename) -> int:
        return -1

        entity_id = (f"sensor.{self.iosapp_battery_level_entity.get(devicename)}")

        try:
            if self.iosapp_monitor_dev_trk_flag.get(devicename):
                battery_level = self.hass.states.get(entity_id).state
                return int(battery_level)

            else:
                return 0

        except Exception as err:
            #_LOGGER.exception(err)
            return 0

#########################################################
#
#   DEVICE ZONE ROUTINES
#
#########################################################
    def _get_zone(self, devicename, latitude, longitude, display_zone_msg=True):

        '''
        Get current zone of the device based on the location """

        This is the same code as (active_zone/async_active_zone) in zone.py
        but inserted here to use zone table loaded at startup rather than
        calling hass on all polls
        '''
        zone_selected_dist = HIGH_INTEGER
        zone_selected      = None
        zones_msg          = ""
        iosapp_zone_msg    = ""

        zone_iosapp = self.state_this_poll.get(devicename) if self._is_inzone_zonename(self.state_this_poll.get(devicename)) else None

        for zone in self.zone_lat:
            #Skip another device's stationary zone or if at base location
            if (instr(zone, STATIONARY) and instr(zone, devicename) is False):
                continue

            zone_dist = self._calc_distance_km(latitude, longitude,
                    self.zone_lat.get(zone), self.zone_long.get(zone))

            #Do not check Stat Zone if radius=1 (at base loc) but include in log_msg
            if self.zone_radius_m.get(zone) > 1:
                in_zone_flag      = zone_dist < self.zone_radius_km.get(zone)
                closer_zone_flag  = zone_selected is None or zone_dist < zone_selected_dist
                smaller_zone_flag = (zone_dist == zone_selected_dist
                        and self.zone_radius_km.get(zone) <= self.zone_radius_km.get(zone_selected))

                if in_zone_flag and (closer_zone_flag or smaller_zone_flag):
                    zone_selected_dist = zone_dist
                    zone_selected      = zone
                    iosapp_zone_msg    = ""

                #If closer than 200m, keep zone name for ios app state override  f
                #ios app is in a Zone but dist is still outside a zone's radius
                elif (zone_iosapp and zone == zone_iosapp and zone_dist < .2):
                    zone_selected_dist = zone_dist
                    zone_selected      = zone
                    iosapp_zone_msg    = " (Using iOSApp State)"

            if (instr(zone, STATIONARY)):
                zones_msg += self.zone_to_display.get(STATIONARY)
            else:
                zones_msg += self.zone_to_display.get(zone)
            zones_msg += (f"-{self._format_dist(zone_dist)}"
                         f"/r{round(self.zone_radius_m.get(zone))}, ")

        if zone_selected is None:
            zone_selected      = NOT_HOME
            zone_selected_dist = 0

            #If not in a zone and was in a Stationary Zone, Exit the zone and reset everything
            if self.in_stationary_zone_flag.get(devicename):
                self._update_stationary_zone(
                        devicename,
                        self.stat_zone_base_lat,
                        self.stat_zone_base_long,
                        STAT_ZONE_MOVE_TO_BASE, '_get_zone')

        elif instr(zone,'nearzone'):
            zone_selected = 'near_zone'

        event_msg  = (f"Selected Zone > ")

        if self.DISPLAY_ZFNAME:
            zname, ztitle, zfname = self._get_zone_names(zone_selected)
            event_msg += zname
        else:
            event_msg += self.zone_to_display.get(zone_selected, NOT_HOME)

        event_msg += (f"{iosapp_zone_msg} > {zones_msg[:-2]}")

        self._log_debug_msg(devicename, event_msg)
        if display_zone_msg:
            self._save_event(devicename, event_msg)

        if (self.zone_last.get(devicename) == ''):
            self.zone_last[devicename]  = zone_selected

        #Get distance between zone selected and current zone to see if they overlap
        if self._is_overlapping_zone(self.zone_current.get(devicename), zone_selected):
            if (self.zone_current.get(devicename) != zone_selected):
                self.zone_last[devicename]      = self.zone_current.get(devicename)
                self.zone_current[devicename]   = zone_selected
                self.zone_timestamp[devicename] = \
                            dt_util.now().strftime(self.um_date_time_strfmt)

        #If the zone changed from a previous poll, save it and set the new one
        #First time thru, initialize zone_last
        elif (self.zone_current.get(devicename) != zone_selected):
            self.zone_last[devicename]      = self.zone_current.get(devicename)
            self.zone_current[devicename]   = zone_selected
            self.zone_timestamp[devicename] = \
                        dt_util.now().strftime(self.um_date_time_strfmt)

        log_msg = (f"GET ZONE RESULTS, Zone-{zone_selected}, "
                   f"{format_gps(latitude, longitude, 0)}, "
                   f"StateThisPoll-{self.state_this_poll.get(devicename)}, "
                   f"LastZone-{self.zone_last.get(devicename)}, "
                   f"ThisZone-{self.zone_current.get(devicename)}")
        self._log_debug_msg(devicename, log_msg)

        return zone_selected

#--------------------------------------------------------------------
    def _is_overlapping_zone(self, zone1, zone2):
        '''
        zone1 and zone2 overlap if their distance between centers is less than 2m
        '''
        try:
            if zone1 == zone2:
                return True

            if zone1 == "": zone1 = HOME
            zone_dist = self._calc_distance_m(
                self.zone_lat.get(zone1), self.zone_long.get(zone1),
                self.zone_lat.get(zone2), self.zone_long.get(zone2))

            return (zone_dist <= 2)

        except:
            return False

#--------------------------------------------------------------------
    def _get_zone_names(self, zone):
        """
        Make zone_names 1, 2, & 3 out of the zone_name value for sensors

        name  = home --> Home
                not_home --> Away
                gary_iphone_stationary --> Stationary
                the_shores --> TheShores
        title = gary_iphone_stationary --> Gary Iphone Stationary
                office_bldg_1 --> Office Bldg 1
        fname = gary_iphone_stationary --> GaryIphoneStationary
                office__bldg_1 --> Office Bldg1
        """
        if zone:
            ztitle = zone.title().replace("_S_","'s " ).replace("_", " ")
            zfname = self.zone_fname.get(zone, ztitle)

            if instr(zone, STATIONARY):
                zname = STATIONARY
            elif instr(zone, NOT_HOME):
                zname = AWAY
            else:
                zname = ztitle.replace(" ","")

        else:
            zname  = NOT_SET
            ztitle = 'Not Set'
            zfname = 'NotSet'

        return [zname, ztitle, zfname]

#--------------------------------------------------------------------
    @staticmethod
    def _format_zone_name(devicename, zone):
        '''
        The Stationary zone info is kept by 'devicename_stationary'. Other zones
        are kept as 'zone'. Format the name based on the zone.
        '''
        return f"{devicename}_stationary" if zone == STATIONARY else zone

#--------------------------------------------------------------------
    def _set_base_zone_name_lat_long_radius(self, zone):
        '''
        Set the base_zone's name, lat, long & radius
        '''
        self.base_zone        = zone
        self.base_zone_name   = self.zone_to_display.get(zone)
        self.base_zone_lat    = self.zone_lat.get(zone)
        self.base_zone_long   = self.zone_long.get(zone)
        self.base_zone_radius_km = float(self.zone_radius_km.get(zone))

        return

#--------------------------------------------------------------------
    def _zone_distance_m(self, devicename, zone, latitude, longitude):
        '''
        Get the distance from zone `zone`
        '''

        zone_dist = HIGH_INTEGER

        if self.zone_lat.get(zone):
            zone_name = self._format_zone_name(devicename, zone)

            zone_dist = self._calc_distance_m(
                            latitude,
                            longitude,
                            self.zone_lat.get(zone_name),
                            self.zone_long.get(zone_name))

            log_msg = (f"ZONE DIST {devicename}, Zone-{zone_name}, "
                       f"CurrGPS-{format_gps(latitude, longitude, 0)}, "
                       f"ZoneGPS-{format_gps(self.zone_lat.get(zone_name), self.zone_long.get(zone_name), 0)}, "
                       f"Dist-{zone_dist}m")
            #self._log_debug_msg(devicename, log_msg)

        return zone_dist

#--------------------------------------------------------------------
    def _is_inzone(self, devicename):
        return (self.state_this_poll.get(devicename) != NOT_HOME)

    def _isnot_inzone(self, devicename):
        return (self.state_this_poll.get(devicename) == NOT_HOME)

    def _was_inzone(self, devicename):
        return (self.state_last_poll.get(devicename) != NOT_HOME)

    def _wasnot_inzone(self, devicename):
        return (self.state_last_poll.get(devicename) == NOT_HOME)

    def _is_inzone_stationary(self, devicename):
        return (instr(self.state_this_poll.get(devicename), STATIONARY))

    def _isnot_inzone_stationary(self, devicename):
        return (instr(self.state_this_poll.get(devicename), STATIONARY) is False)

    def _was_inzone_stationary(self, devicename):
        return (instr(self.state_last_poll.get(devicename), STATIONARY))

    def _wasnot_inzone_stationary(self, devicename):
        return (instr(self.state_last_poll.get(devicename), STATIONARY) is False)

    @staticmethod
    def _is_inzone_zonename(zone):
        return (zone != NOT_HOME)

    @staticmethod
    def _isnot_inzone_zonename(zone):
        #_LOGGER.warning("_isnot_inzone_zonename = %s",(zone == NOT_HOME))
        return (zone == NOT_HOME)
#--------------------------------------------------------------------
    def _wait_if_update_in_process(self, devicename=None):
        #An update is in process, must wait until done
        wait_cnt = 0
        while self.update_in_process_flag:
            wait_cnt += 1
            if devicename:
                attrs = {}
                attrs[ATTR_INTERVAL] = (f"WAIT-{wait_cnt}")

                self._update_device_sensors(devicename, attrs)

            time.sleep(2)

#--------------------------------------------------------------------
    def _update_last_latitude_longitude(self, devicename, latitude, longitude, called_from=""):
        #Make sure that the last latitude/longitude is not set to the
        #base stationary one before updating. If it is, do not save them

        if latitude is None or longitude is None:
            error_msg = (f"Discarded > Undefined GPS Coordinates, "
                         f"UpdateRequestedBy-{called_from}")

        elif latitude == self.stat_zone_base_lat and longitude == self.stat_zone_base_long:
            error_msg = (f"Discarded > Can not set current location to Stationary "
                         f"Base Zone location {format_gps(latitude, longitude, 0)}, "
                         f"UpdateRequestedBy-{called_from}")
        else:
            self.last_lat[devicename]  = latitude
            self.last_long[devicename] = longitude
            return True

        self._save_event_halog_info(devicename, error_msg)
        return False

#--------------------------------------------------------------------
    @staticmethod
    def _latitude_longitude_none(latitude, longitude):
        return (latitude is None or longitude is None)

#--------------------------------------------------------------------
    def _update_stationary_zone(self, devicename, latitude, longitude, enter_exit_flag, calledfrom=''):
        """ Set, Enter, Exit, Move stationary zone """

        try:

            event_log_devicename = "*" if self.start_icloud3_inprocess_flag else devicename
            stat_zone_name = self._format_zone_name(devicename, STATIONARY)
            self.stat_zone_update_location[stat_zone_name] = ""       #clear update location

            if latitude is None or longitude is None:
                return

            stat_zone_dist = self._calc_distance_m(latitude, longitude,
                                    self.zone_lat.get(stat_zone_name), self.zone_long.get(stat_zone_name))
            stat_home_dist = self._calc_distance_m(latitude, longitude,
                                    self.zone_home_lat, self.zone_home_long,)

            #Make sure stationary zone is not being moved to another zone's location unless it a
            #Stationary Zone
            for zone in self.zone_lat:
                if instr(zone, STATIONARY) is False:
                    zone_dist = self._calc_distance_m(latitude, longitude, self.zone_lat.get(zone), self.zone_long.get(zone))
                    if zone_dist < self.zone_radius_m.get(zone):
                        event_msg = (f"Move into stationary zone cancelled > Too close to zone-{zone}, Dist-{zone_dist}m")
                        self._save_event(devicename, event_msg)
                        self.stat_zone_timer[devicename] = self.this_update_secs + self.stat_zone_still_time

                        return False

            self.zone_lat[stat_zone_name]          = latitude
            self.zone_long[stat_zone_name]         = longitude
            self.zone_passive[stat_zone_name]      = not enter_exit_flag
            self.stat_zone_moved_total[devicename] = 0

            attrs = {}
            attrs[CONF_NAME]          = stat_zone_name
            attrs[ATTR_LATITUDE]      = latitude
            attrs[ATTR_LONGITUDE]     = longitude
            attrs['icon']             = (f"mdi:{self.stat_zone_devicename_icon.get(devicename)}")
            attrs[ATTR_FRIENDLY_NAME] = stat_zone_name

            #If Stationary zone is exited, move it back to it's base location
            #and reduce it's size
            if enter_exit_flag == STAT_ZONE_MOVE_TO_BASE:
                attrs['passive']                    = True
                attrs[ATTR_RADIUS]                  = 1
                self.zone_radius_m[stat_zone_name]  = 1
                self.zone_radius_km[stat_zone_name] = .1
                self.stat_zone_timer[devicename]    = 0
                self.in_stationary_zone_flag[devicename] = False

                self.stat_zone_update_location[stat_zone_name] = attrs

                if self.start_icloud3_inprocess_flag is False:
                    event_msg = (f"Reset Stationary Zone Location > {stat_zone_name}, "
                                 f"Moved to Base Location-{format_gps(latitude, longitude, 0)}, "
                                 f"DistFromHome-{self._format_dist_m(stat_home_dist)}")
                    self._save_event(devicename, event_msg)

                else:
                    self.zone_to_display[stat_zone_name]   = 'Stationary'
                    self.state_to_zone[stat_zone_name] = stat_zone_name

                return True

            #Set Stationary Zone at new location
            attrs['passive']                    = False
            attrs[ATTR_RADIUS]                  = self.stat_zone_radius_m
            self.zone_radius_m[stat_zone_name]  = self.stat_zone_radius_m
            self.zone_radius_km[stat_zone_name] = self.stat_zone_radius_km
            self.in_stationary_zone_flag[devicename] = True

            self.stat_zone_update_location[stat_zone_name] = attrs

            self._trace_device_attributes(stat_zone_name, "SET.STAT.ZONE", "SetStatZone", attrs)

            if stat_zone_dist > self.stat_zone_radius_m:
                event_msg = (f"Moving Into Stationary Zone >")
            else:
                event_msg = (f"Moving Stationary Zone Location >")
            event_msg  += (f" {stat_zone_name}, "
                         f"GPS-{format_gps(latitude, longitude, 0)}, "
                         f"DistFromHome-{self._format_dist_m(stat_home_dist)}")
            if stat_zone_dist <= self.stat_zone_radius_m:
                event_msg += (f", DistFromLastLoc-{stat_zone_dist}m")
            if self.stat_zone_timer.get(devicename) > 0:
                event_msg += (f", StationarySince-{self._format_time_age(self.stat_zone_timer.get(devicename) - self.stat_zone_still_time)}")
            self._save_event_halog_info(event_log_devicename, event_msg)

            self.stat_zone_timer[devicename] = 0

            return True

        except Exception as err:
            _LOGGER.exception(err)
            log_msg = (f"►INTERNAL ERROR (UpdtStatZone-{err})")
            self._log_error_msg(log_msg)

            return False

#--------------------------------------------------------------------
    def _update_stationary_zone_location(self, devicename):
        ''' move the stationary zone to it's new location if necessary '''

        try:
            stat_zone_name = self._format_zone_name(devicename, STATIONARY)

            attrs =  self.stat_zone_update_location.get(stat_zone_name, '')
            if attrs != '':
                self._set_state("zone." + stat_zone_name, "zoning", attrs)


        except Exception as err:
            _LOGGER.exception(err)
            pass

#--------------------------------------------------------------------
    def _reset_stat_zone_time(self):
        ''' returns the initial value of the stationary zone timer '''
        return self.this_update_secs + self.stat_zone_still_time

#--------------------------------------------------------------------
    def _update_device_sensors(self, arg_devicename, attrs:dict):
        '''
        Update/Create sensor for the device attributes

        sensor_device_attrs = ['distance', 'calc_distance', 'waze_distance',
                          'travel_time', 'dir_of_travel', 'interval', 'info',
                          'last_located', 'last_update', 'next_update',
                          'poll_count', 'trigger', 'battery', 'battery_state',
                          'gps_accuracy', 'zone', 'last_zone', 'travel_distance']

        sensor_attrs_format = {'distance': 'dist', 'calc_distance': 'dist',
                          'travel_distance': 'dist', 'battery': '%',
                          'dir_of_travel': 'title'}
        '''
        try:
            if not attrs:
                return

            #check to see if arg_devicename is really devicename_zone
            if instr(arg_devicename, ":") is False:
                devicename  = arg_devicename
                prefix_zone = self.base_zone
            else:
                devicename  = arg_devicename.split(':')[0]
                prefix_zone = arg_devicename.split(':')[1]

            badge_state = None
            badge_zone  = None
            badge_dist  = None
            attr_fname_prefix = self.sensor_attr_fname_prefix.get(devicename)
            base_entity = self.sensor_prefix_name.get(devicename, devicename)

            if prefix_zone == HOME:
                base_entity       = (f"sensor.{self.sensor_prefix_name.get(devicename, devicename)}")
            else:
                base_entity       = (f"sensor.{prefix_zone}_{self.sensor_prefix_name.get(devicename, devicename)}")

            for attr_name in SENSOR_DEVICE_ATTRS:
                sensor_entity = (f"{base_entity}_{attr_name}")
                if attr_name in attrs:
                    state_value = attrs.get(attr_name)
                else:
                    continue

                sensor_attrs = {}
                if attr_name in SENSOR_ATTR_FORMAT:
                    format_type = SENSOR_ATTR_FORMAT.get(attr_name)
                    if format_type == 'dist':
                        sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = self.unit_of_measurement

                    elif format_type == 'diststr':
                        try:
                            x = (state_value / 2)
                            sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = self.unit_of_measurement
                        except:
                            sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = ''
                    elif format_type == '%':
                        sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = '%'
                    elif format_type == 'min' and instr(state_value, 'min') is False and instr(state_value, 'hr') is False:
                        sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = 'min'
                    elif format_type == 'title':
                        state_value = state_value.title().replace('_', ' ')
                    elif format_type == 'kph-mph':
                        sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = self.um_kph_mph
                    elif format_type == 'm-ft':
                        sensor_attrs[CONF_UNIT_OF_MEASUREMENT] = self.um_m_ft
                    elif format_type == 'timestamp-time':
                        if state_value == TIMESTAMP_ZERO:
                            state_value = ''
                        else:
                            state_value = self._timestamp_to_time(state_value)
                            state_value = self._time_to_12hrtime(state_value)

                if attr_name in SENSOR_ATTR_ICON:
                    sensor_attrs['icon'] = SENSOR_ATTR_ICON.get(attr_name)

                if attr_name in SENSOR_ATTR_FNAME:
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix}{SENSOR_ATTR_FNAME.get(attr_name)}")

                self._update_device_sensors_hass(devicename, base_entity, attr_name,
                                    state_value, sensor_attrs)

                if attr_name == ATTR_ZONE:
                    zname, ztitle, zfname = self._get_zone_names(state_value)
                    zone_attrs = {}
                    zone_attrs['icon'] = SENSOR_ATTR_ICON.get(attr_name)
                    if badge_state is None: badge_state = zname

                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Zone Name")
                    self._update_device_sensors_hass(devicename, base_entity, "zone_name", zname, sensor_attrs)
                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Zone Title")
                    self._update_device_sensors_hass(devicename, base_entity, "zone_title", ztitle, sensor_attrs)
                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Zone Fname")
                    self._update_device_sensors_hass(devicename, base_entity, "zone_fname", zfname, sensor_attrs)

                elif attr_name == 'last_zone':
                    zname, ztitle, zfname = self._get_zone_names(state_value)
                    zone_attrs = {}
                    zone_attrs['icon'] = SENSOR_ATTR_ICON.get(attr_name)

                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Last Zone Name")
                    self._update_device_sensors_hass(devicename, base_entity, "last_zone_name", zname, sensor_attrs)
                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Last Zone Title")
                    self._update_device_sensors_hass(devicename, base_entity,  "last_zone_title", ztitle, sensor_attrs)
                    sensor_attrs = dict(zone_attrs)
                    sensor_attrs[ATTR_FRIENDLY_NAME] = (f"{attr_fname_prefix} Last Zone Fname")
                    self._update_device_sensors_hass(devicename, base_entity,  "last_zone_fname", zfname, sensor_attrs)

                elif attr_name == 'zone_distance':
                    if state_value and float(state_value) > 0:
                        badge_state = (f"{state_value} {self.unit_of_measurement}")

            if self._is_device_paused(devicename): badge_state = PAUSED_CAPS

            if badge_state:
                self._update_device_sensors_hass(devicename,
                            base_entity,
                            "badge",
                            badge_state,
                            self.sensor_badge_attrs.get(devicename))
            return True

        except Exception as err:
            _LOGGER.exception(err)
            log_msg = (f"►INTERNAL ERROR (UpdtSensorUpdate-{err})")
            self._log_error_msg(log_msg)

            return False
#--------------------------------------------------------------------
    def _update_device_sensors_hass(self, devicename, base_entity, attr_name,
                                    state_value, sensor_attrs):

        try:
            state_value = state_value[0:250]
        except:
            pass

        if attr_name in self.sensors_custom_list:
            sensor_entity = (f"{base_entity}_{attr_name}")

            self._set_state(sensor_entity, state_value, sensor_attrs)

#--------------------------------------------------------------------
    def _format_info_attr(self, devicename, battery,
                            gps_accuracy, dist_last_poll_moved_km,
                            zone):

        """
        Initialize info attribute
        """
        devicename_zone = self._format_devicename_zone(devicename)
        try:
            info_msg = ''
            if self.info_notification != '':
                info_msg = f"●●{self.info_notification}●●"
                self.info_notification = ''

            if self.base_zone != HOME:
                info_msg += (f" • Base.Zone: {self.base_zone_name}")

            if (self.TRK_METHOD_IOSAPP
                    and self.tracking_method_config != IOSAPP):
                info_msg += (f" • Track.Method: iOSApp")

            if self.override_interval_seconds.get(devicename) > 0:
                info_msg += " • Overriding.Interval"

            if zone == 'near_zone':
                info_msg += " • NearZone"

            if battery > 0:
                info_msg += f" • Battery-{battery}%"

            if gps_accuracy > self.gps_accuracy_threshold:
                info_msg += (f" • Poor.GPS.Accuracy, Dist-{self._format_dist(gps_accuracy)}")
                if self.poor_location_gps_cnt.get(devicename) > 0:
                    info_msg += (f" (#{self.poor_location_gps_cnt.get(devicename)})")
                if (self._is_inzone_zonename(zone)
                        and self.ignore_gps_accuracy_inzone_flag):
                    info_msg += " - Discarded"

            old_cnt = self.poor_location_gps_cnt.get(devicename)
            if old_cnt > 16:
                location_age = self._secs_since(self.last_located_secs.get(devicename))
                info_msg += (f" • May Be Offline, "
                             f"LocTime-{self._format_time_age(self.last_located_secs.get(devicename))}, "
                             f"OldCnt-#{old_cnt}")

            if self.stat_zone_timer.get(devicename) > 0:
                info_msg += (f" • MoveIntoStatZone@{self._secs_to_time(self.stat_zone_timer.get(devicename))}")

            if self.waze_data_copied_from.get(devicename):
                copied_from = self.waze_data_copied_from.get(devicename)
                if devicename != copied_from:
                    info_msg += (f" • Using Waze data from {self.fname.get(copied_from)}")

        except Exception as err:
            _LOGGER.exception(err)
            info_msg += (f"Error setting up info attribute-{err}")
            self._log_error_msg(info_msg)

        return info_msg

#--------------------------------------------------------------------
    def _display_info_status_msg(self, devicename_zone, info_msg, start_icloud3_initial_load_flag=False):
        '''
        Display a status message in the info sensor. If the devicename_zone
        parameter contains the base zone (devicename:zone), display only for that
        devicename_zone, otherwise (devicename), display for all zones for
        the devicename.
        '''
        try:
            #save_base_zone = self.base_zone
            if (start_icloud3_initial_load_flag
                    or self.config_track_devices_fields == []):
                return ""

            if devicename_zone == '':
                devicename = self.config_track_devices_fields[0].get(CONF_DEVICENAME)

            elif instr(devicename_zone, ':'):
                devicename = devicename_zone.split(':')[0]

            else:
                devicename = devicename_zone

            elapsed_time = ''

            attrs = {}
            attrs[ATTR_INFO] = f"●● {info_msg}{elapsed_time} ●●"
            self._update_device_sensors(devicename, attrs)

        #Will get an error before the tracked devices info is set up
        except Exception as err:
            _LOGGER.exception(err)
            return ""

        #return formatted msg for event log
        return (f"{CRLF_DOT}{info_msg}")

#--------------------------------------------------------------------
    def _update_count_discarded_update_attribute(self, devicename, info = None):
        self.count_discarded_update[devicename] += 1

        try:
            attrs  = {}
            attrs[ATTR_POLL_COUNT] = self._format_poll_count(devicename)

            self._update_device_sensors(devicename, attrs)

        except:
            pass
#--------------------------------------------------------------------
    def _format_poll_count(self, devicename):

        return (f"{self.count_update_icloud.get(devicename)}:"
                f"{self.count_update_iosapp.get(devicename)}:"
                f"{self.count_discarded_update.get(devicename)}")

#--------------------------------------------------------------------
    def _display_usage_counts(self, devicename, force_display=False):


        try:
            if devicename not in self.count_update_icloud:
                self._initialize_usage_counters(devicename, True)

            total_count = self.count_update_icloud.get(devicename) + \
                          self.count_update_iosapp.get(devicename) + \
                          self.count_discarded_update.get(devicename) + \
                          self.count_state_changed.get(devicename) + \
                          self.count_trigger_changed.get(devicename) + \
                          self.iosapp_request_loc_cnt.get(devicename)

            pyi_avg_time_per_call = 0
            if self.count_pyicloud_location_update > 0:
                pyi_avg_time_per_call = self.time_pyicloud_calls / \
                    (self.count_pyicloud_authentications + self.count_pyicloud_location_update)

            #Verify average and counts, reset counts if average time > 1 min
            if pyi_avg_time_per_call > 60:
                pyi_avg_time_per_call               = 0
                self.time_pyicloud_calls            = 0
                self.count_pyicloud_authentications = 0
                self.count_pyicloud_location_update = 0

            #If updating the devicename's info_msg, only add to the event log
            #and info_msg if the counter total is divisible by 5.
            total_count = 1
            hour = int(dt_util.now().strftime('%H'))
            if force_display:
                pass
            elif (hour % 3) != 0:
                return (None, 0)
            elif total_count == 0:
                return (None, 0)

            #    ¤s=<table>                         Table start, Row start
            #    ¤e=</table>                        Row end, Table end
            #    §=</tr><tr>                        Row end, next row start
            #    »   =</td></tr>
            #    «LT- =<tr><td style='width: 28%'>    Col start, 40% width
            #    ¦LC-=</td><td style='width: 8%'>   Col end, next col start-width 40%
            #    ¦RT-=</td><td style='width: 28%'>   Col end, next col start-width 10%
            #    ¦RC-=</td><td style='width: 8%'>   Col end, next col start-width 40%

            count_msg =  (f"¤s")
            state_trig_count = self.count_state_changed.get(devicename) + self.count_trigger_changed.get(devicename)

            if self.TRK_METHOD_FMF_FAMSHR:
                count_msg += (f"«HS¦LH-Device Counts¦RH-iCloud Counts»HE"
                              f"«LT-State/Trigger Chgs¦LC-{state_trig_count}¦RT-Authentications¦RC-{self.count_pyicloud_authentications}»"
                              f"«LT-iCloud Updates¦LC-{self.count_update_icloud.get(devicename)}¦RT-Total iCloud Loc Rqsts¦RC-{self.count_pyicloud_location_update}»"
                              f"«LT-iOS App Updates¦LC-{self.count_update_iosapp.get(devicename)}¦RT-Time/Locate (secs)¦RC-{round(pyi_avg_time_per_call, 2)}»")
            else:
                count_msg += (f"«HS¦LH-Device Counts¦RH-iOS App Counts»HE"
                              f"«LT-State/Triggers Chgs¦LC-{state_trig_count}¦RT-iOS Locate Requests¦RC-{self.iosapp_request_loc_cnt.get(devicename)}»"
                              f"«LT-iCloud Updates¦LC-{self.count_update_icloud.get(devicename)}¦RT-iOS App Updates¦RC-{self.count_update_iosapp.get(devicename)}»")

            count_msg     += (f"«LT-Discarded¦LC-{self.count_discarded_update.get(devicename)}¦RT-Waze Routes¦RC-{self.count_waze_locates.get(devicename)}»"
                              f"¤e")

            self._save_event(devicename, f"{count_msg}")

        except Exception as err:
            _LOGGER.exception(err)

        return (None, 0)

#########################################################
#
#   Perform tasks on a regular time schedule
#
#########################################################
    def _timer_tasks_every_hour(self):
        for devicename in self.tracked_devices:
            self._display_usage_counts(devicename)

#--------------------------------------------------------------------
    def _timer_tasks_midnight(self):
        for devicename in self.tracked_devices:
            devicename_zone = self._format_devicename_zone(devicename, HOME)

            event_msg = (f"^^^iCloud3 v{VERSION} Daily Summary > "
                         f"{dt_util.now().strftime('%A, %b %d')}")
            self._save_event_halog_info(devicename, event_msg)

            self.count_pyicloud_authentications = 0
            self.count_pyicloud_location_update = 0
            self.time_pyicloud_calls            = 0.0
            self._initialize_usage_counters(devicename, True)

        for devicename_zone in self.waze_distance_history:
            self.waze_distance_history[devicename_zone] = ''

#--------------------------------------------------------------------
    def _timer_tasks_1am(self):
        self._calculate_time_zone_offset()

#########################################################
#
#   VARIABLE DEFINITION & INITIALIZATION FUNCTIONS
#
#########################################################
    def _define_tracking_control_fields(self):
        self.icloud3_started_secs            = 0
        self.icloud_acct_auth_error_cnt      = 0
        self.immediate_retry_flag            = False
        self.time_zone_offset_seconds        = self._calculate_time_zone_offset()
        self.setinterval_cmd_devicename      = None
        self.update_in_process_flag          = False
        self.track_devicename_list           = ''       #text string used during initialization that is displayed in evlog
        self.any_device_being_updated_flag   = False
        self.tracked_devices                 = []       #list of devicenames that have been verified that are being tracked
        self.config_track_devices_fields     = []       #track_devices + devices config parameter list/dict of fields for each device
        self.config_ic3_track_devices_fields = []       #track_devices + devices config parameter list/dict of fields for each device
        self.trigger                         = {}       #device update trigger
        self.last_iosapp_trigger             = {}       #last trigger issued by iosapp
        self.got_exit_trigger_flag           = {}       #iosapp issued exit trigger leaving zone
        self.device_being_updated_flag       = {}
        self.device_being_updated_retry_cnt  = {}
        self.last_iosapp_state               = {}
        self.last_iosapp_state_changed_time  = {}
        self.last_iosapp_state_changed_secs  = {}
        self.last_iosapp_trigger             = {}
        self.last_iosapp_trigger_changed_time= {}
        self.last_iosapp_trigger_changed_secs= {}

        self.iosapp_update_flag              = {}
        self.iosapp_monitor_dev_trk_flag     = {}
        self.iosapp_monitor_error_cnt        = {}
        self.iosapp_last_trigger_entity      = {} #sensor entity extracted from entity_registry
        self.iosapp_battery_level_entity     = {} #sensor entity extracted from entity_registry

        self.iosapp_stat_zone_action_msg_cnt = {}
        self.authenticated_time              = 0
        self.authentication_error_cnt        = 0
        self.authentication_error_retry_secs = HIGH_INTEGER
        self.info_notification               = ''
        self.broadcast_msg                   = ''

        this_update_time = dt_util.now().strftime('%H:%M:%S')
#--------------------------------------------------------------------
    def _define_event_log_fields(self):
        self.event_log_table              = []
        self.event_log_base_attrs         = ''
        self.log_table_max_items          = 999
        self.event_log_clear_secs         = HIGH_INTEGER
        self.event_log_sensor_state       = ''
        self.event_log_last_devicename    = '*'

#--------------------------------------------------------------------
    def _define_device_fields(self):
        '''
        Dictionary fields for each devicename
        '''
        self.fname                        = {}    #name made from status[CONF_NAME]
        self.badge_picture                = {}    #devicename picture from badge setup
        self.api_devices                  = None  #icloud.api.devices obj
        self.famshr_data_devicename_fname = {}    #famshr device data, devicename by fname, fname by devicename
        self.devicename_device_id         = {}    #fmf/famshr devicenname's device id
        self.devicename_device_id_fmf     = {}    #fmf devicenname's device id
        self.devicename_device_id_famshr  = {}    #famshr devicenname's device id
        self.devicename_by_device_id      = {}    #fmf/famshr devices id's devicename
        self.data_source                  = {}
        self.device_type                  = {}
        self.device_status                = {}
        self.devicename_iosapp_entity     = {}
        self.devicename_iosapp_suffix     = {}
        self.notify_iosapp_entity         = {}
        self.devicename_tracking_method   = {}
        self.devicename_evlog_tracked_msg     = {}
        self.devicename_evlog_not_tracked_msg = {}
        self.devicename_verified          = {}    #Set to True in mode setup fcts
        self.devicename_email             = {}
        self.seen_this_device_flag        = {}
        self.device_tracker_entity_ic3    = {}
        self.device_tracker_entity_iosapp = {}
        self.track_from_zones             = {}    #Track device from other zone
        self.inzone_interval_secs         = {}
        self.display_text_as              = {}

#--------------------------------------------------------------------
    def _define_device_status_fields(self):
        '''
        Dictionary fields for each devicename
        '''
        self.state_this_poll              = {}
        self.state_last_poll              = {}
        self.zone_last                    = {}
        self.zone_current                 = {}
        self.zone_timestamp               = {}
        self.state_change_flag            = {}
        self.location_data                = {}
        self.last_located_time            = {}
        self.last_located_secs            = {}    #device timestamp in seconds
        self.went_3km                     = {} #>3 km/mi, probably driving

#--------------------------------------------------------------------
    def _initialize_device_status_fields(self, devicename):
        '''
        Make domain name entity ids for the device_tracker and
        sensors for each device so we don't have to do it all the
        time. Then check to see if 'sensor.geocode_location'
        exists. If it does, then using iosapp version 2.
        '''
        entity_id                                     = (f"device_tracker.{devicename}")
        self.device_tracker_entity_ic3[devicename]    = entity_id
        self.state_this_poll[devicename]              = self._get_state(entity_id)
        self.state_last_poll[devicename]              = NOT_SET
        self.device_status[devicename]                = UNKNOWN
        self.zone_last[devicename]                    = ''
        self.zone_current[devicename]                 = ''
        self.zone_timestamp[devicename]               = ''
        self.state_change_flag[devicename]            = False
        self.location_data[devicename]                = INITIAL_LOCATION_DATA
        self.last_located_time[devicename]            = HHMMSS_ZERO
        self.last_located_secs[devicename]            = 0
        self.went_3km[devicename]                     = False

        self.trigger[devicename]                      = 'iCloud3'
        self.got_exit_trigger_flag[devicename]        = False
        self.seen_this_device_flag[devicename]        = False
        self.device_being_updated_flag[devicename]    = False
        self.device_being_updated_retry_cnt[devicename] = 0

        self.iosapp_update_flag[devicename]           = False

        #iosapp v2 entity info
        self.last_iosapp_state[devicename]                = ''
        self.last_iosapp_state_changed_time[devicename]   = ''
        self.last_iosapp_state_changed_secs[devicename]   = 0
        self.last_iosapp_trigger[devicename]              = ''
        self.last_iosapp_trigger_changed_time[devicename] = ''
        self.last_iosapp_trigger_changed_secs[devicename] = 0
        self.iosapp_monitor_error_cnt[devicename]         = 0


#--------------------------------------------------------------------
    def _initialize_um_formats(self, unit_of_measurement):
        #Define variables, lists & tables
        if unit_of_measurement == 'mi':
            if self.time_format != 24: self.time_format = 12
            self.um_km_mi_factor          = 0.62137
            self.um_m_ft                  = 'ft'
            self.um_kph_mph               = 'mph'
        else:
            if self.time_format != 12: self.time_format = 24
            self.um_km_mi_factor          = 1
            self.um_m_ft                  = 'm'
            self.um_kph_mph               = 'kph'

        if self.time_format == 12:
            self.um_time_strfmt       = '%I:%M:%S'
            self.um_time_strfmt_ampm  = '%I:%M:%S%P'
            self.um_date_time_strfmt  = '%Y-%m-%d %I:%M:%S'
        else:
            self.um_time_strfmt       = '%H:%M:%S'
            self.um_time_strfmt_ampm  = '%H:%M:%S'
            self.um_date_time_strfmt  = '%Y-%m-%d %H:%M:%S'

#--------------------------------------------------------------------
    def _setup_tracking_method(self, tracking_method):
        '''
        Set up tracking method
        '''
        self.TRK_METHOD_FMF_FAMSHR = (tracking_method in FMF_FAMSHR)
        self.CONF_TRK_METHOD_FMF_FAMSHR = (tracking_method in FMF_FAMSHR)
        if (self.TRK_METHOD_FMF_FAMSHR and PYICLOUD_IC3_IMPORT_SUCCESSFUL is False):
           tracking_method = IOSAPP

        self.TRK_METHOD_IOSAPP = (tracking_method in IOSAPP_IOSAPP1)

        self.trk_method_config     = tracking_method
        self.trk_method            = tracking_method
        self.attr_tracking_msg     = ""

        if self.TRK_METHOD_FMF_FAMSHR and self.password == '':
            event_msg = ("iCloud3 Error > The password is required for the "
                f"iCloud Location Services tracking method. "
                f"The iOS App tracking_method will be used.")
            self._save_event_halog_error("*", event_msg)

            self._setup_iosapp_tracking_method()
#--------------------------------------------------------------------
    def _setup_iosapp_tracking_method(self):
        """ Change tracking method to iOSAPP if FMF or FAMSHR error """
        self.trk_method_config     = IOSAPP
        self.trk_method            = IOSAPP
        self.TRK_METHOD_IOSAPP     = True
        self.TRK_METHOD_FMF_FAMSHR = False

#--------------------------------------------------------------------
    def _define_device_tracking_fields(self):
        #times, flags
        self.update_timer              = {}
        self.override_interval_seconds = {}
        self.dist_from_zone_km_small_move_total = {}
        self.this_update_secs          = 0

        #location, gps
        self.poor_location_gps_cnt    = {}    # override interval while < 4
        self.poor_location_gps_msg    = {}
        self.old_location_secs        = {}
        self.poor_gps_flag            = {}
        self.last_lat                 = {}
        self.last_long                = {}
        self.last_battery             = {}   #used to detect iosapp v2 change
        self.last_gps_accuracy        = {}   #used to detect iosapp v2 change

#--------------------------------------------------------------------
    def _initialize_device_tracking_fields(self, devicename):
        #times, flags
        self.update_timer[devicename]              = time.time()
        self.override_interval_seconds[devicename] = 0
        self.dist_from_zone_km_small_move_total[devicename] = 0

        #location, gps
        self.poor_location_gps_cnt[devicename]  = 0
        self.poor_location_gps_msg[devicename]  = False
        self.old_location_secs[devicename]      = 90    #Timer (secs) before a location is old
        self.poor_gps_flag[devicename]          = False
        self.last_lat[devicename]               = self.zone_home_lat
        self.last_long[devicename]              = self.zone_home_long
        self.last_battery[devicename]           = 0
        self.last_gps_accuracy[devicename]      = 0
        self.stat_zone_timer[devicename]        = 0
        self.stat_zone_moved_total[devicename]  = 0

        stat_zone_name = self._format_zone_name(devicename, STATIONARY)
        self.stat_zone_update_location[stat_zone_name] = ''

        #Other items
        self.data_source[devicename]            = ''
        self.last_iosapp_msg[devicename]        = ''
        self.last_device_monitor_msg[devicename] = ''
        self.iosapp_stat_zone_action_msg_cnt[devicename]= 0

#--------------------------------------------------------------------
    def _define_usage_counters(self):
        self.count_update_icloud            = {}
        self.count_update_iosapp            = {}
        self.count_discarded_update            = {}
        self.count_state_changed            = {}
        self.count_trigger_changed          = {}
        self.count_waze_locates             = {}
        self.time_waze_calls                = {}
        self.count_pyicloud_authentications = 0
        self.count_pyicloud_location_update = 0
        self.time_pyicloud_calls            = 0.0

#--------------------------------------------------------------------
    def _initialize_usage_counters(self, devicename, clear_counters=True):
        if devicename not in self.count_update_icloud or clear_counters:
            self.count_update_icloud[devicename]   = 0
            self.count_update_iosapp[devicename]   = 0
            self.count_discarded_update[devicename]   = 0
            self.count_state_changed[devicename]   = 0
            self.count_trigger_changed[devicename] = 0
            self.count_waze_locates[devicename]    = 0
            self.time_waze_calls[devicename]       = 0.0
#--------------------------------------------------------------------
    def _define_iosapp_message_fields(self):
        self.iosapp_request_loc_sent_flag      = {}
        self.iosapp_request_loc_sent_secs      = {}
        self.iosapp_request_loc_cnt            = {}
        self.iosapp_request_loc_retry_cnt      = {}

#--------------------------------------------------------------------
    def _initialize_iosapp_message_fields(self, devicename):
        self.iosapp_request_loc_sent_flag[devicename] = False
        self.iosapp_request_loc_sent_secs[devicename] = 0
        self.iosapp_request_loc_cnt[devicename]       = 0
        self.iosapp_request_loc_retry_cnt[devicename] = 0

#--------------------------------------------------------------------
    def _initialize_next_update_time(self, devicename):
        for zone in self.track_from_zones.get(devicename):
            devicename_zone = self._format_devicename_zone(devicename, zone)

            self.next_update_time[devicename_zone] = HHMMSS_ZERO
            self.next_update_secs[devicename_zone] = 0

#--------------------------------------------------------------------
    def _define_sensor_fields(self, initial_load_flag):
        #Prepare sensors and base attributes

        if initial_load_flag:
            self.sensor_devicenames       = []
            self.sensors_custom_list      = []
            self.sensor_badge_attrs       = {}
            self.sensor_prefix_name       = {}
            self.sensor_attr_fname_prefix = {}

#--------------------------------------------------------------------
    def _define_zone_fields(self):
        '''
        Dictionary fields for zone friendly names
        '''
        self.zones          = []
        self.zone_to_display= dict(ZONE_TO_DISPLAY_BASE)
        self.state_to_zone  = dict(STATE_TO_ZONE_BASE)
        self.zone_fname     = {}
        self.zone_lat       = {}
        self.zone_long      = {}
        self.zone_radius_km = {}
        self.zone_radius_m  = {}
        self.zone_passive   = {}

#--------------------------------------------------------------------
    def _define_device_zone_fields(self):
        '''
        Dictionary fields for each devicename_zone
        '''
        self.last_tavel_time        = {}
        self.interval_seconds       = {}
        self.interval_str           = {}
        self.last_distance_str      = {}
        self.last_update_time       = {}
        self.last_update_secs       = {}
        self.next_update_secs       = {}
        self.next_update_time       = {}
        self.next_update_in_secs    = {}
        self.next_update_devicenames= []

        #used to calculate distance traveled since last poll
        self.waze_time              = {}
        self.waze_dist              = {}
        self.calc_dist              = {}
        self.zone_dist              = {}

        self.last_ic3dev_timestamp_ses = {}

#--------------------------------------------------------------------
    def _initialize_device_zone_fields(self, devicename):
        #interval, distances, times

        for zone in self.track_from_zones.get(devicename):
            devicename_zone = self._format_devicename_zone(devicename, zone)

            self.last_tavel_time[devicename_zone]   = ''
            self.interval_seconds[devicename_zone]  = 0
            self.interval_str[devicename_zone]      = '0 sec'
            self.last_distance_str[devicename_zone] = ''
            self.last_update_time[devicename_zone]  = HHMMSS_ZERO
            self.last_update_secs[devicename_zone]  = 0
            self.next_update_time[devicename_zone]  = HHMMSS_ZERO
            self.next_update_secs[devicename_zone]  = 0
            self.next_update_in_secs[devicename_zone] = 0

            self.waze_history_data_used_flag[devicename_zone] = False
            self.waze_time[devicename_zone]         = 0
            self.waze_dist[devicename_zone]         = 0
            self.calc_dist[devicename_zone]         = 0
            self.zone_dist[devicename_zone]         = 0

        try:
            #set up stationary zone icon for devicename
            first_initial = self.fname.get(devicename)[0].lower()

            if devicename in self.stat_zone_devicename_icon:
                icon = self.stat_zone_devicename_icon.get(devicename)
            elif (f"alpha-{first_initial}-box") not in self.stat_zone_devicename_icon:
                icon_name = (f"alpha-{first_initial}-box")
            elif (f"alpha-{first_initial}-circle") not in self.stat_zone_devicename_icon:
                icon_name = (f"alpha-{first_initial}-circle")
            elif (f"alpha-{first_initial}-box-outline") not in self.stat_zone_devicename_icon:
                icon_name = (f"alpha-{first_initial}-box-outline")
            elif (f"alpha-{first_initial}-circle-outline") not in self.stat_zone_devicename_icon:
                icon_name = (f"alpha-{first_initial}-circle-outline")
            else:
                icon_name = (f"alpha-{first_initial}")

            self.stat_zone_devicename_icon[devicename] = icon_name
            self.stat_zone_devicename_icon[icon_name]  = devicename

            stat_zone_name = self._format_zone_name(devicename, STATIONARY)
            self.zone_to_display[stat_zone_name] = "Stationary"

        except Exception as err:
            _LOGGER.exception(err)
            self.stat_zone_devicename_icon[devicename] = 'account'

#--------------------------------------------------------------------
    def _initialize_waze_fields(self, waze_region, waze_min_distance,
                waze_max_distance, waze_realtime):
        #Keep distance data to be used by another device if nearby. Also keep
        #source of copied data so that device won't reclone from the device
        #using it.
        self.waze_region   = waze_region.upper()
        self.waze_realtime = waze_realtime

        self.WazeRouteCalc = WazeRouteCalculator(self.waze_region, self.waze_realtime)

        min_dist_msg = (f"{waze_min_distance} {self.unit_of_measurement}")
        max_dist_msg = (f"{waze_max_distance} {self.unit_of_measurement}")

        if self.unit_of_measurement == 'mi':
            self.waze_min_distance = self._mi_to_km(waze_min_distance)
            self.waze_max_distance = self._mi_to_km(waze_max_distance)
            min_dist_msg += (f" ({self.waze_min_distance}km)")
            max_dist_msg += (f" ({self.waze_max_distance}km)")
        else:
            self.waze_min_distance = float(waze_min_distance)
            self.waze_max_distance = float(waze_max_distance)

        self.waze_distance_history = {}
        self.waze_data_copied_from = {}
        self.waze_history_data_used_flag = {}

        self.waze_manual_pause_flag        = False  #If Paused vid iCloud command
        self.waze_close_to_zone_pause_flag = False  #pause if dist from zone < 1 flag

        if self.distance_method_waze_flag:
            log_msg = (f"Set Up Waze > Region-{self.waze_region}, "
                       f"MinDist-{min_dist_msg}, "
                       f"MaxDist-{max_dist_msg}, "
                       f"Realtime-{self.waze_realtime}")
            self._log_info_msg(log_msg)
            self._save_event("*", log_msg)

#--------------------------------------------------------------------
    def _initialize_attrs(self, devicename):
        attrs = {}
        attrs[ATTR_NAME]               = ''
        attrs[ATTR_ZONE]               = NOT_SET
        attrs[ATTR_LAST_ZONE]          = NOT_SET
        attrs[ATTR_ZONE_TIMESTAMP]     = ''
        attrs[ATTR_INTERVAL]           = '___'
        attrs[ATTR_WAZE_TIME]          = 0
        attrs[ATTR_ZONE_DISTANCE]      = 0
        attrs[ATTR_CALC_DISTANCE]      = 0
        attrs[ATTR_WAZE_DISTANCE]      = 0
        attrs[ATTR_LAST_LOCATED]       = '___'    #TIMESTAMP_ZERO
        attrs[ATTR_LAST_UPDATE_TIME]   = '___'    #TIMESTAMP_ZERO
        attrs[ATTR_NEXT_UPDATE_TIME]   = '___'    #TIMESTAMP_ZERO
        attrs[ATTR_POLL_COUNT]         = '0:0:0'
        attrs[ATTR_DIR_OF_TRAVEL]      = '___'
        attrs[ATTR_TRAVEL_DISTANCE]    = 0
        attrs[ATTR_TRIGGER]            = '___'
        attrs[ATTR_TIMESTAMP]          = dt_util.utcnow().isoformat()[0:19]
        attrs[ATTR_AUTHENTICATED]      = ''
        attrs[ATTR_BATTERY]            = 0
        attrs[ATTR_BATTERY_STATUS]     = UNKNOWN
        attrs[ATTR_INFO]               = "● HA is initializing dev_trk attributes ●"
        attrs[ATTR_ALTITUDE]           = 0
        attrs[ATTR_VERT_ACCURACY]      = 0
        attrs[ATTR_DEVICE_STATUS]      = UNKNOWN
        attrs[ATTR_LOW_POWER_MODE]     = ''
        attrs[ATTR_PICTURE]            = self.badge_picture.get(devicename)
        attrs[ATTR_TRACKING]           = self.attr_tracking_msg
        attrs[ATTR_ICLOUD3_VERSION]    = VERSION

        return attrs

#--------------------------------------------------------------------
    def _initialize_zone_tables_step_1(self):
        '''
        Get the zone names from HA, fill the zone tables
        '''

        try:
            if self.start_icloud3_initial_load_flag is False:
                self.hass.services.call(ATTR_ZONE, "reload")
        except:
            pass

        log_msg = (f"Reloading Zone.yaml config file")
        self._log_debug_msg("*", log_msg)

        #zones = self._get_entity_registry_entities('zone', 'zone')
        #zone_ha_config_name = {}
        #for zone_entity in zones:
        #    zone = zone_entity.get('entity_id').replace('zone.', '')
        #    zone_ha_config_name[zone] = zone_entity.get('original_name')
        #TRACE("6309 zone_config_name",zone_ha_config_name)

        zone_msg = ''
        zones = self.hass.states.entity_ids(ATTR_ZONE)
        self._log_debug_msg("*",f"ZONES - {zones}")

        for zone_entity in zones:
            try:
                zone_data = self.hass.states.get(zone_entity).attributes
                zone      = zone_entity.replace('zone.', '')      #zone_entity = 'zone.'+zone

                self.zones.append(zone.lower())
                self._log_debug_msg("*",f"ZONE.DATA - [zone.{zone}--{zone_data}]")

                if ATTR_LATITUDE in zone_data:
                    zname, ztitle, zfname = self._get_zone_names(zone)

                    self.zone_lat[zone]       = zone_data.get(ATTR_LATITUDE, 0)
                    self.zone_long[zone]      = zone_data.get(ATTR_LONGITUDE, 0)
                    self.zone_passive[zone]   = zone_data.get('passive', True)
                    self.zone_radius_m[zone]  = int(zone_data.get(ATTR_RADIUS, 100))
                    self.zone_radius_km[zone] = round(self.zone_radius_m[zone]/1000, 4)
                    zfname                    = zone_data.get(ATTR_FRIENDLY_NAME, zfname)
                    #zfname                    = zone_ha_config_name.get(zone, zfname)
                    self.zone_fname[zone]     = zfname
                    self.zone_fname[zfname]   = zone

                    self.zone_to_display[zone] = zname
                    self.state_to_zone[zfname] = zone
                    if ztitle not in self.state_to_zone:
                        self.state_to_zone[ztitle] = zone
                    ztitle_w = ztitle.replace(' ', '')
                    if ztitle_w not in self.state_to_zone:
                        self.state_to_zone[ztitle_w] = zone

                if instr(zone.lower(), STATIONARY):
                    self.zone_to_display[zone] = 'Stationary'
                    self.zone_fname[zone]      = 'Stationary'

                    self.zone_home_lat    = self.zone_lat.get(HOME)

            except KeyError:
                self.zone_passive[zone] = False

            except Exception as err:
                _LOGGER.exception(err)

        self.zone_home_lat    = self.zone_lat.get(HOME)
        self.zone_home_long   = self.zone_long.get(HOME)
        self.zone_home_radius_km = float(self.zone_radius_km.get(HOME))
        self.zone_home_radius_m  = self.zone_radius_m.get(HOME)

        self.base_zone        = HOME
        self.base_zone_name   = self.zone_to_display.get(HOME)
        self.base_zone_lat    = self.zone_lat.get(HOME)
        self.base_zone_long   = self.zone_long.get(HOME)
        self.base_zone_radius_km = float(self.zone_radius_km.get(HOME))

#--------------------------------------------------------------------
    def _initialize_zone_tables_step_2(self):
        '''
        Display the loaded tables in the Event Log.
        Set up the zone value to be displayed based on the display_zone_format parameter
        '''

        zone_msg = ''
        self.DISPLAY_ZONE   = (self.display_zone_format == CONF_ZONE)
        self.DISPLAY_ZNAME  = (self.display_zone_format == CONF_NAME)
        self.DISPLAY_ZTITLE = (self.display_zone_format == 'title')
        self.DISPLAY_ZFNAME = (self.display_zone_format == 'fname')

        for zone in self.zones:
            zname, ztitle, zfname = self._get_zone_names(zone)

            if self.DISPLAY_ZNAME:
                self.zone_to_display[zone] = zname
            elif self.DISPLAY_ZTITLE:
                self.zone_to_display[zone] = ztitle
            elif self.DISPLAY_ZFNAME:
                self.zone_to_display[zone] = zfname
            elif self.DISPLAY_ZONE:
                self.zone_to_display[zone] = zone
            else:
                self.zone_to_display[zone] = zname

            zone_msg += (f"{CRLF_DOT}{zone}/{self.zone_to_display.get(zone)} "
                        f"(r{self.zone_radius_m[zone]}m)")

        log_msg = (f"Set up Zones (zone/{self.display_zone_format}) > {zone_msg}")
        self._save_event_halog_info("*", log_msg)

        return

#--------------------------------------------------------------------
    def _define_stationary_zone_fields(self, stationary_inzone_interval_str,
                    stationary_still_time_str):
        #create dynamic zone used by ios app when stationary
        self.stat_zone_inzone_interval = self._time_str_to_secs(stationary_inzone_interval_str)
        self.stat_zone_still_time      = self._time_str_to_secs(stationary_still_time_str)
        self.stat_zone_half_still_time = self.stat_zone_still_time / 2
        self.in_stationary_zone_flag   = {}
        self.stat_zone_devicename_icon = {}  #icon to be used for a devicename
        self.stat_zone_moved_total     = {}  #Total of small distances
        self.stat_zone_timer           = {}  #Time when distance set to 0
        self.stat_zone_update_location = {}  #zonename/attrs to be updated after track results
        self.stat_min_dist_from_zone_km  = round(self.zone_home_radius_km * 2.5, 2)
        self.stat_dist_move_limit      = round(self.zone_home_radius_km * 1.5, 2)
        self.stat_zone_radius_km       = round(self.zone_home_radius_km * 2, 2)
        self.stat_zone_radius_m        = self.zone_home_radius_m * 2
        if self.stat_zone_radius_km    > .1:  self.stat_zone_radius_km = .1
        if self.stat_zone_radius_m     > 100: self.stat_zone_radius_m  = 100

        #Offset the stat zone from the Home zone based on the stationary_zone_offset parameter
        self.stat_zone_base_long       = self.zone_home_long
        if instr(self.stationary_zone_offset, "("):
            szo = self.stationary_zone_offset.replace("(", "").replace(")", "")
            self.stat_zone_base_lat  =  float(szo.split(',')[0])
            self.stat_zone_base_long =  float(szo.split(',')[1])
        else:
            offset_lat  = float(self.stationary_zone_offset.split(',')[0]) * STATIONARY_ZONE_1KM_LAT
            offset_long = float(self.stationary_zone_offset.split(',')[1]) * STATIONARY_ZONE_1KM_LONG
            self.stat_zone_base_lat  = self.zone_home_lat  + offset_lat
            self.stat_zone_base_long = self.zone_home_long + offset_long

        dist = self._calc_distance_km(self.zone_home_lat, self.zone_home_long,
                    self.stat_zone_base_lat, self.stat_zone_base_long)

        log_msg = (f"Set Initial Stationary Zone Location > "
                   f"GPS-{format_gps(self.stat_zone_base_lat, self.stat_zone_base_long, 0)}, "
                   f"Radius-{self.stat_zone_radius_m}m, DistFromHome-{dist}km")
        self._log_debug_msg("*", log_msg)
        self._save_event("*", log_msg)

#--------------------------------------------------------------------
    def _initialize_debug_control(self, log_level):
        #string set using the update_icloud command to pass debug commands
        #into icloud3 to monitor operations or to set test variables
        #   interval - toggle display of interval calulation method in info fld
        #   debug - log 'debug' messages to the log file under the 'info' type
        #   debug_rawdata - log data read from records to the log file
        #   eventlog - Add debug items to ic3 event log
        #   debug+eventlog - Add debug items to HA log file and ic3 event log

        #Save log_level flags across restarts via Event Log > Actions
        if self.log_debug_flag_restart is not None or self.log_rawdata_flag_restart is not None:
            if self.log_debug_flag_restart is not None:
                self.log_debug_flag         = self.log_debug_flag_restart
                self.log_debug_flag_restart = None

            if self.log_rawdata_flag_restart is not None:
                self.log_rawdata_flag         = self.log_rawdata_flag_restart
                self.log_rawdata_flag_restart = None
        else:
            self.log_debug_flag   = instr(log_level, 'debug') or DEBUG_TRACE_CONTROL_FLAG
            self.log_rawdata_flag = instr(log_level, 'rawdata')

        self.log_intervalcalc_flag = DEBUG_TRACE_CONTROL_FLAG or instr(log_level, 'intervalcalc')
        self.log_eventlog_flag     = self.log_eventlog_flag or instr(log_level, 'eventlog')

        self.debug_counter = 0
        self.last_iosapp_msg = {} #can be used to compare changes in debug msgs
        self.last_device_monitor_msg = {}

#########################################################
#
#   INITIALIZE PYICLOUD DEVICE API
#   DEVICE SETUP SUPPORT FUNCTIONS FOR MODES FMF, FAMSHR, IOSAPP
#
#########################################################
    def _pyicloud_initialize_device_api(self):
        #See if pyicloud_ic3 is available
        if (PYICLOUD_IC3_IMPORT_SUCCESSFUL is False and self.CONF_TRK_METHOD_FMF_FAMSHR):
            event_msg = ("iCloud3 Error > An error was encountered setting up the `pyicloud_ic3.py` "
                f"module. Either the module was not found or there was an error loading it."
                f"The iCloud Location Service is disabled and the "
                f"iOS App tracking_method will be used.")
            self._save_event_halog_error("*", event_msg)

            self._setup_iosapp_tracking_method()

        else:
            #Set up pyicloud cookies directory & file names
            try:
                self.icloud_cookies_dir  = self.hass.config.path(STORAGE_DIR, STORAGE_KEY_ICLOUD)
                self.icloud_cookies_file = "".join([c for c in self.username if match(r"\w", c)])
                if not os.path.exists(self.icloud_cookies_dir):
                    os.makedirs(self.icloud_cookies_dir)

            except Exception as err:
                _LOGGER.exception(err)

        if self.TRK_METHOD_IOSAPP:
            self.api = None

        elif self.CONF_TRK_METHOD_FMF_FAMSHR:
            event_msg = ("iCloud Web Services interface (pyicloud_ic3.py) > Verified")
            self._save_event_halog_info("*", event_msg)

            self._pyicloud_authenticate_account(initial_setup=True)

#--------------------------------------------------------------------
    def _pyicloud_authenticate_account(self, devicename="", initial_setup=False):
        '''
        Authenticate the iCloud Acount via pyicloud
        If successful - self.api to the api of the pyicloudservice for the username
        If not        - set self.api = None
        '''
        try:
            auth_start_time = time.time()
            if self.api:
                self.api.authenticate(refresh_session=True, service='find')

            else:
                self.api = PyiCloudService(self.username, self.password,
                                        cookie_directory=self.icloud_cookies_dir,
                                        session_directory=(f"{self.icloud_cookies_dir}/session"),
                                        verify=True)

            self.time_pyicloud_calls += (time.time() - auth_start_time)

            if self.authentication_error_retry_secs != HIGH_INTEGER:
                self.authentication_error_cnt = 0
                self.authentication_error_retry_secs = HIGH_INTEGER
                self._setup_tracking_method(self.tracking_method_config)

            if self.api:
                self._is_authentication_2fa_code_needed(initial_setup=True)

            self._check_authentication_message(devicename)

        except (PyiCloudFailedLoginException, PyiCloudNoDevicesException,
                PyiCloudAPIResponseException) as err:

            self._authentication_error()
            return False
        except (PyiCloud2SARequiredException) as err:
            self._is_authentication_2fa_code_needed()
            return False
        except Exception as err:
            _LOGGER.exception(err)
            return False

        return True

#--------------------------------------------------------------------
    def _check_authentication_message(self, devicename):
        '''
        If an authentication was done, update the count & time and display
        an Event Log message
        '''
        if not self.api.authentication_method:
            return

        self.count_pyicloud_authentications += 1
        last_authenticated_time = self.authenticated_time
        self.authenticated_time = time.time()

        event_msg = (f"iCloud Account Authenticated "
                    f"(#{self.count_pyicloud_authentications}) > LastAuth-")
        if last_authenticated_time == 0:
            event_msg += "Never (Initializing)"
        else:
            event_msg += (f"{self._secs_to_time(last_authenticated_time)} "
                        f" ({self._format_age(self.authenticated_time - last_authenticated_time)})")
        event_msg += (f", Method-{self.api.authentication_method}")
        if devicename: event_msg += (f", RequestedBy-{devicename}")
        self._save_event_halog_info("*", event_msg)

#--------------------------------------------------------------------
    def _is_authentication_2fa_code_needed(self, initial_setup=False):
        '''
        Make sure iCloud is still available and doesn't need to be authenticationd
        in 15-second polling loop

        Returns True  if Authentication is needed.
        Returns False if Authentication succeeded
        '''
        if self.CONF_TRK_METHOD_FMF_FAMSHR is False:
            return
        elif initial_setup:
            pass
        elif self.start_icloud3_inprocess_flag:
            return False

        fct_name = "icloud_authenticate_account"

        from .pyicloud_ic3 import PyiCloudService
        from .pyicloud_ic3 import PyiCloudException

        try:
            if initial_setup is False:
                if self.api is None:
                    event_msg = ("iCloud/FmF API Error, No device API information "
                                    "for devices. Resetting iCloud")
                    self._save_event_halog_error(event_msg)
                    self._start_icloud3()

                elif self.start_icloud3_request_flag:    #via service call
                    event_msg = ("iCloud Restarting, Reset command issued")
                    self._save_event_halog_error(event_msg)
                    self._start_icloud3()

                if self.api is None:
                    event_msg = ("iCloud Authentication Required, will retry")
                    self._save_event_halog_error(event_msg)
                    return True #Authentication needed

            try:
                if self.api is None:
                    return True

                #See if 2fa Verification needed
                if self.api.requires_2fa is False:
                    return False

                alert_msg = (f"{EVLOG_ALERT}iCloud3 Alert > 2fa Verification Required")
                self._save_event("*", alert_msg)
                if self.verification_code is None:
                    self._icloud_2fa1_show_verification_code_entry_form()
                    return True  #Verification needed

            except PyiCloudException as error:
                event_msg = (f"iCloud3 Error > Setting up 2fa > {error}")
                self._save_event_halog_error(event_msg)
                return True         #Verification needed, Verification Failed

            self.authenticated_time = time.time()
            self.trusted_device    = None
            self.verification_code = None

            return False         #Verification succeeded

        except Exception as err:
            _LOGGER.exception(err)
            #x = self._internal_error_msg(fct_name, err, 'AuthiCloud')
            return True

#--------------------------------------
    def _authentication_error(self):
            #Set up for retry in X minutes
            self.authentication_error_cnt += 1
            if self.authentication_error_cnt >= 8:
                retry_secs = 3600           #1 hours
            elif self.authentication_error_cnt >= 4:
                retry_secs = 1800           #30 minutes
            else:
                retry_secs = 900            #15 minutes

            self.authentication_error_retry_secs = time.time() + retry_secs
            auth_retry_time = self._secs_to_time(self.authentication_error_retry_secs)

            event_msg = (f"iCloud3 Error > An error occurred authenticating {self.username}."
                f"CRLFThe iCloud Web Services may be down or the Username/Password"
                f" may be invalid. The iCloud Location Services tracking method "
                f"is disabled and the iOS App tracking method will be used. "
                f"CRLFThe authentication will be retried in "
                f"{self._secs_to_time_str(retry_secs)} at {auth_retry_time}.")
            self._save_event_halog_error("*", event_msg)

            self._setup_iosapp_tracking_method()

#--------------------------------------------------------------------
    def _pyicloud_reset_session(self):
        '''
        Reset the urrent session and authenticate to restart pyicloud_ic3
        and enter a new verification code
        '''
        if self.api == None:
            return

        try:
            self._save_event("*", f"^^^iCloud interface initialization started")
            cookies_file     = (f"{self.icloud_cookies_dir}/{self.icloud_cookies_file}")
            session_file     = (f"{self.icloud_cookies_dir}/{self.icloud_cookies_file}")

            self._cookies_file_rename("", "cookies")
            self._cookies_file_rename("/session", "session")

            session_dir_suffix = ''
            self._save_event("*", f"iCloud initializing interface")
            self.api.__init__(self.username, self.password,
                            cookie_directory=self.icloud_cookies_dir,
                            session_directory=(f"{self.icloud_cookies_dir}/session{session_dir_suffix}"),
                            verify=True)

            self.api = None
            self.verification_code = None

            self._pyicloud_authenticate_account(initial_setup=True)

            self._save_event("*", f"^^^iCloud interface initialization completed")

            self._update_sensor_ic3_event_log(f"{self.tracked_devices[0]}")

        except Exception as err:
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _cookies_file_rename(self, dir_sub_path, file_desc, save_extn='sv'):
        try:
            file_msg = ""
            file_name = (f"{self.icloud_cookies_dir}{dir_sub_path}/{self.icloud_cookies_file}")
            file_name_sv = (f"{file_name}.{save_extn}")
            if os.path.isfile(file_name_sv):
                os.remove(file_name_sv)
                file_msg += (f"{CRLF_DOT}Deleted backup {file_desc} file ({self.icloud_cookies_file}.{save_extn})")
            if os.path.isfile(file_name):
                os.rename(file_name, file_name_sv)
                file_msg += (f"{CRLF_DOT}Renamed current {file_desc} file ({self.icloud_cookies_file}"
                             f" -- > {self.icloud_cookies_file}.{save_extn})")
            if file_msg != "":
                event_msg = (f"Reset iCloud {file_desc} file > CRLF•{file_name}{file_msg}")
                self._save_event("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _check_ic3_update_2sa_to_2fa(self):
        '''
        When upgrading from v2.2.1 (2sa) to v2.2.2 (2fa), the cookies file must be deleted
        so the trust cookie for 2sa is reset. If this is not done, the 2fa code is not requested
        and it constantly asks for a notification code.

        This routine checks to see if '\session\cookiesfilename(icloudacct@email.com)' exists. If not, it is an upgrade
        and the cookie file is deleted.
            - rename cookiesfile to cookiesfile.2sa
            - rename sessionfile to sessionfile.2sa
        '''
        try:
            self.icloud_cookies_dir  = self.hass.config.path(STORAGE_DIR, STORAGE_KEY_ICLOUD)
            self.icloud_cookies_file = "".join([c for c in self.username if match(r"\w", c)])
            cookies_file     = (f"{self.icloud_cookies_dir}/{self.icloud_cookies_file}")
            session_file     = (f"{self.icloud_cookies_dir}/{self.icloud_cookies_file}")

            if os.path.isfile(session_file):
                return
            elif os.path.isfile(cookies_file):
                event_msg = ("iCloud3 Upgrade Notification > Deleted the iCloud cookies file "
                             "with 2sa data to prepare for Apple native 2fa support")

                file_msg = ""
                cookies_file_2sa = (f"{self.icloud_cookies_dir}/{self.icloud_cookies_file}.2sa")
                session_2sa_file = (f"{self.icloud_cookies_dir}/session-2sa/{self.icloud_cookies_file}")

                if os.path.isfile(cookies_file_2sa):
                    os.remove(cookies_file)
                    file_msg += (f"{CRLF_DOT}Deleted cookies file ({cookies_file})")
                elif os.path.isfile(cookies_file):
                    os.rename(cookies_file, cookies_file_2sa)
                    file_msg += (f"{CRLF_DOT}Renamed current cookies file ({cookies_file}"
                                f" --> {cookies_file_2sa})")
                self._save_event("*", event_msg + file_msg)

        except Exception as err:
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _setup_tracked_devices_for_fmf(self):
        '''
        Cycle thru the Find My Friends contact data. Extract the name, id &
        email address. Scan fmf_email config parameter to tie the devicename_device_id in
        the location record to the devicename.

                    email --> devicename <--devicename_device_id
        '''
        api_friends = None
        try:
            api_friends = self.api.friends
        except:
            pass

        if api_friends == None:
            event_msg = "FindMy App Friends (People) that can be tracked > No entries found"
            self._save_event("*", event_msg)
            return

        try:
            self._log_rawdata("iCloud FmF Raw Data - (api_friends.data)", api_friends.data)

            devicename_friend_emails = {}
            friend_valid_emails_msg = ''

            #Extract the email & ID from the friends being followed by the main user
            try:
                for friend in api_friends.following:
                    friend_emails = friend.get('invitationAcceptedHandles')
                    friend_id     = friend.get('id')
                    friend_email_id, friend_valid_emails_msg = \
                            self._extract_fmf_email_id(friend_emails, friend_id, friend_valid_emails_msg)
                    devicename_friend_emails.update(friend_email_id)

                    self._log_rawdata(f"iCloud FmF Raw Data, following -- {friend_emails}", friend)
            except Exception as err:
                pass

            #Extract the email & ID from the friends following the main user
            try:
                for friend in api_friends.followers:
                    friend_emails = friend.get('invitationFromHandles')
                    friend_id     = friend.get('id')
                    friend_email_id, friend_valid_emails_msg = \
                            self._extract_fmf_email_id(friend_emails, friend_id, friend_valid_emails_msg)
                    devicename_friend_emails.update(friend_email_id)

                    self._log_rawdata(f"iCloud FmF Raw Data, followers -- {friend_emails}", friend)
            except Exception as err:
                pass

            #Extract the email & ID from the friends contacts
            try:
                for friend in api_friends.contact_details:
                    friend_emails = friend.get('emails')
                    friend_id     = friend.get('id')
                    friend_email_id, friend_valid_emails_msg = \
                            self._extract_fmf_email_id(friend_emails, friend_id, friend_valid_emails_msg)
                    devicename_friend_emails.update(friend_email_id)

                    self._log_rawdata(f"iCloud FmF Raw Data, contactDetails -- {friend_emails}", friend)
            except Exception as err:
                pass

            #Normally, the username's device can not be shared with itself so we must check to see
            #if the username's device was verified by FmF. If not, get the 'me' DeviceId
            #from the FamShr data and the 'me' device will be located using FamShr
            friend_valid_emails_msg = self._get_me_device_id(api_friends, friend_valid_emails_msg)

            log_msg = (f"Friends in the FindMy app data that can be located > {friend_valid_emails_msg}")
            self._save_event_halog_info("*", log_msg)

            for devicename in self.devicename_verified:
                #The devicename email was not in the fmf following/followed list
                if self.devicename_verified.get(devicename) is False:
                    parm_email = self.devicename_email.get(devicename)
                    if parm_email:
                        devicename_friend_emails[devicename] = parm_email
                        log_msg = (f"iCloud3 Alert for {self._format_fname_devicename(devicename)} > "
                                f"The email address `{parm_email}` is not in the FindMy > People list "
                                f"or being followed by another person and may not be correct. "
                                f"The Family Sharing list will be checked next.")
                        self._save_event_halog_error("*", log_msg)

            self.devicename_email = {}
            self.devicename_email.update(devicename_friend_emails)

        except Exception as err:
            self._setup_iosapp_tracking_method()
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _extract_fmf_email_id(self, friend_emails, friend_id, friend_valid_emails_msg):
    #cycle thru the emails on the tracked_devices config parameter

        devicename_friend_emails = {}

        #No devices to track error, display emails anyway
        if self.devicename_email == {}:
            for friend_email in friend_emails:
                if (instr(friend_email, '@')
                        and instr(friend_valid_emails_msg, friend_email) is False):
                     friend_valid_emails_msg += (f"{CRLF_DOT}{friend_email}")
            return devicename_friend_emails, friend_valid_emails_msg

        for parm_email in self.devicename_email:
            if instr(parm_email, '@') is False:
                continue

            #cycle thru the contacts emails
            matched_friend = False
            devicename = self.devicename_email.get(parm_email, "")

            for friend_email in friend_emails:
                if instr(friend_email, '@') is False:
                    continue
                elif devicename in self.devicename_evlog_tracked_msg:
                    continue

                if instr(friend_valid_emails_msg, friend_email) is False:
                    friend_valid_emails_msg += (f"{CRLF_DOT}{friend_email}")

                if devicename not in self.devicename_evlog_not_tracked_msg:
                    self.devicename_evlog_not_tracked_msg[devicename] = (f"{friend_email}")

                if (self.devicename_verified.get(devicename) is False
                        and friend_email.startswith(parm_email)):
                    #update temp list with full email from contact recd
                    matched_friend = True
                    devicename_friend_emails[friend_email]     = devicename
                    devicename_friend_emails[devicename]       = friend_email

                    self.devicename_verified[devicename]        = True
                    self.devicename_tracking_method[devicename] = FMF
                    self.devicename_by_device_id[friend_id]     = devicename
                    self.devicename_device_id[devicename]       = friend_id
                    self.devicename_device_id_fmf[devicename]   = friend_id
                    self.devicename_evlog_tracked_msg[devicename] = (f"{friend_email} > {self._format_fname_devicename(devicename)}")
                    self.devicename_evlog_not_tracked_msg.pop(devicename, None)

                    matched_text = (f"✓ {friend_email} > {self._format_fname_devicename(devicename)}")
                    friend_valid_emails_msg = \
                                friend_valid_emails_msg.replace(f"• {friend_email}", f"{matched_text}")
                    log_msg = (f"Matched FmF Contact > "
                                f"{self._format_fname_devicename(devicename)} "
                                f"with {friend_email}, Id: {friend_id}")
                    self._log_info_msg(log_msg)
                    break

        return devicename_friend_emails, friend_valid_emails_msg

#--------------------------------------------------------------------
    def _get_me_device_id(self, api_friends, friend_valid_emails_msg):
        '''
        Check to see if the devicename email is the same as the username and is verified by being
        in the followed or is being followed list. If it was not verified, get this devicename's
        device id from fmf MyPrefs, then follow the trail to get the device_id from the famshr
        devices. That device id will be used to get the 'me device' location. If it is verified,
        fmf tracking is already set up for it.
        '''
        for devicename in self.devicename_verified:
            if (self.devicename_email.get(devicename) == self.username
                    and self.devicename_verified.get(devicename) is False):
                fmf_data = api_friends.data
                my_info = fmf_data['myInfo']
                if self.username in my_info['emails']:
                    for fmf_device in fmf_data['devices']:
                        if fmf_device['id'] == my_info['meDeviceId']:
                            me_device_id = fmf_device['idsDeviceId']
                            famshr_devices_data = self.api.devices.response["content"]
                            for famshr_device in famshr_devices_data:
                                if famshr_device['deviceDiscoveryId'] == me_device_id:
                                    device_id = famshr_device['id']

                                    friend_valid_emails_msg += (f"{CRLF_CHK}{self.username} > "
                                                f"{self._format_fname_devicename(devicename)} (Set as MyDevice)")

                                    #If going to track device by famshr, erase fmf device id if needed
                                    if devicename in self.devicename_device_id:
                                        fmf_device_id = self.devicename_device_id.get(devicename)
                                        self.devicename_by_device_id.pop(fmf_device_id)

                                    self.devicename_verified[devicename]        = True
                                    self.devicename_tracking_method[devicename] = FAMSHR
                                    self.devicename_by_device_id[device_id]     = devicename
                                    self.devicename_device_id[devicename]       = device_id
                                    self.devicename_device_id_famshr[devicename]= device_id
                                    self.devicename_evlog_tracked_msg[devicename]  = (f"{self.username} > "
                                                f"{self._format_fname_devicename(devicename)}")
                                    break

        return friend_valid_emails_msg

#--------------------------------------------------------------------
    def _setup_tracked_devices_for_famshr(self):
        '''
        Get the device info from iCloud Web Svcs via pyicloud. Then cycle through
        the iCloud devices and for each device, see if it is in the list of devicenames
        to be tracked. If in the list, set it's verified flag to True.

        Returns the devices being tracked and the devices in the iCloud list that are
        not being tracked.
        '''

        devices_data = None
        try:
            devices_data = self.api.devices.response["content"]
        except:
            pass

        if devices_data == None:
            event_msg = "Family Sharing List devices that can be tracked > No entries found"
            self._save_event("*", event_msg)
            return

        try:
            event_msg = "Family Sharing List devices that can be tracked >"

            for device_data in devices_data:
                device_fname = device_data[ATTR_NAME].replace(u'\xa0', u' ')
                device_id    = device_data['id']
                devicename   = slugify(device_fname)
                device_type  = device_data[ATTR_ICLOUD_DEVICE_CLASS]
                self._log_rawdata((f"FamShr iCloud Data, device_data -- {devicename}"), device_data)

                if devicename in self.devicename_verified:
                    if self.devicename_verified.get(devicename) is False:
                        self.devicename_verified[devicename]        = True
                        self.devicename_tracking_method[devicename] = FAMSHR
                        self.devicename_by_device_id[device_id]     = devicename
                        self.devicename_device_id[devicename]       = device_id

                    self.devicename_device_id_famshr[devicename]= device_id

                    event_msg += (f"{CRLF_CHK}{devicename} > {device_fname}, {device_type}")
                    self.devicename_evlog_tracked_msg[devicename] = (f"{devicename} > {device_fname}, {device_type}")
                else:
                    event_msg += (f"{CRLF_DOT}{devicename} > {device_fname}, {device_type}")
                    self.devicename_evlog_not_tracked_msg[devicename] = (f"{devicename} > {device_fname}, {device_type}")

            self._save_event("*", event_msg)
            return

        except Exception as err:
            _LOGGER.exception(err)

            event_msg = (f"iCloud3 Error for {self.username} > "
                "Error Authenticating account or no data was returned from "
                "iCloud Web Services. Web Services may be down or the "
                "Username/Password may be invalid.")
            self._save_event_halog_error("*", event_msg)

        return

#--------------------------------------------------------------------
    def _tune_tracked_devices_fmf_famshr(self):
        '''
        The goal is to get either all fmf or all famshr to minimize the number of
        calls to iCloud Web Services by pyicloud_ic3. Look at the fmf and famshr
        devices to see if:
        1. All devices are fmf or all devices are famshr.
        2. There are famshr devices and all the fmf devices are in the famshr list.
        3. Most devices are famshr but there is a fmf device that is not in the
        famshr list.
        If:
        1. Then there will be no famshr locates (acceptible).
        2. Change the all fmf devices to  famshr and update the device id for the device.
        3. Leave alone since it will need calls to both.
        '''

        fmf_cnt    = 0
        famshr_cnt = 0
        iosapp_cnt = 0
        device_cnt = 0
        for devicename in self.devicename_tracking_method:
            device_cnt += 1
            if self.devicename_tracking_method.get(devicename) == FMF:
                fmf_cnt += 1
            elif self.devicename_tracking_method.get(devicename) == FAMSHR:
                famshr_cnt += 1
            else:
                iosapp_cnt += 1

        if fmf_cnt == 0 or famshr_cnt == 0:
            return

        elif fmf_cnt > 0 and famshr_cnt > 0:
            #Go through devices and move from fmf to famshr if famshr is available
            for devicename in self.devicename_tracking_method:
                if (self.devicename_tracking_method.get(devicename) == FMF
                        and devicename in self.devicename_device_id_famshr):
                    device_id = self.devicename_device_id_famshr.get(devicename)
                    self.devicename_tracking_method[devicename] = FAMSHR
                    self.devicename_by_device_id[device_id] = devicename
                    self.devicename_device_id[devicename]   = device_id

                    fmf_cnt    -= 1
                    famshr_cnt += 1

#--------------------------------------------------------------------
    def _setup_tracked_devices_for_iosapp(self):
        '''
        The devices to be tracked are in the track_devices or the
        include_devices config parameters.
        '''
        for devicename in self.devicename_verified:
            self.devicename_verified[devicename] = True
            if self.TRK_METHOD_FMF_FAMSHR is False:
                self.devicename_tracking_method[devicename] = IOSAPP

        event_msg = (f"Verified Device for iOS App Tracking > "
                     f"{self._format_list(self.devicename_verified)}")
        self._save_event_halog_info("*", event_msg)
        return

#--------------------------------------------------------------------
    def _set_track_devices_fields_from_config_parms(self):
        '''
        Set up the devices to be tracked and it's associated information
        for the configuration line entry. This will fill in the following
        fields based on the extracted devicename:
            device_type
            friendly_name
            fmf email address
            sensor.picture name
            device tracking flags
            tracked_devices list
        These fields may be overridden by the routines associated with the
        operating mode (fmf, icloud, iosapp)
        '''

        # Extract device fields from ha config file 'devices:' parameter
        self.config_track_devices_fields.extend(
                self._get_devices_list_from_config_devices_parm(\
                        self.config_devices_schema, 'HA config'))

        # Get device fields from iCloud3 config_ic3 file
        self.config_track_devices_fields.extend(self.config_ic3_track_devices_fields)

        # Extract device fields from ha config file 'track_devices:' parameter
        self.config_track_devices_fields.extend(\
                self._get_devices_list_from_config_track_devices_parm(\
                        self.config_track_devices_parm, 'HA config'))

        try:
            for device_fields in self.config_track_devices_fields:
                if CONF_DEVICENAME not in device_fields:
                   continue

                devicename = device_fields.get(CONF_DEVICENAME)
                if devicename in self.devicename_verified:
                    event_msg = (f"Duplicate Entry Discarded > {devicename} > The parameters "
                                 f"for this device have already been processed. Parameters "
                                 f"in the {device_fields.get(CONF_CONFIG)} file will not be used.")
                    self._save_event("*", event_msg)
                    continue

                warning_msg = ""


                if (self.iosapp_monitor_dev_trk_flag.get(devicename)
                        and devicename == device_fields.get(CONF_IOSAPP_ENTITY)):
                    event_msg = (f"iCloud3 Error > iCloud3 is not tracking {devicename}. "
                        f"The iCloud3 tracked_device is already assigned to "
                        f"the iOSApp and duplicate names are not allowed for HA "
                        f"Integration entities. You must change the iOS App "
                        f"entity name on the HA `Sidebar > Configuration > Integrations` "
                        f"screen. Then do the following: "
                        f"CRLF{'-'*25}"
                        f"CRLF 1. Select the Mobile_App entry for `{devicename}`."
                        f"CRLF 2. Scroll to the `device_tracker.{devicename}` statement."
                        f"CRLF 3. Select it."
                        f"CRLF 4. Click the Settings icon."
                        f"CRLF 5. Add or change the suffix of the "
                        f"`device_tracker.{devicename}` Entity ID to another value "
                        f"(e.g., _2, _app, etc)."
                        f"CRLF 6. Restart HA.")
                    self._save_event_halog_error("*", event_msg)
                    continue

                self.devicename_verified[devicename] = False
                self.device_type[devicename] = device_fields.get(CONF_DEVICE_TYPE, UNKNOWN)
                device_type                  = device_fields.get(CONF_DEVICE_TYPE, UNKNOWN).lower()
                self.fname[devicename]       = device_fields.get(CONF_NAME, devicename)

                email = device_fields.get(CONF_EMAIL, '')
                if email and email in self.devicename_email:
                    wrning_msg = (f"The email address {email} is also assigned to {self.devicename_email.get(email)}")
                    email = ""
                picture = device_fields.get(CONF_PICTURE, '')

                #Make a list of tracked devices from the parameter
                track_from_zones = device_fields.get(CONF_TRACK_FROM_ZONE, '').replace(',', ' ').split()
                track_from_zones.append(HOME)

                iosapp_monitor_flag = device_fields.get(CONF_IOSAPP_INSTALLED, True)
                iosapp_entity       = ''
                iosapp_suffix       = ''
                iosapp_info_event_msg = ''
                iosapp_inzone_interval_key = ''

                if iosapp_monitor_flag is False:
                    iosapp_inzone_interval_key = CONF_NO_IOSAPP
                    iosapp_info_event_msg = "iOSApp-NotUsed"
                elif CONF_IOSAPP_ENTITY in device_fields:
                    iosapp_entity         = device_fields.get(CONF_IOSAPP_ENTITY)
                    iosapp_info_event_msg = (f"iOSAppEntity-{device_fields.get(CONF_IOSAPP_ENTITY)}")
                elif CONF_IOSAPP_SUFFIX in device_fields:
                    iosapp_entity         = (f"{devicename}{device_fields.get(CONF_IOSAPP_SUFFIX)}")
                    iosapp_suffix         = device_fields.get(CONF_IOSAPP_SUFFIX)
                    iosapp_info_event_msg = (f"iOSAppSuffix-{device_fields.get(CONF_IOSAPP_SUFFIX)}")

                self.devicename_email[email]                 = devicename
                self.devicename_email[devicename]            = email
                self.badge_picture[devicename]               = picture if instr(picture, '/') else (f"/local/{picture}")
                self.iosapp_monitor_dev_trk_flag[devicename] = iosapp_monitor_flag
                self.devicename_iosapp_entity[devicename]    = iosapp_entity
                self.devicename_iosapp_suffix[devicename]    = iosapp_suffix
                self.devicename_verified[devicename]         = False
                self.devicename_tracking_method[devicename]  = None
                self.track_from_zones[devicename]            = track_from_zones

                #Set interval-specified for device, then use device type, then use default inzone_interval parm
                self.inzone_interval_secs[devicename]        = \
                        device_fields.get(CONF_INZONE_INTERVAL,
                            self.config_inzone_interval_secs.get(iosapp_inzone_interval_key,
                                self.config_inzone_interval_secs.get(device_type,
                                    self.config_inzone_interval_secs.get(CONF_INZONE_INTERVAL,
                                        self.inzone_interval_secs))))

                event_msg =      (f"Decoding ... {device_fields.get(CONF_SOURCE)} >CRLF") if CONF_SOURCE in device_fields else ""
                event_msg +=     (f"✓ {devicename} > Name-{device_fields.get(CONF_NAME)}, ")
                if picture: event_msg += (f"Picture-{device_fields.get(CONF_PICTURE)}, ")
                if email:   event_msg += (f"email-{email}, ")
                event_msg += (f"Type-{self.device_type.get(devicename)}, "
                              f"inZoneInterval-{self._secs_to_time_str(self.inzone_interval_secs.get(devicename))}")

                if track_from_zones != [HOME]:
                    zones_str = ", ".join(track_from_zones)
                    event_msg += (f", TrackFromZone-{zones_str}, ")
                if iosapp_info_event_msg: event_msg += (f", {iosapp_info_event_msg}, ")
                if warning_msg:           event_msg += (f", WARNING-{warning_msg}")

                self._save_event_halog_info("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)

        return

#--------------------------------------------------------------------
    def _decode_track_devices_parameter(self, track_devices_device):
        '''
        This will decode the device's parameter in the configuration file for
        the include_devices, sensor_name_prefix, track_devices items in the
        format of:
           - devicename > email, picture, iosapp, sensornameprefix

        If the item cotains '@', it is an email item,
        If the item contains .png  or .jpg, it is a picture item.
        Otherwise, it is the prefix name item for sensors

        The device_type and friendly names are also returned in the
        following order as a list item:
            devicename, device_type, friendlyname, email, picture, sensor name

        '''

        try:
            device_fields       = {}
            picture             = ""
            email               = ""
            name                = ""
            device_type         = ""
            track_from_zones    = []
            dev_trk_entity_id   = ""
            iosapp_suffix       = ""
            dev_trk_device_id   = ""
            iosapp_monitor_flag = True

            devicename_parameters = track_devices_device.split('>')
            devicename  = slugify(devicename_parameters[0])

            #If tracking method is IOSAPP or FAMSHR, try to make a friendly
            #name from the devicename. If FMF, it will be retrieved from the
            #contacts data. If it is specified on the config parms, it will be
            #overridden with the specified name later.

            name, device_type = self._extract_name_device_type(devicename)
            device_fields[CONF_DEVICENAME]  = devicename
            device_fields[CONF_NAME]        = name
            device_fields[CONF_DEVICE_TYPE] = device_type
            device_fields[CONF_SOURCE]      = track_devices_device

            if instr(track_devices_device, '>'):
                parameter_items = devicename_parameters[1].strip().split(',')

                for parameter_item in parameter_items:
                    pvalue = parameter_item.strip().replace(' ', '_').lower()

                    if pvalue == '':
                        continue
                    elif instr(pvalue, '@'):
                        device_fields[CONF_EMAIL] = pvalue

                    elif (instr(pvalue, 'png')
                            or instr(pvalue, 'jpg')
                            or instr(pvalue, 'jpeg')):
                        device_fields[CONF_PICTURE] = pvalue

                    elif pvalue in [CONF_NOIOSAPP, CONF_NO_IOSAPP]:
                        device_fields[CONF_IOSAPP_INSTALLED] = False

                    elif pvalue.startswith("_"):
                        device_fields[CONF_IOSAPP_SUFFIX] = pvalue
                        device_fields.pop(CONF_IOSAPP_ENTITY, None)

                    elif instr(pvalue, "_"):
                        device_fields[CONF_IOSAPP_ENTITY] = pvalue
                        device_fields.pop(CONF_IOSAPP_SUFFIX, None)

                    elif pvalue == self.zones:
                        track_from_zones.append(pvalue)

                    else:
                        device_fields[CONF_NAME] = parameter_item.strip()

            if track_from_zones != []:
                device_fields[CONF_TRACK_FROM_ZONE] = track_from_zones

        except Exception as err:
            _LOGGER.exception(err)

        return device_fields

    #--------------------------------------------------------------------
    def _setup_monitored_iosapp_entities(self, devicename, iosapp_entities, notify_devicenames, dev_trk_iosapp_suffix):

        #Cycle through the mobile_app 'core.entity_registry' items and see
        #if this 'device_tracker.devicename' exists. If so, it is using
        #the iosapp v2 component. Return the devicename with the device suffix (_#)
        #and the sensor.xxxx_last_update_trigger entity for that device.


        if (self.iosapp_monitor_dev_trk_flag.get(devicename) is False):
            self.device_tracker_entity_iosapp[devicename] = (f"device_tracker.{devicename}")
            self.notify_iosapp_entity[devicename]  = (f"ios_{devicename}")
            return ("", "", "", "")

        dev_trk_iosapp_suffix       = "" if dev_trk_iosapp_suffix == None else dev_trk_iosapp_suffix
        dev_trk_entity_id           = devicename + dev_trk_iosapp_suffix if dev_trk_iosapp_suffix != "" else ""
        sensor_last_trigger_entity  = ""
        sensor_battery_level_entity = ""
        dev_trk_list                = ""
        dev_trk_device_id           = ""

        #Cycle through iosapp_entities in
        #.storage/core.entity_registry (mobile_app pltform) and get the
        #names of the iosapp device_tracker and sensor.last_update_trigger
        #names for this devicename. If iosapp_id suffix or device tracker entity name
        # is specified, look for the device_tracker with that number.
        dev_trk_entity_cnt = 0

        log_msg = (f"Scanning {self.entity_registry_file} Entity Registry for "
            f"iOS App device_tracker {devicename}")
        if dev_trk_entity_id != "":
            log_msg += (f", Specified Entity-({dev_trk_entity_id})")
        self._log_info_msg(log_msg)

        #Get the entity for the devicename entity specified on the track_devices parameter
        if dev_trk_entity_id != "":
            device_tracker_entities = [x for x in iosapp_entities \
                    if (x['entity_id'] == f"device_tracker.{dev_trk_entity_id}")]
            dev_trk_entity_cnt = len(device_tracker_entities)

        #If the entity specified was not found, get all entities for the device
        if dev_trk_entity_cnt == 0:
            device_tracker_entities = [x for x in iosapp_entities \
                    if (x['entity_id'].startswith("device_tracker.") and instr(x['entity_id'], devicename))]
            dev_trk_entity_cnt = len(device_tracker_entities)

        #Extract the device_id for each entity found. If more than 1 was found, display an
        #error message about duplicate entities and select the last one.
        for entity in device_tracker_entities:
            entity_id             = entity['entity_id']
            dev_trk_entity_id     = entity_id.replace("device_tracker.", "")
            dev_trk_iosapp_suffix = dev_trk_entity_id.replace(devicename, "")
            dev_trk_device_id     = entity['device_id']
            dev_trk_list         += (f"{CRLF_DOT}{dev_trk_entity_id} ({dev_trk_iosapp_suffix})")

        log_msg = (f"SCAN ENTITY REG, device_trackers found-[{dev_trk_list}]")
        self._log_debug_msg(devicename, log_msg)

        #Will monitor if found an iosapp device_tracker entity
        self.iosapp_monitor_dev_trk_flag[devicename] = (dev_trk_entity_cnt > 0)

        if dev_trk_entity_cnt > 1:
            self.info_notification = (f"iOS App Device Tracker not specified for "
                            f"{self._format_fname_devicename(devicename)}. See Event Log for more information.")
            dev_trk_list += " ← ← Will be monitored"
            event_msg = (f"iCloud3 Setup Error > There are {dev_trk_entity_cnt} iOS App "
                        f"device_tracker entities for {devicename}. iCloud3 can only monitor one."
                        f"CRLF{'-'*25}CRLFDo one of the following:"
                        f"CRLF●  Delete the incorrect device_tracker from the Entity Registry, or"
                        f"CRLF●  Add the full entity name or the suffix of the device_tracker entity that "
                        f"should be monitored to the `devices/device_name: {devicename}` parameter, or"
                        f"CRLF●  Change the device_tracker entity's name of the one that should not be monitored "
                        f"so it does not start with `{devicename}`."
                        f"CRLF{'-'*25}CRLFDevice_tracker entities (suffixes) found:"
                        f"{dev_trk_list}")
            self._save_event_halog_error("*", event_msg)

        #Get the sensor.last_update_trigger for deviceID
        if dev_trk_device_id:
            sensor_last_trigger_entity = \
                self._get_entity_registry_item(devicename, iosapp_entities, dev_trk_device_id, '_last_update_trigger')
            sensor_battery_level_entity = ''

        if self.iosapp_monitor_dev_trk_flag.get(devicename) is False:
            event_msg = (f"iCloud3 Setup Error > {devicename} > "
                         f"The iOS App device_tracker entity was not found in the "
                         f"Entity Registry for this device.")
            self._save_event_halog_error("*", event_msg)
            self.info_notification = ICLOUD3_ERROR_MSG

            dev_trk_entity_id           = ''        #devicename
            dev_trk_iosapp_suffix       = ''
            sensor_last_trigger_entity  = ''
            sensor_battery_level_entity = ''

        self.devicename_iosapp_entity[devicename]    = dev_trk_entity_id
        self.devicename_iosapp_suffix[devicename]    = dev_trk_iosapp_suffix
        self.iosapp_last_trigger_entity[devicename]  = sensor_last_trigger_entity
        self.iosapp_battery_level_entity[devicename] = sensor_battery_level_entity

        if dev_trk_entity_id:
            #Extract all notify entitity id's with this devicename in them from hass notify services notify list
            notify_devicename_list = []
            db=(f"7379 {notify_devicenames=}")
            self._save_event_halog_info("*", db)
            for notify_devicename in notify_devicenames:
                if instr(notify_devicename, devicename):
                    notify_devicename_list.append(notify_devicename.replace("mobile_app_", ""))
                db=(f"7382 {notify_devicename=} {notify_devicename_list=}")
                self._save_event_halog_info("*", db)

            self.notify_iosapp_entity[devicename] = notify_devicename_list
            self.device_tracker_entity_iosapp[devicename] = (f"device_tracker.{dev_trk_entity_id}")
        else:
            self.notify_iosapp_entity[devicename] = ''
            self.device_tracker_entity_iosapp[devicename] = ''
            self.iosapp_monitor_dev_trk_flag[devicename] is False

        db=(f"7390 {self.device_tracker_entity_iosapp=}")
        self._save_event_halog_info("*", db)
        db=(f"7390 {self.notify_iosapp_entity=}")
        self._save_event_halog_info("*", db)
        return

#--------------------------------------------------------------------
    def _get_entity_registry_entities(self, platform, entity_prefix):
        '''
        Read the /config/.storage/core.entity_registry file and return
        the entities for platform ('mobile_app', 'ios', etc)
        '''

        try:
            if self.entity_registry_file is None:
                self.entity_registry_file  = self.hass.config.path(
                        STORAGE_DIR, STORAGE_KEY_ENTITY_REGISTRY)

            entity_prefix       += '.'
            entities            = []
            entity_reg_file     = open(self.entity_registry_file)
            entity_reg_str      = entity_reg_file.read()
            entity_reg_data     = json.loads(entity_reg_str)
            entity_reg_entities = entity_reg_data['data']['entities']
            entity_reg_file.close()

            entity_devicename_list = ""
            for entity in entity_reg_entities:
                if (entity['platform'] == platform):
                    entities.append(entity)
                    if entity['entity_id'].startswith(entity_prefix):
                        entity_devicename_list += (f"{CRLF_DOT}{entity['entity_id'].replace(entity_prefix, '')} "
                                                   f"({entity['original_name']})")

            event_msg = (f"Entity Registry {platform} {entity_prefix} entities found >{entity_devicename_list}")
            self._save_event("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)
            pass

        return entities
#--------------------------------------------------------------------
    def _get_mobile_app_notify_devicenames(self):
        '''
        Extract notify services devicenames from hass
        '''
        try:
            notify_devicenames = []
            services = self.hass.services
            notify_services = dict(services.__dict__)['_services']['notify']

            for notify_service in notify_services:
                if notify_service.startswith("mobile_app_"):
                    notify_devicenames.append(notify_service)
        except:
            pass

        return notify_devicenames
#--------------------------------------------------------------------
    def _get_entity_registry_item(self, devicename, iosapp_entities, device_id, desired_entity_name):
        '''
        Scan through the iosapp entities and get the actual ios app entity_id for
        the desired entity
        '''
        for entity in (x for x in iosapp_entities \
                if x['unique_id'].endswith(desired_entity_name)):

            if (entity['device_id'] == device_id):
                real_entity = entity['entity_id'].replace('sensor.', '')
                log_msg = (f"Matched iOS App {entity['entity_id']} with "
                            f"iCloud3 tracked_device {devicename}")
                self._log_info_msg(log_msg)

                return real_entity

        return ''

#--------------------------------------------------------------------
    def _is_valid_ha_device_tracker(self, devicename):
        '''
        Validate the 'device_tracker.devicename' entity during the iCloud3
        Stage 2 initialization. If it does not exist, then it has not been set
        up in known_devices.yaml (and/or the iosapp) and can not be used ty
        the 'see' function thatupdates the location information.
        '''
        try:
            retry_cnt = 0
            entity_id = self._format_entity_id(devicename)

            while retry_cnt < 10:
                ic3dev_data  = self.hass.states.get(entity_id)

                if ic3dev_data:
                    ic3dev_attrs = ic3dev_data.attributes

                    if ic3dev_attrs:
                        return True
                retry_cnt += 1

        #except (KeyError, AttributeError):
        #    pass

        except Exception as err:
            _LOGGER.exception(err)

        return False

#########################################################
#
#   DEVICE SENSOR SETUP ROUTINES
#
#########################################################
    def _setup_sensor_base_attrs(self, devicename):
        '''
        The sensor name prefix can be the devicename or a name specified on
        the track_device configuration parameter        '''

        self.sensor_prefix_name[devicename] = devicename

        attr_prefix_fname = self.sensor_prefix_name.get(devicename)

        #Format sensor['friendly_name'] attribute prefix
        attr_prefix_fname = attr_prefix_fname.replace('_','-').title()
        attr_prefix_fname = attr_prefix_fname.replace('Ip','-iP')
        attr_prefix_fname = attr_prefix_fname.replace('Iw','-iW')
        attr_prefix_fname = attr_prefix_fname.replace('--','-')
        attr_prefix_fname = attr_prefix_fname.replace('-De-', '-de-')
        if attr_prefix_fname.startswith('-'): attr_prefix_fname = attr_prefix_fname[1:]

        self.sensor_attr_fname_prefix[devicename] = (f"{attr_prefix_fname} ")

        badge_attrs = {}
        badge_attrs['entity_picture'] = self.badge_picture.get(devicename)
        badge_attrs[ATTR_FRIENDLY_NAME]  = self.fname.get(devicename)
        badge_attrs['icon']           = SENSOR_ATTR_ICON.get('badge')
        self.sensor_badge_attrs[devicename] = badge_attrs

        event_msg = ""
        for zone in self.track_from_zones.get(devicename):
            if zone == HOME:
                zone_prefix = ''
            else:
                zone_prefix = zone + '_'
            event_msg = (f"{CRLF_DOT}Sensor entity prefix > sensor.{zone_prefix}"
                         f"{self.sensor_prefix_name.get(devicename)}")

        log_msg = (f"Set up sensor name for device, devicename-{devicename}, "
                    f"entity_base-{self.sensor_prefix_name.get(devicename)}")
        self._log_debug_msg(devicename, log_msg)

        #Return text for the event msg during startup
        return event_msg

#--------------------------------------------------------------------
    def _setup_sensors_custom_list(self, initial_load_flag):
        '''
        This will process the 'sensors' and 'exclude_sensors' config
        parameters if 'sensors' exists, only those sensors wil be displayed.
        if 'exclude_sensors' eists, those sensors will not be displayed.
        'sensors' takes ppresidence over 'exclude_sensors'.
        '''

        if initial_load_flag is False:
            return

        if self.sensor_ids != []:
            self.sensors_custom_list = []
            for sensor_id in self.sensor_ids[0].split(','):
                id = sensor_id.lower().strip()
                if id in SENSOR_ID_NAME_LIST:
                    self.sensors_custom_list.append(SENSOR_ID_NAME_LIST.get(id))

        elif self.exclude_sensor_ids != []:
            self.sensors_custom_list.extend(SENSOR_DEVICE_ATTRS)
            for sensor_id in self.exclude_sensor_ids[0].split(','):
                id = sensor_id.lower().strip()
                if id in SENSOR_ID_NAME_LIST:
                    if SENSOR_ID_NAME_LIST.get(id) in self.sensors_custom_list:
                        self.sensors_custom_list.remove(SENSOR_ID_NAME_LIST.get(id))
        else:
            self.sensors_custom_list.extend(SENSOR_DEVICE_ATTRS)


#########################################################
#
#   DEVICE STATUS SUPPORT FUNCTIONS FOR GPS ACCURACY, OLD LOC DATA, ETC
#
#########################################################
    def _check_poor_location_gps(self, devicename, timestamp_secs, gps_accuracy, checkOnly=False):
        """
        If this is checked in the icloud location cycle,
        check if the location isold flag. Then check to see if
        the current timestamp is the same as the timestamp on the previous
        poll.

        If this is checked in the iosapp cycle,  the trigger transaction has
        already updated the lat/long so
        you don't want to discard the record just because it is old.
        If in a zone, use the trigger but check the distance from the
        zone when updating the device.

        Update the old_location_poor_gps_cnt if just_check=False
        """

        try:
            discard_reason    = ""
            location_age      = int(self._secs_since(timestamp_secs))
            location_age_str  = (f"{self._format_age(location_age)}")
            location_time_age = self._format_time_age(timestamp_secs)
            old_location_flag = (location_age > self.old_location_secs.get(devicename))
            poor_gps_flag     = (gps_accuracy > self.gps_accuracy_threshold)

            if old_location_flag and poor_gps_flag:
                discard_reason = (f"OldLocation-{location_time_age}, PoorGPS-{gps_accuracy}m")
            elif old_location_flag:
                discard_reason = (f"OldLocation-{location_time_age}")
            elif poor_gps_flag:
                discard_reason = (f"PoorGPS-{gps_accuracy}m")

            #Do not update status and count if just checking poor loc gps status
            if checkOnly:
                return (old_location_flag or poor_gps_flag)


            if old_location_flag or poor_gps_flag:
                self.poor_gps_flag[devicename] = True
                self.poor_location_gps_cnt[devicename] += 1
                discard_reason += (f" (#{self.poor_location_gps_cnt.get(devicename)})")
            else:
                self.poor_gps_flag[devicename] = False
                self.poor_location_gps_cnt[devicename]  = 0

            #log_msg = (f"CHECK ISOLD/GPS ACCURACY, Time-{self._secs_to_time(timestamp_secs)}, "
            #            f"isOldFlag-{old_location_flag}, Age-{location_age_str}, "
            log_msg = (f"CHECK ISOLD/GPS ACCURACY, Time-{location_time_age}, "
                        f"isOldFlag-{old_location_flag}, "
                        f"GPSAccuracy-{gps_accuracy}m, GPSAccuracyFlag-{poor_gps_flag}",
                        f"Results-{self.poor_gps_flag.get(devicename)}, "
                        f"DiscardReason-{discard_reason}")
            self._log_debug_msg(devicename, log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            self.poor_gps_flag[devicename] = False
            self.poor_location_gps_cnt[devicename] = 0

            log_msg = ("►INTERNAL ERROR (ChkOldLocPoorGPS)")
            self._log_error_msg(log_msg)

        return (self.poor_gps_flag.get(devicename), discard_reason)

#--------------------------------------------------------------------
    def _is_next_update_time_reached(self, devicename=None):
        '''
        Cycle through the next_update_secs for all devices and
        determine if one of them is earlier than the current time.
        If so, the devices need to be updated.

        Return  None    - Next update time has not been reached on any devicename:zone
                devicename - devicename of phone that needs to be updated
        '''
        try:
            if self.next_update_secs is None:
                return None

            self.next_update_devicenames = []
            for devicename_zone in self.next_update_secs:
                if (devicename is None or devicename_zone.startswith(devicename)):
                    time_till_update = self.next_update_secs.get(devicename_zone) - \
                            self.this_update_secs

                    if time_till_update <= 5:
                        self.next_update_devicenames.append(devicename_zone.split(':')[0])

                        return (f"{devicename_zone.split(':')[0]}")

        except Exception as err:
            _LOGGER.exception(err)

        return None

#--------------------------------------------------------------------
    def _is_next_update_time_reached_devicename(self, devicename):
        '''
        Cycle through the next_update_secs for this devicename and
        determine if one of them is earlier than the current time.
        If so, the devicename need to be updated.

        Return  True    - Reached next_update_secs, update devicename
                False   - Do not update devicename
        '''
        try:
            if self.next_update_secs is None:
                return False

            for devicename_zone in self.next_update_secs:
                if devicename_zone.startswith(devicename):
                    time_till_update = self.next_update_secs.get(devicename_zone) - \
                            self.this_update_secs

                    if time_till_update <= 5:
                        return True

        except Exception as err:
            _LOGGER.exception(err)

        return False
#--------------------------------------------------------------------
    def _is_in_zone_and_before_next_update(self, devicename):
        '''
        If updated because another device was updated and this device is
        in a zone and it's next time has not been reached, do not update now
        '''
        try:
            if (self.state_this_poll.get(devicename) != NOT_SET
                    and self._is_inzone(devicename)
                    and self._was_inzone(devicename)
                    and self._is_next_update_time_reached(devicename) is None):

                return True

        except Exception as err:
            _LOGGER.exception(err)

        return False

#--------------------------------------------------------------------
    def _is_outside_zone_no_exit(self, devicename, zone, trigger, latitude, longitude):
        '''
        If the device is outside of the zone and less than the zone radius + gps_acuracy_threshold
        and no Geographic Zone Exit trigger was received, it has probably wandered due to
        GPS errors. If so, discard the poll and try again later
        '''
        trigger = self.trigger.get(devicename) if trigger == '' else trigger
        if trigger in IOS_TRIGGERS_ENTER:
            return False, ''

        dist_from_zone_m  = self._zone_distance_m(
                                devicename,
                                zone,
                                latitude,
                                longitude)

        zone_radius_m = self.zone_radius_m.get(
                                zone,
                                self.zone_radius_m.get(HOME))
        zone_radius_accuracy_m = zone_radius_m + self.gps_accuracy_threshold

        msg = ''
        if (dist_from_zone_m > zone_radius_m
                and self.got_exit_trigger_flag.get(devicename) is False
                and instr(zone, STATIONARY) is False):
            if dist_from_zone_m < zone_radius_accuracy_m:
                self.poor_gps_flag[devicename] = True

                msg = ("Outside Zone and No Exit Zone trigger, "
                    f"Keeping in zone > Zone-{zone}, "
                    f"Distance-{dist_from_zone_m}m, "
                    f"DiscardDist-{zone_radius_m}m to {zone_radius_accuracy_m}m ")
                return True, msg
            else:
                msg = ("Outside Zone and No Exit Zone trigger but outside threshold, "
                    f"Exiting zone > Zone-{zone}, "
                    f"Distance-{dist_from_zone_m}m, "
                    f"DiscardDist-{zone_radius_m}m to {zone_radius_accuracy_m}m ")

        return False, ''

#--------------------------------------------------------------------
    def _pause_device(self, devicename):
        '''
        Pause tracking the device
        '''
        devicename_zone = self._format_devicename_zone(devicename, HOME)

        self.next_update_secs[devicename_zone] = HIGH_INTEGER
        self.next_update_time[devicename_zone] = PAUSED

        attrs = {}
        attrs[ATTR_NEXT_UPDATE_TIME] = PAUSED
        self._update_device_sensors(devicename_zone, attrs)

        self._display_info_status_msg(devicename, PAUSED_CAPS)

#--------------------------------------------------------------------
    def _is_device_paused(self, devicename):
        '''
        Return True if the device is paused
        '''
        devicename_zone = self._format_devicename_zone(devicename, HOME)

        return (self.next_update_time.get(devicename_zone) == PAUSED)

#--------------------------------------------------------------------
    def _get_interval_for_error_retry_cnt(self, devicename, counter=POOR_LOC_GPS_CNT, pause_control_flag=False):
        '''
        Get the interval time based on the retry_cnt.
        retry_cnt   =   poor_location_gps count (default)
                    =   iosapp_request_loc_sent_retry_cnt
                    =   retry pyicloud authorization count
        pause_control_flag = True if device will be paused (interval is negative)
                           = False if just getting interfal and device will not be paused

        Returns     interval in minutes
                    (interval is negative if device should be paused)

        Interval range table - key = retry_cnt, value = time in minutes
        - poor_location_gps cnt, icloud_authentication cnt (default):
            interval_range_1 = {0:.25, 4:1, 8:5,  12:30, 16:60, 20:120, 24:240}
        - request iosapp location retry cnt:
            interval_range_2 = {0:.5,  4:2, 8:30, 12:60, 16:120}

        '''
        if counter == POOR_LOC_GPS_CNT:
            retry_cnt = self.poor_location_gps_cnt.get(devicename, 0)
            range_tbl = RETRY_INTERVAL_RANGE_1

        elif counter == AUTH_ERROR_CNT:
            retry_cnt = self.icloud_acct_auth_error_cnt
            range_tbl = RETRY_INTERVAL_RANGE_1

        elif counter == IOSAPP_REQUEST_LOC_CNT:
            retry_cnt = self.iosapp_request_loc_retry_cnt.get(devicename)
            range_tbl = RETRY_INTERVAL_RANGE_2
        else:
            return 60

        interval = .25
        for k, v in range_tbl.items():
            if k <= retry_cnt:
                interval = v

        if pause_control_flag is False: interval = abs(interval)
        interval = interval * 60

        return interval
#--------------------------------------------------------------------
    def _display_time_till_update_info_msg(self, devicename_zone, age_secs):
        '''
        Display the secs until the next update in the next update time field.
        if between 90s to -90s. if between -90s and -120s, resisplay time
        without the age to make sure it goes away.
        '''

        info_msg=(f"{self._secs_to_timestamp(self.next_update_secs.get(devicename_zone))}")
        if age_secs <= 90 and age_secs >= -90:
            info_msg += (f"-{age_secs}s")

        if age_secs <= 90 and age_secs > -120:
            attrs = {}
            attrs[ATTR_NEXT_UPDATE_TIME] = info_msg
            self._update_device_sensors(devicename_zone, attrs)

#--------------------------------------------------------------------
    def _log_device_status_attrubutes(self, status):

        """
        Status-{'batteryLevel': 1.0, 'deviceDisplayName': 'iPhone X',
        ATTR_ICLOUD_DEVICE_STATUS: '200', CONF_NAME: 'Gary-iPhone',
        'deviceModel': 'iphoneX-1-2-0', 'rawDeviceModel': 'iPhone10,6',
        ATTR_ICLOUD_DEVICE_CLASS: 'iPhone',
        'id':'qyXlfsz1BIOGxcqDxDleX63Mr63NqBxvJcajuZT3y05RyahM3/OMpuHYVN
        SUzmWV', 'lowPowerMode': False, 'batteryStatus': 'NotCharging',
        'fmlyShare': False, 'location': {'isOld': False,
        'isInaccurate': False, 'altitude': 0.0, 'positionType': 'GPS'
        'latitude': 27.726843548976, 'floorLevel': 0,
        'horizontalAccuracy': 48.00000000000001,
        'locationType': '', 'timeStamp': 1539662398966,
        'locationFinished': False, 'verticalAccuracy': 0.0,
        'longitude': -80.39036092533418}, 'locationCapable': True,
        'locationEnabled': True, 'isLocating': True, 'remoteLock': None,
        'activationLocked': True, 'lockedTimestamp': None,
        'lostModeCapable': True, 'lostModeEnabled': False,
        'locFoundEnabled': False, 'lostDevice': None,
        'lostTimestamp': '', 'remoteWipe': None,
        'wipeInProgress': False, 'wipedTimestamp': None, 'isMac': False}
        """

        log_msg = (f"ICLOUD DATA, DEVICE ID-{status}, ▶deviceDisplayName-{status['deviceDisplayName']}")
        self._log_debug_msg('*', log_msg)

        location = status[ATTR_LOCATION]

        log_msg = (f"ICLOUD DEVICE STATUS/LOCATION, "
            f"●deviceDisplayName-{status['deviceDisplayName']}, "
            f"●deviceStatus-{status[ATTR_ICLOUD_DEVICE_STATUS]}, "
            f"●name-{status[CONF_NAME]}, "
            f"●deviceClass-{status[ATTR_ICLOUD_DEVICE_CLASS]}, "
            f"●batteryLevel-{status[ATTR_ICLOUD_BATTERY_LEVEL]}, "
            f"●batteryStatus-{status[ATTR_ICLOUD_BATTERY_STATUS]}, "
            f"●positionType-{location['positionType']}, "
            f"●latitude-{location[ATTR_LATITUDE]}, "
            f"●longitude-{location[ATTR_LONGITUDE]}, "
            f"●horizontalAccuracy-{location[ATTR_ICLOUD_HORIZONTAL_ACCURACY]}, "
            f"●timeStamp-{location[ATTR_ICLOUD_TIMESTAMP]}"
            f"({self._timestamp_to_time_utcsecs(location[ATTR_ICLOUD_TIMESTAMP])})")
            #f"●isOld-{location[ATTR_ISOLD]}, "
        self._log_debug_msg('*', log_msg)
        return True

#--------------------------------------------------------------------
    def _log_start_finish_update_banner(self, start_finish_symbol, devicename,
                method, update_reason):
        '''
        Display a banner in the log file at the start and finish of a
        device update cycle
        '''

        log_msg = (f"^ {method} ^ {devicename}-{self.group}-{self.base_zone} ^^ "
                   f"State-{self.state_this_poll.get(devicename)} ^^ {update_reason} ^")

        log_msg2 = log_msg.replace('^', start_finish_symbol, 99).replace(" ",".").upper()
        self._log_debug_msg(devicename, log_msg2)

#########################################################
#
#   EVENT LOG ROUTINES
#
#########################################################
    def _setup_event_log_base_attrs(self, initial_load_flag):
        '''
        Set up the name, picture and devicename attributes in the Event Log
        sensor. Read the sensor attributes first to see if it was set up by
        another instance of iCloud3 for a different iCloud acount.
        '''
        try:
            curr_base_attrs = self.hass.states.get(SENSOR_EVENT_LOG_ENTITY).attributes

            base_attrs = {k: v for k, v in curr_base_attrs.items()}

        except (KeyError, AttributeError):
            base_attrs         = {}
            base_attrs["logs"] = ""

        except Exception as err:
            _LOGGER.exception(err)

        try:
            name_attrs = {}
            if self.tracked_devices:
                for devicename in self.tracked_devices:
                    name_attrs[devicename] = self.fname.get(devicename)
            else:
                name_attrs = {'No Tracked Devices Error'}

            if len(self.tracked_devices) > 0:
                self.log_table_max_items  = EVLOG_RECDS_PER_DEVICE * len(self.tracked_devices)
                if len(self.track_from_zones.get(devicename)) > 1:
                    self.log_table_max_items  = .25 * self.log_table_max_items * len(self.track_from_zones.get(devicename))

            base_attrs["names"] = name_attrs

            self._set_state(SENSOR_EVENT_LOG_ENTITY, "Initialized", base_attrs)

            self.event_log_base_attrs = {k: v for k, v in base_attrs.items() if k != "logs"}
            self.event_log_base_attrs["logs"] = ""

        except Exception as err:
            _LOGGER.exception(err)

        return

#------------------------------------------------------
    def _save_sysevent(self, event_text):
        self._save_event("*", event_text)

    def _save_event(self, devicename, event_text):
        '''
        Add records to the Event Log table the devicename. If the devicename="*",
        the event_text is added to all devicesnames table.

        The event_text can consist of pseudo codes that display a 2-column table (see
        _display_usage_counts function for an example and details)

        The event_log lovelace card will display the event in a special color if
        the text starts with a special character:
        '''
        try:
            if (instr(event_text, "▼") or instr(event_text, "▲")
                    or len(event_text) == 0
                    or instr(event_text, "event_log")):
                return

            devicename_zone  = self._format_devicename_zone(devicename, HOME)
            this_update_time = dt_util.now().strftime('%H:%M:%S')
            this_update_time = self._time_to_12hrtime(this_update_time, ampm=True)

            if devicename is None: devicename = '*'

            if ((self.start_icloud3_inprocess_flag and self.state_this_poll.get(devicename) == '')
                    or devicename == "*"):
                iosapp_state= ''
                zone_names  = ''
                zone        = ''
                interval    = ''
                travel_time = ''
                distance    = ''

            else:
                iosapp_state= self.last_iosapp_state.get(devicename, '')
                zone        = self.zone_current.get(devicename, AWAY)
                interval    = self.interval_str.get(devicename_zone, '').split("(")[0]
                travel_time = self.last_tavel_time.get(devicename_zone, '')
                distance    = self.last_distance_str.get(devicename_zone, '')

            if (instr(type(event_text), 'dict') or instr(type(event_text), 'list')):
                 event_text = str(event_text)

            if instr(zone, STATIONARY):         zone = STATIONARY
            if instr(iosapp_state, STATIONARY): iosapp_state = STATIONARY

            iosapp_state = self.zone_to_display.get(iosapp_state, iosapp_state.title())
            zone         = self.zone_to_display.get(zone, zone.title())
            iosapp_state = iosapp_state.replace("'", "`")
            zone         = zone.replace("'", "`")

            if iosapp_state == None: iosapp_state = ''
            if zone         == None: zone         = ''

            if len(event_text) == 0: event_text = 'Info Message'
            if event_text.startswith('__'): event_text = event_text[2:]
            event_text = event_text.replace('"', '`')
            event_text = event_text.replace("'", "`")
            event_text = event_text.replace('~','--')
            event_text = event_text.replace('Background','Bkgnd')
            event_text = event_text.replace('Geographic','Geo')
            event_text = event_text.replace('Significant','Sig')

            for from_text in self.display_text_as_list:
                event_text = event_text.replace(from_text, self.display_text_as_list.get(from_text))

            #Keep track of special colors so it will continue on the
            #next text chunk
            color_symbol = ''
            if event_text.startswith('^1^'): color_symbol = '^1^'
            if event_text.startswith('^2^'): color_symbol = '^2^'
            if event_text.startswith('^3^'): color_symbol = '^3^'
            if event_text.startswith('^4^'): color_symbol = '^4^'
            if event_text.startswith('^5^'): color_symbol = '^5^'
            if event_text.startswith('^6^'): color_symbol = '^6^'
            if instr(event_text, ERROR):     color_symbol = '!'
            char_per_line = 2000

            #Break the event_text string into chunks of 250 characters each and
            #create an event_log recd for each chunk
            if len(event_text) < char_per_line:
                event_recd = [devicename, this_update_time,
                                iosapp_state, zone, interval, travel_time,
                                distance, event_text]
                self._insert_event_log_recd(event_recd)

            else:
                line_no       = int(len(event_text)/char_per_line + .5)
                char_per_line = int(len(event_text) / line_no)
                event_text+=f" ({len(event_text)}-{line_no}-{char_per_line})"

                if event_text.find("CRLF") > 0:
                    split_str = "CRLF"
                else:
                    split_str = " "
                split_str_end_len = -1 * len(split_str)
                word_chunk = event_text.split(split_str)

                line_no = len(word_chunk)-1
                event_chunk = ''
                while line_no >= 0:
                    if len(event_chunk) + len(word_chunk[line_no]) + len(split_str) > char_per_line:
                        event_recd = [devicename, '', '', '', '', '', '',
                                     (f"{color_symbol}{event_chunk[:split_str_end_len]} ({event_chunk[:split_str_end_len]})")]
                        self._insert_event_log_recd(event_recd)

                        event_chunk = ''

                    if len(word_chunk[line_no]) > 0:
                        event_chunk = word_chunk[line_no] + split_str + event_chunk

                    line_no-=1

                event_recd = [devicename, this_update_time,
                                iosapp_state, zone, interval, travel_time,
                                distance, (f"{event_chunk[:split_str_end_len]} ({event_chunk[:split_str_end_len]})")]
                self._insert_event_log_recd(event_recd)

        except Exception as err:
            _LOGGER.exception(err)

#-------------------------------------------------------
    def _insert_event_log_recd(self, event_recd):
        """Add the event recd into the event table"""

        if self.event_log_table is None:
            self.event_log_table = INITIAL_EVLOG_TABLE

        while len(self.event_log_table) >= self.log_table_max_items:
            self.event_log_table.pop()

        self.event_log_table.insert(0, event_recd)

#------------------------------------------------------
    def _update_sensor_ic3_event_log(self, devicename):
        """Display the event log"""

        try:
            log_attrs = self.event_log_base_attrs.copy() if self.event_log_base_attrs else {}

            attr_recd  = {}
            attr_event = {}
            log_attr_text = ""
            if self.log_eventlog_flag: log_attr_text += "evlog,"
            if self.log_debug_flag:    log_attr_text += "halog,"
            if self.log_rawdata_flag:  log_attr_text += "rawdata,"
            log_attrs["log_level_debug"] = log_attr_text

            if devicename is None:
                return
            elif devicename == "clear_log_items":
                log_attrs["filtername"] = "ClearLogItems"
            elif devicename == "*" :
                log_attrs["filtername"] = "Initialize"
            else:
                log_attrs["filtername"] = self.fname.get(devicename)

            if devicename == 'clear_log_items':
                max_recds  = EVENT_LOG_CLEAR_CNT
                self.event_log_clear_secs = HIGH_INTEGER
                devicename = self.event_log_last_devicename
            else:
                max_recds = HIGH_INTEGER
                self.event_log_clear_secs = self.this_update_secs + EVENT_LOG_CLEAR_SECS
                self.event_log_last_devicename = devicename

            #The state must change for the recds to be refreshed on the
            #Lovelace card. If the state does not change, the new information
            #is not displayed. Add the update time to make it unique.
            log_update_time = (f"{dt_util.now().strftime('%a, %m/%d')}, "
                               f"{dt_util.now().strftime(self.um_time_strfmt)}")
            log_attrs["update_time"] = log_update_time
            self.event_log_sensor_state = (f"{devicename}:{log_update_time}")

            attr_recd = self._update_sensor_ic3_event_log_recds(devicename, max_recds)
            log_attrs["logs"] = attr_recd

            self._set_state(SENSOR_EVENT_LOG_ENTITY, self.event_log_sensor_state, log_attrs)

        except Exception as err:
            _LOGGER.exception(err)
#------------------------------------------------------
    def _update_sensor_ic3_event_log_recds(self, devicename, max_recds=HIGH_INTEGER):
        '''
        Build the event items attribute for the event log sensor. Each item record
        is [devicename, time, state, zone, interval, travTime, dist, textMsg]
        Select the items for the devicename or '*' and return the string of
        the resulting list to be passed to the Event Log
        '''
        if devicename == "startup_log":
            devicename = "*"

        el_devicename_check=['*', devicename]

        if self.log_eventlog_flag:
            attr_recd = [el_recd[1:8] for el_recd in self.event_log_table \
                if el_recd[0] in el_devicename_check]
        elif devicename == "*":
            attr_recd = [el_recd[1:8] for el_recd in self.event_log_table \
                if ((el_recd[0] in el_devicename_check
                        or el_recd[7].startswith(EVLOG_ALERT))
                    and (el_recd[7].startswith(EVLOG_DEBUG) is False))]
        else:
            attr_recd = [el_recd[1:8] for el_recd in self.event_log_table \
                if (el_recd[0] in el_devicename_check
                    and el_recd[7].startswith(EVLOG_DEBUG) is False)]

        if max_recds == EVENT_LOG_CLEAR_CNT:
            recd_cnt = len(attr_recd)
            attr_recd = attr_recd[0:max_recds]
            control_recd = ['',' ',' ',' ',' ',' ',f'^^^Click `Refresh` to display \
                                all records ({max_recds} of {recd_cnt} displayed)^^^']
            attr_recd.insert(0, control_recd)

        control_recd = [HHMMSS_ZERO,'','','','','','Last Record']
        attr_recd.append(control_recd)

        return str(attr_recd)

#------------------------------------------------------
    def _export_ic3_event_log(self):
        ''' Export Event Log to 'config/icloud_event_log.txt' '''

        try:
            log_update_time = (f"{dt_util.now().strftime('%a, %m/%d')}, "
                                f"{dt_util.now().strftime(self.um_time_strfmt)}")
            hdr_recd    ="devicename\tTime\tiOSApp State\tiC3 Zone\tInterval\tTravel Time\tDistance\tText"
            export_recd = (f"{hdr_recd}\n"
                           f"Tracked Devices: { self.tracked_devices:}\n"
                           f"Log Update Time: {log_update_time}\n")

            #Prepare Global '*' records. Reverse the list elements using [::-1] and make a string of the results
            el_recds     = [el_recd for el_recd in self.event_log_table if (el_recd[0] == "*")]
            dev_recds    = str(el_recds[::-1])
            export_recd += self._export_ic3_event_log_reformat_recds(dev_recds)

            #Prepare recds for each devicename
            for devicename in  self.tracked_devices:
                el_devicename_check=[devicename]
                el_recds     = [el_recd for el_recd in self.event_log_table \
                                if (el_recd[0] == devicename and el_recd[3] != "Device.Cnts")]
                dev_recds    = str(el_recds[::-1])
                export_recd += self._export_ic3_event_log_reformat_recds(dev_recds)

            ic3_directory = os.path.abspath(os.path.dirname(__file__))
            export_filename = (f"{ic3_directory.split('custom_components')[0]}/icloud3-event-log.txt")
            export_filename = export_filename.replace("//", "/")

            export_file = open(export_filename, "w")
            export_file.write(export_recd)
            export_file.close()

            event_msg = (f"iCloud3 Event Log Exported > File {export_filename}")
            self._save_event_halog_info("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)

#--------------------------------------------------------------------
    def _export_ic3_event_log_reformat_recds(self, recd_str):
        recd_str = recd_str.replace("[[", "").replace("]]","").replace("], [", "\n")
        recd_str = recd_str.replace("''", "'-'").replace("', '","\t")
        recd_str = recd_str.replace("'", "").replace("CRLF", ", ")
        recd_str = recd_str.replace("^^^", "").replace("^1^", "").replace("^2^", "").replace("^3^", "")
        recd_str = recd_str.replace("^4^", "").replace("^5^", "").replace("^6^", "")
        recd_str = recd_str.replace("*", "-- sys event --")

        for from_text in self.display_text_as_list:
            recd_str = recd_str.replace(from_text, self.display_text_as_list.get(from_text))

        recd_str += "\n\n"
        return recd_str

#########################################################
#
#   WAZE ROUTINES
#
#########################################################
    def _get_waze_data(self, devicename,
                            this_lat, this_long, last_lat,
                            last_long, zone, last_dist_from_zone_km):

        try:
            if (not self.distance_method_waze_flag
                    or self.WazeRouteCalc is None):
                return (WAZE_NOT_USED, 0, 0, 0)
            elif zone == self.base_zone:
                return (WAZE_USED, 0, 0, 0)
            elif self.waze_status == WAZE_PAUSED:
                return (WAZE_PAUSED, 0, 0, 0)

            try:
                log_msg = (f"Request Waze Info, CurrentLoc to {self.base_zone}")
                self._log_info_msg(log_msg)
                waze_from_zone = self._get_waze_distance(devicename,
                        this_lat, this_long,
                        self.base_zone_lat, self.base_zone_long)

                waze_status = waze_from_zone[0]
                if waze_status == WAZE_NO_DATA:
                    event_msg = (f"Waze Route Failure > No Response from Waze Servers, "
                                 f"Calc distance will be used")
                    self._save_event_halog_info(devicename, event_msg)

                    return (WAZE_NO_DATA, 0, 0, 0)

                log_msg = (f"Request Waze Info, CurrentLoc to LastLoc")
                self._log_info_msg(log_msg)
                waze_from_last_poll = self._get_waze_distance(devicename,
                        last_lat, last_long, this_lat, this_long)

            except Exception as err:
                _LOGGER.exception(err)

                if err == "Name 'WazeRouteCalculator' is not defined":
                    self.distance_method_waze_flag = False
                    return (WAZE_NOT_USED, 0, 0, 0)

                return (WAZE_NO_DATA, 0, 0, 0)

            try:
                waze_dist_from_zone_km = self._round_to_zero(waze_from_zone[1])
                waze_time_from_zone    = self._round_to_zero(waze_from_zone[2])
                waze_dist_last_poll    = self._round_to_zero(waze_from_last_poll[1])

                if waze_dist_from_zone_km == 0:
                    waze_time_from_zone = 0
                else:
                    waze_time_from_zone = self._round_to_zero(waze_from_zone[2])

                if ((waze_dist_from_zone_km > self.waze_max_distance)
                        or (waze_dist_from_zone_km < self.waze_min_distance)):
                    waze_status = WAZE_OUT_OF_RANGE

            except Exception as err:
                _LOGGER.exception(err)
                log_msg = (f"►INTERNAL ERROR (ProcWazeData)-{err})")
                self._log_error_msg(log_msg)

            waze_time_msg = self._format_waze_time_msg(waze_time_from_zone)
            event_msg = (f"Waze Route Info: {self.zone_to_display.get(self.base_zone)} > "
                         f"Dist-{waze_dist_from_zone_km}km, "
                         f"TravTime-{waze_time_msg}, "
                         f"DistMovedSinceLastUpdate-{waze_dist_last_poll}km")
            self._save_event(devicename, event_msg)

            log_msg = (f"WAZE DISTANCES CALCULATED>, "
                      f"Status-{waze_status}, DistFromHome-{waze_dist_from_zone_km}, "
                      f"TimeFromHome-{waze_time_from_zone}, "
                      f"DistLastPoll-{waze_dist_last_poll}, "
                      f"WazeFromHome-{waze_from_zone}, "
                      f"WazeFromLastPoll-{waze_from_last_poll}")
            self._log_debug_interval_msg(devicename, log_msg)

            return (waze_status, waze_dist_from_zone_km, waze_time_from_zone,
                    waze_dist_last_poll)

        except Exception as err:
            _LOGGER.exception(err)
            self._set_waze_not_available_error(err)

            return (WAZE_NO_DATA, 0, 0, 0)

#--------------------------------------------------------------------
    def _get_waze_distance(self, devicename, from_lat, from_long, to_lat,
                        to_long):
        """
        Example output:
            Time 72.42 minutes, distance 121.33 km.
            (72.41666666666667, 121.325)

        See https://github.com/home-assistant/home-assistant/blob
        /master/homeassistant/components/sensor/waze_travel_time.py
        See https://github.com/kovacsbalu/WazeRouteCalculator
        """

        try:
            retry_cnt = 0
            while retry_cnt < 3:
                try:
                    self.count_waze_locates[devicename] += 1
                    waze_call_start_time = time.time()

                    route_time, route_distance = \
                            self.WazeRouteCalc.calc_route_info(from_lat, from_long, to_lat, to_long)

                    self.time_waze_calls[devicename] += (time.time() - waze_call_start_time)

                    route_time     = round(route_time, 0)
                    route_distance = round(route_distance, 2)

                    return (WAZE_USED, route_distance, route_time)

                # except WazeRouteCalculator.WRCError as err:
                except WRCError as err:
                    retry_cnt += 1
                    log_msg = (f"Waze Server Error (#{retry_cnt}), Retrying, Type-{err}")
                    self._log_info_msg(log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            self._set_waze_not_available_error(err)

        return (WAZE_NO_DATA, 0, 0)

#--------------------------------------------------------------------
    def _set_waze_not_available_error(self, err):
        ''' Turn Waze off if connection error '''
        if (instr(err, "www.waze.com")
                and instr(err, "HTTPSConnectionPool")
                and instr(err, "Max retries exceeded")
                and instr(err, "TIMEOUT")):
            self.waze_status = WAZE_NOT_USED
            event_msg = ("!Waze Server Error > Connection error accessing www.waze.com, "
                        "Waze is not available, Will use `distance_method: calc`")
            self._save_event_halog_error_msg(devicename, event_msg)
        else:
            log_msg = (f"►INTERNAL ERROR (GetWazeDist-{err})")
            self._log_info_msg(log_msg)

#--------------------------------------------------------------------
    def _get_waze_from_data_history(self, devicename,
                        curr_dist_from_zone_km, this_lat, this_long):
        '''
        Before getting Waze data, look at all other devices to see
        if there are any really close. If so, don't call waze but use their
        distance & time instead if the data it passes distance and age
        tests.

        The other device's distance from home and distance from last
        poll might not be the same as this devices current location
        but it should be close enough.

        last_waze_data is a list in the following format:
           [timestamp, latitudeWhenCalculated, longitudeWhenCalculated,
                [distance, time, distMoved]]

        Returns: [ Waze History Data]
        '''

        devicename_zone = self._format_devicename_zone(devicename)
        if not self.distance_method_waze_flag:
            return None
        elif self.waze_status == WAZE_PAUSED:
            return None

        #Delete Waze history if entered/exited zone
        #v2.2.0rc7
        elif self.trigger.get(devicename) in IOS_TRIGGERS_ENTER_EXIT:
            self.waze_distance_history[devicename_zone] = []
            self.waze_history_data_used_flag[devicename_zone] = False
            return None

        #Calculate how far the old data can be from the new data before the
        #data will be refreshed.
        test_distance = curr_dist_from_zone_km * .05
        if test_distance > 5:
            test_distance = 5

        try:
            #other_closest_device_data = None
            used_data_from_devicename_zone = None
            for near_devicename_zone in self.waze_distance_history:
                self.waze_history_data_used_flag[devicename_zone] = False
                waze_data_other_device = self.waze_distance_history.get(near_devicename_zone)
                #Skip if this device doesn't have any Waze data saved or it's for
                #another base_zone.
                if len(waze_data_other_device) == 0:
                    continue
                elif len(waze_data_other_device[3]) == 0:
                    continue
                elif near_devicename_zone.endswith(':'+self.base_zone) is False:
                    continue

                waze_data_timestamp = waze_data_other_device[0]
                waze_data_latitude  = waze_data_other_device[1]
                waze_data_longitude = waze_data_other_device[2]

                dist_from_other_waze_data = self._calc_distance_km(
                            this_lat, this_long,
                            waze_data_latitude, waze_data_longitude)

                #Find device's waze data closest to my current location
                #If close enough, use it regardless of whose it is
                if dist_from_other_waze_data < test_distance:
                    used_data_from_devicename_zone = near_devicename_zone
                    other_closest_device_data      = waze_data_other_device[3]
                    test_distance                  = dist_from_other_waze_data

            #Return the waze history data for the other closest device
            #if used_data_from_devicename_zone is not None:
            if used_data_from_devicename_zone:
                used_devicename = used_data_from_devicename_zone.split(':')[0]
                event_msg = (f"Waze Route History Used: {self.zone_to_display.get(self.base_zone)} > "
                             f"Dist-{other_closest_device_data[1]}km, "
                             f"TravTime-{round(other_closest_device_data[2], 0)} min, "
                             f"UsedInfoFrom-{self._format_fname_devicename(used_devicename)}, "
                             f"({test_distance}m AwayFromMyLoc)")
                self._save_event_halog_info(devicename, event_msg)

                #Return Waze data (Status, distance, time, dist_moved)
                self.waze_history_data_used_flag[used_data_from_devicename_zone] = True
                self.waze_data_copied_from[devicename_zone] = used_data_from_devicename_zone
                return other_closest_device_data

        except Exception as err:
            _LOGGER.exception(err)

        return None

#--------------------------------------------------------------------
    def _format_waze_time_msg(self, waze_time_from_zone):
        '''
        Return the message displayed in the waze time field ►►
        '''

        #Display time to the nearest minute if more than 3 min away
        if self.waze_status == WAZE_USED:
            t = waze_time_from_zone * 60
            r = 0
            if t > 180:
                t, r = divmod(t, 60)
                t = t + 1 if r > 30 else t
                t = t * 60

            waze_time_msg = self._secs_to_time_str(t)

        else:
            waze_time_msg = '0 min'

        return waze_time_msg
#--------------------------------------------------------------------
    def _verify_waze_installation(self):
        '''
        Report on Waze Route alculator service availability
        '''

        self._log_info_msg("Verifying Waze Route Service component")

        if (WAZE_IMPORT_SUCCESSFUL and self.distance_method_waze_flag):
            self.waze_status = WAZE_USED
        else:
            self.waze_status = WAZE_NOT_USED
            self.distance_method_waze_flag = False
            self._log_info_msg("Waze Route Service not available")

#######################################################################
#
#   EXTRACT ICLOUD3 PARAMETERS FROM THE CONFIG_IC3.YAML PARAMETER FILE.
#
#   The ic3 parameters are specified in the HA configuration.yaml file and
#   processed when HA starts. The 'config_ic3.yaml' file lets you specify
#   parameters at HA startup time or when iCloud3 is restarted using the
#   Restart-iC3 command on the Event Log screen. When iC3 is restarted,
#   the parameters will override those specified at HA startup time.
#
#   1. You can, for example, add new tracked devices without restarting HA.
#   2. You can specify the username, password and tracking method in this
#      file but these items are onlyu processed when iC3 initially loads.
#      A restart will discard these items
#
#   Default file is config/custom_components/icloud3/config-ic3.yaml
#   if no '/' on the config_ic3_file_name parameter:
#       check the default directory
#       if not found, check the /config directory
#
#
#######################################################################
    def _get_config_ic3_parameters(self):

        try:
            config_filename = ""
            ic3_directory   = os.path.abspath(os.path.dirname(__file__))
            evlog_notice_color = "" if ic3_directory == "/config/custom_components/icloud3" else EVLOG_ALERT
            self._save_event("*", f"{evlog_notice_color}iCloud3 Directory > {ic3_directory}")
            event_msg = (f"iCloud3 Configuration File > ")

            #File name specified
            if self.config_ic3_file_name != "":
                if (instr(self.config_ic3_file_name, "/")
                        and os.path.exists(self.config_ic3_file_name)):
                    config_filename = self.config_ic3_file_name

                elif os.path.exists(f"/config/{self.config_ic3_file_name}"):
                    config_filename = (f"/config/{self.config_ic3_file_name}")

                elif os.path.exists(f"{ic3_directory}/{self.config_ic3_file_name}"):
                    config_filename = (f"{ic3_directory}/{self.config_ic3_file_name}")

            elif os.path.exists(DEFAULT_CONFIG_IC3_FILE_NAME):
                config_filename = DEFAULT_CONFIG_IC3_FILE_NAME

            elif os.path.exists(f"{ic3_directory}/config_ic3.yaml"):
                config_filename = (f"{ic3_directory}/config_ic3.yaml")

                alert_msg = (f"{EVLOG_ALERT}iCloud3 Alert > The `config_ic3.yaml` "
                             f"configuration file should moved to the `/config` "
                             f"directory so it is not deleted when HACS updates iCloud3")
                self._save_event("*", alert_msg)

            if config_filename == "":
                if self.config_ic3_file_name:
                    event_msg = (f"{EVLOG_ERROR}iCloud3 Error, Configuration File > "
                                 f"File not Found - {self.config_ic3_file_name}")
                else:
                    event_msg += "iCloud3 Configuration File > config_ic3.yaml not used"
                self._save_event("*", event_msg)
                return

            config_filename = config_filename.replace("//", "/")

            event_msg += (f"{config_filename}")
            self._save_event("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)
            return

        log_success_msg, log_error_msg = \
                self._get_recds_from_config_ic3(config_filename)

        if log_error_msg != "":
            event_msg = (f"{EVLOG_ERROR}iCloud3 Error processing '{config_filename}` parameters. "
                         f"The following parameters are invalid >{log_error_msg}")
            self._save_event_halog_error("*", event_msg)

        return

#-------------------------------------------------------------------------
    def _get_recds_from_config_ic3(self, config_filename):
        '''
        OrderedDict([('devices', [OrderedDict([('device_name', 'Gary-iPhone'),
        ('name', 'Gary'), ('email', 'gcobb321@gmail.com'),
        ('picture', 'gary.png'), ('track_from_zone', 'warehouse')]), OrderedDict([('device_name', 'lillian_iphone'),
        ('name', 'Lillian'), ('picture', 'lillian.png'), ('email', 'lilliancobb321@gmail.com')])]),
        ('display_text_as', ['gcobb321@gmail.com > gary_2fa@email.com', 'lilliancobb321@gmail.com > lillian_2fa@email.com',
        'twitter:@lillianhc > twitter:@lillian_twitter_handle', 'gary-real-email@gmail.com > gary_secret@email.com',
        'lillian-real-email@gmail.com > lillian_secret@email.com']),
        ('inzone_interval', '30 min'),
        ('display_zone_format', 'fname')])
        '''
        try:
            log_success_msg = ""
            log_error_msg   = ""
            success_msg     = ""
            error_msg       = ""
            devices_list    = []

            try:
                config_yaml_recds = yaml_loader.load_yaml(config_filename)
            except Exception as err:
                #_LOGGER.exception(err)
                #A missing quote mark gives the following error:
                #while parsing a block mapping in "/config/config_ic3.yaml", line 18, column 1
                #expected <block end>, but found '<scalar>' in "/config/config_ic3.yaml", line 47, column 31
                err_text = str(err)
                err_parts = err_text.split(', ')
                error_msg = (f"{EVLOG_ERROR}iCloud3 Error > Invalid configuration parameter > "
                        f"{CRLF_DOT}File-{config_filename}, {err_parts[4]}"
                        f"{CRLF_DOT}A mismatched quote (`) was found. Can not continue. Setup will be aborted.")
                self._save_event_halog_error("*", error_msg)
                return log_success_msg, log_error_msg

            #log_msg = (f"{EVLOG_DEBUG}config_ic3 Parameter Records > {config_yaml_recds}")
            #self._save_event("*", log_msg)

            #reset any changed items in config_ic3 from the last ic3 reset back to it's default value
            try:
                for last_config_ic3_item in self.last_config_ic3_items:
                    self._get_non_device_parms_from_config_ic3(
                                last_config_ic3_item, DEFAULT_CONFIG_VALUES.get(last_config_ic3_item))
            except:
                pass

            self.last_config_ic3_items = []

            for pname, pvalue in config_yaml_recds.items():
                if pname == CONF_DEVICES:
                    self.config_ic3_track_devices_fields.extend(\
                            self._get_devices_list_from_config_devices_parm(pvalue, 'config_ic3'))

                elif pname == CONF_TRACK_DEVICES:
                    self.config_ic3_track_devices_fields.extend(\
                             self._get_devices_list_from_config_track_devices_parm(pvalue, 'config_ic3'))
                else:
                    success_msg, error_msg = self._set_non_device_parm_in_config_parameter_dictionary(pname, pvalue)
                    if success_msg != "":
                        self.last_config_ic3_items.append(pname)

                    log_success_msg += success_msg
                    log_error_msg   += error_msg

        except Exception as err:
            _LOGGER.exception(err)
            pass

        return log_success_msg, log_error_msg

#-------------------------------------------------------------------------
    def _get_devices_list_from_config_devices_parm(self, conf_devices_parameter, source_file):
        '''
        Process the CONF_DEVICES parameter. This is the general routine for parsing
        the parameter and creating a dictionary (devices_list) containing values
        associated with each device_name.

        Input:      The CONF_DEVICES parameter
        Returns:    The dictionary with the fields associated with all of the devices
        '''
        devices_list = []
        for device in conf_devices_parameter:
            device_fields = {}
            for pname, pvalue in device.items():
                if pname in VALID_CONF_DEVICES_ITEMS:
                    if pname == CONF_DEVICENAME:
                        devicename        = slugify(pvalue)
                        name, device_type = self._extract_name_device_type(pvalue)
                        device_fields[CONF_DEVICENAME]  = devicename
                        device_fields[CONF_DEVICE_TYPE] = device_type
                        device_fields[CONF_NAME]        = name
                        device_fields[CONF_CONFIG]      = source_file
                        device_fields[CONF_SOURCE]      = 'Config Devices Parameter'

                    #You can track from multiple zones, cycle through zones and check each one
                    elif pname == CONF_TRACK_FROM_ZONE:
                        zones = pvalue.replace('zone.', '')
                        zones = zones.split(',')
                        db=f"8648 {self.zones=} {self.zone_fname=} {pvalue=} {zones=}"
                        self._save_sysevent(db)
                        pvalue = ''
                        for zone in zones:
                            zone = zone.strip()
                            if zone == HOME: continue
                            zfname = zone.replace(' ', '_')
                            if zone in self.zones:
                                pvalue += (f"{zone},")
                            elif zfname in self.zones:
                                pvalue += (f"{zfname},")
                            elif zone in self.zone_fname:
                                pvalue += (f"{self.zone_fname.get(zone)},")
                            elif zfname in self.zone_fname:
                                pvalue += (f"{self.zone_fname.get(zfname)},")
                            else:
                                self._display_config_parameter_error_msg(CONF_TRACK_FROM_ZONE, zone,
                                        self.zones, '(Invalid Zone Name)')
                        device_fields[CONF_TRACK_FROM_ZONE] = pvalue[:-1]

                    elif pname == CONF_IOSAPP_SUFFIX:
                            device_fields[CONF_IOSAPP_SUFFIX] = pvalue
                            device_fields.pop(CONF_IOSAPP_ENTITY, None)
                    elif pname == CONF_IOSAPP_ENTITY:
                            device_fields[CONF_IOSAPP_ENTITY] = pvalue
                            device_fields.pop(CONF_IOSAPP_SUFFIX, None)

                    elif pname == CONF_INZONE_INTERVAL:
                        device_fields[CONF_INZONE_INTERVAL] = self._time_str_to_secs(pvalue)

                    elif pname in [CONF_NOIOSAPP, CONF_NO_IOSAPP] and pvalue:
                        device_fields[CONF_IOSAPP_INSTALLED] = not pvalue

                    else:
                        device_fields[pname] = pvalue
                else:
                    self._display_config_parameter_error_msg(
                                pname, pvalue, VALID_CONF_DEVICES_ITEMS)

            devices_list.append(device_fields)

        return devices_list

#-------------------------------------------------------------------------
    def _get_devices_list_from_config_track_devices_parm(self, \
                            conf_track_devices_parameter, source_file):
        '''
        Process the CONF_TRACK_DEVICES parameter. This is the general routine for parsing
        the parameter and creating a dictionary (devices_list) containing values
        associated with each device_name.

        Input:      The CONF_DEVICES parameter
        Returns:    The dictionary with the fields associated with all of the devices
        '''
        devices_list = []
        for devicename_parameter in conf_track_devices_parameter:
            device_fields = {}
            device_fields = self._decode_track_devices_parameter(devicename_parameter)
            device_fields[CONF_CONFIG] = source_file
            device_fields[CONF_SOURCE] = devicename_parameter
            devices_list.append(device_fields)
        return devices_list

#-------------------------------------------------------------------------
    def _set_non_device_parm_in_config_parameter_dictionary(self, pname, pvalue):
        '''
        Set the config_parameters[key] master parameter dictionary from the
        config_ic3 parameter file

        Input:      parameter name & value
        Output:     Valid parameters are added to the config_parameter[pname] dictionary
        '''
        try:
            success_msg = ""
            error_msg   = ""
            if pname == "":
                return ("", "")

             #These parameters can not be changed
            if pname in [CONF_GROUP, CONF_USERNAME, CONF_PASSWORD,
                                  CONF_TRACKING_METHOD,
                                  CONF_CREATE_SENSORS, CONF_EXCLUDE_SENSORS,
                                  CONF_ENTITY_REGISTRY_FILE, CONF_CONFIG_IC3_FILE_NAME]:
                return ("", "")

            log_msg = (f"config_ic3 Parameter > {pname}: {pvalue}")
            self._evlog_debug_msg("*", log_msg)

            if pname in self.config_parameter:
                self.config_parameter[pname] = pvalue

            else:
                error_msg = (f"{CRLF_DOT}{pname}: {pvalue}")
                log_msg = (f"Invalid parameter-{pname}: {pvalue}")
                self._log_debug_msg("*", log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            error_msg = (f"{CRLF_DOT}{err}")

        if error_msg == "":
            success_msg = (f"{CRLF_DOT}{pname}: {pvalue}")

        return (success_msg, error_msg)

#-------------------------------------------------------------------------
    def _validate_config_parameters(self):
        '''
        Cycle through the each of the validate_parameters_type lists and
        validate the parameter values for each list type.

        If the value is invalid, display an error message in the event log
        and reset the config_parameter[xxx] value to it's default value.
        '''

        #validate list parameters: CONF_UNIT_OF_MEASUREMENT: ['mi', 'km']
        for pname in VALIDATE_PARAMETER_LIST:
            pvalue       = self.config_parameter.get(pname)
            valid_values = VALIDATE_PARAMETER_LIST.get(pname)
            if pvalue not in valid_values:
                self._display_config_parameter_error_msg(pname, pvalue, valid_values)

        #validate true/false parameters: CONF_CENTER_IN_ZONE (center_in_zone: false)
        for pname in VALIDATE_PARAMETER_TRUE_FALSE:
            pvalue       = self.config_parameter.get(pname)
            valid_values = [True, False]
            if pvalue not in valid_values:
                self._display_config_parameter_error_msg(pname, pvalue, valid_values)

        #validate number parameters: CONF_TRAVEL_TIME_FACTOR (travel_time_factor: .6)
        for pname in VALIDATE_PARAMETER_NUMBER:
            pvalue       = self.config_parameter.get(pname)
            valid_values = 'Number'
            if pvalue and isnumber(str(pvalue)) is False:
                self._display_config_parameter_error_msg(pname, pvalue, valid_values)

        #validate time parameters: CONF_INZONE_INTERVAL (inzone_interval: 30 min)
        for pname in VALIDATE_PARAMETER_TIME:
            pvalue       = self.config_parameter.get(pname)
            valid_values = ['sec', 'secs', 'min', 'mins', 'hr', 'hrs']
            time_parts   = (f"{pvalue} min").split(' ')
            if (time_parts[0] and time_parts[1] in valid_values
                    and isnumber(str(time_parts[0]))) is False:
                self._display_config_parameter_error_msg(pname, pvalue, valid_values)

#-------------------------------------------------------------------------
    def _display_config_parameter_error_msg(self, pname, pvalue, valid_values, msg=''):
        '''
        Display an invalid parameter error in the Event Log
        '''
        try:
            if valid_values == [True, False]:
                valid_values = 'true, false'

            elif type(valid_values) is list:
                if type(pvalue) is not int:
                    valid_values = ', '.join(valid_values)

        except Exception as err:
            _LOGGER.exception(err)
            pass

        default_value = DEFAULT_CONFIG_VALUES.get(pname, '')
        self.config_parameter[pname] = default_value

        error_msg = (f"{EVLOG_ERROR}iCloud3 Error > Invalid configuration parameter > "
                        f"{CRLF_DOT}Parameter .. - {pname}: {pvalue} {msg}"
                        f"{CRLF_DOT}Valid values - {valid_values}"
                        f"{CRLF_DOT}Resetting to - {default_value}")
        self._save_event_halog_error("*", error_msg)

#-------------------------------------------------------------------------
    def _set_data_fields_from_config_parameter_dictionary(self):
        '''
        Set the iCloud3 variables from the configuration parameters
        '''
        self.username                     = self.config_parameter[CONF_USERNAME]
        self.username_base                = self.username.split('@')[0]
        self.password                     = self.config_parameter[CONF_PASSWORD]
        self.group                        = self.config_parameter[CONF_GROUP]
        self.entity_registry_file         = self.config_parameter[CONF_ENTITY_REGISTRY_FILE]
        self.config_ic3_file_name         = self.config_parameter[CONF_CONFIG_IC3_FILE_NAME]
        self.event_log_card_directory     = self.config_parameter[CONF_EVENT_LOG_CARD_DIRECTORY]
        self.event_log_card_filename      = self.config_parameter[CONF_EVENT_LOG_CARD_FILENAME]
        self.config_devices_schema        = self.config_parameter[CONF_DEVICES]
        self.config_track_devices_parm    = self.config_parameter[CONF_TRACK_DEVICES]

        self.display_text_as              = self.config_parameter[CONF_DISPLAY_TEXT_AS]
        self.tracking_method_config       = self.config_parameter[CONF_TRACKING_METHOD]
        self.sensor_ids                   = self.config_parameter[CONF_CREATE_SENSORS]
        self.exclude_sensor_ids           = self.config_parameter[CONF_EXCLUDE_SENSORS]
        self.unit_of_measurement          = self.config_parameter[CONF_UNIT_OF_MEASUREMENT]
        self.time_format                  = self.config_parameter[CONF_TIME_FORMAT]
        self.display_zone_format          = self.config_parameter[CONF_DISPLAY_ZONE_FORMAT]
        self.center_in_zone_flag          = self.config_parameter[CONF_CENTER_IN_ZONE]
        self.max_interval_secs            = self._time_str_to_secs(self.config_parameter[CONF_MAX_INTERVAL])
        self.travel_time_factor           = self.config_parameter[CONF_TRAVEL_TIME_FACTOR]
        self.gps_accuracy_threshold       = self.config_parameter[CONF_GPS_ACCURACY_THRESHOLD]
        self.old_location_threshold       = self._time_str_to_secs(self.config_parameter[CONF_OLD_LOCATION_THRESHOLD])
        self.ignore_gps_accuracy_inzone_flag = self.config_parameter[CONF_IGNORE_GPS_ACC_INZONE]
        self.check_gps_accuracy_inzone_flag  = not self.ignore_gps_accuracy_inzone_flag
        self.hide_gps_coordinates         = self.config_parameter[CONF_HIDE_GPS_COORDINATES]
        self.distance_method_waze_flag    = (self.config_parameter[CONF_DISTANCE_METHOD].lower() == WAZE)
        self.legacy_mode_flag             = self.config_parameter[CONF_LEGACY_MODE]
        self.waze_region                  = self.config_parameter[CONF_WAZE_REGION]
        self.waze_max_distance            = self.config_parameter[CONF_WAZE_MAX_DISTANCE]
        self.waze_min_distance            = self.config_parameter[CONF_WAZE_MIN_DISTANCE]
        self.waze_realtime                = self.config_parameter[CONF_WAZE_REALTIME]
        self.stationary_still_time_str    = self.config_parameter[CONF_STATIONARY_STILL_TIME]
        self.stationary_zone_offset       = self.config_parameter[CONF_STATIONARY_ZONE_OFFSET]
        self.stationary_inzone_interval_str = self.config_parameter[CONF_STATIONARY_INZONE_INTERVAL]
        self.log_level                    = self.config_parameter[CONF_LOG_LEVEL]
        self.iosapp_request_loc_max_cnt   = self.config_parameter[CONF_IOSAPP_REQUEST_LOC_MAX_CNT]

        #update the interval time for each of the interval types (i.e., ipad: 2 hrs, noiosapp: 15 min)
        self.config_inzone_interval_secs = {}
        self.config_inzone_interval_secs[CONF_INZONE_INTERVAL] = \
                self._time_str_to_secs(self.config_parameter[CONF_INZONE_INTERVAL])
        try:
            for itype_itime in self.config_parameter[CONF_INZONE_INTERVALS]:
                for itype, itime in itype_itime.items():
                    self.config_inzone_interval_secs[itype] = self._time_str_to_secs(itime)
        except:
            pass

        if self.start_icloud3_inprocess_flag:
            event_msg = (f"inZone Intervals > ")
            for itype, itime in self.config_inzone_interval_secs.items():
                event_msg += (f"{itype}-{self._secs_to_time_str(itime)}, ")
            self._save_event("*", event_msg)

#########################################################
#
#   CHECK THE IC3 EVENT LOG VERSION BEING USED
#
#   Read the icloud3-event-log-card.js file in the iCloud3 directory and the
#   Lovelace Custom Card directory (default=www/custom_cards) and extract
#   the current version (Version=x.x.x (mm.dd.yyyy)) comment entry before
#   the first 'class' statement. If the version in the ic3 directory is
#   newer than the www/custom_cards directory, copy the ic3 version
#   to the www/custom_cards directory.
#
#   The custom_cards directory can be changed using the event_log_card_directory
#   parameter.
#
#########################################################
    def _check_ic3_event_log_file_version(self):
        try:
            ic3_directory = os.path.abspath(os.path.dirname(__file__))
            if instr(self.event_log_card_filename, '.js') is False:
                self.event_log_card_filename += '.js'
            ic3_evlog_filename = (f"{ic3_directory}/{self.event_log_card_filename}")

            if os.path.exists(ic3_evlog_filename) is False:
                return

            www_directory      = (f"{ic3_evlog_filename.split('custom_components')[0]}"
                                  f"{self.event_log_card_directory}")
            www_evlog_filename = (f"{www_directory}/{self.event_log_card_filename}")
            www_evlog_file_exists_flag = os.path.exists(www_evlog_filename)


        except Exception as err:
            _LOGGER.exception(err)

        try:
            ic3_version, ic3_beta_version, ic3_version_text = self._read_event_log_card_js_file(ic3_evlog_filename)
            if www_evlog_file_exists_flag:
                www_version, www_beta_version, www_version_text = self._read_event_log_card_js_file(www_evlog_filename)
            else:
                www_version      = 0
                www_beta_version = 0
                www_version_text = UNKNOWN
                try:
                    os.mkdir(www_directory)
                except FileExistsError:
                    pass
                except Exception as err:
                    _LOGGER.exception(err)
                    pass

            update_event_log_card_flag = False
            if ic3_version > www_version:
                update_event_log_card_flag = True
            elif ic3_version == www_version:
                if www_beta_version == 0:
                    pass
                elif (ic3_beta_version > www_beta_version
                        or ic3_beta_version == 0 and www_beta_version > 0):
                    update_event_log_card_flag = True

            if update_event_log_card_flag:
                shutil.copy(ic3_evlog_filename, www_evlog_filename)
                event_msg = (f"{EVLOG_NOTICE}"
                             f"Event Log Alert > Event Log was updated"
                             f"{CRLF_DOT}Old Version.. - v{www_version_text}"
                             f"{CRLF_DOT}New Version - v{ic3_version_text}"
                             f"{CRLF_DOT}Copied From - {ic3_directory}"
                             f"{CRLF_DOT}Copied To..... - {www_directory}"
                             f"CRLF{'-'*75}"
                             f"CRLFThe Event Log Card was updated to v{ic3_version_text}. "
                              "Refresh your browser and do the following on every tracked "
                              "devices running the iOS App to load the new version."
                              "CRLF1. Select HA Sidebar > APP Configuration."
                              "CRLF2. Scroll to the botton of the General screen."
                              "CRLF3. Select Reset Frontend Cache, then select Done."
                              "CRLF4. Display the Event Log, then pull down to refresh the page. "
                              "You should see the busy spinning wheel as the new version is loaded.")
                self._save_event_halog_info("*", event_msg)
                self.info_notification = (f"Event Log Card updated to v{ic3_version_text}. "
                              "See Event Log for more info.")
                title       = (f"iCloud3 Event Log Card updated to v{ic3_version_text}")
                message     = ("Refresh the iOS App to load the new version. "
                              "Select HA Sidebar > APP Configuration. Scroll down. Select Refresh "
                              "Frontend Cache. Select Done. Pull down to refresh App.")
                self.broadcast_msg = {
                            "title": title,
                            "message": message,
                            "data": {"subtitle": "Event Log needs to be refreshed"}}

            else:
                event_msg = (f"Event Log Version Check > Current release is being used. "
                             f"Version-{www_version_text}, {www_directory}")
                self._save_event_halog_info("*", event_msg)

        except Exception as err:
            _LOGGER.exception(err)
            return

#--------------------------------------
    def _read_event_log_card_js_file(self, evlog_filename):
        '''
        Read the records in the the evlog_filename up to the 'class' statement and
        extract the version and date.
        Return the Version number and the Version text (#.#.#b## (m/d/yyy))
        Return 0, 0, "Unknown" if the Version number was not found
        '''
        try:
            #Cycle thru the file looking for the Version
            evlog_version_text = UNKNOWN
            evlog_version_no   = 0
            evlog_file = open(evlog_filename)
            evlog_version_parts = [0, 0, 0, 0]

            for evlog_recd in evlog_file:
                if instr(evlog_recd.lower().replace(' ', ''), 'version='):
                    break

                #exit if find 'class' recd before 'version' recd
                elif instr(evlog_recd, "class"):
                    return (0, 0, UNKNOWN)

            evlog_recd   = evlog_recd.replace("("," (").replace("  "," ")
            version_text = evlog_recd.split("=")[1].replace('\n', '')
            version_date = version_text.split(' ')
            version_beta = (f"{version_date[0]}b0").split('b')

            version_parts = version_beta[0].split('.')
            beta_version = int(version_beta[1])

            version  = 0
            version += int(version_parts[0])*10000
            version += int(version_parts[1])*100
            version += int(version_parts[2])*1

        except FileNotFoundError:
            return (0, 0, UNKNOWN)

        except Exception as err:
            _LOGGER.exception(err)
            return (0, 0, 'Error')

        evlog_file.close()

        return (version, beta_version, version_text)

#########################################################
#
#   log_, trace_ MESSAGE ROUTINES
#
#########################################################
    def _log_info_msg(self, log_msg):
        ''' Always add log_msg to HA log '''
        if self.start_icloud3_inprocess_flag and not self.log_debug_flag:
            self.startup_log_msgs       += f"{self.startup_log_msgs_prefix}\n {log_msg}"
            self.startup_log_msgs_prefix = ""
        else:
            _LOGGER.info(log_msg)

#--------------------------------------
    def _save_event_halog_info(self, devicename, log_msg, log_title=""):
        ''' Always display log_msg in Event Log; Always add log_msg to HA log  '''

        self._save_event(devicename, log_msg)

        log_msg = str(log_msg).replace("CRLF", ". ")
        if devicename != "*":
            log_msg = (f"{log_title}{self._format_fname_devtype(devicename)} {log_msg}")

        if self.start_icloud3_inprocess_flag and not self.log_debug_flag:
            self.startup_log_msgs       += f"{self.startup_log_msgs_prefix}\n {log_msg}"
            self.startup_log_msgs_prefix = ""
        else:
            self._log_info_msg(log_msg)

#--------------------------------------
    def _save_event_halog_debug(self, devicename, log_msg, log_title=""):
        ''' Always display log_msg in Event Log; add to HA log only when "log_level: debug" '''
        self._save_event(devicename, f"{log_msg}")

        if devicename != "*":
            log_msg = (f"{log_title}{self._format_fname_devtype(devicename)} {log_msg}")
        self._log_debug_msg(devicename, log_msg)

#--------------------------------------
    def _evlog_debug_msg(self, devicename, log_msg, log_title=""):
        ''' Only display log_msg in Event Log and HA log when "log_level: eventlog" '''
        self._save_event(devicename, f"{EVLOG_DEBUG}{log_msg}")

        if self.log_eventlog_flag:
            if devicename != "*":
                log_msg = (f"{self._format_fname_devtype(devicename)} {log_msg}")
            self._log_debug_msg(devicename, log_msg, log_title)

#--------------------------------------
    @staticmethod
    def _log_warning_msg(log_msg):
        _LOGGER.warning(log_msg)

#--------------------------------------
    @staticmethod
    def _log_error_msg(log_msg):
        _LOGGER.error(log_msg)

#--------------------------------------
    def _save_event_halog_error(self, devicename, log_msg):
        ''' Always display log_msg in Event Log; always add to HA log '''
        if instr(log_msg, "iCloud3 Error"):
            self.info_notification = ICLOUD3_ERROR_MSG
            for td_devicename in self.tracked_devices:
                self._display_info_status_msg(td_devicename, ICLOUD3_ERROR_MSG)

        self._save_event(devicename, log_msg)
        log_msg = (f"{self._format_fname_devtype(devicename)} {log_msg}")
        log_msg = str(log_msg).replace("CRLF", ". ")

        if self.start_icloud3_inprocess_flag and not self.log_debug_flag:
            self.startup_log_msgs       += f"{self.startup_log_msgs_prefix}\n {log_msg}"
            self.startup_log_msgs_prefix = ""

        self._log_error_msg(log_msg)

#--------------------------------------
    def _log_debug_msg(self, devicename, log_msg, log_title=""):
        ''' Always add log_msg to HA log only when "log_level: debug" '''

        log_msg = str(log_msg).replace("CRLF", ". ")
        if self.log_debug_flag:
            _LOGGER.info(f"◆{devicename}--{log_title}◆{log_msg}")
        else:
            _LOGGER.debug(f"◆{devicename}--{log_title}◆{log_msg}")

#--------------------------------------
    def _log_debug_interval_msg(self, devicename, log_msg):
        ''' Add log_msg to HA log only when "log_level: intervalcalc" '''
        if self.log_intervalcalc_flag:
            _LOGGER.debug(f"◆{devicename}--{log_msg}")

            if self.log_eventlog_flag:
                self._save_event(devicename, (f"{EVLOG_DEBUG}{str(log_msg).replace('►','')}"))

#--------------------------------------
    def _log_rawdata(self, title, data, log_rawdata=False):
        ''' Add log_msg to HA log only when "log_level: rawdata" '''
        display_title = title.replace(" ",".").upper()

        if self.log_rawdata_flag or log_rawdata:
            _LOGGER.info(f"▼-----▼-----▼--{display_title}--▼-----▼-----▼")
            _LOGGER.info(f"{data}")
            _LOGGER.info("-"*75)
#--------------------------------------
    def _log_debug_msg2(self, log_msg):
            _LOGGER.debug(log_msg)

#--------------------------------------
    def _internal_error_msg(self, function_name, err_text: str='',
                section_name: str=''):
        log_msg = (f"►INTERNAL ERROR-RETRYING ({function_name}:{section_name}-{err_text})")
        _LOGGER.error(log_msg)
        self._save_event("*", log_msg)

        attrs = {}
        attrs[ATTR_INTERVAL]         = '0 sec'
        attrs[ATTR_NEXT_UPDATE_TIME] = TIMESTAMP_ZERO
        attrs[ATTR_INFO]             = log_msg

        return attrs

#########################################################
#
#   TIME & DISTANCE UTILITY ROUTINES
#
#########################################################
    @staticmethod
    def _time_now_secs():
        ''' Return the epoch seconds in utc time '''

        return int(time.time())

#--------------------------------------------------------------------
    def _secs_to_time(self, e_seconds):
        """ Convert seconds to hh:mm:ss """

        if e_seconds == 0 or e_seconds == HIGH_INTEGER:
            return HHMMSS_ZERO
        else:
            t_struct = time.localtime(e_seconds + self.e_seconds_local_offset_secs)
            return  time.strftime(self.um_time_strfmt, t_struct).lstrip('0')

#--------------------------------------------------------------------
    @staticmethod
    def _secs_to_time_str(secs):
        """ Create the time string from seconds """

        try:
            if secs >= 86400:
                time_str = self._secs_to_dhms_str(secs)
            elif secs < 60:
                time_str = str(round(secs, 0)) + " sec"
            elif secs < 3600:
                time_str = str(round(secs/60, 1)) + " min"
            elif secs == 3600:
                time_str = "1 hr"
            else:
                time_str = str(round(secs/3600, 1)) + " hrs"

            # xx.0 min/hr --> xx min/hr
            time_str = time_str.replace('.0 ', ' ')

        except:
            time_str = ""

        return time_str
#--------------------------------------------------------------------
    @staticmethod
    def _secs_to_dhms_str(secs):
        """ Create the time 0d0h0m0s time string from seconds """

        try:
            secs_dhms = float(secs)
            dhms_str = ""
            if (secs >= 86400): dhms_str += f"{secs_dhms // 86400}d"
            secs_dhms = secs_dhms % 86400
            if (secs >= 3600): dhms_str += f"{secs_dhms // 3600}h"
            secs_dhms %= 3600
            if (secs >= 60): dhms_str += f"{secs_dhms // 60}m"
            secs_dhms %= 60
            dhms_str += f"{secs_dhms}s"

            dhms_str = dhms_str.replace('.0', '')

        except:
            dhms_srt = ""

        return dhms_str

#--------------------------------------------------------------------
    def _secs_since(self, e_secs) -> int:
        return round(time.time() - e_secs)
#--------------------------------------------------------------------
    def _secs_to(self, e_secs) -> int:
        return round(e_secs - time.time())
#--------------------------------------------------------------------
    @staticmethod
    def _time_to_secs(hhmmss):
        """ Convert hh:mm:ss into seconds """
        try:
            hh_mm_ss = hhmmss.split(":")
            secs = int(hh_mm_ss[0]) * 3600 + int(hh_mm_ss[1]) * 60 + int(hh_mm_ss[2])

        except:
            secs = 0

        return secs

#--------------------------------------------------------------------
    def _time_to_12hrtime(self, hhmmss, ampm=False):
        '''
        Change hh:mm:ss time to a 12 hour time
        Input : hh:mm:ss where hh=(0-23)
              : hh:mm:ss (30s)
        Return: hh:mm:ss where hh=(0-11) with 'a' or 'p'
        '''

        try:
            if self.time_format == 12:
                hh_mm_ss    = hhmmss.split(':')
                hhmmss_hh   = int(hh_mm_ss[0])
                secs_suffix = hh_mm_ss[2].split('-')

                ap = 'a'
                if hhmmss_hh > 12:
                    hhmmss_hh -= 12
                    ap = 'p'
                elif hhmmss_hh == 12:
                    ap = 'p'
                elif hhmmss_hh == 0:
                    hhmmss_hh = 12

                ap = '' if ampm is False else ap

                hhmmss = f"{hhmmss_hh}:{hh_mm_ss[1]}:{secs_suffix[0]}{ap}"
                if len(secs_suffix) == 2:
                    hhmmss += f"-{secs_suffix[1]}"
        except:
             pass

        return hhmmss
#--------------------------------------------------------------------
    @staticmethod
    def _time_str_to_secs(time_str='30 min') -> int:
        """
        Calculate the seconds in the time string.
        The time attribute is in the form of '15 sec' ',
        '2 min', '60 min', etc
        """

        if time_str == "":
            return 0

        try:
            s1 = str(time_str).replace('_', ' ') + " min"
            time_part = float((s1.split(" ")[0]))
            text_part = s1.split(" ")[1]

            if text_part in ('sec', 'secs'):
                secs = time_part
            elif text_part in ('min', 'mins'):
                secs = time_part * 60
            elif text_part in ('hr', 'hrs'):
                secs = time_part * 3600
            else:
                secs = 1800      #default to 20 minutes

        except:
            secs = 1800

        return secs

#--------------------------------------------------------------------
    def _timestamp_to_time_utcsecs(self, utc_timestamp) -> int:
        """
        Convert iCloud timeStamp into the local time zone and
        return hh:mm:ss
        """

        ts_local = int(float(utc_timestamp)/1000) + self.time_zone_offset_seconds
        hhmmss   = dt_util.utc_from_timestamp(ts_local).strftime(self.um_time_strfmt)
        if hhmmss[0] == "0":
            hhmmss = hhmmss[1:]

        return hhmmss

#--------------------------------------------------------------------
    def _timestamp_to_time(self, timestamp):
        """
        Extract the time from the device timeStamp attribute
        updated by the IOS app.
        Format #1 is --'timestamp': '2019-02-02 12:12:38.358-0500'
        Format #2 is --'timestamp': '2019-02-02 12:12:38 (30s)'
        """

        try:
            #'000-00-00 00:00:00' --> '00:00:00'
            if timestamp == TIMESTAMP_ZERO:
                return HHMMSS_ZERO

            #'2019-02-02 12:12:38.358-0500' --> '12:12:38'
            elif instr(timestamp, '.'):
                return timestamp[11:19]

            #'2019-02-02 12:12:38 (30s)' --> '12:12:38 (30s)'
            elif instr(timestamp, '-'):
                return timestamp[11:]

            else:
                return timestamp

        except:
            pass

        return timestamp

#--------------------------------------------------------------------
    def _timestamp_to_secs_utc(self, utc_timestamp) -> int:
        """
        Convert timeStamp seconds (1567604461006) into the local time zone and
        return time in seconds.
        """

        try:
            ts_local = int(float(utc_timestamp)/1000) + self.time_zone_offset_seconds

            hhmmss = dt_util.utc_from_timestamp(ts_local).strftime('%X')
            if hhmmss[0] == "0":
                hhmmss = hhmmss[1:]

        except:
            hhmmss = 0

        return self._time_to_secs(hhmmss)

#--------------------------------------------------------------------
    @staticmethod
    def _secs_to_timestamp(secs):
        """
        Convert seconds to timestamp
        Return timestamp (2020-05-19 09:12:30)
        """

        try:
            time_struct = time.localtime(secs)
            timestamp   = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)

        except Exception as err:
            _LOGGER.exception(err)
            timestamp = "0000-00-00 00:00:00"

        return timestamp

#--------------------------------------------------------------------
    def _timestamp_to_secs(self, timestamp, utc_local = LOCAL_TIME) -> int:
        """
        Convert the timestamp from the device timestamp attribute
        updated by the IOS app.
        Format is --'timestamp': '2019-02-02T12:12:38.358-0500'
        Return epoch seconds
        """
        try:
            if timestamp is None:
                secs = 0
            elif timestamp == '' or timestamp[0:19] == TIMESTAMP_ZERO:
                secs = 0
            else:
                timestamp = timestamp.replace("T", " ")[0:19]
                secs = time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
                if utc_local is UTC_TIME:
                  secs += self.time_zone_offset_seconds

        except:
            secs = 0

        return secs
#--------------------------------------------------------------------
    def _calculate_time_zone_offset(self):
        """
        Calculate time zone offset seconds
        """
        try:
            local_zone_offset = dt_util.now().strftime('%z')
            local_zone_offset_secs = int(local_zone_offset[1:3])*3600 + \
                        int(local_zone_offset[3:])*60
            if local_zone_offset[:1] == "-":
                local_zone_offset_secs = -1*local_zone_offset_secs

            t_now    = int(time.time())
            t_hhmmss = dt_util.now().strftime('%H%M%S')
            l_now    = time.localtime(t_now)
            l_hhmmss = time.strftime('%H%M%S', l_now)
            g_now    = time.gmtime(t_now)
            g_hhmmss = time.strftime('%H%M%S', g_now)

            if (l_hhmmss == g_hhmmss):
                self.e_seconds_local_offset_secs = local_zone_offset_secs

            log_msg = (f"Time Zone Offset, Local Zone-{local_zone_offset} hrs, "
                       f"{local_zone_offset_secs} secs")
            self._log_debug_msg('*', log_msg)

        except Exception as err:
            _LOGGER.exception(err)
            x = self._internal_error_msg(fct_name, err, 'CalcTZOffset')
            local_zone_offset_secs = 0

        return local_zone_offset_secs

#--------------------------------------------------------------------
    def _km_to_mi(self, arg_distance):
        """
        convert km to miles
        """

        try:
            mi = arg_distance * self.um_km_mi_factor

            if mi == 0:
                mi = 0
            elif mi <= 10:
                mi = round(mi, 2)
            elif mi <= 100:
                mi = round(mi, 1)
            else:
                mi = round(mi)

        except:
            mi = 0
        return mi

    def _mi_to_km(self, arg_distance):
        return round(float(arg_distance) / self.um_km_mi_factor, 2)

#--------------------------------------------------------------------
    @staticmethod
    def _format_dist(dist):
        return f"{dist}km" if dist > .5 else f"{round(dist*1000)}m"

    @staticmethod
    def _format_dist_m(dist):
        return f"{round(dist/1000, 2)}km" if dist > 500 else f"{round(dist)}m"
#--------------------------------------------------------------------
    @staticmethod
    def _calc_distance_km(from_lat, from_long, to_lat, to_long):
        if from_lat is None or from_long is None or to_lat is None or to_long is None:
            return 0

        d = distance(from_lat, from_long, to_lat, to_long) / 1000
        if d < .05: d = 0
        return round(d, 2)

    @staticmethod
    def _calc_distance_m(from_lat, from_long, to_lat, to_long):
        if from_lat is None or from_long is None or to_lat is None or to_long is None:
            return 0

        d = distance(from_lat, from_long, to_lat, to_long)

        return round(d, 2)

#--------------------------------------------------------------------
    @staticmethod
    def _round_to_zero(arg_distance):
        if abs(arg_distance) < .05: arg_distance = 0
        return round(arg_distance, 2)

#--------------------------------------------------------------------
    def _add_comma_to_str(self, text):
        """ Add a comma to info if it is not an empty string """
        if text:
            return f"{text}, "
        return ''

#--------------------------------------------------------------------
    @staticmethod
    def _isnumber(string):

        try:
            test_number = float(string)

            return True
        except:
            return False

#--------------------------------------------------------------------
    def _extract_name_device_type(self, devicename):
        '''Extract the name and device type from the devicename'''

        try:
            fname       = devicename.lower()
            device_type = ""
            for ic3dev_type in APPLE_DEVICE_TYPES:
                if devicename == ic3dev_type:
                    return (devicename, devicename)

                elif instr(devicename, ic3dev_type):
                    fnamew = devicename.replace(ic3dev_type, "")
                    fname  = fnamew.replace("_", "").replace("-", "").title().strip()
                    device_type = DEVICE_TYPE_FNAME.get(ic3dev_type, ic3dev_type)
                    break

            if device_type == "":
                fname  = fname.replace("_", "").replace("-", "").title().strip()

        except Exception as err:
            _LOGGER.exception(err)

        return (fname, device_type)

#--------------------------------------------------------------------
    def _device_online(self, devicename):
        ''' Returns True/False if the device is online based on the device_status '''
        if self.TRK_METHOD_IOSAPP:
            return True
        else:
            return (self.device_status.get(devicename) in DEVICE_STATUS_ONLINE)

#--------------------------------------------------------------------
    def _device_offline(self, devicename):
        ''' Returns True/False if the device is offline based on the device_status '''
        return not self._device_online(devicename)

#--------------------------------------------------------------------
    def _devicename_fmf(self, devicename):
        return (self.devicename_tracking_method.get(devicename) == FMF)

    def _devicename_famshr(self, devicename):
        return (self.devicename_tracking_method.get(devicename) == FAMSHR)

#########################################################
#
#   These functions handle notification and entry of the
#   iCloud Account trusted device verification code.
#
#########################################################
    def _icloud_2fa1_show_verification_code_entry_form(self, invalid_code_msg=""):

        """Return the verification code."""

        self._icloud3_update_service_handler(self.group, arg_command='pause')

        configurator = self.hass.components.configurator
        if self.username in self.hass_configurator_request_id:
            request_id   = self.hass_configurator_request_id.pop(self.username)
            configurator = self.hass.components.configurator
            configurator.request_done(request_id)
            self._save_event("*", f"2fa1.10 Completed HA Notification Window Release (id-{request_id})")

        self._save_event("*", f"2fa1.1 Requesting New HA Notification Window")
        self.hass_configurator_request_id[self.username] = \
            configurator.request_config(
                ("Apple ID Verification Code"),
                self._icloud_2fa2_handle_verification_code_entry,
                description    = (f"{invalid_code_msg}Enter the Apple ID Verification Code sent to the Trusted Device"),
                entity_picture = "/static/images/config_icloud.png",
                submit_caption = 'Confirm',
                fields         = [{'id': 'code', CONF_NAME: 'Verification Code'}]
        )
        self._save_event("*", f"2fa1.2 Completed New HA Notification Window Request")

#--------------------------------------------------------------------
    def _icloud_2fa2_handle_verification_code_entry(self, callback_data):
        """Handle the chosen trusted device."""

        self._save_event("*", f"2fa2.err0 Validating pyicloud-ic3 iCloud API")
        if self._icloud_valid_api() is False:
            self._save_event("*", f"2fa2.err1 Error, iCloud API not set up")
            return

        from .pyicloud_ic3 import PyiCloudException

        self.verification_code = callback_data.get('code')
        event_msg = (f"Submit Apple ID Verification Code > Code-{callback_data}")
        self._save_event("*", event_msg)

        try:
            invalid_code_text = ''
            self._save_event("*", f"2fa2.1 Sending Verification Code {self.verification_code} to iCloud for Verification")
            valid_code = self.api.validate_2fa_code(self.verification_code)
            self._save_event("*", f"2fa2.2 Recieved Response, Valid Code-{valid_code}")
            if valid_code is False:
                invalid_code_text = (f"The code {self.verification_code} in incorrect.\n\n")
                self._save_event("*", f"2fa2.3 Invalid Code, Redisplay Code Entry Window")
                self._icloud_2fa1_show_verification_code_entry_form(
                            invalid_code_msg=invalid_code_text)
                self._save_event("*", f"2fa2.4 Invalid Code, Completed Code Entry Window Redisplay")
                return

            event_msg = "Apple/iCloud Account Verification Successful"
            self._save_event("*", event_msg)

        except PyiCloudException as error:
            # Reset to the initial 2FA state to allow the user to retry
            invalid_code_msg = (f"Failed to verify account > Error-{error}")
            self._save_event("*", f"2fa2.5 Other Error, Redisplay Code Entry Window")
            self._save_event_halog_error("*", invalid_code_msg)

            # Trigger the code rentry step immediately
            invalid_code_text = (f"The code {self.verification_code} in incorrect.\n\n")
            self._icloud_2fa1_show_verification_code_entry_form(
                            invalid_code_msg=invalid_code_text)
            self._save_event("*", f"2fa2.6 Other Error, Completed Code Entry Window Redisplay")
            return

        if valid_code is False:
                invalid_code_text = (f"The Verification Code {self.verification_code} in incorrect.\n\n")
                self._save_event("*", f"2fa2.7 Invalid Code, Redisplay Code Entry Window")
                self._icloud_2fa1_show_verification_code_entry_form(
                            invalid_code_msg=invalid_code_text)
                self._save_event("*", f"2fa2.8 Other Error, Completed Code Entry Window Redisplay")
                return

        if self.username in self.hass_configurator_request_id:
            request_id   = self.hass_configurator_request_id.pop(self.username)
            configurator = self.hass.components.configurator
            configurator.request_done(request_id)
            self._save_event("*", f"2fa2.10 Completed HA Notification Window Release (id-{request_id})")

        self._setup_tracking_method(self.tracking_method_config)
        event_msg = (f"{EVLOG_ALERT}iCloud Alert > iCloud Account Verification completed")
        self._save_event("*", event_msg)
        self._start_icloud3()

#--------------------------------------------------------------------
    def _icloud_valid_api(self):
        '''
        Make sure the pyicloud_ic3 api is valid
        '''

        if self.api == None:
            event_msg = (f"{EVLOG_ERROR}iCloud3 Error > There was an error logging into the "
                         f"Apple/iCloud Account when iCloud3 was started. Verification can not "
                         f"be completed. Review the iCloud3 Event Log for more information.")
            self._save_event_halog_error('*', event_msg)
            return False
        return True

#########################################################
#
#   ICLOUD ROUTINES
#
#########################################################
    def _icloud3_find_iphone_alert_service_handlert(self, group, devicename):
        """
        Call the lost iPhone function if using th e FamShr tracking method.
        Otherwise, send a notification to the iOS App
        """

        #if self.TRK_METHOD_FAMSHR:
        if self._devicename_famshr(devicename):
            device_id = self.devicename_device_id.get(devicename, None)
            if device_id and self.api:
                self.api.play_sound(device_id)

                self._save_event(devicename, "iCloud Find My iPhone Alert sent")
                return
            else:
                event_msg = ("iCloud Device not available, the alert will be "
                             "sent to the iOS App")
                self._save_event(devicename, event_msg)

        message =   {"message": "Find My iPhone Alert",
                        "data": {
                            "push": {
                                "sound": {
                                "name": "alarm.caf",
                                "critical": 1,
                                "volume": 1
                                }
                            }
                        }
                    }
        self._send_message_to_device(devicename, message)

#--------------------------------------------------------------------
    def _icloud3_update_service_handler(self, group, arg_devicename=None,
                    arg_command=None):
        """
        Authenticate against iCloud and scan for devices.


        Commands:
        - waze reset range = reset the min-max rnge to defaults (1-1000)
        - waze toggle      = toggle waze on or off
        - pause            = stop polling for the devicename or all devices
        - resume           = resume polling devicename or all devices, reset
                             the interval override to normal interval
                             calculations
        - pause-resume     = same as above but toggles between pause and resume
        - zone xxxx        = updates the devie state to xxxx and updates all
                             of the iloud3 attributes. This does the see
                             service call and then an update.
        - reset            = reset everything and rescans all of the devices
        - debug interval   = displays the interval formula being used
        - debug gps        = simulates bad gps accuracy
        - debug old        = simulates that the location informaiton is old
        - info xxx         = the same as 'debug'
        - location         = request location update from ios app
        """

        #If several iCloud groups are used, this will be called for each
        #one. Exit if this instance of iCloud is not the one handling this
        #device. But if devicename = 'reset', it is an event_log service cmd.
        log_msg = (f"iCLOUD3 COMMAND, Device: `{arg_devicename}`, Command: `{arg_command}`")
        self._log_debug_msg("*", log_msg)

        self._evlog_debug_msg(arg_devicename, (f"Service Call Command Received > `{arg_command}`"))

        arg_command         = (f"{arg_command} ")
        arg_command_cmd     = arg_command.split(' ')[0].lower()
        arg_command_parm    = arg_command.split(' ')[1]       #original value
        arg_command_parmlow = arg_command_parm.lower()
        log_level_msg       = ""
        msg_devicename = arg_devicename if arg_devicename else "All"
        log_msg = (f"iCloud3 Command Processed > Device-{msg_devicename}, Command-{arg_command}")

        #System level commands
        if arg_command_cmd == 'restart':
            #preserve debug & rawdata across restarts
            self.log_debug_flag_restart   = self.log_debug_flag
            self.log_rawdata_flag_restart = self.log_rawdata_flag

            self._start_icloud3()

            return

            if self.tracked_devices == []:
                self._start_icloud3()
            elif self.start_icloud3_inprocess_flag is False:
                self.start_icloud3_request_flag = True
            self._save_event_halog_info("*", log_msg)
            return

        elif arg_command_cmd == 'export_event_log':
            self._save_event("*", log_msg)
            self._export_ic3_event_log()
            self._update_sensor_ic3_event_log(arg_devicename)
            return

        elif arg_command_cmd == 'refresh_event_log':
            self.last_iosapp_msg[arg_devicename] = ""
            self._update_sensor_ic3_event_log(arg_devicename)
            return

        elif arg_command_cmd == 'startuplog':
            self._update_sensor_ic3_event_log("*")
            return

        elif arg_command_cmd == "counts":
            for devicename in self.count_update_iosapp:
                self._display_usage_counts(devicename, force_display=True)
            return

        elif arg_command_cmd == 'trusted_device':
            self._icloud_2fa1_show_verification_code_entry_form()
            return

        elif arg_command_cmd == 'reset_session':
            self._pyicloud_reset_session()
            return

        elif arg_command_cmd == 'event_log':
            error_msg = ("Error > Event Log v1.0 is being used. You may need to clear your "
                         "browser cache and then refresh the Event Log page in your browser several times. "
                         "The latest Event Log version has [Refresh] [Actions] buttons at the top of the screen. "
                         "You may also need to clear the iOS App cache on each device. Select "
                         "HA Sidebar>App Configuration, then scroll down, select Reset Frontend Cache and "
                         "refresh your device by swiping down from the top of the screen.")
            self._save_event("*", error_msg)

            self.last_iosapp_msg[arg_devicename] = ""
            self._update_sensor_ic3_event_log(arg_devicename)
            return

        #command preprocessor, reformat specific commands
        elif instr(arg_command_cmd, 'log_level'):
            if instr(arg_command_parm, 'debug'):
                self.log_debug_flag = (not self.log_debug_flag)

            if instr(arg_command_parm, 'rawdata'):
                self.log_rawdata_flag = (not self.log_rawdata_flag)
                #if self.log_rawdata_flag: self.log_debug_flag = True
                if self.log_rawdata_flag:
                    self.log_rawdata_flag_restart = True
                    self._start_icloud3()

            if instr(arg_command_parm, 'intervalcalc'):
                self.log_intervalcalc_flag = (not self.log_intervalcalc_flag)

            if instr(arg_command_parm, 'eventlog'):
                self.log_eventlog_flag = (not self.log_eventlog_flag)

            event_msg = ""
            if self.log_eventlog_flag:     event_msg += "Event Log Details: On, "
            if self.log_debug_flag:        event_msg += "Debug: On, "
            if self.log_rawdata_flag:      event_msg += "Rawdata: On, "
            if self.log_intervalcalc_flag: event_msg += "IntervalCalc: On, "
            event_msg = "Logging: Off" if event_msg == "" else event_msg
            event_msg = (f"Log Level State > {event_msg}")
            self._save_event_halog_debug("*", event_msg)

            self._update_sensor_ic3_event_log(arg_devicename)

            return

        self._save_event_halog_info("*", log_msg)

        #Location level commands
        if arg_command_cmd == WAZE:
            if self.waze_status == WAZE_NOT_USED:
                arg_command_cmd = ''
                return
            elif arg_command_parmlow == 'reset_range':
                self.waze_min_distance = 0
                self.waze_max_distance = HIGH_INTEGER
                self.waze_manual_pause_flag = False
                self.waze_status = WAZE_USED
            elif arg_command_parmlow == 'toggle':
                if self.waze_status == WAZE_PAUSED:
                    self.waze_manual_pause_flag = False
                    self.waze_status = WAZE_USED
                else:
                    self.waze_manual_pause_flag = True
                    self.waze_status = WAZE_PAUSED
            elif arg_command_parmlow == 'pause':
                self.waze_manual_pause_flag = False
                self.waze_status = WAZE_USED
            elif arg_command_parmlow != 'pause':
                self.waze_manual_pause_flag = True
                self.waze_status = WAZE_PAUSED

        elif arg_command_cmd == CONF_ZONE:     #parmeter is the new zone
            #if HOME in arg_command_parmlow:    #home/not_home is lower case
            if self.base_zone in arg_command_parmlow:    #home/not_home is lower case
                arg_command_parm = arg_command_parmlow

            kwargs = {}
            attrs  = {}

            self._wait_if_update_in_process(arg_devicename)
            self.override_interval_seconds[arg_devicename] = 0
            self.update_in_process_flag = False
            self._initialize_next_update_time(arg_devicename)

            self._update_device_icloud('Command', arg_devicename)

            return

        #Device level commands
        device_time_adj = 0
        for devicename in self.tracked_devices:
            if arg_devicename and devicename != arg_devicename:
                continue

            device_time_adj += 3
            devicename_zone = self._format_devicename_zone(devicename, HOME)

            now_secs_str = dt_util.now().strftime('%X')
            now_seconds  = self._time_to_secs(now_secs_str)
            x, update_in_secs = divmod(now_seconds, 15)
            update_in_secs = 15 - update_in_secs + device_time_adj

            attrs = {}

            #command processor, execute the entered command
            info_msg = None
            if arg_command_cmd == 'pause':
                cmd_type = CMD_PAUSE
                self._pause_device(devicename)

            elif arg_command_cmd == 'resume':
                cmd_type = CMD_RESUME
                self.next_update_time[devicename_zone]        = HHMMSS_ZERO
                self.next_update_secs[devicename_zone]        = 0
                self.override_interval_seconds[devicename]    = 0
                self.poor_location_gps_cnt[devicename]        = 0
                self.poor_location_gps_msg[devicename]        = False
                self.poor_gps_flag[devicename]                = False
                self.iosapp_request_loc_retry_cnt[devicename] = 0
                self.iosapp_request_loc_retry_cnt[devicename] = 0
                self.iosapp_request_loc_sent_secs[devicename] = 0
                self.iosapp_request_loc_sent_flag[devicename] = False
                self.icloud_acct_auth_error_cnt               = 0

                self._display_info_status_msg(devicename, 'RESUMING')
                self._update_device_icloud('Resuming', devicename)

            elif arg_command_cmd == WAZE:
                cmd_type = CMD_WAZE
                if self.waze_status == WAZE_USED:
                    self.next_update_time[devicename_zone] = HHMMSS_ZERO
                    self.next_update_secs[devicename_zone] = 0
                    attrs[ATTR_NEXT_UPDATE_TIME]           = TIMESTAMP_ZERO
                    attrs[ATTR_WAZE_DISTANCE]              = 'Resuming'
                    self.override_interval_seconds[devicename] = 0
                    self._update_device_sensors(devicename, attrs)
                    attrs = {}

                    self._update_device_icloud('Resuming', devicename)
                else:
                    attrs[ATTR_WAZE_DISTANCE] = PAUSED
                    attrs[ATTR_WAZE_TIME]     = 0

            elif arg_command_cmd == 'location':
                cmd_type = CMD_LOCATION
                self._display_info_status_msg(devicename, 'locating')
                if self.iosapp_monitor_dev_trk_flag.get(devicename):
                    self._iosapp_request_loc_update(devicename)
                else:
                    self.next_update_time[devicename_zone]    = HHMMSS_ZERO
                    self.next_update_secs[devicename_zone]    = 0
                    self.override_interval_seconds[devicename] = 0
                    self._update_device_icloud('Locating', devicename)
                self._update_sensor_ic3_event_log(devicename)

            else:
                cmd_type = CMD_ERROR
                info_msg = (f"INVALID COMMAND > {arg_command_cmd}")
                self._display_info_status_msg(devicename, info_msg)

            if attrs:
                self._update_device_sensors(devicename, attrs)

        #end for devicename in devs loop

#--------------------------------------------------------------------
    def _icloud3_setinterval_service_handlerl(self, group, arg_interval=None,
                    arg_devicename=None):

        """
        Set the interval or process the action command of the given devices.
            'interval' has the following options:
                - 15               = 15 minutes
                - 15 min           = 15 minutes
                - 15 sec           = 15 seconds
                - 5 hrs            = 5 hours
                - Pause            = Pause polling for all devices
                                     (or specific device if devicename
                                      is specified)
                - Resume            = Resume polling for all devices
                                     (or specific device if devicename
                                      is specified)
                - Waze              = Toggle Waze on/off
        """
        #If several iCloud groups are used, this will be called for each
        #one. Exit if this instance of iCloud is not the one handling this
        #device.

        if arg_devicename and self.TRK_METHOD_IOSAPP:
            if self.iosapp_request_loc_cnt.get(arg_devicename) > self.iosapp_request_loc_max_cnt:
                event_msg = (f"Can not Set Interval, location request cnt "
                             f"exceeded ({self.iosapp_request_location_cnt.get(arg_devicename)} "
                             f"of {self.iosapp_request_loc_max_cnt})")
                self._save_event(arg_devicename, event_msg)
                return

        if arg_interval is None:
            #if arg_devicename is not None:
            if arg_devicename:
                self._save_event(arg_devicename, "Set Interval Command Error, "
                        "no new interval specified")
            return

        cmd_type = CMD_INTERVAL
        new_interval = arg_interval.lower().replace('_', ' ')

#       loop through all devices being tracked and
#       update the attributes. Set various flags if pausing or resuming
#       that will be processed by the next poll in '_polling_loop_15_sec_icloud'
        device_time_adj = 0
        for devicename in self.tracked_devices:
            if arg_devicename and devicename != arg_devicename:
                continue

            device_time_adj += 3
            devicename_zone = self._format_devicename_zone(devicename, HOME)

            self._wait_if_update_in_process()

            log_msg = (f"SET INTERVAL COMMAND Start {devicename}, "
                f"ArgDevname-{arg_devicename}, ArgInterval-{arg_interval}, "
                f"New Interval-{new_interval}")
            self._log_debug_msg(devicename, log_msg)
            self._save_event(devicename,
                    (f"Set Interval Command handled, New interval {arg_interval}"))

            self.next_update_time[devicename_zone] = HHMMSS_ZERO
            self.next_update_secs[devicename_zone] = 0
            self.interval_str[devicename_zone]        = new_interval
            self.override_interval_seconds[devicename] = self._time_str_to_secs(new_interval)

            now_seconds = self._time_to_secs(dt_util.now().strftime('%X'))
            x, update_in_secs = divmod(now_seconds, 15)
            time_suffix = 15 - update_in_secs + device_time_adj

            info_msg = 'Updating'
            self._display_info_status_msg(devicename, info_msg)

            log_msg = (f"SET INTERVAL COMMAND END {devicename}")
            self._log_debug_msg(devicename, log_msg)

#--------------------------------------------------------------------
