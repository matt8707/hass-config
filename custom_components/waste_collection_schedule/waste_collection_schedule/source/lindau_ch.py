import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Abfall Lindau"
DESCRIPTION = "Source for Lindau waste collection."
URL = "https://www.lindau.ch/abfalldaten"
TEST_CASES = {
    "Tagelswangen": {"city": "Tagelswangen"},
    "Grafstal": {"city": "190"},
}


IconMap = {
    "kehricht": "mdi:trash-can",
    "grungut": "mdi:leaf",
    "hackseldienst": "mdi:leaf",
    "papier und karton": "mdi:package-variant",
    "altmetalle": "mdi:nail",
}


class Source:
    def __init__(self, city):
        self._city = city

    def fetch(self):
        response = requests.get("https://www.lindau.ch/abfalldaten")

        html = BeautifulSoup(response.text, "html.parser")

        table = html.find("table", attrs={"id": "icmsTable-abfallsammlung"})
        data = json.loads(table.attrs["data-entities"])

        entries = []
        for item in data["data"]:
            if (
                self._city in item["abfallkreisIds"]
                or self._city in item["abfallkreisNameList"]
            ):
                next_pickup = item["_anlassDate-sort"].split()[0]
                next_pickup_date = datetime.fromisoformat(next_pickup).date()

                waste_type = BeautifulSoup(item["name"], "html.parser").text
                waste_type_sorted = BeautifulSoup(item["name-sort"], "html.parser").text

                entries.append(
                    Collection(
                        date=next_pickup_date,
                        t=waste_type,
                        icon=IconMap.get(waste_type_sorted, "mdi:trash-can"),
                    )
                )

        return entries
