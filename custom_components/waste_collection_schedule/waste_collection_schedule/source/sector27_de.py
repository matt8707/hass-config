import datetime
import json
import logging
import re

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Sector 27"
DESCRIPTION = "Source for Muellkalender in Kreis RE."
URL = "https://muellkalender.sector27.de"
TEST_CASES = {
    "Datteln": {"city": "Datteln", "street": "Am Bahnhof"},
    "Marl": {"city": "Marl", "street": "Ahornweg"},
    "Oer-Erkenschick": {"city": "Oer-Erkenschwick", "street": "An der Zechenbahn"},
}

_LOGGER = logging.getLogger(__name__)

CITIES = {
    "Datteln": {"idCity": 9, "licenseKey": "DTTLN20137REKE382EHSE"},
    "Marl": {"idCity": 3, "licenseKey": "MRL3102HBBUHENWIP"},
    "Oer-Erkenschwick": {"idCity": 8, "licenseKey": "OSC1115KREHDFESEK"},
}

HEADERS = {"user-agent": "Mozilla/5.0"}


class Source:
    def __init__(self, city, street):
        self._city = city
        self._street = street

    def getviewYearRange(self):
        yRange = []

        now = datetime.datetime.now()

        month = now.month
        year = now.year

        d = datetime.datetime(year, 1, 1, hour=12)

        yRange.append(int(datetime.datetime.timestamp(d)))

        # in november & december always fetch next year also
        if month > 8:
            d = datetime.datetime(year + 1, 1, 1, hour=12)
            yRange.append(int(datetime.datetime.timestamp(d)))

        return yRange

    def fetch(self):
        city = CITIES.get(self._city)
        if city is None:
            _LOGGER.error(f"city not found {self._city}")
            return []

        args = city
        args["searchFor"] = self._street

        r = requests.get(
            "https://muellkalender.sector27.de/web/searchForStreets",
            params=args,
            headers=HEADERS,
        )
        streets = {
            e["name"].strip(): e["id"] for (e) in json.loads(extractJson(r.text))
        }

        if self._street not in streets:
            _LOGGER.error(f"street not found {self._street}")
            return []

        args = {
            "licenseKey": city["licenseKey"],
            "cityId": city["idCity"],
            "streetId": streets[self._street],
            "viewrange": "yearRange",
        }

        entries = []

        for dt in self.getviewYearRange():
            args["viewdate"] = dt

            r = requests.get(
                "https://muellkalender.sector27.de/web/fetchPickups",
                params=args,
                headers=HEADERS,
            )
            data = json.loads(extractJson(r.text))

            for ts, pickups in data["pickups"].items():
                for pickup in pickups:
                    type = pickup["label"]
                    pickupdate = datetime.date.fromtimestamp(int(ts))
                    entries.append(Collection(pickupdate, type))

        return entries


def extractJson(text):
    m = re.fullmatch(r"callbackFunc\((.*)\);", text)
    return m.group(1) if m else text
