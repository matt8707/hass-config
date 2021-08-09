from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.AbfallnaviDe import AbfallnaviDe

TITLE = "AbfallNavi"
DESCRIPTION = (
    "Source for AbfallNavi waste collection. AbfallNavi is a brand name of regioit.de."
)
URL = "https://www.regioit.de"
TEST_CASES = {
    "Aachen, Abteiplatz 7": {
        "service": "aachen",
        "ort": "Aachen",
        "strasse": "Abteiplatz",
        "hausnummer": "7",
    },
    "Lindlar, Aggerweg": {
        "service": "lindlar",
        "ort": "Lindlar",
        "strasse": "Aggerweg",
    },
    "Roetgen, Am Sportplatz 2": {
        "service": "roe",
        "ort": "Roetgen",
        "strasse": "Am Sportplatz",
        "hausnummer": "2",
    },
}


class Source:
    def __init__(self, service, ort, strasse, hausnummer=None):
        self._api = AbfallnaviDe(service)
        self._ort = ort
        self._strasse = strasse
        self._hausnummer = hausnummer

    def fetch(self):
        dates = self._api.get_dates(self._ort, self._strasse, self._hausnummer)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
