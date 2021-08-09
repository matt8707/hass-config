import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Stadtreinigung Hamburg"
DESCRIPTION = "Source for Stadtreinigung Hamburg waste collection."
URL = "https://www.stadtreinigung.hamburg"
TEST_CASES = {
    "Hamburg": {"asId": 5087, "hnId": 113084},
}


class Source:
    def __init__(self, asId, hnId):
        self._asId = asId
        self._hnId = hnId
        self._ics = ICS(offset=1, regex="Erinnerung: Abfuhr (.*) morgen")

    def fetch(self):
        args = {"asId": self._asId, "hnId": self._hnId, "adresse": "MeineAdresse"}

        # get ics file
        r = requests.post(
            "https://www.stadtreinigung.hamburg/privatkunden/abfuhrkalender/Abfuhrtermin.ics",
            data=args,
        )

        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
