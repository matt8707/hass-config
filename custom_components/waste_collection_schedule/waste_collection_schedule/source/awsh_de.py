import json
import logging

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "AWSH"
DESCRIPTION = "Source for Abfallwirtschaft Südholstein"
URL = "https://www.awsh.de"
TEST_CASES = {
    "Reinbek": {"city": "Reinbek", "street": "Ahornweg"},
}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, city, street):
        self._city = city
        self._street = street
        self._ics = ICS()

    def fetch(self):
        # retrieve list of cities
        r = requests.get("https://www.awsh.de/api_v2/collection_dates/1/orte")
        cities = json.loads(r.text)

        # create city to id map from retrieved cities
        city_to_id = {
            city["ortsbezeichnung"]: city["ortsnummer"] for (city) in cities["orte"]
        }

        if self._city not in city_to_id:
            _LOGGER.error(f"city not found: {self._city}")
            return []

        cityId = city_to_id[self._city]

        # retrieve list of streets
        r = requests.get(
            f"https://www.awsh.de/api_v2/collection_dates/1/ort/{cityId}/strassen"
        )
        streets = json.loads(r.text)

        # create street to id map from retrieved cities
        street_to_id = {
            street["strassenbezeichnung"]: street["strassennummer"]
            for (street) in streets["strassen"]
        }

        if self._street not in street_to_id:
            _LOGGER.error(f"street not found: {self._street}")
            return []

        streetId = street_to_id[self._street]

        # retrieve list of waste types
        r = requests.get(
            f"https://www.awsh.de/api_v2/collection_dates/1/ort/{cityId}/abfallarten"
        )
        waste_types = json.loads(r.text)
        wt = "-".join([t["id"] for t in waste_types["abfallarten"]])

        # get ics file
        r = requests.get(
            f"https://www.awsh.de/api_v2/collection_dates/1/ort/{cityId}/strasse/{streetId}/hausnummern/0/abfallarten/{wt}/kalender.ics"
        )

        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
