import json
import logging

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

_LOGGER = logging.getLogger(__name__)

TITLE = "Stadtreinigung Leipzig"
DESCRIPTION = "Source for Stadtreinigung Leipzig."
URL = "https://stadtreinigung-leipzig.de"
TEST_CASES = {"Bahnhofsallee": {"street": "Bahnhofsallee", "house_number": 7}}


class Source:
    def __init__(self, street, house_number):
        self._street = street
        self._house_number = house_number
        self._ics = ICS()

    def fetch(self):
        params = {
            "name": self._street,
        }

        # get list of streets and house numbers
        r = requests.get(
            "https://stadtreinigung-leipzig.de/rest/wastecalendarstreets", params=params
        )

        data = json.loads(r.text)
        if len(data["results"]) == 0:
            _LOGGER.error(f"street not found: {self._street}")
            return []
        street_entry = data["results"].get(self._street)
        if street_entry is None:
            _LOGGER.error(f"street not found: {self._street}")
            return []

        id = street_entry.get(str(self._house_number))
        if id is None:
            _LOGGER.error(f"house_number not found: {self._house_number}")
            return []

        # get ics file
        params = {
            "position_nos": id,
        }
        r = requests.get(
            "https://stadtreinigung-leipzig.de/wir-kommen-zu-ihnen/abfallkalender/ical.ics",
            params=params,
        )
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1].removesuffix(", ")))
        return entries
