import datetime
import json
import logging

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "The Hills Shire Council"
DESCRIPTION = "Source for Hills Shire Council, Sidney, Australia waste collection."
URL = "https://www.thehills.nsw.gov.au/"
TEST_CASES = {
    "Annangrove, Amanda Place 10": {
        "suburb": "ANNANGROVE",
        "street": "Amanda Place",
        "houseNo": 10,
    }
}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, suburb, street, houseNo):
        self._suburb = suburb
        self._street = street
        self._houseNo = str(houseNo)
        self._url = "https://apps.thehills.nsw.gov.au/seamlessproxy/api"

    def fetch(self):
        # get list of suburbs
        r = requests.get(f"{self._url}/suburbs/get")
        data = json.loads(r.text)

        suburbs = {}
        for entry in data:
            suburbs[entry["Suburb"].strip()] = entry["SuburbKey"]

        # check if suburb exists
        if self._suburb not in suburbs:
            _LOGGER.error(f"suburb not found: {self._suburb}")
            return []
        suburbKey = suburbs[self._suburb]

        # get list of streets for selected suburb
        r = requests.get(f"{self._url}/streets/{suburbKey}")
        data = json.loads(r.text)

        streets = {}
        for entry in data:
            streets[entry["Street"].strip()] = entry["StreetKey"]

        # check if street exists
        if self._street not in streets:
            _LOGGER.error(f"street not found: {self._street}")
            return []
        streetKey = streets[self._street]

        # get list of house numbers for selected street
        params = {"streetkey": streetKey, "suburbKey": suburbKey}
        r = requests.get(
            f"{self._url}/properties/GetPropertiesByStreetAndSuburbKey", params=params,
        )
        data = json.loads(r.text)

        houseNos = {}
        for entry in data:
            houseNos[
                str(int(entry["HouseNo"])) + entry.get("HouseSuffix", "").strip()
            ] = entry["PropertyKey"]

        # check if house number exists
        if self._houseNo not in houseNos:
            _LOGGER.error(f"house number not found: {self._houseNo}")
            return []
        propertyKey = houseNos[self._houseNo]

        # get collection schedule
        r = requests.get(f"{self._url}/services/{propertyKey}")
        data = json.loads(r.text)

        entries = []
        for entry in data:
            name = entry["Name"]
            for dateStr in entry["CollectionDays"]:
                date = datetime.datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%S").date()
                entries.append(Collection(date, name))
        return entries
