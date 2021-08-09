import datetime
import json
import logging

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "AWIDO"
DESCRIPTION = "Source for AWIDO waste collection."
URL = "https://www.awido-online.de/"
TEST_CASES = {
    "Schorndorf, Miedelsbacher Straße 30 /1": {
        "customer": "rmk",
        "city": "Schorndorf",
        "street": "Miedelsbacher Straße",
        "housenumber": "30 /1",
    },
    "Altomünster, Maisbrunn": {
        "customer": "lra-dah",
        "city": "Altomünster",
        "street": "Maisbrunn",
    },
    "SOK-Alsmannsdorf": {"customer": "zaso", "city": "SOK-Alsmannsdorf"},
    "Kaufbeuren, Rehgrund": {
        "customer": "kaufbeuren",
        "city": "Kaufbeuren",
        "street": "Rehgrund",
    },
}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, customer, city, street=None, housenumber=None):
        self._customer = customer
        self._city = city
        self._street = street
        self._housenumber = housenumber

    def fetch(self):
        # Retrieve list of places
        r = requests.get(
            f"https://awido.cubefour.de/WebServices/Awido.Service.svc/secure/getPlaces/client={self._customer}"
        )
        places = json.loads(r.text)

        # create city to key map from retrieved places
        city_to_oid = {place["value"].strip(): place["key"] for (place) in places}

        if self._city not in city_to_oid:
            _LOGGER.error(f"city not found: {self._city}")
            return []

        oid = city_to_oid[self._city]

        if self._street is not None:
            r = requests.get(
                f"https://awido.cubefour.de/WebServices/Awido.Service.svc/secure/getGroupedStreets/{oid}",
                params={"client": self._customer},
            )
            streets = json.loads(r.text)

            # create street to key map from retrieved places
            street_to_oid = {
                street["value"].strip(): street["key"] for (street) in streets
            }

            if self._street not in street_to_oid:
                _LOGGER.error(f"street not found: {self._street}")
                return []

            oid = street_to_oid[self._street]

            if self._housenumber is not None:
                r = requests.get(
                    f"https://awido.cubefour.de/WebServices/Awido.Service.svc/secure/getStreetAddons/{oid}",
                    params={"client": self._customer},
                )
                hsnbrs = json.loads(r.text)

                # create housenumber to key map from retrieved places
                hsnbr_to_oid = {
                    hsnbr["value"].strip(): hsnbr["key"] for (hsnbr) in hsnbrs
                }

                if self._housenumber not in hsnbr_to_oid:
                    _LOGGER.error(f"housenumber not found: {self._housenumber}")
                    return []

                oid = hsnbr_to_oid[self._housenumber]

        # get calendar data
        r = requests.get(
            f"https://awido.cubefour.de/WebServices/Awido.Service.svc/secure/getData/{oid}",
            params={"fractions": "", "client": self._customer},
        )
        cal_json = json.loads(r.text)

        # map fraction code to fraction name
        fractions = {fract["snm"]: fract["nm"] for (fract) in cal_json["fracts"]}

        # calendar also contains public holidays. In this case, 'ad' is None
        calendar = [item for item in cal_json["calendar"] if item["ad"] is not None]

        entries = []
        for calitem in calendar:
            date = datetime.datetime.strptime(calitem["dt"], "%Y%m%d").date()

            # add all fractions for this date
            for fracitem in calitem["fr"]:
                waste_type = fractions[fracitem]
                entries.append(Collection(date, waste_type))

        return entries
