import datetime
import logging

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "EGN Abfallkalender"
DESCRIPTION = "Source for EGN Abfallkalender"
URL = "https://www.egn-abfallkalender.de/kalender"
TEST_CASES = {
    "Grevenbroich": {
        "city": "Grevenbroich",
        "district": "Noithausen",
        "street": "Von-Immelhausen-Straße",
        "housenumber": 12,
    },
    "Dormagen": {
        "city": "Dormagen",
        "district": "Hackenbroich",
        "street": "Aggerstraße",
        "housenumber": 2,
    },
    "Grefrath": {
        "city": "Grefrath",
        "district": "Grefrath",
        "street": "An Haus Bruch",
        "housenumber": 18,
    },
}

_LOGGER = logging.getLogger(__name__)

IconMap = {
    "Grau": "mdi:trash-can",
    "Gelb": "mdi:sack",
    "Blau": "mdi:package-variant",
    "Braun": "mdi:leaf",
}


class Source:
    def __init__(self, city, district, street, housenumber):
        self._city = city
        self._district = district
        self._street = street
        self._housenumber = housenumber

    def fetch(self):
        s = requests.session()
        r = s.get(URL)

        soup = BeautifulSoup(r.text, features="html.parser")
        tag = soup.find("meta", {"name": "csrf-token"})
        if tag is None:
            return []

        headers = {"x-csrf-token": tag["content"]}
        post_data = {
            "city": self._city,
            "district": self._district,
            "street": self._street,
            "street_number": self._housenumber,
        }
        r = s.post(URL, data=post_data, headers=headers)

        data = r.json()

        if data.get("error"):
            for type, errormsg in data["errors"].items():
                _LOGGER.error(f"{type} - {errormsg}")
            return []

        entries = []
        for year, months in data["waste_discharge"].items():
            for month, days in months.items():
                for day, types in days.items():
                    date = datetime.datetime(
                        year=int(year), month=int(month), day=int(day)
                    ).date()
                    for type in types:
                        color = (
                            data["trash_type_colors"]
                            .get(str(type).lower(), type)
                            .capitalize()
                        )
                        entries.append(
                            Collection(date=date, t=color, icon=IconMap.get(color))
                        )

        return entries
