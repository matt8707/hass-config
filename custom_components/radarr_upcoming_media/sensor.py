"""
Home Assistant component to feed the Upcoming Media Lovelace card with
Radarr upcoming releases.

https://github.com/custom-components/sensor.radarr_upcoming_media

https://github.com/custom-cards/upcoming-media-card

"""
import json
import time
import logging
from datetime import date, datetime
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.helpers.entity import Entity

__version__ = '0.3.2'

_LOGGER = logging.getLogger(__name__)

CONF_DAYS = 'days'
CONF_URLBASE = 'urlbase'
CONF_THEATERS = 'theaters'
CONF_MAX = 'max'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_DAYS, default='60'): cv.string,
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=7878): cv.port,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_URLBASE, default=''): cv.string,
    vol.Optional(CONF_THEATERS, default=True): cv.boolean,
    vol.Optional(CONF_MAX, default=5): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([RadarrUpcomingMediaSensor(hass, config)], True)


class RadarrUpcomingMediaSensor(Entity):

    def __init__(self, hass, conf):
        from pytz import timezone
        self._tz = timezone(str(hass.config.time_zone))
        self.now = str(get_date(self._tz))
        self.ssl = 's' if conf.get(CONF_SSL) else ''
        self.host = conf.get(CONF_HOST)
        self.port = conf.get(CONF_PORT)
        self.apikey = conf.get(CONF_API_KEY)
        self.urlbase = conf.get(CONF_URLBASE)
        if self.urlbase:
            self.urlbase = "{}/".format(self.urlbase.strip('/'))
        self.days = int(conf.get(CONF_DAYS))
        self.theaters = conf.get(CONF_THEATERS)
        self.max_items = int(conf.get(CONF_MAX))
        self._state = None
        self.change_detected = False
        self.data = []
        self.card_json = []
        self.api_json = []

    @property
    def name(self):
        return 'Radarr_Upcoming_Media'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        attributes = {}
        if self.change_detected:
            """Return JSON for the sensor."""
            self.card_json = []
            default = {}
            default['title_default'] = '$title'
            default['line1_default'] = '$release'
            default['line2_default'] = '$genres'
            default['line3_default'] = '$rating - $runtime'
            default['line4_default'] = '$studio'
            default['icon'] = 'mdi:arrow-down-bold'
            self.card_json.append(default)
            for movie in sorted(self.data, key=lambda i: i['path']):
                card_item = {}
                if ('inCinemas' in movie and
                        days_until(movie['inCinemas'], self._tz) > -1):
                        if not self.theaters:
                            continue
                        card_item['airdate'] = movie['inCinemas']
                        if days_until(movie['inCinemas'], self._tz) <= 7:
                            card_item['release'] = 'In Theaters $day'
                        else:
                            card_item['release'] = 'In Theaters $day, $date'
                elif 'physicalRelease' in movie:
                    card_item['airdate'] = movie['physicalRelease']
                    if days_until(movie['physicalRelease'], self._tz) <= 7:
                        card_item['release'] = 'Available $day'
                    else:
                        card_item['release'] = 'Available $day, $date'
                else:
                    continue
                card_item['flag'] = movie.get('hasFile', '')
                card_item['title'] = movie.get('title', '')
                card_item['runtime'] = movie.get('runtime', '')
                card_item['studio'] = movie.get('studio', '')
                card_item['genres'] = movie.get('genres', '')
                if 'ratings' in movie and movie['ratings']['value'] > 0:
                    card_item['rating'] = ('\N{BLACK STAR} ' +
                                           str(movie['ratings']['value']))
                else:
                    card_item['rating'] = ''
                if 'images' in movie:
                    if len(movie['images']):
                        card_item['poster'] = movie['images'][0]
                    if len(movie['images']) > 1 and '.jpg' in movie['images'][1]:
                        card_item['fanart'] = movie['images'][1]
                    else:
                        card_item['fanart'] = ''
                else:
                    continue
                self.card_json.append(card_item)
                self.change_detected = False
        attributes['data'] = self.card_json
        return attributes

    def update(self):
        import requests
        radarr = requests.Session()
        start = get_date(self._tz)
        end = get_date(self._tz, self.days)
        try:
            api = radarr.get(('http{0}://{1}:{2}/{3}api/calendar?start={4}'
                              '&end={5}').format(self.ssl, self.host,
                                                 self.port, self.urlbase,
                                                 start, end),
                             headers={'X-Api-Key': self.apikey}, timeout=10)
        except OSError:
            _LOGGER.warning("Host %s is not available", self.host)
            self._state = '%s cannot be reached' % self.host
            return

        if api.status_code == 200:
            self._state = 'Online'
            if self.days == 1:
                in_cinemas = list(filter(
                    lambda x: x['inCinemas'][:-10] == str(start), api.json()))
                physical_release = (list(filter(lambda x: x[
                    'physicalRelease'][:-10] == str(start), api.json())))
                combined = in_cinemas + physical_release
                self.api_json = combined[:self.max_items]
            else:
                self.api_json = api.json()[:self.max_items]

            """Radarr's API isn't great, so we use tmdb to suppliment"""
            if (media_ids(self.api_json) != media_ids(self.data) or
                    view_count(self.api_json) != view_count(self.data)):
                self.data = self.api_json
                self.change_detected = True
                for movie in self.data:
                    session = requests.Session()
                    try:
                        tmdb_url = session.get('http://api.tmdb.org/3/movie/'
                                               '{}?api_key=1f7708bb9a218ab891'
                                               'a5d438b1b63992'.format(
                                                str(movie['tmdbId'])))
                        tmdb_json = tmdb_url.json()
                    except:
                        _LOGGER.warning('api.themoviedb.org is not responding')
                        return
                    image_url = 'https://image.tmdb.org/t/p/w%s%s'
                    try:
                        movie['images'][0] = image_url % (
                            '500', tmdb_json['poster_path'])
                    except:
                        continue
                    try:
                        movie['images'][1] = image_url % (
                            '780', tmdb_json['backdrop_path'])
                    except:
                        pass
                    if 'inCinemas' in movie and days_until(movie['inCinemas'], self._tz) > -1:
                        movie['path'] = movie['inCinemas']
                    elif 'physicalRelease' in movie:
                        movie['path'] = movie['physicalRelease']
                    else:
                        continue
                    try:
                        movie['genres'] = ', '.join([genre['name'] for genre
                                                     in tmdb_json['genres'
                                                                  ]][:3])
                    except:
                        movie['genres'] = ''
        else:
            self._state = '%s cannot be reached' % self.host


def get_date(zone, offset=0):
    """Get date based on timezone and offset of days."""
    return datetime.date(datetime.fromtimestamp(
        time.time() + 86400 * offset, tz=zone))


def days_until(date, tz):
    from pytz import utc
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date = str(date.replace(tzinfo=utc).astimezone(tz))[:10]
    date = time.strptime(date, '%Y-%m-%d')
    date = time.mktime(date)
    now = datetime.now().strftime('%Y-%m-%d')
    now = time.strptime(now, '%Y-%m-%d')
    now = time.mktime(now)
    return int((date - now) / 86400)


def media_ids(data):
    ids = []
    for media in data:
        if 'tmdbId' in media:
            ids.append(str(media['tmdbId']))
            ids.append(str(media['hasFile']))
        else:
            continue
    return ids


def view_count(data):
    ids = []
    for media in data:
        if 'tmdbId' in media:
            if 'hasFile' in media:
                ids.append(str(media['hasFile']))
            else:
                continue
        else:
            continue
    return ids
