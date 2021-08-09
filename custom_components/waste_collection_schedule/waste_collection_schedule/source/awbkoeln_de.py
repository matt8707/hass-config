import datetime
import json

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "AWB Köln"
DESCRIPTION = "Source for Abfallwirtschaftsbetriebe Köln waste collection."
URL = "https://www.awbkoeln.de"
TEST_CASES = {"Koeln": {"street_code": 2, "building_number": 50}}


class Source:
    def __init__(self, street_code, building_number):
        self._street_code = street_code
        self._building_number = building_number

    def fetch(self):
        args = {
            "street_code": self._street_code,
            "building_number": self._building_number,
        }

        now = datetime.datetime.now()
        args["start_year"] = now.year
        args["start_month"] = now.month
        args["end_year"] = now.year + 1
        args["end_month"] = now.month

        # get json file
        r = requests.get("https://www.awbkoeln.de/api/calendar", params=args)

        data = json.loads(r.text)

        entries = []
        for d in data["data"]:
            date = datetime.date(year=d["year"], month=d["month"], day=d["day"])
            entries.append(Collection(date, d["type"]))

        return entries
