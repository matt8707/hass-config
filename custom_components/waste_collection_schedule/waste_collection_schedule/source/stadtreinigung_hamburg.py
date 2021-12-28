import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Stadtreinigung Hamburg"
DESCRIPTION = "Source for Stadtreinigung Hamburg waste collection."
URL = "https://www.stadtreinigung.hamburg"
TEST_CASES = {
    "Zabelweg 1B": {"hnId": 53814},
}


class Source:
    def __init__(self, hnId, asId=None):
        self._hnId = hnId
        self._ics = ICS()

    def fetch(self):
        args = {"hnIds": self._hnId, "adresse": "MeineAdresse"}

        # get ics file
        r = requests.get(
            "https://backend.stadtreinigung.hamburg/kalender/abholtermine.ics",
            params=args,
        )

        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
