import logging
from datetime import datetime, timedelta

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Recycle!"
DESCRIPTION = "Source for RecycleApp.be"
URL = "https://www.recycleapp.be"
TEST_CASES = {
    "1140 Evere, Bazellaan 1": {
        "postcode": 1140,
        "street": "Bazellaan",
        "house_number": 1,
    }
}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, postcode, street, house_number):
        self._postcode = postcode
        self._street = street
        self._house_number = house_number

    def fetch(self):
        url = "https://recycleapp.be/api/app/v1"
        headers = {
            "x-secret": "Crgja3EGWe8jdapyr4EEoMBgZACYYjRRcRpaMQrLDW9HJBvmgkfGQyYqLgeXPavAGvnJqkV87PBB2b8zx43q46sUgzqio4yRZbABhtKeagkVKypTEDjKfPgGycjLyJTtLHYpzwJgp4YmmCuJZN9ZmJY8CGEoFs8MKfdJpU9RjkEVfngmmk2LYD4QzFegLNKUbcCeAdEW",
            "x-consumer": "recycleapp.be",
            "User-Agent": "",
            "Authorization": "",
        }
        r = requests.get(f"{url}/access-token", headers=headers)
        headers["Authorization"] = r.json()["accessToken"]

        params = {"q": self._postcode}
        r = requests.get(f"{url}/zipcodes", params=params, headers=headers)
        if r.status_code != 200:
            _LOGGER.error("Get zip code failed")
            return []
        zipcodeId = r.json()["items"][0]["id"]

        params = {"q": self._street, "zipcodes": zipcodeId}
        r = requests.get(f"{url}/streets", params=params, headers=headers)
        if r.status_code != 200:
            _LOGGER.error("Get street id failed")
            return []

        for item in r.json()["items"]:
            if item["name"] == self._street:
                streetId = item["id"]
        if streetId is None:
            streetId = r.json()["items"][0]["id"]

        now = datetime.now()
        fromDate = now.strftime("%Y-%m-%d")
        untilDate = (now + timedelta(days=365)).strftime("%Y-%m-%d")
        params = {
            "zipcodeId": zipcodeId,
            "streetId": streetId,
            "houseNumber": self._house_number,
            "fromDate": fromDate,
            "untilDate": untilDate,
            #            "size":100,
        }
        r = requests.get(f"{url}/collections", params=params, headers=headers)
        if r.status_code != 200:
            _LOGGER.error("Get data failed")
            return []

        entries = []
        for item in r.json()["items"]:
            if "exception" in item and "replacedBy" in item["exception"]:
                continue

            date = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S.000Z").date()
            entries.append(Collection(date, item["fraction"]["name"]["en"]))
        return entries
