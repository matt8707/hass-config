#Smartthings TV integration#
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json
import os
from homeassistant.const import (
    STATE_OFF,
    STATE_ON,
)
API_BASEURL = "https://api.smartthings.com/v1"
API_DEVICES = API_BASEURL + "/devices/"
COMMAND_POWER_OFF = "{'commands': [{'component': 'main','capability': 'switch','command': 'off'}]}"
COMMAND_POWER_ON = "{'commands': [{'component': 'main','capability': 'switch','command': 'on'}]}"
COMMAND_REFRESH = "{'commands':[{'component': 'main','capability': 'refresh','command': 'refresh'}]}"
COMMAND_PAUSE = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'pause'}]}"
COMMAND_MUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'mute'}]}"
COMMAND_UNMUTE = "{'commands':[{'component': 'main','capability': 'audioMute','command': 'unmute'}]}"
COMMAND_PLAY = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'play'}]}"
COMMAND_STOP = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'stop'}]}"
COMMAND_REWIND = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'rewind'}]}"
COMMAND_FAST_FORWARD = "{'commands':[{'component': 'main','capability': 'mediaPlayback','command': 'fastForward'}]}"

class smartthingstv:

  def __init__(self):
      self._cloud_state = STATE_OFF
      self._cloud_muted = False
      self._cloud_volume = 10


  def device_update(self):
      API_KEY = self._api_key
      REQUEST_HEADERS = {"Authorization": "Bearer " + API_KEY}
      DEVICE_ID = self._device_id
      API_DEVICE = API_DEVICES + DEVICE_ID
      API_DEVICE_STATUS = API_DEVICE + "/states"
      API_COMMAND = API_DEVICE + "/commands"
      cmdurl = requests.post(API_COMMAND,data=COMMAND_REFRESH ,headers=REQUEST_HEADERS)
      resp = requests.get(API_DEVICE_STATUS,headers=REQUEST_HEADERS)
      data = resp.json()
      device_volume = data['main']['volume']['value']
      device_volume = int(device_volume) / 100
      device_state = data['main']['switch']['value']
      device_source = data['main']['inputSource']['value']
      device_all_sources = json.loads(data['main']['supportedInputSources']['value'])
      device_tv_chan = data['main']['tvChannel']['value']
      device_tv_chan_name = data['main']['tvChannelName']['value']
      device_muted = data['main']['mute']['value'] 
      self._cloud_state = device_state
      if device_state == "off":
         self._cloud_state = STATE_OFF
      else:
         self._cloud_state = STATE_ON
      self._cloud_volume = device_volume
      self._cloud_source_list = device_all_sources
      if device_muted == "mute":
         self._cloud_muted = True
      else:
         self._cloud_muted = False
      self._cloud_source = device_source
      self._cloud_channel = device_tv_chan
      self._cloud_channel_name = device_tv_chan_name

  def send_command(self, command, cmdtype):
      API_KEY = self._api_key
      REQUEST_HEADERS = {"Authorization": "Bearer " + API_KEY}
      DEVICE_ID = self._device_id
      API_DEVICES = API_BASEURL + "/devices/"
      API_DEVICE = API_DEVICES + DEVICE_ID
      API_COMMAND = API_DEVICE + "/commands"

      if cmdtype == "setvolume": # sets volume
         API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'setVolume','arguments': "
         API_COMMAND_ARG  = "[{}]}}]}}".format(command)
         API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
         cmdurl = requests.post(API_COMMAND,data=API_FULL ,headers=REQUEST_HEADERS)
      elif cmdtype == "stepvolume": # steps volume up or down
         if command == "up":
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeUp'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
         else:
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'audioVolume','command': 'volumeDown'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
      elif cmdtype == "audiomute": # mutes audio
         if command == "on":
            cmdurl = requests.post(API_COMMAND,data=COMMAND_MUTE ,headers=REQUEST_HEADERS)
         elif command == "off":
            cmdurl = requests.post(API_COMMAND,data=COMMAND_UNMUTE ,headers=REQUEST_HEADERS)
      elif cmdtype == "turn_off": # turns off
         cmdurl = requests.post(API_COMMAND,data=COMMAND_POWER_OFF ,headers=REQUEST_HEADERS)
      elif cmdtype == "turn_on": # turns on
         cmdurl = requests.post(API_COMMAND,data=COMMAND_POWER_ON ,headers=REQUEST_HEADERS)
      elif cmdtype == "selectsource": #changes source
         API_COMMAND_DATA =  "{'commands':[{'component': 'main','capability': 'mediaInputSource','command': 'setInputSource', 'arguments': "
         API_COMMAND_ARG  = "['{}']}}]}}".format(command)
         API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
         cmdurl = requests.post(API_COMMAND,data=API_FULL ,headers=REQUEST_HEADERS)
      elif cmdtype == "selectchannel": #changes channel
         API_COMMAND_DATA =  "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'setTvChannel', 'arguments': "
         API_COMMAND_ARG  = "['{}']}}]}}".format(command)
         API_FULL = API_COMMAND_DATA + API_COMMAND_ARG
         cmdurl = requests.post(API_COMMAND,data=API_FULL ,headers=REQUEST_HEADERS)
      elif cmdtype == "stepchannel": # steps channel up or down
         if command == "up":
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelUp'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
         else:
            API_COMMAND_DATA = "{'commands':[{'component': 'main','capability': 'tvChannel','command': 'channelDown'}]}"
            cmdurl = requests.post(API_COMMAND,data=API_COMMAND_DATA ,headers=REQUEST_HEADERS)
