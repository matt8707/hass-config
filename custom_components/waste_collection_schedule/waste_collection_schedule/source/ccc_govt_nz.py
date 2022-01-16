import datetime

import requests
from waste_collection_schedule import Collection

TITLE = "Christchurch City Council"
DESCRIPTION = "Source for Christchurch City Council."
URL = "https://ccc.govt.nz/services/rubbish-and-recycling/collections"
TEST_CASES = {"53 Hereford Street": {"address": "53 Hereford Street"}}


class Source:
    def __init__(self, address):
        self._address = address

    def fetch(self):
        entries = []

        # Find the Rating Unit ID by the physical address
        # While a property may have more than one address, bins are allocated by each Rating Unit
        addressQuery = {
            "q": self._address,
            "status": "current",
            "crs": "epsg:4326",
            "limit": 1,
        }
        r = requests.get(
            "https://opendata.ccc.govt.nz/CCCSearch/rest/address/suggest",
            params=addressQuery,
        )
        address = r.json()

        # Find the Bin service by Rating Unit ID
        binsQuery = {"ID": address[0]["RatingUnitID"]}
        r = requests.get(
            "https://ccc.govt.nz/services/rubbish-and-recycling/collections/getProperty",
            params=binsQuery,
        )
        bins = r.json()

        # Deduplicate the Bins in case the Rating Unit has more than one of the same Bin type
        bins = {each["material"]: each for each in bins["bins"]["collections"]}.values()

        # Process each Bin
        for bin in bins:
            entries.append(
                Collection(
                    datetime.datetime.strptime(
                        bin["next_planned_date"], "%Y-%m-%d"
                    ).date(),
                    bin["material"],
                )
            )

        return entries
