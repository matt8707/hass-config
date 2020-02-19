"""

Support for getting data from krisinformation.se.

Data is fetched from https://api.krisinformation.se/v1/capmessage?format=json

Example configuration

sensor:
  - platform: krisinformation

Example advanced configuration

sensor:
  - platform: krisinformation
    latitude: !secret lat_coord
    longitude: !secret long_coord
    county: 'Stockholms län'
    radius: 100
"""
import logging
import json
from datetime import timedelta
from math import radians, sin, cos, acos
import requests

from urllib.request import urlopen
import aiohttp

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME, CONF_RADIUS)
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util
from homeassistant.components.rest.sensor import RestData

__version__ = '1.0.0'

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Krisinformation'

CONF_COUNTY = 'county'
CONF_COUNTRY = 'country'

SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_RADIUS, default=50) : cv.positive_int,
    vol.Optional(CONF_COUNTY) : cv.string,
    vol.Optional(CONF_COUNTRY) : cv.string,
    vol.Optional(CONF_LATITUDE): cv.latitude,
    vol.Optional(CONF_LONGITUDE): cv.longitude
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Krisinformation sensor."""
    name = config.get(CONF_NAME)
    latitude = config.get(CONF_LATITUDE) if config.get(CONF_LATITUDE) is not None else hass.config.latitude
    longitude = config.get(CONF_LONGITUDE) if config.get(CONF_LONGITUDE) is not None else hass.config.longitude
    radius = config.get(CONF_RADIUS)
    county = config.get(CONF_COUNTY)
    country = config.get(CONF_COUNTRY)
    if config.get(CONF_COUNTRY) is not None and config.get(CONF_NAME) is None:
        name = "{} {}".format(DEFAULT_NAME, country)
    elif config.get(CONF_NAME) is None:
        name = DEFAULT_NAME


    api = KrisinformationAPI(longitude, latitude, county, radius, country)

    add_entities([KrisinformationSensor(api, name)], True)


class KrisinformationSensor(Entity):
    """Representation of a Krisinformation sensor."""

    def __init__(self, api, name):
        """Initialize a Krisinformation sensor."""
        self._api = api
        self._name = name
        self._icon = "mdi:alert"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._api.data['state']

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        data = {
            'messages': self._api.attributes['messages']
        }

        return data

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    def update(self):
        """Get the latest data from the Krisinformation API."""
        self._api.update()


class KrisinformationAPI:
    """Get the latest data and update the states."""

    def __init__(self, longitude, latitude, county, radius, country):
        """Initialize the data object."""
        
        self.slat = latitude
        self.slon = longitude
        self.county = county
        self.radius = radius
        self.country = country
        self.attributes = {}
        self.attributes["messages"] = []
        self.data = {}
        self.available = True
        self.update()
        self.data['state'] = "No new messages"

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from Krisinformation."""
        try:
            _LOGGER.debug("Trying to update")
            response = urlopen('https://api.krisinformation.se/v2/feed?format=json')
            data = response.read().decode('utf-8')
            jsondata = json.loads(data)

            self.data['state'] = "No new messages"
            self.attributes["messages"] = []
            for index, element in enumerate(jsondata):
                self.make_object(index = index, element = element)
            
            self.data['attributes'] = self.attributes
            self.available = True
        except Exception as e:
            _LOGGER.error("Unable to fetch data from Krisinformation.")
            _LOGGER.error(str(e))
            self.available = False
            
    def make_object(self, index, element):
        message = {}
        message['Area'] = []
        
        distance = None
        within_range = False
        is_in_county = False
        is_in_country = False
        
        for count, area in enumerate(element['Area']):
            message['Area'].append({ "Type" : area['Type'], "Description" : area['Description'], "Coordinate" : area['Coordinate']})
            
            if self.country is not None:
                if area['Type'] == 'Country':
                    if self.country.lower() in area['Description'].lower():
                        is_in_country = True
                
            else:
                if self.county is not None:
                    if area['Type'] == 'County':
                        if self.county.lower() in area['Description'].lower():
                            is_in_county = True
                    
                distance = self.calculate_distance(coords = area['Coordinate'])
                if float(distance) < float(self.radius):
                    within_range = True
        
        if within_range or is_in_county or is_in_country:
            message['ID'] = element['Identifier']
            message['Message'] = element['PushMessage']
            message['Updated'] = element['Updated']
            message['Published'] = element['Published']
            message['Headline'] = element['Headline']
            message['Preamble'] = element['Preamble']
            message['BodyText'] = element['BodyText']
            message['Web'] = element['Web']
            message['Language'] = element['Language']
            message['Event'] = element['Event']
            message['SenderName'] = element['SenderName']
            message['Links'] = []
            if element['BodyLinks'] is not None:
                for numbers, link in enumerate(element['BodyLinks']):
                    message['Links'].append(link['Url'])
            message['SourceID'] = element['SourceID']
            
            self.attributes["messages"].append(message)
            if element['Event'] == "Alert":
                self.state = "Alert"
            else:
                self.state = "News"
            self.data['state'] = self.state
            
    def calculate_distance(self, coords):
        coords = coords.split()
        coords = coords[0].split(',')
        elon = coords[0]
        elat = coords[1]
        
        #Convert coordinates to radians
        elat2 = radians(float(elat))
        slat2 = radians(float(self.slat))
        elon2 = radians(float(elon))
        slon2 = radians(float(self.slon))
        
        #Calculate the distance between them
        dist = 6371.01 * acos(sin(slat2)*sin(elat2) + cos(slat2)*cos(elat2)*cos(slon2 - elon2))

        return dist