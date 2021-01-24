from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import logging
import datetime
import traceback
from collections import OrderedDict
from ytmusicapi import YTMusic


from homeassistant.const import (
	EVENT_HOMEASSISTANT_START,
	ATTR_ENTITY_ID,
	CONF_DEVICE_ID,
	CONF_NAME,
	CONF_USERNAME,
	CONF_PASSWORD,
	STATE_PLAYING,
	STATE_PAUSED,
	STATE_OFF,
	STATE_IDLE,
	ATTR_COMMAND,
)

from homeassistant.components.media_player.const import (
    MEDIA_CLASS_ALBUM,
    MEDIA_CLASS_ARTIST,
    MEDIA_CLASS_CHANNEL,
    MEDIA_CLASS_DIRECTORY,
    MEDIA_CLASS_EPISODE,
    MEDIA_CLASS_MOVIE,
    MEDIA_CLASS_MUSIC,
    MEDIA_CLASS_PLAYLIST,
    MEDIA_CLASS_SEASON,
    MEDIA_CLASS_TRACK,
    MEDIA_CLASS_TV_SHOW,
    MEDIA_TYPE_ALBUM,
    MEDIA_TYPE_ARTIST,
    MEDIA_TYPE_CHANNEL,
    MEDIA_TYPE_EPISODE,
    MEDIA_TYPE_MOVIE,
    MEDIA_TYPE_PLAYLIST,
    MEDIA_TYPE_SEASON,
    MEDIA_TYPE_TRACK,
    MEDIA_TYPE_TVSHOW,
)


from homeassistant.components.media_player import (
	MediaPlayerEntity,
	PLATFORM_SCHEMA,
	SERVICE_TURN_ON,
	SERVICE_TURN_OFF,
	SERVICE_PLAY_MEDIA,
	SERVICE_MEDIA_PAUSE,
	SERVICE_VOLUME_UP,
	SERVICE_VOLUME_DOWN,
	SERVICE_VOLUME_SET,
	ATTR_MEDIA_VOLUME_LEVEL,
	ATTR_MEDIA_CONTENT_ID,
	ATTR_MEDIA_CONTENT_TYPE,
	DOMAIN as DOMAIN_MP,
)

from homeassistant.components.input_boolean import (
	SERVICE_TURN_OFF as IB_OFF,
	SERVICE_TURN_ON as IB_ON,
	DOMAIN as DOMAIN_IB,
)

from homeassistant.components.media_player.const import (
	SUPPORT_STOP,
	SUPPORT_PLAY,
	SUPPORT_PAUSE,
	SUPPORT_PLAY_MEDIA,
	SUPPORT_PREVIOUS_TRACK,
	SUPPORT_NEXT_TRACK,
	SUPPORT_VOLUME_MUTE,
 	SUPPORT_VOLUME_SET,
	SUPPORT_VOLUME_STEP,
	SUPPORT_TURN_ON,
	SUPPORT_TURN_OFF,
	SUPPORT_SHUFFLE_SET,
	SUPPORT_BROWSE_MEDIA,
	SUPPORT_REPEAT_SET,
	SUPPORT_SELECT_SOURCE,
	SUPPORT_SEEK,
	MEDIA_TYPE_MUSIC,
	REPEAT_MODE_ALL,
    REPEAT_MODE_OFF,
)

import homeassistant.components.input_select as input_select
import homeassistant.components.input_boolean as input_boolean

# Should be equal to the name of your component.
PLATFORM = "media_player"
DOMAIN = "ytube_music_player"

SUPPORT_YTUBEMUSIC_PLAYER = (
	SUPPORT_TURN_ON
	| SUPPORT_TURN_OFF
	| SUPPORT_PLAY
	| SUPPORT_PLAY_MEDIA
	| SUPPORT_PAUSE
	| SUPPORT_STOP
	| SUPPORT_VOLUME_SET
	| SUPPORT_VOLUME_STEP
	| SUPPORT_VOLUME_MUTE
	| SUPPORT_PREVIOUS_TRACK
	| SUPPORT_NEXT_TRACK
	| SUPPORT_SHUFFLE_SET
	| SUPPORT_REPEAT_SET
	| SUPPORT_BROWSE_MEDIA
	| SUPPORT_SELECT_SOURCE
)

SERVICE_CALL_METHOD = "call_method"
ATTR_PARAMETERS = "parameters"
SERVICE_CALL_RATE_TRACK = "rate_track"
SERVICE_CALL_THUMB_UP = "thumb_up"
SERVICE_CALL_THUMB_DOWN = "thumb_down"
SERVICE_CALL_THUMB_MIDDLE = "thumb_middle"
SERVICE_CALL_TOGGLE_THUMB_UP_MIDDLE = "thumb_toggle_up_middle"
SERVICE_CALL_INTERRUPT_START = "interrupt_start"
SERVICE_CALL_INTERRUPT_RESUME = "interrupt_resume"
SERVICE_CALL_RELOAD_DROPDOWNS = "reload_dropdowns"
SERVICE_CALL_OFF_IS_IDLE = "off_is_idle"
SERVICE_CALL_PAUSED_IS_IDLE = "paused_is_idle"


CONF_RECEIVERS = 'speakers'	 # list of speakers (media_players)
CONF_HEADER_PATH = 'header_path'
CONF_SHUFFLE = 'shuffle'
CONF_SHUFFLE_MODE = 'shuffle_mode'
CONF_COOKIE = 'cookie'
CONF_BRAND_ID = 'brand_id'

CONF_PROXY_URL = 'proxy_url'
CONF_PROXY_PATH = 'proxy_path'

CONF_SELECT_SOURCE = 'select_source'
CONF_SELECT_PLAYLIST = 'select_playlist'
CONF_SELECT_SPEAKERS = 'select_speakers'
CONF_SELECT_PLAYMODE = 'select_playmode'
CONF_SELECT_PLAYCONTINUOUS = 'select_playcontinuous'

DEFAULT_SELECT_PLAYCONTINUOUS = input_boolean.DOMAIN + "." + DOMAIN + '_playcontinuous'
DEFAULT_SELECT_SOURCE = input_select.DOMAIN + "." + DOMAIN + '_source'
DEFAULT_SELECT_PLAYLIST = input_select.DOMAIN + "." + DOMAIN + '_playlist'
DEFAULT_SELECT_PLAYMODE = input_select.DOMAIN + "." + DOMAIN + '_playmode'
DEFAULT_SELECT_SPEAKERS = input_select.DOMAIN + "." + DOMAIN + '_speakers'
DEFAULT_HEADER_FILENAME = 'ytube_header.json'
PROXY_FILENAME = "ytube_proxy.mp4"

DEFAULT_SHUFFLE_MODE = 1
DEFAULT_SHUFFLE = True

ERROR_COOKIE = 'ERROR_COOKIE'
ERROR_AUTH_USER = 'ERROR_AUTH_USER'
ERROR_GENERIC = 'ERROR_GENERIC'
ERROR_CONTENTS = 'ERROR_CONTENTS'
ERROR_FORMAT = 'ERROR_FORMAT'
ERROR_NONE = 'ERROR_NONE'

PLAYMODE_SHUFFLE = "Shuffle"
PLAYMODE_RANDOM = "Random"
PLAYMODE_SHUFFLE_RANDOM = "Shuffle Random"
PLAYMODE_DIRECT = "Direct"

LIB_PLAYLIST = 'library_playlists'
LIB_ALBUM = 'library_albums'
LIB_TRACKS = 'library_tracks'
USER_TRACKS = 'user_tracks'
USER_ALBUMS = 'user_albums'
USER_ALBUM = 'user_album'
USER_ARTISTS = 'user_artists'
USER_ARTISTS_2 = 'user_artists2'
USER_ARTIST = 'user_artist'
USER_ARTIST_2 = 'user_artist2'
CHANNEL = 'channel'
HISTORY = 'history'
BROWSER_LIMIT = 500


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend = vol.Schema({
	DOMAIN: vol.Schema({
		vol.Optional(CONF_RECEIVERS): cv.string,
		vol.Optional(CONF_HEADER_PATH, default=DEFAULT_HEADER_FILENAME): cv.string,
		vol.Optional(CONF_SELECT_SOURCE, default=DEFAULT_SELECT_SOURCE): cv.string,
		vol.Optional(CONF_SELECT_PLAYLIST, default=DEFAULT_SELECT_PLAYLIST): cv.string,
		vol.Optional(CONF_SELECT_PLAYMODE, default=DEFAULT_SELECT_PLAYMODE): cv.string,
		vol.Optional(CONF_SELECT_SPEAKERS, default=DEFAULT_SELECT_SPEAKERS): cv.string,
	})
}, extra=vol.ALLOW_EXTRA)

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)


def check_data(user_input):
	"""Check validity of the provided date."""
	ret = {}
	if(CONF_COOKIE in user_input and CONF_HEADER_PATH in user_input):
		# sadly config flow will not allow to have a multiline text field
		# we get a looong string that we've to rearrange into multiline for ytmusic

		# the only thing we need is cookie + x-goog-authuser, lets try to cut this out
		# so the fields are written like 'identifier':'value', but some values actually have ':' inside, bummer.
		c = user_input[CONF_COOKIE]
		clean_cookie = ""
		clean_x_goog_authuser = ""
		## lets try to find the cookie part
		cookie_pos = c.lower().find('cookie')
		if(cookie_pos>=0):
			#_LOGGER.debug("found cookie in text")
			cookie_end = c[cookie_pos:]
			cookie_end_split = cookie_end.split(':')
			if(len(cookie_end_split)>=3):
				#_LOGGER.debug("found three or more sections")
				cookie_length_last_field = cookie_end_split[2].rfind(' ')
				if(cookie_length_last_field>=0):
					#_LOGGER.debug("found a space")
					cookie_length = len(cookie_end_split[0])+1+len(cookie_end_split[1])+1+cookie_length_last_field
					clean_cookie = c[cookie_pos:cookie_pos+cookie_length]
					#_LOGGER.debug(clean_cookie)
		## lets try to find x-auth-part
		xauth_pos = c.lower().find('x-goog-authuser: ')
		if(xauth_pos>=0):
			#_LOGGER.debug("found x-goog-authuser in text")
			#_LOGGER.debug(c[xauth_pos+len('x-goog-authuser: '):])
			xauth_len = c[xauth_pos+len('x-goog-authuser: '):].find(' ')
			#_LOGGER.debug(xauth_len)
			if(xauth_len>=0):
				#_LOGGER.debug("found space in text")
				clean_x_goog_authuser = c[xauth_pos:(xauth_pos+len('x-goog-authuser: ')+xauth_len)]
				#_LOGGER.debug(clean_x_goog_authuser)
		## lets see what we got
		if(clean_cookie!="" and clean_x_goog_authuser!=""):
			# woop woop, this COULD be it
			c = clean_cookie+"\n"+clean_x_goog_authuser+"\n"
		else:
			# well we've failed to find the cookie, the only thing we can do is at least to help with some breaks
			c = c.replace('cookie','\ncookie')
			c = c.replace('Cookie','\nCookie')
			c = c.replace('x-goog-authuser','\nx-goog-authuser')
			c = c.replace('X-Goog-AuthUser','\nX-Goog-AuthUser')
		#_LOGGER.debug("feeding with: ")
		#_LOGGER.debug(c)
		YTMusic.setup(filepath = user_input[CONF_HEADER_PATH], headers_raw = c)
		[ret, msg, api] = try_login(user_input[CONF_HEADER_PATH],"")
	return ret

def try_login(path, brand_id):
	ret = {}
	api = None
	msg = ""
	#### try to init object #####
	try:
		if(brand_id!=""):
			_LOGGER.debug("- using brand ID: "+brand_id)
			api = YTMusic(path,brand_id)
		else:
			_LOGGER.debug("- login without brand ID")
			api = YTMusic(path)
	except KeyError as err:
		_LOGGER.debug("- Key exception")
		if(str(err)=="'contents'"):
			msg = "Format of cookie is OK, found '__Secure-3PAPISID' and '__Secure-3PSID' but can't retrieve any data with this settings, maybe you didn't copy all data?"
			_LOGGER.error(msg)
			ret["base"] = ERROR_CONTENTS
		elif(str(err)=="'Cookie'"):
			msg = "Format of cookie is NOT OK, Field 'Cookie' not found!"
			_LOGGER.error(msg)
			ret["base"] = ERROR_COOKIE
		elif(str(err)=="'__Secure-3PAPISID'" or str(err)=="'__Secure-3PSID'"):
			msg = "Format of cookie is NOT OK, likely missing '__Secure-3PAPISID' or '__Secure-3PSID'"
			_LOGGER.error(msg)
			ret["base"] = ERROR_FORMAT
		else:
			msg = "Some unknown error occured during the cookies usage, key is: "+str(err)
			_LOGGER.error(msg)
			_LOGGER.error("please see below")
			_LOGGER.error(traceback.format_exc())
			ret["base"] = ERROR_GENERIC
	except:
		_LOGGER.debug("- Generic exception")
		msg = "Format of cookie is NOT OK, missing e.g. AuthUser or Cookie"
		_LOGGER.error(msg)
		ret["base"] = ERROR_FORMAT

	#### try to grab library data #####
	if(api == None and ret == {}):
		msg = "Format of cookie seams OK, but the returned sub API object is None"
		_LOGGER.error(msg)
		ret["base"] = ERROR_NONE
	elif(not(api == None) and ret == {}):
		try:
			api.get_library_songs()
		except KeyError as err:
			if(str(err)=="'contents'"):
				msg = "Format of cookie is OK, found '__Secure-3PAPISID' and '__Secure-3PSID' but can't retrieve any data with this settings, maybe you didn't copy all data? Or did you log-out?"
				_LOGGER.error(msg)
				ret["base"] = ERROR_CONTENTS
		except:
			msg = "Running get_library_songs resulted in an exception, no idea why.. honestly"
			_LOGGER.error(msg)
			_LOGGER.error("Please see below")
			_LOGGER.error(traceback.format_exc())
			ret["base"] = ERROR_GENERIC
	return [ret, msg, api]

def ensure_config(user_input):
	"""Make sure that needed Parameter exist and are filled with default if not."""
	out = {}
	#out[CONF_ICON] = DEFAULT_ICON
	out[CONF_NAME] = DOMAIN
	out[CONF_RECEIVERS] = ''
	out[CONF_SHUFFLE] = DEFAULT_SHUFFLE
	out[CONF_SHUFFLE_MODE] = DEFAULT_SHUFFLE_MODE
	out[CONF_SELECT_SOURCE] = DEFAULT_SELECT_SOURCE
	out[CONF_SELECT_PLAYLIST] = DEFAULT_SELECT_PLAYLIST
	out[CONF_SELECT_PLAYMODE] = DEFAULT_SELECT_PLAYMODE
	out[CONF_SELECT_SPEAKERS] = DEFAULT_SELECT_SPEAKERS
	out[CONF_SELECT_PLAYCONTINUOUS] = DEFAULT_SELECT_PLAYCONTINUOUS
	out[CONF_PROXY_PATH] = ""
	out[CONF_PROXY_URL] = ""
	out[CONF_BRAND_ID] = ""
	out[CONF_COOKIE] = ""

	if user_input is not None:
		if CONF_NAME in user_input:
			out[CONF_NAME] = user_input[CONF_NAME]
		if CONF_HEADER_PATH in user_input:
			out[CONF_HEADER_PATH] = user_input[CONF_HEADER_PATH]
		else:
			_LOGGER.error("ohoh no header path in the input, not sure how we got here")
		if CONF_RECEIVERS in user_input:
			out[CONF_RECEIVERS] = user_input[CONF_RECEIVERS]
		if CONF_SHUFFLE in user_input:
			out[CONF_SHUFFLE] = user_input[CONF_SHUFFLE]
		if CONF_SHUFFLE_MODE in user_input:
			out[CONF_SHUFFLE_MODE] = user_input[CONF_SHUFFLE_MODE]
		if CONF_SELECT_SOURCE in user_input:
			out[CONF_SELECT_SOURCE] = user_input[CONF_SELECT_SOURCE]
		if CONF_SELECT_PLAYLIST in user_input:
			out[CONF_SELECT_PLAYLIST] = user_input[CONF_SELECT_PLAYLIST]
		if CONF_SELECT_PLAYMODE in user_input:
			out[CONF_SELECT_PLAYMODE] = user_input[CONF_SELECT_PLAYMODE]
		if CONF_SELECT_SPEAKERS in user_input:
			out[CONF_SELECT_SPEAKERS] = user_input[CONF_SELECT_SPEAKERS]
		if CONF_PROXY_PATH in user_input:
			out[CONF_PROXY_PATH] = user_input[CONF_PROXY_PATH]
		if CONF_PROXY_URL in user_input:
			out[CONF_PROXY_URL] = user_input[CONF_PROXY_URL]
		if CONF_BRAND_ID in user_input:
			out[CONF_BRAND_ID] = user_input[CONF_BRAND_ID]
		if CONF_COOKIE in user_input:
			out[CONF_COOKIE] = user_input[CONF_COOKIE]
		if CONF_SELECT_PLAYCONTINUOUS in user_input:
			out[CONF_SELECT_PLAYCONTINUOUS] = user_input[CONF_SELECT_PLAYCONTINUOUS]
	return out


def create_form(user_input, page=1):
	"""Create form for UI setup."""
	user_input = ensure_config(user_input)
	data_schema = OrderedDict()

	if(page == 1):
		data_schema[vol.Required(CONF_NAME, default=user_input[CONF_NAME])] = str # name of the component without domain
		data_schema[vol.Required(CONF_COOKIE, default=user_input[CONF_COOKIE])] = str # configuration of the cookie
		data_schema[vol.Optional(CONF_RECEIVERS, default=user_input[CONF_RECEIVERS])] = str # default remote_player
		#data_schema[vol.Optional(CONF_SHUFFLE, default=user_input[CONF_SHUFFLE])] = vol.Coerce(bool) # default duffle, TRUE/FALSE
		#data_schema[vol.Optional(CONF_SHUFFLE_MODE, default=user_input[CONF_SHUFFLE_MODE])] = vol.Coerce(int) # [1] = Shuffle .. 2....
		data_schema[vol.Optional(CONF_BRAND_ID, default=user_input[CONF_BRAND_ID])] = str # brand id
		data_schema[vol.Required(CONF_HEADER_PATH, default=user_input[CONF_HEADER_PATH])] = str # file path of the header
	elif(page == 2):
		data_schema[vol.Optional(CONF_SELECT_SPEAKERS, default=user_input[CONF_SELECT_SPEAKERS])] = str # drop down to select remote_player
		data_schema[vol.Optional(CONF_SELECT_SOURCE, default=user_input[CONF_SELECT_SOURCE])] = str # drop down to select playlist / playlist-radio
		data_schema[vol.Optional(CONF_SELECT_PLAYLIST, default=user_input[CONF_SELECT_PLAYLIST])] = str # drop down that holds the playlists
		data_schema[vol.Optional(CONF_SELECT_PLAYCONTINUOUS, default=user_input[CONF_SELECT_PLAYCONTINUOUS])] = str # select of input_boolean -> continuous on/off

		data_schema[vol.Optional(CONF_PROXY_PATH, default=user_input[CONF_PROXY_PATH])] = str # select of input_boolean -> continuous on/off
		data_schema[vol.Optional(CONF_PROXY_URL, default=user_input[CONF_PROXY_URL])] = str # select of input_boolean -> continuous on/off

	return data_schema
