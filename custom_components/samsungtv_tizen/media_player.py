"""Support for interface with an Samsung TV."""
import asyncio
from datetime import timedelta, datetime
import logging
import socket
import json
import voluptuous as vol
import os
import wakeonlan
import websocket
import requests
import time
import numpy as np

from .websockets import SamsungTVWS
from . import exceptions

from .smartthings import smartthingstv as smartthings

from .upnp import upnp

from homeassistant import util
try:
    from homeassistant.components.media_player import MediaPlayerEntity, PLATFORM_SCHEMA, DEVICE_CLASS_TV
except ImportError:
    from homeassistant.components.media_player import MediaPlayerDevice as MediaPlayerEntity, PLATFORM_SCHEMA, DEVICE_CLASS_TV

from homeassistant.components.media_player.const import (
    MEDIA_TYPE_CHANNEL,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
    SUPPORT_VOLUME_SET,
    MEDIA_TYPE_APP,
    MEDIA_TYPE_URL,
)

from homeassistant.const import (
    CONF_BROADCAST_ADDRESS,
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
    CONF_API_KEY,
    CONF_DEVICE_ID,
    STATE_OFF,
    STATE_ON,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

CONF_SHOW_CHANNEL_NR = "show_channel_number"

DEFAULT_NAME = "Samsung TV Remote"
DEFAULT_PORT = 8002
DEFAULT_TIMEOUT = 3
DEFAULT_KEY_CHAIN_DELAY = 1.25
DEFAULT_UPDATE_METHOD = "ping"
DEFAULT_SOURCE_LIST = '{"TV": "KEY_TV", "HDMI": "KEY_HDMI"}'
CONF_UPDATE_METHOD = "update_method"
CONF_UPDATE_CUSTOM_PING_URL = "update_custom_ping_url"
CONF_SOURCE_LIST = "source_list"
CONF_APP_LIST = "app_list"
CONF_CHANNEL_LIST = "channel_list"
CONF_SCAN_APP_HTTP = "scan_app_http"
CONF_IS_FRAME_TV = "is_frame_tv"
CONF_SHOW_LOGOS = "show_logos"

KNOWN_DEVICES_KEY = "samsungtv_known_devices"
MEDIA_TYPE_KEY = "send_key"
MEDIA_TYPE_BROWSER = "browser"

SCAN_INTERVAL = timedelta(seconds=15)

MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(milliseconds=100)
MIN_TIME_BETWEEN_SCANS = SCAN_INTERVAL

KEYHOLD_MAX_DELAY = 5.0
KEY_PRESS_TIMEOUT = 0.5
UPDATE_PING_TIMEOUT = 1.0
UPDATE_STATUS_DELAY = 1
UPDATE_SOURCE_INTERVAL = 5
WS_CONN_TIMEOUT = 10
POWER_OFF_DELAY = timedelta(seconds=20)

SUPPORT_SAMSUNGTV = (
    SUPPORT_PAUSE
    | SUPPORT_VOLUME_STEP
    | SUPPORT_VOLUME_MUTE
    | SUPPORT_VOLUME_SET
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_NEXT_TRACK
    | SUPPORT_TURN_OFF
    | SUPPORT_PLAY
    | SUPPORT_PLAY_MEDIA
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_MAC): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_UPDATE_METHOD, default=DEFAULT_UPDATE_METHOD): cv.string,
        vol.Optional(CONF_UPDATE_CUSTOM_PING_URL): cv.string,
        vol.Optional(CONF_SOURCE_LIST, default=DEFAULT_SOURCE_LIST): cv.string,
        vol.Optional(CONF_APP_LIST): cv.string,
        vol.Optional(CONF_CHANNEL_LIST): cv.string,
        vol.Optional(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_API_KEY): cv.string,
        vol.Optional(CONF_SHOW_CHANNEL_NR, default=False): cv.boolean,
        vol.Optional(CONF_BROADCAST_ADDRESS): cv.string,
        vol.Optional(CONF_SCAN_APP_HTTP, default=True): cv.boolean,
        vol.Optional(CONF_IS_FRAME_TV, default=False): cv.boolean,
        vol.Optional(CONF_SHOW_LOGOS, default="white-color"): cv.string
    }
)

MEDIA_IMAGE_OPTIONS = {'none': 'none', 'blue-color': '05a9f4-color', 'blue-white': '05a9f4-white', 'dark-white': '282c34-white', 'darkblue-white': '212c39-white', 'white-color': 'fff-color', 'transparent-color': 'transparent-color', 'transparent-white': 'transparent-white'}
MEDIA_FILE_IMAGE_TO_PATH = os.path.dirname(os.path.realpath(__file__)) + '/logo_paths.json'
MEDIA_IMAGE_MIN_SCORE_REQUIRED = 80
MEDIA_TITLE_KEYWORD_REMOVAL = ['HD']

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Samsung TV platform."""
    known_devices = hass.data.get(KNOWN_DEVICES_KEY)
    if known_devices is None:
        known_devices = set()
        hass.data[KNOWN_DEVICES_KEY] = known_devices

    uuid = None

    # Is this a manual configuration?
    if config.get(CONF_HOST) is not None:
        host = config.get(CONF_HOST)
        port = config.get(CONF_PORT)
        name = config.get(CONF_NAME)
        mac = config.get(CONF_MAC)
        broadcast = config.get(CONF_BROADCAST_ADDRESS)
        timeout = config.get(CONF_TIMEOUT)
        update_method = config.get(CONF_UPDATE_METHOD)
        update_custom_ping_url = config.get(CONF_UPDATE_CUSTOM_PING_URL)
        source_list = config.get(CONF_SOURCE_LIST)
        app_list = config.get(CONF_APP_LIST)
        channel_list = config.get(CONF_CHANNEL_LIST)
        api_key = config.get(CONF_API_KEY)
        device_id = config.get(CONF_DEVICE_ID)
        show_channel_number = config.get(CONF_SHOW_CHANNEL_NR)
        scan_app_http = config.get(CONF_SCAN_APP_HTTP)
        is_frame_tv = config.get(CONF_IS_FRAME_TV)
        show_logos = config.get(CONF_SHOW_LOGOS)
    elif discovery_info is not None:
        tv_name = discovery_info.get("name")
        model = discovery_info.get("model_name")
        host = discovery_info.get("host")
        name = f"{tv_name} ({model})"
        port = DEFAULT_PORT
        timeout = DEFAULT_TIMEOUT
        update_method = DEFAULT_UPDATE_METHOD
        update_custom_ping_url = None
        source_list = DEFAULT_SOURCE_LIST
        app_list = None
        mac = None
        udn = discovery_info.get("udn")
        if udn and udn.startswith("uuid:"):
            uuid = udn[len("uuid:") :]
    else:
        _LOGGER.warning("Cannot determine device")
        return

    # Only add a device once, so discovered devices do not override manual
    # config.
    ip_addr = socket.gethostbyname(host)
    if ip_addr not in known_devices:
        known_devices.add(ip_addr)
        add_entities([SamsungTVDevice(host, port, name, timeout, mac, uuid, update_method, update_custom_ping_url, source_list, app_list, channel_list, api_key, device_id, show_channel_number, broadcast, scan_app_http, is_frame_tv, show_logos)])
        _LOGGER.info("Samsung TV %s:%d added as '%s'", host, port, name)
    else:
        _LOGGER.info("Ignoring duplicate Samsung TV %s:%d", host, port)


class SamsungTVDevice(MediaPlayerEntity):
    """Representation of a Samsung TV."""

    def __init__(self, host, port, name, timeout, mac, uuid, update_method, update_custom_ping_url, source_list, app_list, channel_list, api_key, device_id, show_channel_number, broadcast, scan_app_http, is_frame_tv, show_logos):
        """Initialize the Samsung device."""

        # Save a reference to the imported classes
        self._host = host
        self._name = name
        self._api_key = api_key
        self._device_id = device_id
        self._show_channel_number = show_channel_number
        self._timeout = timeout
        self._mac = mac
        self._update_method = update_method
        self._update_custom_ping_url = update_custom_ping_url
        self._broadcast = broadcast
        self._scan_app_http = scan_app_http
        self._is_frame_tv = is_frame_tv
        
        self._source = None
        self._source_list = json.loads(source_list)
        
        self._running_app = None
        if app_list is not None:
           self._auto_gen_installed_app_list = False
           dlist = self._split_app_list(json.loads(app_list), "/")
           self._app_list = dlist["app"]
           self._app_list_ST = dlist["appST"]
        else:
           self._auto_gen_installed_app_list = True
           self._app_list = None
           self._app_list_ST = None

        self._channel = None
        if channel_list is not None:
            self._channel_list = json.loads(channel_list)
        else:
            self._channel_list = None
        
        self._uuid = uuid
        self._is_ws_connection = True if port in (8001, 8002) else False
        # Assume that the TV is not muted and volume is 0
        self._muted = False
        self._volume = 0
        # Assume that the TV is in Play mode
        self._playing = True
        self._state = None
        # Mark the end of a shutdown command (need to wait 15 seconds before
        # sending the next command to avoid turning the TV back ON).
        self._end_of_power_off = None
        self._token_file = None
        
        self._last_command_time = datetime.now()
        self._last_source_time = None

        # Generate token file only for WS + SSL + Token connection
        if port == 8002:
            self._gen_token_file()

        self._ws = SamsungTVWS(
            name=name,
            host=host,
            port=port,
            timeout=self._timeout,
            key_press_delay=KEY_PRESS_TIMEOUT,
            token_file=self._token_file,
            app_list=self._app_list
        )

        self._upnp = upnp(
            host=host
        )

        self._media_title = None
        self._media_image_url = None
        self._media_image_base_url = None

        if show_logos in MEDIA_IMAGE_OPTIONS:
            if MEDIA_IMAGE_OPTIONS[show_logos] == "none":
                self._media_image_base_url = None
            else:
                self._media_image_base_url = "https://jaruba.github.io/channel-logos/export/{}".format(MEDIA_IMAGE_OPTIONS[show_logos])
        else:
            _LOGGER.warning("Unrecognized value '%s' for 'show_logos' option (%s). Using default value.",show_logos,self._name)
            self._media_image_base_url = "https://jaruba.github.io/channel-logos/export/fff-color"

    def _split_app_list(self, app_list, sep = "/"):
        retval = {"app": {}, "appST": {}}
        
        for attr, value in app_list.items():
            value_split = value.split(sep, 1)
            idx = 1 if len(value_split) > 1 else 0
            retval["app"].update({attr: value_split[0]})
            retval["appST"].update({attr: value_split[idx]})
            
        return retval

    def _gen_token_file(self):
        self._token_file = os.path.dirname(os.path.realpath(__file__)) + '/token-' + self._host + '.txt'

        if os.path.isfile(self._token_file) is False:
            # For correct auth
            self._timeout = 45

            # Create token file for catch possible errors
            try:
                handle = open(self._token_file, "w+")
                handle.close()
            except:
                _LOGGER.error("Samsung TV - Error creating token file: %s", self._token_file)

    def _power_off_in_progress(self):
        return (
            self._end_of_power_off is not None
            and self._end_of_power_off > dt_util.utcnow()
        )

    def _ping_device(self):
        _LOGGER.debug("Updating SamsungTV %s, With Method: %s", self._name,self._update_method)
        # Smartthings Update
        if self._update_method == "smartthings" and self._api_key and self._device_id:
            if hasattr(self, '_cloud_state'):
                self._state = self._cloud_state
            else:
                self._state = STATE_OFF
        # HTTP ping
        elif self._is_ws_connection and self._update_method == "ping":
            try:
                ping_url = "http://{}:8001/api/v2/".format(self._host)
                if self._update_custom_ping_url is not None:
                    ping_url = self._update_custom_ping_url
                requests.get(ping_url,timeout=UPDATE_PING_TIMEOUT)
                self._state = STATE_ON
                tmp_muted=self._upnp.get_mute()
                if tmp_muted is not None:
                    self._muted = tmp_muted
                tmp_vol=self._upnp.get_volume()
                if tmp_vol is not None:
                    self._volume = int(self._upnp.get_volume()) / 100
                if self._app_list is None:
                    self.hass.async_create_task(self._gen_installed_app_list())
            except:
                self._state = STATE_OFF
        # WS ping
        elif self._is_ws_connection and self._update_method == "websockets":
            if self.send_command("KEY", "send_key", 1, 0,bForceUpdate=False):
                tmp_muted=self._upnp.get_mute()
                if tmp_muted is not None:
                    self._muted = tmp_muted
                tmp_vol=self._upnp.get_volume()
                if tmp_vol is not None:
                    self._volume = int(self._upnp.get_volume()) / 100
                if self._app_list is None:
                    self.hass.async_create_task(self._gen_installed_app_list())
            else:
                _LOGGER.debug("SamsungTV %s, Update Error, assuming state: %s", self._name, self._state)
        else:
         _LOGGER.error("SamsungTV %s, Unknown Update Method: %s", self._name,self._update_method)

    def _get_running_app(self):
        if self._app_list is not None:
            if hasattr(self, '_cloud_state') and self._cloud_channel_name != "":
                for attr, value in self._app_list_ST.items():
                    if value == self._cloud_channel_name:
                        self._running_app = attr
                        return
            if self._scan_app_http:
                for app in self._app_list:
                    r = None
                    try:
                        r = requests.get('http://{host}:8001/api/v2/applications/{value}'.format(host=self._host, value=self._app_list[app]), timeout=0.5)
                    except requests.exceptions.RequestException as e:
                        pass
                    try:
                      if r is not None:
                          data = r.text
                          if data is not None:
                              root = json.loads(data.encode('UTF-8'))
                              if 'visible' in root:
                                  if root['visible']:
                                      self._running_app = app
                                      return
                    except Exception as ex:
                           _LOGGER.debug("Samsung TV %s, _get_running_app Failed - %s......",self._name,ex)
        self._running_app = 'TV/HDMI'


    async def _gen_installed_app_list(self):
        if self._app_list is not None:
            _LOGGER.debug("SamsungTV %s, Manual set applist or already got, _gen_installed_app_list not executed", self._name)
            return
        _LOGGER.debug("Samsung TV %, Self Applist %s",self._app_list)
        if self._state == STATE_OFF or self._state == None:
            _LOGGER.debug("Samsung TV %s, is OFF, _gen_installed_app_list not executed...%s",self._name)
            return 
        _LOGGER.debug("Samsung TV %s, _gen_installed_app_list executed......",self._name)
        try:
            app_list = self._ws.app_list()
        except Exception as ex:
            _LOGGER.debug("Samsung TV %s, _gen_installed_app_list Failed - %s......",self._name,ex)
            self._ws.close()
            return
        # app_list is a list of dict
        clean_app_list = {}
        for i in range(len(app_list)):
            try:
                app = app_list[i]
                clean_app_list[ app.get('name') ] = app.get('appId')
            except Exception:
                pass
        self._app_list_ST = self._app_list = clean_app_list
        _LOGGER.debug("Gen installed app_list %s", clean_app_list)


    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update(self):
        """Update state of device."""
        if self._update_method == "smartthings" and self._api_key and self._device_id:
            smartthings.device_update(self)
            self._ping_device()
        else:
            self._ping_device()
            """Still required to get source and media title"""
            if self._api_key and self._device_id:
                smartthings.device_update(self)
        if self._state == STATE_ON and not self._power_off_in_progress():
            self._get_running_app()
            
        if self._state == STATE_OFF:
            self._end_of_power_off = None 

        self.hass.async_add_job(self._update_media_data)

    def _get_source(self):
        """Return the current input source."""
        if self._state != STATE_OFF:
            # we throttle the method for 5 seconds when we change the source from the UI
            # this is done to give the required time to update the real status and provide correct feedback
            # self._last_source_time is set in async_select_source method
            call_time = datetime.now()
            if self._last_source_time is not None:
                difference = (call_time - self._last_source_time).total_seconds()
                if difference < UPDATE_SOURCE_INTERVAL: #update source every 5 seconds
                    return self._source
            self._last_source_time = call_time
            if hasattr(self, '_cloud_state'):
                if self._cloud_state == STATE_OFF:
                    self._source = None
                else:
                    if self._running_app == "TV/HDMI":
                        cloud_key = ""
                        if self._cloud_source in ["DigitalTv", "digitalTv", "TV"]:
                            cloud_key = "ST_TV"
                        else:
                            cloud_key = "ST_" + self._cloud_source
                        found_source = ""
                        for attr, value in self._source_list.items():
                            if value == cloud_key:
                                found_source = attr
                        if found_source != "":
                            self._source = found_source
                        else:
                            self._source = self._running_app
                    else:
                        self._source = self._running_app
            else:
                self._source = self._running_app
        else:
            self._source = None
            self._last_source_time = None
            
        return self._source

    def _smartthings_keys(self, source_key):
        if source_key.startswith("ST_HDMI"):
            smartthings.send_command(self, source_key.replace("ST_", ""), "selectsource")
        elif source_key == "ST_TV":
            smartthings.send_command(self, "digitalTv", "selectsource")
        elif source_key == "ST_CHUP":
            smartthings.send_command(self, "up", "stepchannel")
        elif source_key == "ST_CHDOWN":
            smartthings.send_command(self, "down", "stepchannel")
        elif source_key.startswith("ST_CH"):
            ch_num = source_key.replace("ST_CH", "")
            if ch_num.isdigit():
                smartthings.send_command(self, ch_num, "selectchannel")
        elif source_key == "ST_MUTE":
            smartthings.send_command(self, "off" if self._muted else "on", "audiomute")
        elif source_key == "ST_VOLUP":
            smartthings.send_command(self, "up", "stepvolume")
        elif source_key == "ST_VOLDOWN":
            smartthings.send_command(self, "down", "stepvolume")
        elif source_key.startswith("ST_VOL"):
            vol_lev = source_key.replace("ST_VOL", "")
            if vol_lev.isdigit():
                smartthings.send_command(self, vol_lev, "setvolume")

    def send_command(self, payload, command_type = "send_key", retry_count = 1, key_press_delay=None,bForceUpdate=True):
        """Send a key to the tv and handles exceptions."""
        bReturn = True
        call_time = datetime.now()
        difference = (call_time - self._last_command_time).total_seconds()
        if difference > WS_CONN_TIMEOUT: #always close connection after WS_CONN_TIMEOUT (10 seconds)
            self._ws.close()
        self._last_command_time = call_time
        try:
            # recreate connection if connection was dead
            for _ in range(retry_count + 1):
                try:
                    if command_type == "run_app":
                        #run_app(self, app_id, app_type='DEEP_LINK', meta_tag='')
                        self._ws.run_app(payload)
                    else:
                        hold_delay = 0
                        source_keys = payload.split(",")
                        key_code = source_keys[0]
                        if len(source_keys) > 1:

                            def get_hold_time():
                                hold_time = source_keys[1].replace(" ", "")
                                if not hold_time:
                                    return 0
                                if not hold_time.isdigit():
                                    return 0
                                hold_time = int(hold_time)/1000
                                return min(hold_time, KEYHOLD_MAX_DELAY)

                            hold_delay = get_hold_time()

                        if hold_delay > 0:
                            self._ws.hold_key(key_code, hold_delay)
                        else:
                            self._ws.send_key(payload, key_press_delay)
                    break
                except (ConnectionResetError, AttributeError, BrokenPipeError) as ex:
                    self._ws.close()
                    _LOGGER.debug("Samsung TV %s, Error in send_command() -> %s......",self._name,ex)
            self._state = STATE_ON
        except (websocket._exceptions.WebSocketTimeoutException,exceptions.ConnectionFailure) as ex:
            # We got a response so it's on.
            self._ws.close()
            self._state = STATE_ON
            _LOGGER.debug("Samsung TV %s, Failed sending payload %s command_type %s",self._name,payload, command_type,ex)
            bReturn = False
        except OSError:
            self._ws.close()
            self._state = STATE_OFF
            _LOGGER.debug("Error in send_command() -> OSError")
            bReturn = False
        if bForceUpdate:
            self.update(no_throttle=True)
            self.schedule_update_ha_state(True)
        else:
            self.update()
            self.schedule_update_ha_state()
        return bReturn

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the device."""
        return self._uuid

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._media_title

    @property
    def media_image_url(self):
        """Return the media image URL."""
        return self._media_image_url

    async def _update_media_data(self):
        if self._state == STATE_OFF and self._update_method != "smartthings":
            self._media_title = None
        if self._api_key and self._device_id and hasattr(self, '_cloud_state'):
            if self._cloud_state == STATE_OFF:
                self._state = STATE_OFF
                self._media_title = None
            elif self._running_app == "TV/HDMI" and self._cloud_source in ["DigitalTv", "digitalTv", "TV"] and self._cloud_channel_name == "" and self._cloud_channel != "":
                self._media_title = self._cloud_channel
                self._media_image_url = None
            else:
                if self._running_app == "TV/HDMI" and self._cloud_source in ["DigitalTv", "digitalTv", "TV"] and self._cloud_channel_name != "":
                    new_media_title = search_media_title = self._cloud_channel_name 
                    if self._show_channel_number and  self._cloud_channel != "":
                        new_media_title = new_media_title + " (" + self._cloud_channel + ")"
                else:
                    new_media_title = search_media_title = self._get_source()
                #only match new image if title actually changed and logos are enabled
                if self._media_title != new_media_title and self._media_image_base_url is not None:
                    if new_media_title not in ["TV","HDMI","TV/HDMI"]:
                        _LOGGER.debug("Matching title to image %s",search_media_title)
                        await self._match_title_to_image(search_media_title)
                    else:
                        self._media_image_url = None
                self._media_title = new_media_title
        else:
            new_media_title = self._get_source()
            #only match new image if title actually changed and logos are enabled
            if self._media_title != new_media_title and self._media_image_base_url is not None:
                if new_media_title not in ["TV","HDMI","TV/HDMI"] and new_media_title is not None:
                    _LOGGER.debug("Matching title to image %s",new_media_title)
                    await self._match_title_to_image(new_media_title)
                else:
                    self._media_image_url = None
            self._media_title = new_media_title

    async def _match_title_to_image(self, media_title):
        if media_title is not None:
            for word in MEDIA_TITLE_KEYWORD_REMOVAL:
                media_title = media_title.lower().replace(word.lower(),'')
            media_title = media_title.lower().strip()
            try:
                with open(MEDIA_FILE_IMAGE_TO_PATH, 'r') as f:
                    image_paths = iter(json.load(f).items())
            except:
                self._media_image_url = None
            
            best_match = {"ratio": None, "title": None, "path": None}
            while True:
                try:
                    image_path = next(image_paths)
                    ratio = levenshtein_ratio_and_distance(media_title,image_path[0].lower(),ratio_calc = True)
                    if best_match["ratio"] is None or ratio > best_match["ratio"]:
                        best_match = {"ratio":ratio,"title":image_path[0],"path":image_path[1]}
                except StopIteration:
                    break

            if best_match["ratio"] > MEDIA_IMAGE_MIN_SCORE_REQUIRED/100:
                _LOGGER.debug("Match found for %s: %s (%f) %s", media_title, best_match["title"],  best_match["ratio"], self._media_image_base_url+best_match["path"])
                self._media_image_url = self._media_image_base_url+best_match["path"]
            else:
                _LOGGER.debug("No match found for %s: best candidate was %s (%f) %s", media_title, best_match["title"], best_match["ratio"], self._media_image_base_url+best_match["path"])
                self._media_image_url = None
        else:
            _LOGGER.debug("No media title right now!")
            self._media_image_url = None

    @property
    def state(self):
        """Return the state of the device."""
        
        # Warning: we assume that after a sending a power off command, the command is successful
        # so for 20 seconds (defined in POWER_OFF_DELAY) the state will be off regardless of the actual state. 
        # This is to have better feedback to the command in the UI, but the logic might cause other issues in the future
        if self._power_off_in_progress():
            return STATE_OFF
        return self._state


    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._muted


    @property
    def source_list(self):
        """List of available input sources."""
        if self._app_list is None:
            self._gen_installed_app_list()
        source_list = []
        source_list.extend(list(self._source_list))
        if self._app_list is not None:
            source_list.extend(list(self._app_list))
        if self._channel_list is not None:
            source_list.extend(list(self._channel_list))
        return source_list

    @property
    def channel_list(self):
        """List of available channels."""
        if self._channel_list is None:
            return None
        else:
            return list(self._channel_list)

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume


    @property
    def source(self):
        """Return the current input source."""
        return self._get_source()


    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_SAMSUNGTV | SUPPORT_TURN_ON

    @property
    def device_class(self):
        """Set the device class to TV."""
        return DEVICE_CLASS_TV

    def turn_on(self):
        """Turn the media player on."""
        if self._power_off_in_progress():
            self._end_of_power_off = None 
            if self._is_ws_connection:
                self.hass.async_add_job(self.send_command, "KEY_POWER")
            else:
                self.hass.async_add_job(self.send_command, "KEY_POWEROFF")
        elif self._state == STATE_OFF:
            if self._mac:
                if self._broadcast:
                    for i in range(20):
                        wakeonlan.send_magic_packet(self._mac, ip_address=self._broadcast)
                        time.sleep(0.25)
                else:
                    for i in range(20):
                        wakeonlan.send_magic_packet(self._mac)
                        time.sleep(0.25)
                #Force Update as send command not called
                self.update(no_throttle=True)
                self.schedule_update_ha_state(True)
            else:
                self.hass.async_add_job(self.send_command, "KEY_POWERON")
        #Assume optomistic ON
        self._state = STATE_ON

    def turn_off(self):
        """Turn off media player."""
        if (not self._power_off_in_progress()) and self._state != STATE_OFF:
            self._end_of_power_off = dt_util.utcnow() + POWER_OFF_DELAY
            if self._is_ws_connection:
                if self._is_frame_tv == False:
                    self.hass.async_add_job(self.send_command, "KEY_POWER")
                else:
                    self.hass.async_add_job(self.send_command, "KEY_POWER,3000")
            else:
                self.hass.async_add_job(self.send_command, "KEY_POWEROFF")
            # Force closing of remote session to provide instant UI feedback
            try:
                self._ws.close()
            except OSError:
                _LOGGER.debug("Could not establish connection.")
        #Empty Applist if autogenerated
        if self._auto_gen_installed_app_list == True:
           self._app_list = None
           self._app_list_ST = None
        #Assume optomistic OFF
        self._state = STATE_OFF



    def volume_up(self):
        """Volume up the media player."""
        self._volume = self._volume + 0.1
        if self._volume>1:
            self._volume = 1
        self.hass.async_add_job(self.send_command, "KEY_VOLUP")


    def volume_down(self):
        """Volume down media player."""
        self._volume = self._volume - 0.1
        if self._volume<0:
            self._volume = 0
        self.hass.async_add_job(self.send_command, "KEY_VOLDOWN")


    def mute_volume(self, mute):
        """Send mute command."""
        self._muted = not self._muted
        self.hass.async_add_job(self.send_command, "KEY_MUTE")


    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        self._volume = volume
        self.hass.async_add_job(self._upnp.set_volume, int(volume*100))


    def media_play_pause(self):
        """Simulate play pause media player."""
        if self._playing:
            self.media_pause()
        else:
            self.media_play()


    def media_play(self):
        """Send play command."""
        self._playing = True
        self.hass.async_add_job(self.send_command, "KEY_PLAY")


    def media_pause(self):
        """Send media pause command to media player."""
        self._playing = False
        self.hass.async_add_job(self.send_command, "KEY_PAUSE")


    def media_next_track(self):
        """Send next track command."""
        if self.source == "TV":
            self.hass.async_add_job(self.send_command, "KEY_CHUP")
        else:
            self.hass.async_add_job(self.send_command, "KEY_FF")


    def media_previous_track(self):
        """Send the previous track command."""
        if self.source == "TV":
            self.hass.async_add_job(self.send_command, "KEY_CHDOWN")
        else:
            self.hass.async_add_job(self.send_command, "KEY_REWIND")


    async def async_play_media(self, media_type, media_id, **kwargs):
        # Type channel
        if media_type == MEDIA_TYPE_CHANNEL:
            """Support changing a channel."""
            _LOGGER.debug("Trying to change %s to %s",media_type,media_id) 
            try:
                cv.positive_int(media_id)
            except vol.Invalid:
                _LOGGER.error("Media ID must be positive integer")
                return
            if self._api_key and self._device_id:
                if self._running_app == 'TV/HDMI' and self._cloud_source in ["DigitalTv", "digitalTv", "TV"]:
                    #In TV mode, change channel
                    if self._cloud_channel != media_id:
                        await self.hass.async_add_job(self._smartthings_keys, f"ST_CH{media_id}")
                else:
                    #Change to TV source before changing channel
                    self.hass.async_add_job(self._smartthings_keys, "ST_TV")
                    time.sleep(5)
                    smartthings.device_update(self)
                    if self._cloud_channel != media_id:
                        await self.hass.async_add_job(self._smartthings_keys, f"ST_CH{media_id}")
            else:
                keychain = ""
                for digit in media_id:
                    keychain += "KEY_{}+".format(digit)
                keychain += "KEY_ENTER"
                if self._running_app == 'TV/HDMI':
                    self.hass.async_add_job(self.async_play_media, MEDIA_TYPE_KEY, keychain)
                else:
                    found_source = False
                    for source in self._source_list:
                        if source.lower() in ["tv", "live tv", "livetv"]:
                            found_source = True
                            await self.hass.async_add_job(self.async_select_source, source)
                            time.sleep(2)
                            break
                    if found_source == False:
                        keychain = "KEY_EXIT+KEY_EXIT+{}".format(keychain)
                    self.hass.async_add_job(self.async_play_media, MEDIA_TYPE_KEY, keychain)
        # Launch an app
        elif media_type == MEDIA_TYPE_APP:
            await self.hass.async_add_job(self.send_command, media_id, "run_app")
        # Send custom key
        elif media_type == MEDIA_TYPE_KEY:
            try:
                cv.string(media_id)
            except vol.Invalid:
                _LOGGER.error('Media ID must be a string (ex: "KEY_HOME"')
                return
            source_key = media_id
            if "+" in source_key:
                all_source_keys = source_key.split("+")
                last_was_delay = True
                for this_key in all_source_keys:
                    if this_key.isdigit():
                        last_was_delay = True
                        time.sleep(int(this_key)/1000)
                    else:
                        if this_key.startswith("ST_"):
                            await self.hass.async_add_job(self._smartthings_keys, this_key)
                        else:
                            if last_was_delay == False:
                                time.sleep(DEFAULT_KEY_CHAIN_DELAY)
                            last_was_delay = False
                            self.hass.async_add_job(self.send_command, this_key)
            elif source_key.startswith("ST_"):
                await self.hass.async_add_job(self._smartthings_keys, source_key)
            else:
                await self.hass.async_add_job(self.send_command, source_key)
        # Play media
        elif media_type == MEDIA_TYPE_URL:
            try:
                cv.url(media_id)
            except vol.Invalid:
                _LOGGER.error('Media ID must be an url (ex: "http://"')
                return
            await self.hass.async_add_job(self._upnp.set_current_media, media_id)
            self._playing = True
        # Trying to make stream component work on TV
        elif media_type == "application/vnd.apple.mpegurl":
            await self.hass.async_add_job(self._upnp.set_current_media, media_id)
            self._playing = True
        elif media_type == MEDIA_TYPE_BROWSER:
            try:
                await self.hass.async_add_job(self._ws.open_browser, media_id)
            except (ConnectionResetError, AttributeError, BrokenPipeError,websocket._exceptions.WebSocketTimeoutException):
                self._ws.close()
        else:
            _LOGGER.error("Unsupported media type")
            return

    async def async_select_source(self, source):
        """Select input source."""
        _LOGGER.debug('SamsungTV Trying source:%s',source)
        if source in self._source_list:
            source_key = self._source_list[ source ]
            if "+" in source_key:
                all_source_keys = source_key.split("+")
                for this_key in all_source_keys:
                    if this_key.isdigit():
                        time.sleep(int(this_key)/1000)
                    else:
                        if this_key.startswith("ST_"):
                            await self.hass.async_add_job(self._smartthings_keys, this_key)
                        else:
                            await self.hass.async_add_job(self.send_command, this_key)
            elif source_key.startswith("ST_"):
                await self.hass.async_add_job(self._smartthings_keys, source_key)
            else:
                await self.hass.async_add_job(self.send_command, self._source_list[ source ])
        elif source in self._app_list:
            source_key = self._app_list[ source ]
            await self.hass.async_add_job(self.send_command, source_key, "run_app")
        elif source in self._channel_list:
            source_key = self._channel_list[ source ]
            ch_media_type = MEDIA_TYPE_CHANNEL
            if source_key.startswith("http"): ch_media_type = MEDIA_TYPE_URL
            await self.hass.async_add_job(self.async_play_media,ch_media_type, source_key)
        else:
            _LOGGER.error("Unsupported source")
            return
        self._last_source_time = datetime.now()
        self._source = source

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])
