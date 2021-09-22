import datetime
import re

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Wolfsburger Abfallwirtschaft und Straßenreinigung"
DESCRIPTION = "Source for waste collections for WAS-Wolfsburg, Germany."
URL = "https://was-wolfsburg.de"
TEST_CASES = {"WAS": {"city": "Barnstorf", "street": "Bahnhofspassage"}}


class Source:
    def __init__(self, city, street):
        self._city = city
        self._street = street
        self._ics = ICS()

    def fetch(self):
        # fetch "Gelber Sack"
        args = {"g": self._city}
        r = requests.get(
            "https://was-wolfsburg.de/subgelberweihgarten/php/abfuhrgelber.php",
            params=args,
        )

        entries = []
        match = re.findall(r"(\d{2})\.(\d{2})\.(\d{4})", r.text)
        for m in match:
            date = datetime.date(day=int(m[0]), month=int(m[1]), year=int(m[2]))
            entries.append(Collection(date, "Gelber Sack"))

        # fetch remaining collections
        args = {"ortabf": self._street}
        r = requests.post(
            "https://was-wolfsburg.de/subabfuhrtermine/ics_abfuhrtermine3.php",
            data=args,
        )
        dates = self._ics.convert(r.text)
        for d in dates:
            entries.append(Collection(d[0], d[1]))

        return entries
