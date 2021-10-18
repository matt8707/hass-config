#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
#   WAZE ROUTE CALCULATOR
#
#   This module is a modified version of the WazeRouteCalculator developed by
#   Kovács Bálint, Budapest, Hungary, that is part of the Python Standard Library.
#
#   The modifications include:
#       1.  The WazeRouteCalculator object is initialized one time with the region and
#           real time parameters. All other parameters are removed. It only works with
#           GPS cordinates.
#       2.  The from/to GPS cordinates are passed to the calculator on each request
#           rather than a new object being created each time requiring a second request
#           to retrieve the distance/time results.
#
#   The original code can be found on Kovács Bálint's GitHub repo at
#   https://github.com/kovacsbalu/WazeRouteCalculator.
#
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

import logging
import requests
import re


class WRCError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WazeRouteCalculator(object):
    """Calculate actual route time and distance with Waze API"""

    WAZE_URL = "https://www.waze.com/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "referer": WAZE_URL,
    }
    VEHICLE_TYPES = ('TAXI', 'MOTORCYCLE')
    BASE_COORDS = {
        'US': {"lat": 40.713, "lon": -74.006},
        'EU': {"lat": 47.498, "lon": 19.040},
        'IL': {"lat": 31.768, "lon": 35.214},
        'AU': {"lat": -35.281, "lon": 149.128}
    }
    COORD_SERVERS = {
        'US': 'SearchServer/mozi',
        'EU': 'row-SearchServer/mozi',
        'IL': 'il-SearchServer/mozi',
        'AU': 'row-SearchServer/mozi'
    }
    ROUTING_SERVERS = {
        'US': 'RoutingManager/routingRequest',
        'EU': 'row-RoutingManager/routingRequest',
        'IL': 'il-RoutingManager/routingRequest',
        'AU': 'row-RoutingManager/routingRequest'
    }
    COORD_MATCH = re.compile(r'^([-+]?)([\d]{1,2})(((\.)(\d+)(,)))(\s*)(([-+]?)([\d]{1,3})((\.)(\d+))?)$')


    def __init__(self, region, real_time):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())

        region = region.upper()
        if region == 'NA':
            region = 'US'
        self.region = region

        self.real_time = real_time
        self.vehicle_type = ''
        self.route_options = ['AVOID_TRAILS']
        self.avoid_subscription_roads = False
        self.start_coords = ''
        self.end_coords = ''


    def get_route(self, from_lat, from_long, to_lat, to_long,):
        """Get route data from waze"""

        routing_server = self.ROUTING_SERVERS[self.region]

        url_options = {
            "from": f"x:{from_long} y:{from_lat}",
            "to": f"x:{to_long} y:{to_lat}",
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": 1,
            "options": ','.join('%s:t' % route_option for route_option in self.route_options),
        }

        response = requests.get(self.WAZE_URL + routing_server, params=url_options, headers=self.HEADERS)
        response.encoding = 'utf-8'
        response_json = self._check_response(response)
        if response_json:
            if 'error' in response_json:
                raise WRCError(response_json.get("error"))
            else:
                if response_json.get("alternatives"):
                    return [alt['response'] for alt in response_json['alternatives']]
                response_obj = response_json['response']
                if isinstance(response_obj, list):
                    response_obj = response_obj[0]

                return response_obj
        else:
            raise WRCError("empty response")

    @staticmethod
    def _check_response(response):
        """Check waze server response."""
        if response.ok:
            try:
                return response.json()
            except ValueError:
                return None

    def _add_up_route(self, results, stop_at_bounds=False):
        """Calculate route time and distance."""

        time = 0
        distance = 0
        for segment in results:
            if 'crossTime' in segment:
                time += segment['crossTime' if self.real_time else 'crossTimeWithoutRealTime']
            else:
                time += segment['cross_time' if self.real_time else 'cross_time_without_real_time']
            distance += segment['length']
        route_time = time / 60.0
        route_distance = distance / 1000.0

        return route_time, route_distance

    def calc_route_info(self, from_lat, from_long, to_lat, to_long):
        """Calculate best route info."""

        route = self.get_route(from_lat, from_long, to_lat, to_long)

        route_time, route_distance = self._add_up_route(route['result'])

        self.log.info(f"Location: From-({from_lat:0.5f}, {from_long:0.5f}), To-({to_lat:0.5f}, {to_long:0.5f}), Region-{self.region}")
        self.log.info(f"Results : Time-{route_time:0.2f}min, Distance-{route_distance:0.2f}km")
        return route_time, route_distance
