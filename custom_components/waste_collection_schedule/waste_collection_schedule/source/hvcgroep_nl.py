import json
import logging
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "HVCGroep"
DESCRIPTION = "Source for the Dutch HVCGroep waste management."
URL = "https://www.hvcgroep.nl/zelf-regelen/afvalkalender"
TEST_CASES = {"Tollebeek": {"postal_code": "8309AV", "house_number": "1"}}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, postal_code, house_number):
        self.postal_code = postal_code
        self.house_number = house_number
        self.icons = {
            "plastic-blik-drinkpak": "mdi:recycle",
            "gft": "mdi:leaf",
            "papier-en-karton": "mdi:archive",
            "restafval": "mdi:trash-can",
        }

    def fetch(self):
        bag_id = 0

        # Retrieve bagid (unique waste management identifier)
        r = requests.get(
            f"https://inzamelkalender.hvcgroep.nl/adressen/{self.postal_code}:{self.house_number}"
        )
        data = json.loads(r.text)

        # Something must be wrong, maybe the address isn't valid? No need to do the extra requests so just return here.
        if len(data) == 0:
            _LOGGER.error("no data found for this address")
            return []

        bag_id = data[0]["bagid"]

        # Retrieve the details about different waste management flows (for example, paper, plastic etc.)
        r = requests.get(
            f"https://inzamelkalender.hvcgroep.nl/rest/adressen/{bag_id}/afvalstromen"
        )
        waste_flows = json.loads(r.text)

        # Retrieve the coming pickup dates for waste.
        r = requests.get(
            f"https://inzamelkalender.hvcgroep.nl/rest/adressen/{bag_id}/ophaaldata"
        )
        data = json.loads(r.text)

        entries = []

        for item in data:
            waste_details = [
                x for x in waste_flows if x["id"] == item["afvalstroom_id"]
            ]
            entries.append(
                Collection(
                    date=datetime.strptime(item["ophaaldatum"], "%Y-%m-%d").date(),
                    t=waste_details[0]["title"],
                    icon=self.icons.get(waste_details[0]["icon"], "mdi:trash-can"),
                )
            )

        return entries
