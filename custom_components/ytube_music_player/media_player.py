
"""
Attempting to support yTube Music in Home Assistant
"""
import asyncio
import logging
import time
import random
import pickle
import os.path
import random
import datetime
from urllib.request import urlopen
from urllib.parse import unquote

from .const import *
import voluptuous as vol
from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.helpers.condition import state
from homeassistant.helpers.event import track_state_change
from homeassistant.helpers.event import call_later
from homeassistant.helpers.storage import STORAGE_DIR
from homeassistant.helpers import device_registry

from homeassistant.const import ATTR_ENTITY_ID
import homeassistant.components.input_select as input_select
import homeassistant.components.input_boolean as input_boolean
import homeassistant.components.media_player as media_player

from .browse_media import build_item_response, library_payload

from pytube import YouTube
from pytube import request
from pytube import extract
from pytube.cipher import Cipher
import ytmusicapi
#from .ytmusicapi.ytmusic import *


_LOGGER = logging.getLogger(__name__)


def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
	"""Run setup via YAML."""
	_LOGGER.debug("Config via YAML")
	if(config is not None):
		async_add_entities([yTubeMusicComponent(hass, config,"_yaml")], update_before_add=False)

async def async_setup_entry(hass, config, async_add_devices):
	"""Run setup via Storage."""
	_LOGGER.debug("Config via Storage/UI currently not supported due to me not understanding asyncio")
	if(len(config.data) > 0):
		async_add_devices([yTubeMusicComponent(hass, config.data,"")], update_before_add=False)


class yTubeMusicComponent(MediaPlayerEntity):
	def __init__(self, hass, config, name_add):
		self.hass = hass
		self._name = config.get(CONF_NAME,DOMAIN+name_add)
		# confgurations can be either the full entity_id or just the name
		self._select_playlist = input_select.DOMAIN+"."+config.get(CONF_SELECT_PLAYLIST, DEFAULT_SELECT_PLAYLIST).replace(input_select.DOMAIN+".","")
		self._select_playMode = input_select.DOMAIN+"."+config.get(CONF_SELECT_PLAYMODE, DEFAULT_SELECT_PLAYMODE).replace(input_select.DOMAIN+".","")
		self._select_playContinuous = input_boolean.DOMAIN+"."+config.get(CONF_SELECT_PLAYCONTINUOUS, DEFAULT_SELECT_PLAYCONTINUOUS).replace(input_boolean.DOMAIN+".","")
		self._select_mediaPlayer = input_select.DOMAIN+"."+config.get(CONF_SELECT_SPEAKERS, DEFAULT_SELECT_SPEAKERS).replace(input_select.DOMAIN+".","")
		self._select_source = input_select.DOMAIN+"."+config.get(CONF_SELECT_SOURCE, DEFAULT_SELECT_SOURCE).replace(input_select.DOMAIN+".","")

		default_header_file = os.path.join(hass.config.path(STORAGE_DIR),DEFAULT_HEADER_FILENAME)
		self._header_file = config.get(CONF_HEADER_PATH, default_header_file)
		self._speakersList = config.get(CONF_RECEIVERS)

		# proxy settings
		self._proxy_url = config.get(CONF_PROXY_URL,"")
		self._proxy_path = config.get(CONF_PROXY_PATH,"")


		_LOGGER.debug("YtubeMediaPlayer config: ")
		_LOGGER.debug("- Header path: " + self._header_file)
		_LOGGER.debug("- playlist: " + self._select_playlist)
		_LOGGER.debug("- mediaplayer: " + self._select_mediaPlayer)
		_LOGGER.debug("- source: " + self._select_source)
		_LOGGER.debug("- speakerlist: " + str(self._speakersList))
		_LOGGER.debug("- playModes: " + str(self._select_playMode))
		_LOGGER.debug("- playContinuous: " + str(self._select_playContinuous))

		self._brand_id = str(config.get(CONF_BRAND_ID,""))
		self._api = None
		self._js = ""
		self._update_needed = False

		self._remote_player = ""
		self._untrack_remote_player = None
		self._playlists = []
		self._playlist_to_index = {}
		self._tracks = []
		self._attributes = {}
		self._next_track_no = 0
		self._allow_next = False
		self._last_auto_advance = datetime.datetime.now()
		self._started_by = None
		self._interrupt_data = None
		self._attributes['_media_type'] = None
		self._attributes['_media_id'] = None
		self._attributes['_player_state'] = STATE_OFF

		self._playing = False
		self._state = STATE_OFF
		self._volume = 0.0
		self._is_mute = False
		self._track_name = None
		self._track_artist = None
		self._track_album_name = None
		self._track_album_cover = None
		self._track_artist_cover = None
		self._media_duration = None
		self._media_position = None
		self._media_position_updated = None
		self._shuffle = config.get(CONF_SHUFFLE, DEFAULT_SHUFFLE)
		self._shuffle_mode = config.get(CONF_SHUFFLE_MODE, DEFAULT_SHUFFLE_MODE)
		self._playContinuous = True
		self._x_to_idle = None # Some Mediaplayer don't transition to 'idle' but to 'off' on track end. This re-routes off to idle


		# register "call_method"
		if(name_add==""):
			platform = entity_platform.current_platform.get()
			platform.async_register_entity_service(
				SERVICE_CALL_METHOD,
				{
					vol.Required(ATTR_COMMAND): cv.string,
					vol.Optional(ATTR_PARAMETERS): vol.All(
						cv.ensure_list, vol.Length(min=1), [cv.string]
					),
				},
				"async_call_method",
			)
		# run the api / get_cipher / update select as soon as possible
		if hass.is_running:
			self._update_needed = True
		else:
			hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self.startup)

	# update will be called eventually BEFORE homeassistant is started completly
	# therefore we should not use this method for ths init
	def update(self):
		if(self._update_needed):
			self.startup(self.hass)

	# either called once homeassistant started (component was configured before startup)
	# or call from update(), if the component was configured AFTER homeassistant was started
	def startup(self,hass):
		self._get_cipher('BB2mjBuAtiQ')
		self.check_api()
		self._update_selects()
		self._update_playmode()

	def check_api(self):
		_LOGGER.debug("check_api")
		if(self._api == None):
			_LOGGER.debug("- no valid API, try to login")
			if(os.path.exists(self._header_file)):
				[ret, msg, self._api] = try_login(self._header_file,self._brand_id)
				if(msg!=""):
					self._api = None
					out = "Issue during login: "+msg
					data = {"title": "yTubeMediaPlayer error", "message": out}
					self.hass.services.call("persistent_notification","create", data)
					return False
				else:
					_LOGGER.debug("- YouTube Api initialized ok, version: "+str(ytmusicapi.__version__))
			else:
				out = "can't find header file at "+self._header_file
				_LOGGER.error(out)
				data = {"title": "yTubeMediaPlayer error", "message": out}
				self.hass.services.call("persistent_notification","create", data)
				return False
		return True
			

	@property
	def name(self):
		""" Return the name of the player. """
		return self._name

	@property
	def icon(self):
		return 'mdi:music-circle'

	@property
	def supported_features(self):
		""" Flag media player features that are supported. """
		return SUPPORT_YTUBEMUSIC_PLAYER

	@property
	def should_poll(self):
		""" No polling needed. """
		return False

	@property
	def state(self):
		""" Return the state of the device. """
		return self._state

	@property
	def device_state_attributes(self):
		""" Return the device state attributes. """
		return self._attributes

	@property
	def is_volume_muted(self):
		""" Return True if device is muted """
		return self._is_mute

	@property
	def is_on(self):
		""" Return True if device is on. """
		return self._playing

	@property
	def media_content_type(self):
		""" Content type of current playing media. """
		return MEDIA_TYPE_MUSIC

	@property
	def media_title(self):
		""" Title of current playing media. """
		return self._track_name

	@property
	def media_artist(self):
		""" Artist of current playing media """
		return self._track_artist

	@property
	def media_album_name(self):
		""" Album name of current playing media """
		return self._track_album_name

	@property
	def media_image_url(self):
		""" Image url of current playing media. """
		return self._track_album_cover

	@property
	def media_image_remotely_accessible(self):
		# True  returns: entity_picture: http://lh3.googleusercontent.com/Ndilu...
		# False returns: entity_picture: /api/media_player_proxy/media_player.gmusic_player?token=4454...
		return True

	@property
	def media_position(self):
		"""Position of current playing media in seconds."""
		return self._media_position


	@property
	def media_position_updated_at(self):
		"""When was the position of the current playing media valid.
		Returns value from homeassistant.util.dt.utcnow().
		"""
		return self._media_position_updated


	@property
	def media_duration(self):
		"""Duration of current playing media in seconds."""
		return self._media_duration


	@property
	def shuffle(self):
		""" Boolean if shuffling is enabled. """
		return self._shuffle

	@property
	def repeat(self):
		"""Return current repeat mode."""
		if(self._playContinuous):
			return REPEAT_MODE_ALL
		return REPEAT_MODE_OFF

	def set_repeat(self, repeat: str):
		_LOGGER.debug("set_repleat: "+repeat)
		"""Set repeat mode."""
		data = {ATTR_ENTITY_ID: self._select_playContinuous}
		if repeat != REPEAT_MODE_OFF:
			self._playContinuous = True
			if(self._select_playContinuous!=""):
				self.hass.services.call(DOMAIN_IB, IB_ON, data)
		else:
			self._playContinuous = False
			if(self._select_playContinuous!=""):
				self.hass.services.call(DOMAIN_IB, IB_OFF, data)

	@property
	def volume_level(self):
	  """ Volume level of the media player (0..1). """
	  return self._volume


	def turn_on(self, *args, **kwargs):
		_LOGGER.debug("TURNON")
		""" Turn on the selected media_player from input_select """

		self._started_by = "UI"
		
		# exit if we don't konw what to play (the select_playlist will be set to "" if the config provided a value but the entity_id is not in homeassistant)
		if(self._select_playlist==""):
			_LOGGER.debug("no or wrong playlist select field in the config, exiting")
			msg= "You have no playlist entity_id in your config, or that entity_id is not in homeassistant. I don't know what to play and will exit. Either use the media_browser or add the playlist dropdown"
			data = {"title": "yTubeMediaPlayer error", "message": msg}
			self.hass.services.call("persistent_notification","create", data)
			self._turn_off_media_player()
			return

		# set UI to correct playlist, or grab playlist if none was submitted
		playlist  = self.hass.states.get(self._select_playlist).state
			
		# exit if we don't have any playlists from the account
		if(len(self._playlists)==0):
			_LOGGER.error("playlists empty")
			self._turn_off_media_player()
			return

		# load ID for playlist name
		idx = self._playlist_to_index.get(playlist)
		if idx is None:
			_LOGGER.error("playlist to index is none!")
			self._turn_off_media_player()
			return
		
		# playlist or playlist_radio? 
		if(self._select_source!=""):
			_source = self.hass.states.get(self._select_source)
			if _source is None:
				_LOGGER.error("- (%s) is not a valid input_select entity.", self._select_source)
				return
			if(_source.state == "Playlist"):
				self._attributes['_media_type'] = MEDIA_TYPE_PLAYLIST
			else:
				self._attributes['_media_type'] = CHANNEL
		else:
			self._attributes['_media_type'] = MEDIA_TYPE_PLAYLIST

		# store id and start play_media
		self._attributes['_media_id'] = self._playlists[idx]['playlistId']
		return self.play_media(media_type=self._attributes['_media_type'], media_id=self._attributes['_media_id'])

	def prepare_play(self):
		_LOGGER.debug("prepare_play")
		if(not self.check_api()):
			return

		# get _remote_player
		if not self._update_remote_player():
			return
		_player = self.hass.states.get(self._remote_player)

		# subscribe to changes
		if(self._select_playMode!=""):
			track_state_change(self.hass, self._select_playMode, self._update_playmode)
		if(self._select_playContinuous!=""):
			track_state_change(self.hass, self._select_playContinuous, self._update_playmode)
		if(self._select_mediaPlayer!=""):
			track_state_change(self.hass, self._select_mediaPlayer, self.select_source_helper)
		
		
		# make sure that the player, is on and idle
		if self._playing == True:
			self.media_stop() 
		elif self._playing == False and self._state == STATE_OFF:
			if _player.state == STATE_OFF:
				self._turn_on_media_player()
		else:
			_LOGGER.debug("self._state is: (%s).", self._state)
			if(self._state == STATE_PLAYING):
				self.media_stop() 
			
		# update cipher
		self._get_cipher('BB2mjBuAtiQ')

		# display imidiatly a loading state to provide feedback to the user
		self._allow_next = False
		self._track_album_name = ""
		self._track_artist =  ""
		self._track_artist_cover =  None
		self._track_album_cover = None
		self._track_name =  "loading..."
		self._state = STATE_PLAYING # a bit early otherwise no info will be shown
		self.schedule_update_ha_state()
		return True

	def _turn_on_media_player(self, data=None):
		_LOGGER.debug("_turn_on_media_player")
		"""Fire the on action."""
		if data is None:
			data = {ATTR_ENTITY_ID: self._remote_player}
		self._state = STATE_IDLE
		self.schedule_update_ha_state()
		self.hass.services.call(DOMAIN_MP, 'turn_on', data)


	def turn_off(self, entity_id=None, old_state=None, new_state=None, **kwargs):
		""" Turn off the selected media_player """
		_LOGGER.debug("turn_off")
		self._playing = False
		self._track_name = None
		self._track_artist = None
		self._track_album_name = None
		self._track_album_cover = None
		self._media_duration = None
		self._media_position = None
		self._media_position_updated = None
		self._turn_off_media_player()

	def _turn_off_media_player(self, data=None):
		_LOGGER.debug("_turn_off_media_player")
		"""Fire the off action."""
		self._playing = False
		self._state = STATE_OFF
		self._attributes['_player_state'] = STATE_OFF
		self._attributes['likeStatus'] = ""
		self._attributes['videoId'] = ""
		self._attributes['lyrics'] = ""
		self._attributes['_media_type'] = ""
		self._attributes['_media_id'] = ""
		self._attributes['current_track'] = 0

		self.schedule_update_ha_state()
		if(self._remote_player == ""):
			if(not(self._update_remote_player())):
				return
		if(data != 'skip_remote_player'):
			data = {ATTR_ENTITY_ID: self._remote_player}
			self.hass.services.call(DOMAIN_MP, 'media_stop', data)
			self.hass.services.call(DOMAIN_MP, 'turn_off', data)


	def _update_remote_player(self, remote_player=""):
		_LOGGER.debug("_update_remote_player")
		old_remote_player = self._remote_player
		if(remote_player != ""):
			# make sure that the entity ID is complete
			if(not(remote_player.startswith(DOMAIN_MP+"."))):
				remote_player = DOMAIN_MP+"."+remote_player
			self._remote_player = remote_player
		# sets the current media_player from input_select
		elif(self._select_mediaPlayer == ""): # drop down for player does not exist
			if(self._remote_player == ""): # no preselected entity ID
				self._track_name = "Please select player first"
				self.schedule_update_ha_state()
				msg= "Please select a player before start playing, e.g. via the 'media_player.select_source' method"
				data = {"title": "yTubeMediaPlayer error", "message": msg}
				self.hass.services.call("persistent_notification","create", data)
				return False
			else:
				return True
		else:
			media_player = self.hass.states.get(self._select_mediaPlayer) # Example: self.hass.states.get(input_select.gmusic_player_speakers)
			if media_player is None:
				_LOGGER.error("(%s) is not a valid input_select entity.", self._select_mediaPlayer)
				return False
			_remote_player = "media_player." + media_player.state
			if self.hass.states.get(_remote_player) is None:
				_LOGGER.error("(%s) is not a valid media player.", media_player.state)
				return False
			# Example: self._remote_player = media_player.bedroom_stereo
			self._remote_player = _remote_player

		# unsubscribe / resubscribe
		if self._remote_player != old_remote_player:
			if(self._untrack_remote_player is not None):
				try:
					self._untrack_remote_player()
				except:
					pass
			self._untrack_remote_player = track_state_change(self.hass, self._remote_player, self._sync_player)
		return True


	def _get_cipher(self, videoId):
		_LOGGER.debug("_get_cipher")
		embed_url = "https://www.youtube.com/embed/"+videoId
		embed_html = request.get(url=embed_url)
		js_url = extract.js_url(embed_html)
		self._js = request.get(js_url)
		self._cipher = Cipher(js=self._js)
		#2do some sort of check if tis worked


	def _sync_player(self, entity_id=None, old_state=None, new_state=None):
		_LOGGER.debug("_sync_player")
		if(entity_id!=None and old_state!=None) and new_state!=None:
			_LOGGER.debug(entity_id+": "+old_state.state+" -> "+new_state.state)
			if(entity_id!=self._remote_player):
				_LOGGER.debug("- ignoring old player")
				return
		else:
			_LOGGER.debug(self._remote_player)
		
		""" Perform actions based on the state of the selected (Speakers) media_player """
		if not self._playing:
			return
		""" _player = The selected speakers """
		_player = self.hass.states.get(self._remote_player)

		if('media_duration' in _player.attributes):			
			self._media_duration = _player.attributes['media_duration']
		if('media_position' in _player.attributes):
			self._media_position = _player.attributes['media_position']
			self._media_position_updated = datetime.datetime.now(datetime.timezone.utc)

		""" entity_id of selected speakers. """
		self._attributes['_player_id'] = _player.entity_id

		""" _player state - Example [playing -or- idle]. """
		self._attributes['_player_state'] = _player.state

		""" unlock allow next, some player fail because their media_position is 'strange' catch """
		found_position = False
		try:
			if 'media_position' in _player.attributes:
				found_position = True
				if(isinstance(_player.attributes['media_position'],int)):
					if _player.state == 'playing' and _player.attributes['media_position']>0:
						self._allow_next = True
		except:
			found_position = False
			pass
		if not(found_position) and _player.state == 'playing': # fix for browser mod media_player not providing the 'media_position'
			self._allow_next = True

		""" auto next .. best cast: we have an old and a new state """
		if(old_state!=None and new_state!=None):
			# chromecast quite frequently change from playing to idle twice, so we need some kind of time guard
			if(old_state.state == STATE_PLAYING and new_state.state == STATE_IDLE and (datetime.datetime.now()-self._last_auto_advance).total_seconds() > 10 ):
				self._allow_next = False
				self._get_track()
			# turn this player of when the remote_player was shut down
			elif((old_state.state == STATE_PLAYING or old_state.state == STATE_IDLE) and new_state.state == STATE_OFF):
				if(self._x_to_idle == STATE_OFF): # workaround for MPD (changes to OFF at the end of a track)
					self._allow_next = False
					self._get_track()
				else:
					self._state = STATE_OFF
					_LOGGER.debug("media player got turned off")
					self.turn_off()
			elif(old_state.state == STATE_PLAYING and new_state.state == STATE_PAUSED and # workaround for SONOS (changes to PAUSED at the end of a track)
			       (datetime.datetime.now()-self._last_auto_advance).total_seconds() > 10 and self._x_to_idle == STATE_PAUSED):
				self._allow_next = False
				self._get_track()
			elif(old_state.state == STATE_PAUSED and new_state.state == STATE_IDLE and self._state == STATE_PAUSED):
				_LOGGER.debug("Remote Player changed from PAUSED to IDLE withouth our interaction, so likely another source is using the player now. I'll step back and swich myself off")
				self._turn_off_media_player('skip_remote_player')
				return
		# no states, lets rely on stuff like _allow_next
		elif _player.state == 'idle':
			if self._allow_next:
				if (datetime.datetime.now()-self._last_auto_advance).total_seconds() > 10:
					self._allow_next = False
					self._get_track()


		""" Set new volume if it has been changed on the _player """
		if 'volume_level' in _player.attributes:
			self._volume = round(_player.attributes['volume_level'],2)
		self.schedule_update_ha_state()

	def _ytubemusic_play_media(self, event):
		_LOGGER.debug("_ytubemusic_play_media")
		_speak = event.data.get('speakers')
		_source = event.data.get('source')
		_media = event.data.get('name')

		if event.data['shuffle_mode']:
			self._shuffle_mode = event.data.get('shuffle_mode')
			_LOGGER.info("SHUFFLE_MODE: %s", self._shuffle_mode)

		if event.data['shuffle']:
			self.set_shuffle(event.data.get('shuffle'))
			_LOGGER.info("- SHUFFLE: %s", self._shuffle)

		_LOGGER.debug("- Speakers: (%s) | Source: (%s) | Name: (%s)", _speak, _source, _media)
		self.play_media(_source, _media, _speak)


	def extract_info(self, _track):
		#_LOGGER.debug("extract_info")
		""" If available, get track information. """
		info = dict()
		info['track_album_name'] = ""
		info['track_artist_cover'] = ""
		info['track_name'] = ""
		info['track_artist'] = ""
		info['track_album_cover'] = ""

		
		if 'title' in _track:
			info['track_name'] = _track['title']
		if 'byline' in _track:
			info['track_artist'] = _track['byline']
		elif 'artists' in _track:
			info['track_artist'] = ""
			if(isinstance(_track["artists"],str)):
				info['track_artist'] = _track["artists"]
			elif(isinstance(_track["artists"],list)):
				if 'name' in _track['artists'][0]:
					info['track_artist'] = _track['artists'][0]['name']
				else:
					info['track_artist'] = _track['artists'][0]
		if 'thumbnail' in _track:
			_album_art_ref = _track['thumbnail']   ## returns a list,
			if 'thumbnails' in _album_art_ref:
				_album_art_ref = _album_art_ref['thumbnails']
			# thumbnail [0] is super tiny 32x32? / thumbnail [1] is ok-ish / thumbnail [2] is quite nice quality
			if isinstance(_album_art_ref,list):
				info['track_album_cover'] = _album_art_ref[len(_album_art_ref)-1]['url']
		elif 'thumbnails' in _track:
			_album_art_ref = _track['thumbnails']   ## returns a list
			if isinstance(_album_art_ref,list):
				info['track_album_cover'] = _album_art_ref[len(_album_art_ref)-1]['url']
		return info


	def select_source_helper(self, entity_id=None, old_state=None, new_state=None):
		# redirect call, obviously we got called by status change, so we can call it without argument and let it pick
		return self.select_source()

	def select_source(self, source=None): 
		_LOGGER.debug("select_source("+str(source)+")")
		# source should just be the NAME without DOMAIN, to select it in the dropdown
		if(isinstance(source,str)):
			source = source.replace(DOMAIN_MP+".","")
		# shutdown old player if we're currently playimg
		was_playing = self._playing
		if(self._playing):
			_LOGGER.debug("- was playing")
			old_player = self.hass.states.get(self._remote_player)
			self.media_stop(player=self._remote_player) # important to mention the player here explictly. We're going to change it and stuff runs async
		## get track position of old player TODO
		## set player
		if(source is not None):
			self._update_remote_player(remote_player=DOMAIN_MP+"."+source)
			_LOGGER.debug("- Choosing "+self._remote_player+" as player")
			## try to set drop down
			if(self._select_mediaPlayer != ""):
				if(not self.check_entity_exists(self._select_mediaPlayer)):
					_LOGGER.debug("- Drop down for media player: "+str(self._select_mediaPlayer)+" not found")
				else:
					data = {input_select.ATTR_OPTION: source, ATTR_ENTITY_ID: self._select_mediaPlayer}
					self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SELECT_OPTION, data)
		else:
			# load from dropdown, if that fails, exit
			if(not self._update_remote_player()):
				_LOGGER.error("- _update_remote_player failed")
				return
		## if playing, switch player
		if(was_playing):
			# don't call "_play" here, as that resets the playlist position
			self._next_track_no = max(self._next_track_no-1,-1) # get track will increase the counter
			self._get_track() 
			# seek, if possible
			new_player = self.hass.states.get(self._remote_player)
			if (all(a in old_player.attributes for a in ('media_position','media_position_updated_at','media_duration')) and 'supported_features' in new_player.attributes):
				if(new_player.attributes['supported_features'] | SUPPORT_SEEK):
					now = datetime.datetime.now(datetime.timezone.utc)
					delay = now - old_player.attributes['media_position_updated_at']
					pos = delay.total_seconds() + old_player.attributes['media_position']
					if pos < old_player.attributes['media_duration']:
						data = {'seek_position': pos, ATTR_ENTITY_ID: self._remote_player}
						self.hass.services.call(DOMAIN_MP, media_player.SERVICE_MEDIA_SEEK, data)


	def _update_selects(self, now=None):
		_LOGGER.debug("_update_selects")
		# -- all others -- #
		if(not self.check_entity_exists(self._select_playlist)):
			_LOGGER.debug("- playlist: "+str(self._select_playlist)+" not found")
			self._select_playlist = ""
		if(not self.check_entity_exists(self._select_playMode)):
			_LOGGER.debug("- playmode: "+str(self._select_playMode)+" not found")
			self._select_playMode = ""
		if(not self.check_entity_exists(self._select_playContinuous)):
			_LOGGER.debug("- playContinuous: "+str(self._select_playContinuous)+" not found")
			self._select_playContinuous = ""
		if(not self.check_entity_exists(self._select_mediaPlayer)):
			_LOGGER.debug("- mediaPlayer: "+str(self._select_mediaPlayer)+" not found")
			self._select_mediaPlayer = ""
		if(not self.check_entity_exists(self._select_source)):
			_LOGGER.debug("- Source: "+str(self._select_source)+" not found")
			self._select_source = ""
		# ----------- speaker -----#
		try:
			if(isinstance(self._speakersList,str)):
				speakersList = [self._speakersList]
			else:
				speakersList = list(self._speakersList)
			for i in  range(0,len(speakersList)):
				speakersList[i] = speakersList[i].replace(DOMAIN_MP+".","")
		except:
			speakersList = list()
		# check if the drop down exists
		if(self._select_mediaPlayer == ""):
			_LOGGER.debug("- Drop down for media player not found")
			self._select_mediaPlayer = ""
			# if exactly one unit is provided, stick with it, if it existst
			if(len(speakersList) == 1):
				self._update_remote_player(remote_player=speakersList[0])
				_LOGGER.debug("- Choosing "+self._remote_player+" as player")
		else: #dropdown exists
			defaultPlayer = ''
			if(len(speakersList)<=1):
				if(len(speakersList) == 1):
					defaultPlayer = speakersList[0]
				all_entities = self.hass.states.all()
				for e in all_entities:
					if(e.entity_id.startswith(DOMAIN_MP) and not(e.entity_id.startswith(DOMAIN_MP+"."+DOMAIN))):
						speakersList.append(e.entity_id.replace(DOMAIN_MP+".",""))
			speakersList = list(dict.fromkeys(speakersList))
			data = {input_select.ATTR_OPTIONS: list(speakersList), ATTR_ENTITY_ID: self._select_mediaPlayer}
			self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SET_OPTIONS, data)
			if(defaultPlayer!=''):
				if(defaultPlayer in speakersList):
					data = {input_select.ATTR_OPTION: defaultPlayer, ATTR_ENTITY_ID: self._select_mediaPlayer}
					self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SELECT_OPTION, data)
		
		
		# finally call update playlist to fill the list .. if it exists
		self._update_playlists()
	
	def check_entity_exists(self, e):
		try:
			r = self.hass.states.get(e)
			if(r is None):
				return False
			if(r.state == "unavailable"):
				return False
			return True
		except:
			return False

	def _update_playlists(self, now=None):
		_LOGGER.debug("_update_playlists")
		""" Sync playlists from Google Music library """
		if(self._api == None):
			_LOGGER.debug("- no api, exit")
			return
		if(self._select_playlist == ""):
			_LOGGER.debug("- no playlist select field, exit")
			return

		self._playlist_to_index = {}
		try:
			try:
				self._playlists = self._api.get_library_playlists(limit = 99)
				_LOGGER.debug(" - "+str(len(self._playlists))+" Playlists loaded")
			except:
				self._api = None
				self.exc(resp="ytmusicapi")
				return
			idx = -1
			for playlist in self._playlists:
				idx = idx + 1
				name = playlist.get('title','')
				if len(name) < 1:
					continue
				self._playlist_to_index[name] = idx
				#  the "your likes" playlist won't return a count of tracks
				if not('count' in playlist):
					try:
						extra_info = self._api.get_playlist(playlistId=playlist['playlistId'])
						if('trackCount' in extra_info):
							self._playlists[idx]['count'] = int(extra_info['trackCount'])
						else:
							self._playlists[idx]['count'] = 25
					except:
						if('playlistId' in playlist):
							_LOGGER.debug("- Failed to get_playlist count for playlist ID '"+str(playlist['playlistId'])+"' setting it to 25")
						else:
							_LOGGER.debug("- Failed to get_playlist, no playlist ID")
						self.exc(resp="ytmusicapi")
						self._playlists[idx]['count'] = 25

			if(len(self._playlists)==0):
				self._playlist_to_index["No playlists found"] = 0

			playlists = list(self._playlist_to_index.keys())
			self._attributes['playlists'] = playlists

			data = {"options": list(playlists), "entity_id": self._select_playlist}
			self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SET_OPTIONS, data)
		except:
			self.exc()
			msg= "Caught error while loading playlist. please log for details"
			data = {"title": "yTubeMediaPlayer error", "message": msg}
			self.hass.services.call("persistent_notification","create", data)

		
	def _tracks_to_attribute(self):
		_LOGGER.debug("_tracks_to_attribute")
		self._attributes['total_tracks'] = len(self._tracks)
		self._attributes['tracks'] = []
		for track in self._tracks:
			info = self.extract_info(track)
			self._attributes['tracks'].append(info['track_artist']+" - "+info['track_name'])

	# called from HA when th user changes the input entry, will read selection to membervar
	def _update_playmode(self, entity_id=None, old_state=None, new_state=None):
		_LOGGER.debug("_update_playmode")
		try:
			if(self._select_playContinuous!=""):
				if(self.hass.states.get(self._select_playContinuous).state=="on"):
					self._playContinuous = True
				else:
					self._playContinuous = False
		except:
			_LOGGER.debug("- Selection field "+self._select_playContinuous+" not found, skipping")

		try:
			if(self._select_playMode!=""):
				_playmode = self.hass.states.get(self._select_playMode)
				if _playmode != None:
					if(_playmode.state == PLAYMODE_SHUFFLE):
						self._shuffle = True
						self._shuffle_mode = 1
					elif(_playmode.state == PLAYMODE_RANDOM):
						self._shuffle = True
						self._shuffle_mode = 2
					if(_playmode.state == PLAYMODE_SHUFFLE_RANDOM):
						self._shuffle = True
						self._shuffle_mode = 3
					if(_playmode.state == PLAYMODE_DIRECT):
						self._shuffle = False
				self.set_shuffle(self._shuffle)
		except:
			_LOGGER.debug("- Selection field "+self._select_playMode+" not found, skipping")

		# if we've change the dropdown, reload the playlist and start playing
		# else only change the mode
		if(entity_id == self._select_playMode and old_state != None and new_state != None and self.state == STATE_PLAYING):
			self._allow_next = False # player will change to idle, avoid auto_advance
			return self.play_media(media_type=self._attributes['_media_type'], media_id=self._attributes['_media_id'])


	def _play(self):
		_LOGGER.debug("_play")
		self._next_track_no = -1
		self._get_track() 

	def _get_track(self, entity_id=None, old_state=None, new_state=None, retry=3):
		_LOGGER.debug("_get_track")
		""" Get a track and play it from the track_queue. """
		""" grab next track from prefetched list """
		_track = None
		# get next track nr (randomly or by increasing). 
		if self._shuffle and self._shuffle_mode != 1 and len(self._tracks)>1: #1 will use the list as is (shuffled). 2 and 3 will also take songs randomized
			self._next_track_no = random.randrange(len(self._tracks)) - 1
		else:
			self._next_track_no = self._next_track_no + 1
			_LOGGER.debug("- Playing track nr "+str(self._next_track_no)+" / "+str(len(self._tracks)))
			if self._next_track_no >= len(self._tracks):
				# we've reached the end of the playlist
				if(self._playContinuous):
					# call PLAY_MEDIA with the same arguments
					return self.play_media(media_type=self._attributes['_media_type'], media_id=self._attributes['_media_id'])
				else:
					_LOGGER.info("- End of playlist and playcontinuous is off")
					self._turn_off_media_player()
					return
		try:
			_track = self._tracks[self._next_track_no]
		except IndexError:
			_LOGGER.error("- Out of range! Number of tracks in track_queue == (%s)", len(self._tracks))
			self._api = None
			self._turn_off_media_player()
			return
		if _track is None:
			_LOGGER.error("- _track is None!")
			self._turn_off_media_player()
			return

		self._attributes['current_track'] = self._next_track_no
		self._attributes['videoId'] = _track['videoId']
		if('likeStatus' in _track):
			self._attributes['likeStatus'] = _track['likeStatus']	
		else:	
			self._attributes['likeStatus'] = ""


		""" Find the unique track id. """
		if not('videoId' in _track):
			_LOGGER.error("- Failed to get ID for track: (%s)", _track)
			_LOGGER.error(_track)
			if retry < 1:
				self._turn_off_media_player()
				return
			return self._get_track(retry=retry-1)

		info = self.extract_info(_track)
		self._track_album_name = info['track_album_name']
		self._track_artist_cover = info['track_artist_cover']
		self._track_name = info['track_name']
		self._track_artist = info['track_artist']
		self._track_album_cover = info['track_album_cover']
		
		self.schedule_update_ha_state()

		"""@@@ Get the stream URL and play on media_player @@@"""
		_url = self.get_url(_track['videoId'])
		if(_url == ""):
			if retry < 1:
				_LOGGER.debug("- get track failed to return URL, turning off")
				self._turn_off_media_player()
				return
			else:
				_LOGGER.error("- Retry with: (%i)", retry)
			return self._get_track(retry=retry-1)

		# proxy playback, needed e.g. for sonos
		try:
			if(self._proxy_url!="" and self._proxy_path!=""):
				p1 = datetime.datetime.now()
				open(os.path.join(self._proxy_path,PROXY_FILENAME), 'wb').write(urlopen(_url).read())
				if(self._proxy_url.endswith('/')):
					self._proxy_url = self._proxy_url[:-1]
				_url = self._proxy_url+"/"+PROXY_FILENAME
				t = (datetime.datetime.now() - p1).total_seconds()
				_LOGGER.debug("- proxy loading time: "+str(t)+" sec")
		except:
			_LOGGER.error("The proxy method hit an error, turning off")
			self.exc()
			self._turn_off_media_player()
			return

		### start playback ###
		self._state = STATE_PLAYING
		self._playing = True
		self.schedule_update_ha_state()
		data = {
			ATTR_MEDIA_CONTENT_ID: _url,
			ATTR_MEDIA_CONTENT_TYPE: MEDIA_TYPE_MUSIC,
			ATTR_ENTITY_ID: self._remote_player
			}
		self.hass.services.call(DOMAIN_MP, SERVICE_PLAY_MEDIA, data)
		self._last_auto_advance = datetime.datetime.now() # avoid auto_advance

		### get lyrics after playback started ###
		self._attributes['lyrics'] = 'No lyrics available'
		try:
			l_id = self._api.get_watch_playlist(videoId=_track['videoId'])
			if 'lyrics' in l_id:
				if(l_id['lyrics'] != None):
					lyrics = self._api.get_lyrics(browseId=l_id['lyrics'])
					self._attributes['lyrics'] = lyrics['lyrics']
		except:
			pass
		call_later(self.hass, 15, self._sync_player)


	def get_url(self, videoId=None, retry=False):
		_LOGGER.debug("get_url")
		if(videoId==None):
			_LOGGER.debug("videoId was None")
			return ""
		_url = ""
		self.check_api()
		try:
			_LOGGER.debug("- try to find URL on our own")
			try:
				streamingData=self._api.get_streaming_data(videoId)
			except:
				self._api = None
				self.exc(resp="ytmusicapi")
				return
			if('adaptiveFormats' in streamingData):
				streamingData = streamingData['adaptiveFormats']
			elif('formats' in streamingData): #backup, not sure if that is ever needed, or if adaptiveFormats are always present
				streamingData = streamingData['formats']
			streamId = 0
			# try to find audio only stream
			for i in range(0,len(streamingData)):
				if(streamingData[i]['mimeType'].startswith('audio/mp4')):
					streamId = i
					break
				elif(streamingData[i]['mimeType'].startswith('audio')):
					streamId = i
			if(streamingData[streamId].get('url') is None):
				sigCipher_ch = streamingData[streamId]['signatureCipher']
				sigCipher_ex = sigCipher_ch.split('&')
				res = dict({'s': '', 'url': ''})
				for sig in sigCipher_ex:
					for key in res:
						if(sig.find(key+"=")>=0):
							res[key]=unquote(sig[len(key+"="):])
				# I'm just not sure if the original video from the init will stay online forever
				# in case it's down the player might not load and thus we won't have a javascript loaded
				# so if that happens: we try with this url, might work better (at least the file should be online)
				# the only trouble i could see is that this video is private and thus also won't load the player .. 
				if(self._js == ""):
					self._get_cipher(videoId)
				signature = self._cipher.get_signature(ciphered_signature=res['s'])
				_url = res['url'] + "&sig=" + signature
				_LOGGER.debug("- self decoded URL via cipher")
			else:
				_url = streamingData[streamId]['url']
				_LOGGER.debug("- found URL in api data")

		except Exception as err:
			_LOGGER.error("- Failed to get own(!) URL for track, further details below. Will not try YouTube method")
			_LOGGER.error(traceback.format_exc())
			_LOGGER.error(videoId)
			try:
				_LOGGER.error(self._api.get_song(videoId))
			except:
				self._api = None
				self.exc(resp="ytmusicapi")
				return

		# backup: run youtube stack, only if we failed
		if(_url == ""):
			try:
				streams = YouTube('https://www.youtube.com/watch?v='+videoId).streams
				streams_audio = streams.filter(only_audio=True)
				if(len(streams_audio)):
					_url = streams_audio.order_by('abr').last().url
				else:
					_url = streams.order_by('abr').last().url
				_LOGGER.error("ultimatly")
				_LOGGER.error(_url)

			except Exception as err:
				_LOGGER.error(traceback.format_exc())
				_LOGGER.error("- Failed to get URL with YouTube methode")
				_LOGGER.error(err)
				return ""
		return _url


	def play_media(self, media_type, media_id, _player=None, **kwargs):
		_LOGGER.debug("play_media, media_type: "+str(media_type)+", media_id: "+str(media_id))

		self._started_by = "Browser"
		self._attributes['_media_type'] = media_type
		self._attributes['_media_id'] = media_id

		self.prepare_play()

		# Update player if we got an input 
		if _player is not None:
			self._update_remote_player(remote_player=_player)
			_option = {"option": _player, "entity_id": self._select_mediaPlayer}
			self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SELECT_OPTION, _option)

		# load Tracks depending on input
		try:
			if(media_type == MEDIA_TYPE_PLAYLIST):
				self._tracks = self._api.get_playlist(playlistId=media_id)['tracks']
			elif(media_type == MEDIA_TYPE_ALBUM):
				self._tracks = self._api.get_album(browseId=media_id)['tracks']
			elif(media_type == MEDIA_TYPE_TRACK):
				self._tracks = [self._api.get_song(videoId=media_id)]
			elif(media_id == HISTORY):
				self._tracks = self._api.get_history()
			elif(media_id == USER_TRACKS):
				self._tracks = self._api.get_library_upload_songs(limit=999)
			elif(media_type == CHANNEL):
				# get original playlist from the media_id
				self._tracks = self._api.get_playlist(playlistId=media_id,limit=999)['tracks']
				# select on track randomly
				if(isinstance(self._tracks, list)):
					if(len(self._tracks)>0):
						if(len(self._tracks)>1):
							r_track = self._tracks[random.randrange(0,len(self._tracks)-1)]
						else:
							r_track = self._tracks[0]
						# get a 'channel' based on that random track
						self._tracks = self._api.get_watch_playlist(videoId=r_track['videoId'])['tracks']
				self._started_by = "UI" # technically wrong, but this will enable auto-reload playlist once all tracks are played
			elif(media_type == USER_ALBUM):
				self._tracks = self._api.get_library_upload_album(browseId=media_id)['tracks']
			elif(media_type == USER_ARTIST or media_type == USER_ARTIST_2): # Artist -> Track or Artist [-> Album ->] Track
				self._tracks = self._api.get_library_upload_artist(browseId=media_id, limit=BROWSER_LIMIT)
			else:
				_LOGGER.debug("- error during fetching play_media, turning off")
				self.turn_off()
		except:
			self._api = None
			self.exc(resp="ytmusicapi")
			self.turn_off()
			return

		# mode 1 and 3 shuffle the playlist after generation
		if(isinstance(self._tracks,list)):
			if self._shuffle and self._shuffle_mode != 2 and len(self._tracks)>1:
				random.shuffle(self._tracks)
				_LOGGER.debug("- shuffle new tracklist")
			if(len(self._tracks)==0):
				_LOGGER.error("racklist with 0 tracks loaded, existing")
				self.turn_off()
				return
		else:
			self.turn_off()
			return


		self._tracks_to_attribute()

		# grab track from tracks[] and forward to remote player
		self._next_track_no = -1
		self._play()


	def media_play(self, entity_id=None, old_state=None, new_state=None, **kwargs):
		_LOGGER.debug("media_play")

		"""Send play command."""
		if self._state == STATE_PAUSED:
			self._state = STATE_PLAYING
			self.schedule_update_ha_state()
			data = {ATTR_ENTITY_ID: self._remote_player}
			self.hass.services.call(DOMAIN_MP, 'media_play', data)
		else:
			self._play()
			

	def media_pause(self, **kwargs):
		_LOGGER.debug("media_pause")
		""" Send media pause command to media player """
		self._state = STATE_PAUSED
		#_LOGGER.error(" PAUSE ")
		self.schedule_update_ha_state()
		data = {ATTR_ENTITY_ID: self._remote_player}
		self.hass.services.call(DOMAIN_MP, 'media_pause', data)

	def media_play_pause(self, **kwargs):
		_LOGGER.debug("media_play_pause")
		"""Simulate play pause media player."""
		if self._state == STATE_PLAYING:
			self._allow_next = False
			self.media_pause()
		elif(self._state == STATE_PAUSED):
			self._allow_next = False
			self.media_play()

	def media_previous_track(self, **kwargs):
		"""Send the previous track command."""
		if self._playing:
			self._next_track_no = max(self._next_track_no - 2, -1)
			self._allow_next = False
			self._get_track()

	def media_next_track(self, **kwargs):
		"""Send next track command."""
		if self._playing:
			self._allow_next = False
			self._get_track()

	def media_stop(self, **kwargs):
		"""Send stop command."""
		_LOGGER.debug("media_stop")
		self._state = STATE_IDLE
		self._playing = False
		self._track_artist = None
		self._track_album_name = None
		self._track_name = None
		self._track_album_cover = None
		self.schedule_update_ha_state()
		if('player' in kwargs):
			_LOGGER.debug("- player found")
			data = {ATTR_ENTITY_ID: kwargs.get('player')}
		else:
			data = {ATTR_ENTITY_ID: self._remote_player}
		self.hass.services.call(DOMAIN_MP, 'media_stop', data)
		_LOGGER.debug("- media_stop -> "+self._remote_player)

	def set_shuffle(self, shuffle):
		_LOGGER.debug("set_shuffle: "+str(shuffle))
		self._shuffle = shuffle # True / False
		
		# mode 1 and 3 will shuffle the playlist after generation
		if(isinstance(self._tracks,list)):
			if(self._shuffle and self._shuffle_mode != 2 and len(self._tracks)>1):
				random.shuffle(self._tracks)
		self._tracks_to_attribute()

		if self._shuffle_mode == 1:
			self._attributes['shuffle_mode'] = PLAYMODE_SHUFFLE
		elif self._shuffle_mode == 2:
			self._attributes['shuffle_mode'] = PLAYMODE_RANDOM
		elif self._shuffle_mode == 3:
			self._attributes['shuffle_mode'] = PLAYMODE_SHUFFLE_RANDOM
		else:
			self._attributes['shuffle_mode'] = self._shuffle_mode

		# setting the input will call the "input has changed" - callback .. but that should be alright
		if(self._select_playMode!=""):
			if(self._shuffle):
				data = {input_select.ATTR_OPTION: self._attributes['shuffle_mode'], ATTR_ENTITY_ID: self._select_playMode}
				self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SELECT_OPTION, data)
			else:
				data = {input_select.ATTR_OPTION: PLAYMODE_DIRECT, ATTR_ENTITY_ID: self._select_playMode}
				self.hass.services.call(input_select.DOMAIN, input_select.SERVICE_SELECT_OPTION, data)

		return self.schedule_update_ha_state()


	def set_volume_level(self, volume):
		"""Set volume level."""
		self._volume = round(volume,2)
		data = {ATTR_ENTITY_ID: self._remote_player, 'volume_level': self._volume}
		self.hass.services.call(DOMAIN_MP, 'volume_set', data)
		self.schedule_update_ha_state()

	def volume_up(self, **kwargs):
		"""Volume up the media player."""
		newvolume = min(self._volume + 0.05, 1)
		self.set_volume_level(newvolume)

	def volume_down(self, **kwargs):
		"""Volume down media player."""
		newvolume = max(self._volume - 0.05, 0.01)
		self.set_volume_level(newvolume)

	def mute_volume(self, mute):
		"""Send mute command."""
		if self._is_mute == False:
			self._is_mute = True
		else:
			self._is_mute = False
		self.schedule_update_ha_state()
		data = {ATTR_ENTITY_ID: self._remote_player, "is_volume_muted": self._is_mute}
		self.hass.services.call(DOMAIN_MP, 'volume_mute', data)


	def async_call_method(self, command=None, parameters=None):
		_LOGGER.debug('async_call_method')
		all_params = []
		if parameters:
			for parameter in parameters:
				all_params.append(parameter)
		_LOGGER.debug(command)
		_LOGGER.debug(parameters)
		if(command == SERVICE_CALL_RATE_TRACK):
			if(len(all_params)>=1):
				try:
					arg = 'LIKE'
					if(all_params[0]==SERVICE_CALL_THUMB_UP):
						_LOGGER.debug("rate thumb up")
						arg = 'LIKE'
					elif(all_params[0]==SERVICE_CALL_THUMB_DOWN):
						_LOGGER.debug("rate thumb down")
						arg = 'DISLIKE'
					elif(all_params[0]==SERVICE_CALL_THUMB_MIDDLE):
						_LOGGER.debug("rate thumb middle")
						arg = 'INDIFFERENT'
					elif(all_params[0]==SERVICE_CALL_TOGGLE_THUMB_UP_MIDDLE):
						if('likeStatus' in self._attributes):
							if(self._attributes['likeStatus']=='LIKE'):
								_LOGGER.debug("rate thumb middle")
								arg = 'INDIFFERENT'
							else:
								_LOGGER.debug("rate thumb up")
								arg = 'LIKE'
					self._api.rate_song(videoId=self._attributes['videoId'],rating=arg)
					self._attributes['likeStatus'] = arg
					self.schedule_update_ha_state()
					self._tracks[self._next_track_no]['likeStatus'] = arg
				except:
					self.exc()
		elif(command == SERVICE_CALL_INTERRUPT_START):
			self._update_remote_player()
			#_LOGGER.error(self._remote_player)
			t = self.hass.states.get(self._remote_player)
			#_LOGGER.error(t)
			self._interrupt_data = dict()
			if(all(a in t.attributes for a in ('media_position','media_position_updated_at','media_duration'))):
				now = datetime.datetime.now(datetime.timezone.utc)
				delay = now - t.attributes['media_position_updated_at']
				pos = delay.total_seconds() + t.attributes['media_position']
				if pos < t.attributes['media_duration']:
					self._interrupt_data['pos'] = pos
			#_LOGGER.error(self._interrupt_data)
			#_LOGGER.error(self._remote_player)
			self._interrupt_data['player'] = self._remote_player
			#_LOGGER.error(self._interrupt_data)
			self.media_stop(player=self._remote_player)
			if(self._untrack_remote_player is not None):
				try:
					#_LOGGER.error("calling untrack")
					self._untrack_remote_player()
				except:
					#_LOGGER.error("untrack failed!!")
					pass
		elif(command == SERVICE_CALL_INTERRUPT_RESUME):
			if(self._interrupt_data['player']):
				self._update_remote_player(remote_player=self._interrupt_data['player'])
				self._untrack_remote_player = track_state_change(self.hass, self._remote_player, self._sync_player)
				self._interrupt_data['player'] = None
			self._next_track_no = max(self._next_track_no-1,-1)
			self._get_track() 
			if(self._interrupt_data['pos']):
				player = self.hass.states.get(self._remote_player)
				if(player.attributes['supported_features'] | SUPPORT_SEEK):
					data = {'seek_position': self._interrupt_data['pos'], ATTR_ENTITY_ID: self._remote_player}
					self.hass.services.call(DOMAIN_MP, media_player.SERVICE_MEDIA_SEEK, data)
				self._interrupt_data['pos'] = None
		elif(command == SERVICE_CALL_RELOAD_DROPDOWNS):
			self._update_selects()
		elif(command == SERVICE_CALL_OFF_IS_IDLE): #needed for the MPD but for nobody else
			self._x_to_idle = STATE_OFF 
			_LOGGER.debug("Setting x_is_idle to State Off")
		elif(command == SERVICE_CALL_PAUSED_IS_IDLE): #needed for the Sonos but for nobody else
			self._x_to_idle = STATE_PAUSED 
			_LOGGER.debug("Setting x_is_idle to State Paused")

	

	def exc(self, resp="self"):
		"""Print nicely formated exception."""
		_LOGGER.error("\n\n============= ytube_music_player Integration Error ================")
		if(resp=="self"):
			_LOGGER.error("unfortunately we hit an error, please open a ticket at")
			_LOGGER.error("https://github.com/KoljaWindeler/ytube_music_player/issues")
		else:
			_LOGGER.error("unfortunately we hit an error in the sub api, please open a ticket at")
			_LOGGER.error("https://github.com/sigma67/ytmusicapi/issues")
		_LOGGER.error("and paste the following output:\n")
		_LOGGER.error(traceback.format_exc())
		_LOGGER.error("\nthanks, Kolja")
		_LOGGER.error("============= ytube_music_player Integration Error ================\n\n")


	async def async_browse_media(self, media_content_type=None, media_content_id=None):
		"""Implement the websocket media browsing helper."""
		_LOGGER.debug("async_browse_media")
		self.check_api()

		if media_content_type in [None, "library"]:
			return await self.hass.async_add_executor_job(library_payload, self._api)

		payload = {
			"search_type": media_content_type,
			"search_id": media_content_id,
		}

		response = await build_item_response(self.hass, self._api, payload)
		if response is None:
			raise BrowseError(
				f"Media not found: {media_content_type} / {media_content_id}"
			)
		return response

