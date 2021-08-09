#!/usr/bin/env python3

import datetime
import json

import requests

SERVICE_DOMAINS = {
    "aachen": "Aachen",
    "zew2": "AWA Entsorgungs GmbH",
    "aw-bgl2": "Bergisch Gladbach",
    "bav": "Bergischer Abfallwirtschaftverbund",
    "din": "Dinslaken",
    "dorsten": "Dorsten",
    "gt2": "Gütersloh",
    "hlv": "Halver",
    "coe": "Kreis Coesfeld",
    "krhs": "Kreis Heinsberg",
    "pi": "Kreis Pinneberg",
    "krwaf": "Kreis Warendorf",
    "lindlar": "Lindlar",
    "stl": "Lüdenscheid",
    "nds": "Norderstedt",
    "nuernberg": "Nürnberg",
    "roe": "Roetgen",
    "wml2": "EGW Westmünsterland",
}


class AbfallnaviDe:
    def __init__(self, service_domain):
        self._service_domain = service_domain
        self._service_url = f"https://{service_domain}-abfallapp.regioit.de/abfall-app-{service_domain}/rest"

    def _fetch(self, path, params=None):
        r = requests.get(f"{self._service_url}/{path}", params=params)
        r.encoding = "utf-8"  # requests doesn't guess the encoding correctly
        return r.text

    def _fetch_json(self, path, params=None):
        return json.loads(self._fetch(path, params=params))

    def get_cities(self):
        """Return all cities of service domain."""
        cities = self._fetch_json("orte")
        result = {}
        for city in cities:
            result[city["id"]] = city["name"]
        return result

    def get_city_id(self, city):
        """Return id for given city string."""
        cities = self.get_cities()
        return self._find_in_inverted_dict(cities, city)

    def get_streets(self, city_id):
        """Return all streets of a city."""
        streets = self._fetch_json(f"orte/{city_id}/strassen")
        result = {}
        for street in streets:
            result[street["id"]] = street["name"]
        return result

    def get_street_id(self, city_id, street):
        """Return id for given street string."""
        streets = self.get_streets(city_id)
        return self._find_in_inverted_dict(streets, street)

    def get_house_numbers(self, street_id):
        """Return all house numbers of a street."""
        house_numbers = self._fetch_json(f"strassen/{street_id}")
        result = {}
        for hausNr in house_numbers.get("hausNrList", {}):
            # {"id":5985445,"name":"Adalbert-Stifter-Straße","hausNrList":[{"id":5985446,"nr":"1"},
            result[hausNr["id"]] = hausNr["nr"]
        return result

    def get_house_number_id(self, street_id, house_number):
        """Return id for given house number string."""
        house_numbers = self.get_house_numbers(street_id)
        return self._find_in_inverted_dict(house_numbers, house_number)

    def get_waste_types(self):
        waste_types = self._fetch_json("fraktionen")
        result = {}
        for waste_type in waste_types:
            result[waste_type["id"]] = waste_type["name"]
        return result

    def _get_dates(self, target, id, waste_types=None):
        # retrieve collections
        args = []

        if waste_types is None:
            waste_types = self.get_waste_types()

        for f in waste_types.keys():
            args.append(("fraktion", f))

        results = self._fetch_json(f"{target}/{id}/termine", params=args)

        entries = []
        for r in results:
            date = datetime.datetime.strptime(r["datum"], "%Y-%m-%d").date()
            fraktion = waste_types[r["bezirk"]["fraktionId"]]
            entries.append([date, fraktion])
        return entries

    def get_dates_by_street_id(self, street_id):
        return self._get_dates("strassen", street_id, waste_types=None)

    def get_dates_by_house_number_id(self, house_number_id):
        return self._get_dates("hausnummern", house_number_id, waste_types=None)

    def get_dates(self, city, street, house_number=None):
        """Get dates by strings only for convenience."""
        # find city_id
        city_id = self.get_city_id(city)
        if city_id is None:
            raise Exception(f"No id found for city: {city}")

        # find street_id
        street_id = self.get_street_id(city_id, street)
        if street_id is None:
            raise Exception(f"No id found for street: {street}")

        # find house_number_id (which is optional: not all house number do have an id)
        house_number_id = self.get_house_number_id(street_id, house_number)

        # return dates for specific house number of street if house number
        # doesn't have an own id
        if house_number_id is not None:
            return self.get_dates_by_house_number_id(house_number_id)
        else:
            return self.get_dates_by_street_id(street_id)

    def _find_in_inverted_dict(self, mydict, value):
        inverted_dict = dict(map(reversed, mydict.items()))
        return inverted_dict.get(value)


def main():
    aachen = AbfallnaviDe("aachen")
    print(aachen.get_dates("Aachen", "Abteiplatz", "7"))

    lindlar = AbfallnaviDe("lindlar")
    print(lindlar.get_dates("Lindlar", "Aggerweg"))

    roe = AbfallnaviDe("roe")
    print(roe.get_dates("Roetgen", "Am Sportplatz", "2"))


if __name__ == "__main__":
    main()
