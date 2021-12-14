"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Plex recently added media.

https://github.com/custom-components/sensor.plex_recently_added

https://github.com/custom-cards/upcoming-media-card

"""
import os.path
import logging
import json
import aiohttp
import asyncio
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from datetime import datetime, timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity

SCAN_INTERVAL = timedelta(minutes=3)
_LOGGER = logging.getLogger(__name__)


async def fetch(session, url, self, ssl, content):
    try:
        with async_timeout.timeout(8):
            async with session.get(
                url, ssl=ssl, headers={
                    "Accept": "application/json", "X-Plex-Token": self.token}
            ) as response:
                if content:
                    return await response.content.read()
                else:
                    return await response.text()
    except:
        pass


async def request(url, self, content=False, ssl=False):
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url, self, ssl, content)


CONF_DL_IMAGES = 'download_images'
DEFAULT_NAME = 'Plex Recently Added'
CONF_SERVER = 'server_name'
CONF_SSL_CERT = 'ssl_cert'
CONF_TOKEN = 'token'
CONF_MAX = 'max'
CONF_IMG_CACHE = 'img_dir'
CONF_SECTION_TYPES = 'section_types'
CONF_EXCLUDE_KEYWORDS = 'exclude_keywords'
CONF_RESOLUTION = 'image_resolution'
CONF_ON_DECK = 'on_deck'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_SSL_CERT, default=False): cv.boolean,
    vol.Required(CONF_TOKEN): cv.string,
    vol.Optional(CONF_MAX, default=5): cv.string,
    vol.Optional(CONF_SERVER): cv.string,
    vol.Optional(CONF_DL_IMAGES, default=True): cv.boolean,
    vol.Optional(CONF_ON_DECK, default=False): cv.boolean,
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=32400): cv.port,
    vol.Optional(CONF_SECTION_TYPES,
                 default=['movie', 'show']): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_EXCLUDE_KEYWORDS):
                vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_RESOLUTION, default=200): cv.positive_int,
    vol.Optional(CONF_IMG_CACHE,
                 default='/upcoming-media-card-images/plex/'): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    add_devices([PlexRecentlyAddedSensor(hass, config, name)], True)


class PlexRecentlyAddedSensor(Entity):

    def __init__(self, hass, conf, name):
        from pytz import timezone
        self._name = name
        self.conf_dir = str(hass.config.path()) + '/'
        self._dir = conf.get(CONF_IMG_CACHE)
        if self._name:
            self._dir = self._dir + self._name.replace(' ', '_') + '/'
        self.img = '{0}{1}{2}{3}{4}.jpg'.format(
            self.conf_dir, {}, self._dir, {}, {})
        self.img_url = '{0}{1}{2}{3}.jpg'.format({}, self._dir, {}, {})
        self._tz = timezone(str(hass.config.time_zone))
        self.cert = conf.get(CONF_SSL_CERT)
        self.ssl = 's' if conf.get(CONF_SSL) or self.cert else ''
        self.token = conf.get(CONF_TOKEN)
        self.server_name = conf.get(CONF_SERVER)
        self.max_items = int(conf.get(CONF_MAX))
        self.dl_images = conf.get(CONF_DL_IMAGES)
        self.on_deck = conf.get(CONF_ON_DECK)
        self.sections = conf.get(CONF_SECTION_TYPES)
        self.excludes = conf.get(CONF_EXCLUDE_KEYWORDS)
        self.resolution = conf.get(CONF_RESOLUTION)
        if self.server_name:
            _LOGGER.warning(
                "Plex Recently Added: The server_name option has been removed. Use host and port options instead.")
            return
        else:
            self.server_ip = conf.get(CONF_HOST)
            self.local_ip = conf.get(CONF_HOST)
            self.port = conf.get(CONF_PORT)
        self.url_elements = [self.ssl, self.server_ip, self.local_ip,
                             self.port, self.token, self.cert, self.dl_images]
        self.change_detected = False
        self._state = None
        self.card_json = []
        self.api_json = []
        self.data = [{1}]

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        if self.server_name:
            return "server_name is no longer an option, use host and port."
        return self._state

    @property
    def extra_state_attributes(self):
        if self.server_name:
            return
        import math
        attributes = {}
        if self.change_detected:
            self.card_json = []
            defaults = {}
            """First object in JSON sets card defaults"""
            defaults['title_default'] = '$title'
            defaults['line1_default'] = '$episode'
            defaults['line2_default'] = '$release'
            defaults['line3_default'] = '$number - $rating - $runtime'
            defaults['line4_default'] = '$genres'
            defaults['icon'] = 'mdi:eye-off'
            self.card_json.append(defaults)
            """Format Plex API values for card's JSON"""
            for media in self.data:
                card_item = {}
                if 'ratingKey' in media:
                    key = media['ratingKey']
                else:
                    continue
                if 'addedAt' in media:
                    card_item['airdate'] = datetime.utcfromtimestamp(
                        media['addedAt']).strftime('%Y-%m-%dT%H:%M:%SZ')
                else:
                    continue
                if 'originallyAvailableAt' in media:
                    card_item['aired'] = media.get('originallyAvailableAt', '')
                else:
                    card_item['aired'] = ''
                if days_since(media['addedAt'], self._tz) <= 7:
                    card_item['release'] = '$day, $date $time'
                else:
                    card_item['release'] = '$day, $date $time'
                if 'viewCount' in media:
                    card_item['flag'] = False
                else:
                    card_item['flag'] = True
                if media['type'] == 'movie':
                    card_item['title'] = media.get('title', '')
                    card_item['episode'] = ''
                elif media['type'] == 'episode':
                    card_item['title'] = media.get('grandparentTitle', '')
                    card_item['episode'] = media.get('title', '')
                    card_item['number'] = ('S{:02d}E{:02d}').format(
                        media.get('parentIndex', 0), media.get('index', 0))
                else:
                    continue
                if media.get('duration', 0) > 0:
                    card_item['runtime'] = math.floor(
                        media['duration'] / 60000)
                if 'studio' in media:
                    card_item['studio'] = media.get('studio', '')
                if 'Genre' in media:
                    card_item['genres'] = ', '.join(
                        [genre['tag'] for genre in media['Genre']][:3])
                if media.get('rating', 0) > 0:
                    card_item['rating'] = ('\N{BLACK STAR} ' +
                                           str(media['rating']))
                else:
                    card_item['rating'] = ''
                if media['type'] == 'movie':
                    poster = media.get('thumb', '')
                    fanart = media.get('art', '')
                elif media['type'] == 'episode':
                    poster = media.get('grandparentThumb', '')
                    fanart = media.get('grandparentArt', '')
                else:
                    continue
                if self.dl_images:
                    if os.path.isfile(self.img.format('www', 'p', key)):
                        card_item['poster'] = self.img_url.format('/local',
                                                                  'p', key)
                    else:
                        continue
                    if os.path.isfile(self.img.format('www', 'f', key)):
                        card_item['fanart'] = self.img_url.format('/local',
                                                                  'f', key)
                    else:
                        card_item['fanart'] = ''
                else:
                    card_item['poster'] = image_url(self,
                                                    False, poster, self.resolution)
                    card_item['fanart'] = image_url(self,
                                                    False, fanart, self.resolution)
                should_add = True
                if self.excludes:
                    for exclude in self.excludes:
                        if exclude.lower() in card_item['title'].lower():
                            should_add = False
                if should_add:
                    self.card_json.append(card_item)
                self.change_detected = False
        attributes['data'] = self.card_json
        return attributes

    async def async_update(self):
        import os
        import re
        if self.server_name:
            return
        url_base = 'http{0}://{1}:{2}/library/sections'.format(self.ssl,
                                                               self.server_ip,
                                                               self.port)
        all_libraries = url_base + '/all'
        recently_added = (url_base + '/{0}/recentlyAdded?X-Plex-Container-'
                                     'Start=0&X-Plex-Container-Size={1}')
        on_deck = (url_base + '/{0}/onDeck?X-Plex-Container-'
                   'Start=0&X-Plex-Container-Size={1}')

        """Find the ID of all libraries in Plex."""
        sections = []
        try:
            libraries = await request(all_libraries, self)
            if not libraries:
                self._state = '%s cannot be reached' % self.server_ip
                return
            libraries = json.loads(libraries)
            for lib_section in libraries['MediaContainer']['Directory']:
                if lib_section['type'] in self.sections:
                    sections.append(lib_section['key'])
        except OSError:
            _LOGGER.warning("Host %s is not available", self.server_ip)
            self._state = '%s cannot be reached' % self.server_ip
            return
        self.api_json = []
        self._state = 'Online'
        """Get JSON for each library, combine and sort."""
        for library in sections:
            recent_or_deck = on_deck if self.on_deck else recently_added
            sub_sec = await request(recent_or_deck.format(
                library, self.max_items * 2), self)
            sub_sec = json.loads(sub_sec)
            try:
                self.api_json += sub_sec['MediaContainer']['Metadata']
            except:
                pass
        self.api_json = sorted(self.api_json, key=lambda i: i['addedAt'],
                               reverse=True)[:self.max_items]

        """Update attributes if view count changes"""
        if view_count(self.api_json) != view_count(self.data):
            self.change_detected = True
            self.data = self.api_json

        api_ids = media_ids(self.api_json, True)
        data_ids = media_ids(self.data, True)
        if self.dl_images:
            directory = self.conf_dir + 'www' + self._dir
            if not os.path.exists(directory):
                os.makedirs(directory, mode=0o777)

            """Make list of images in dir that use our naming scheme"""
            dir_re = re.compile(r'[pf]\d+\.jpg')  # p1234.jpg or f1234.jpg
            dir_images = list(filter(dir_re.search,
                                     os.listdir(directory)))
            dir_ids = [file[1:-4] for file in dir_images]
            dir_ids.sort(key=int)

            """Update if media items have changed or images are missing"""
            if dir_ids != api_ids or data_ids != api_ids:
                self.change_detected = True  # Tell attributes to update
                self.data = self.api_json
                """Remove images not in list"""
                for file in dir_images:
                    if not any(str(ids) in file for ids in data_ids):
                        os.remove(directory + file)
                """Retrieve image from Plex if it doesn't exist"""
                for media in self.data:
                    if 'type' not in media:
                        continue
                    elif media['type'] == 'movie':
                        poster = media.get('thumb', '')
                        fanart = media.get('art', '')
                    elif media['type'] == 'episode':
                        poster = media.get('grandparentThumb', '')
                        fanart = media.get('grandparentArt', '')
                    else:
                        _LOGGER.error("Media type: %s", media['type'])
                        continue
                    poster_jpg = '{}p{}.jpg'.format(directory,
                                                    media['ratingKey'])
                    fanart_jpg = '{}f{}.jpg'.format(directory,
                                                    media['ratingKey'])
                    if not os.path.isfile(fanart_jpg):
                        fanart_image = await request(image_url(
                            self, True, fanart, self.resolution), self, True, True)
                        if fanart_image:
                            open(fanart_jpg, 'wb').write(fanart_image)
                        else:
                            pass
                    if not os.path.isfile(poster_jpg):
                        poster_image = await request(image_url(
                            self, True, poster, self.resolution), self, True, True)
                        if poster_image:
                            open(poster_jpg, 'wb').write(poster_image)
                        else:
                            continue
        else:
            """Update if media items have changed"""
            if api_ids != data_ids:
                self.change_detected = True  # Tell attributes to update
                self.data = self.api_json


def image_url(self, cert_check, img, resolution=200):
    """Plex can resize images with a long & partially % encoded url."""
    from urllib.parse import quote
    ssl, host, local, port, token, self_cert, dl_images = self.url_elements
    if not cert_check and not self_cert:
        ssl = ''
    if dl_images:
        host = local
    encoded = quote('http{0}://{1}:{2}{3}?X-Plex-Token={4}'.format(ssl,
                                                                   local,
                                                                   port,
                                                                   img,
                                                                   token),
                    safe='')
    url = ('http{0}://{1}:{2}/photo/:/transcode?width={5}&height={5}'
           '&minSize=1&url={3}&X-Plex-Token={4}').format(ssl, host, port,
                                                         encoded, token,
                                                         resolution)
    return url


def days_since(date, tz):
    import time
    from pytz import utc
    date = datetime.utcfromtimestamp(date).isoformat() + 'Z'
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date = str(date.replace(tzinfo=utc).astimezone(tz))[:10]
    date = time.strptime(date, '%Y-%m-%d')
    date = time.mktime(date)
    now = datetime.now().strftime('%Y-%m-%d')
    now = time.strptime(now, '%Y-%m-%d')
    now = time.mktime(now)
    return int((now - date) / 86400)


def media_ids(data, remote):
    ids = []
    for media in data:
        if 'ratingKey' in media:
            ids.append(str(media['ratingKey']))
        else:
            continue
    """Double ids to compare to dir contents (poster & fanart jpgs)"""
    if remote:
        ids = ids * 2
    ids.sort(key=int)
    return ids


def view_count(data):
    ids = []
    for media in data:
        if 'ratingKey' in media:
            if 'viewCount' in media:
                ids.append(str(media['viewCount']))
            else:
                ids.append('0')
        else:
            continue
    return ids
