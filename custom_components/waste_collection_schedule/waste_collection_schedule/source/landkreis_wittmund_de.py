import requests
import json
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS
from bs4 import BeautifulSoup

TITLE = "Landkreis-Wittmund.de"
DESCRIPTION = "Source for Landkreis Wittmund waste collection."
URL = "https://www.landkreis-wittmund.de/Leben-Wohnen/Wohnen/Abfall/Abfuhrkalender/"
AUTOCOMPLETE_URL = "https://www.landkreis-wittmund.de/output/autocomplete.php?out=json&type=abto&mode=&select=2&refid={}&term="
DOWNLOAD_URL = "https://www.landkreis-wittmund.de/output/options.php?ModID=48&call=ical&ArtID%5B0%5D=3105.1&ArtID%5B1%5D=1.4&ArtID%5B2%5D=1.2&ArtID%5B3%5D=1.3&ArtID%5B4%5D=1.1&pois={}&alarm=0"

TEST_CASES = {
    "CityWithoutStreet": {
        "city": "Werdum",
    },
    "CityWithStreet": {
        "city": "Werdum",
        "street": "alle Straßen",
    },
}

class Source:
    def __init__(self, city, street=None):
        self._city = city
        self._street = street
        self._ics = ICS()

    def fetch(self):
        cityId = self.fetch_city_id(self._city)
        streetId = self.fetch_street_id(cityId, self._street)

        return self.fetch_ics(DOWNLOAD_URL.format(streetId))

    def is_city_selection(self, tag, cityName):
        return tag['value'] != "" and tag.string == self._city

    def fetch_city_id(self, cityName):
        r = requests.get(URL)
        if not r.ok:
            raise Exception(
                "Error: failed to fetch url: {}".format(
                    URL
                )
            )

        soup = BeautifulSoup(r.text, 'html.parser')
        citySelection = [ a for a in soup.select('#sf_locid > option[value]') if self.is_city_selection(a, cityName) ]
        if len(citySelection) == 0:
            raise Exception(
                "Error: could not find id for city: '{}'".format(
                    cityName
                )
            )

        if len(citySelection) > 1:
            raise Exception(
                "Error: non-unique match for city: '{}'".format(
                    cityName
                )
            )

        return citySelection[0]['value']

    def fetch_street_id(self, cityId, streetName):
        r = requests.get(AUTOCOMPLETE_URL.format(cityId, streetName), headers={
            "Referer": URL
        })

        if not r.ok:
            raise Exception(
                "Error: failed to fetch url: {}".format(
                    AUTOCOMPLETE_URL.format(cityId, streetName)
                )
            )

        streets = json.loads(r.text)
        if streetName != None:
            streetId = [ item[0] for item in streets if streetName in item[1] ]
        else:
            streetId = [ item[0] for item in streets ]

        if len(streetId) == 0:
            raise Exception(
                "Error: could not find streets for city id / street: {}, '{}'".format(
                    cityId,
                    streetName
                )
            )

        if len(streetId) > 1:
            raise Exception(
                "Error: non-unique match for city id / street: {}, '{}'".format(
                    cityId,
                    streetName
                )
            )

        return streetId[0]

    def fetch_ics(self, url):
        r = requests.get(url, headers={
            "Referer": URL
        })

        if not r.ok:
            raise Exception(
                "Error: failed to fetch url: {}".format(
                    url
                )
            )

        # parse ics file
        r.encoding = "utf-8"
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
