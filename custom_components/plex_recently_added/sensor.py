"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Plex recently added media.

https://github.com/custom-components/sensor.plex_recently_added

https://github.com/custom-cards/upcoming-media-card

"""
import os.path
import logging
import json
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from datetime import datetime
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity

__version__ = '0.2.9'

_LOGGER = logging.getLogger(__name__)

CONF_DL_IMAGES = 'download_images'
DEFAULT_NAME = 'Plex Recently Added'
CONF_SERVER = 'server_name'
CONF_SSL_CERT = 'ssl_cert'
CONF_TOKEN = 'token'
CONF_MAX = 'max'
CONF_IMG_CACHE = 'img_dir'
CONF_SECTION_TYPES = 'section_types'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_SSL_CERT, default=False): cv.boolean,
    vol.Required(CONF_TOKEN): cv.string,
    vol.Optional(CONF_MAX, default=5): cv.string,
    vol.Optional(CONF_SERVER): cv.string,
    vol.Optional(CONF_DL_IMAGES, default=True): cv.boolean,
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=32400): cv.port,
    vol.Optional(CONF_SECTION_TYPES, 
                default=['movie', 'show']): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_IMG_CACHE, 
                default='/custom-lovelace/upcoming-media-card/images/plex/'): cv.string
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
        self.sections = conf.get(CONF_SECTION_TYPES)
        if self.server_name:
            self.server_ip, self.local_ip, self.port = get_server_ip(
                self.server_name, self.token)
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
        return self._state

    @property
    def device_state_attributes(self):
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
                    card_item['poster'] = image_url(self.url_elements,
                                                    False, poster)
                    card_item['fanart'] = image_url(self.url_elements,
                                                    False, fanart)
                self.card_json.append(card_item)
                self.change_detected = False
        attributes['data'] = json.dumps(self.card_json)
        return attributes

    def update(self):
        import re
        import os
        plex = requests.Session()
        if not self.cert:
            """Default SSL certificate is for plex.tv not our api server"""
            plex.verify = False
        headers = {"Accept": "application/json", "X-Plex-Token": self.token}
        url_base = 'http{0}://{1}:{2}/library/sections'.format(self.ssl,
                                                               self.server_ip,
                                                               self.port)
        all_libraries = url_base + '/all'
        recently_added = (url_base + '/{0}/recentlyAdded?X-Plex-Container-'
                                     'Start=0&X-Plex-Container-Size={1}')

        """Find the ID of all libraries in Plex."""
        sections = []
        try:
            libraries = plex.get(all_libraries, headers=headers, timeout=10)
            for lib_section in libraries.json()['MediaContainer']['Directory']:
                if lib_section['type'] in self.sections:
                    sections.append(lib_section['key'])
        except OSError:
            _LOGGER.warning("Host %s is not available", self.server_ip)
            self._state = '%s cannot be reached' % self.server_ip
            return
        if libraries.status_code == 200:
            self.api_json = []
            self._state = 'Online'
            """Get JSON for each library, combine and sort."""
            for library in sections:
                sub_sec = plex.get(recently_added.format(
                    library, self.max_items * 2), headers=headers, timeout=10) 
                try:
                    self.api_json += sub_sec.json()['MediaContainer']['Metadata']
                except:
                    _LOGGER.warning('No Metadata field for "{}"'.format(sub_sec.json()['MediaContainer']['librarySectionTitle']))
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
                            if image_url(self.url_elements, True, fanart):
                                image = plex.get(image_url(
                                    self.url_elements, True, fanart),
                                    headers=headers, timeout=10).content
                                open(fanart_jpg, 'wb').write(image)
                            else:
                                pass
                        if not os.path.isfile(poster_jpg):
                            if image_url(self.url_elements, True, poster):
                                image = plex.get(image_url(
                                    self.url_elements, True, poster),
                                    headers=headers, timeout=10).content
                                open(poster_jpg, 'wb').write(image)
                            else:
                                continue
            else:
                """Update if media items have changed"""
                if api_ids != data_ids:
                    self.change_detected = True  # Tell attributes to update
                    self.data = self.api_json
        else:
            self._state = '%s cannot be reached' % self.server_ip


def image_url(url_elements, cert_check, img):
    """Plex can resize images with a long & partially % encoded url."""
    from urllib.parse import quote
    ssl, host, local, port, token, self_cert, dl_images = url_elements
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
    url = ('http{0}://{1}:{2}/photo/:/transcode?width=200&height=200'
           '&minSize=1&url={3}&X-Plex-Token={4}').format(ssl, host, port,
                                                         encoded, token)
    """Check if image exists"""
    if not self_cert:
        r = requests.head(url, verify=False)
    else:
        r = requests.head(url)
    if r.status_code == 200:
        return url
    else:
        return False


def get_server_ip(name, token):
    """With a token and server name we get server's ip, local ip, and port"""
    import xml.etree.ElementTree as ET
    from unicodedata import normalize
    plex_tv = requests.get(
        'https://plex.tv/api/servers.xml?X-Plex-Token=' + token, timeout=10)
    plex_xml = ET.fromstring(plex_tv.content)
    for server in plex_xml.findall('Server'):
        server_name = server.get('name').casefold()
        name = name.casefold()
        if normalize('NFKD', server_name) == normalize('NFKD', name):
            return (server.get('address'), server.get('localAddresses'),
                    server.get('port'))


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
