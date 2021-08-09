from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Abfall Zollernalbkreis"
DESCRIPTION = "Source for Abfallwirtschaft Zollernalbkreis waste collection."
URL = "https://www.abfallkalender-zak.de"
TEST_CASES = {
    "Ebingen": {
        "city": "2,3,4",
        "street": "3",
        "types": [
            "restmuell",
            "gelbersack",
            "papiertonne",
            "biomuell",
            "gruenabfall",
            "schadstoffsammlung",
            "altpapiersammlung",
            "schrottsammlung",
            "weihnachtsbaeume",
            "elektrosammlung",
        ],
    },
    "Erlaheim": {
        "city": "79",
        "street": "",
        "types": [
            "restmuell",
            "gelbersack",
            "papiertonne",
            "biomuell",
            "gruenabfall",
            "schadstoffsammlung",
            "altpapiersammlung",
            "schrottsammlung",
            "weihnachtsbaeume",
            "elektrosammlung",
        ],
    },
}


class Source:
    def __init__(self, city, types, street=None):
        self._city = city
        self._street = street
        self._types = types
        self._ics = ICS()

    def fetch(self):
        now = datetime.now()
        entries = self.fetch_year(now.year, self._city, self._street, self._types)
        if now.month == 12:
            # also get data for next year if we are already in december
            try:
                entries.extend(
                    self.fetch_year(
                        (now.year + 1), self._city, self._street, self._types
                    )
                )
            except Exception:
                # ignore if fetch for next year fails
                pass
        return entries

    def fetch_year(self, year, city, street, types):
        args = {
            "city": city,
            "street": street,
            "year": year,
            "types[]": types,
            "go_ics": "Download",
        }

        # get ics file
        r = requests.get("https://www.abfallkalender-zak.de", params=args)

        # parse ics file
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
