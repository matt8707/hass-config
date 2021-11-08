import datetime
import json
import time

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Hygea"
DESCRIPTION = "Source for Hygea garbage collection"
URL = "https://www.hygea.be/"
TEST_CASES = {
    "Soignies": {"streetIndex": "3758"},
    "Frameries": {"streetIndex": "4203"},
    "Erquelinnes": {"cp": "6560"},
}

WASTE_MAP = {
    "om": {"type": "Ordures ménagères", "icon": "mdi:trash-can"},
    "pmc": {"type": "PMC", "icon": "mdi:recycle"},
    "sacvert": {"type": "Déchets Organiques", "icon": "mdi:trash-can"},
    "fourth": {"type": "Papier & cartons", "icon": "mdi:leaf"},
}


class Source:
    def __init__(self, streetIndex=None, cp=None):
        self._street_index = streetIndex
        self._cp = cp

    def fetch(self):
        params = {"start": int(time.time()), "end": int(time.time() + 2678400)}
        if self._street_index is not None:
            params["street"] = self._street_index
            response = requests.get(
                "https://www.hygea.be/displaycal.html", params=params
            )
        elif self._cp is not None:
            params["street"] = self._cp
            response = requests.get(
                "https://www.hygea.be/displaycalws.html", params=params
            )

        if not response.ok:
            return []
        data = json.loads(response.text)

        entries = []
        for day in data:
            date = datetime.datetime.strptime(
                day["start"], "%Y-%m-%dT%H:%M:%S%z"
            ).date()

            # example for day["className"]: 12  notadded pos136 om multi
            waste_types = set(day["className"].split())
            for abbr, map in WASTE_MAP.items():
                if abbr in waste_types:
                    c = Collection(date=date, t=map["type"], icon=map["icon"])
                    entries.append(c)

        return entries
