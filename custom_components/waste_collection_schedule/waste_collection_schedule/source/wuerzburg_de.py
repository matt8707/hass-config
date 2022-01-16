import datetime

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Abfallkalender Würzburg"
DESCRIPTION = "Source for waste collection in the city of Würzburg, Germany."
URL = "https://www.wuerzburg.de/themen/umwelt-verkehr/vorsorge-entsorgung/abfallkalender/32208.Abfallkalender.html"
TEST_CASES = {
    "District only": {"district": "Altstadt"},
    "Street only": {"street": "Juliuspromenade"},
    "District + Street": {"district": "Altstadt", "street": "Juliuspromenade"},
    "District + Street diff": {"district": "Altstadt", "street": "Oberer Burgweg"},
}


class Source:
    def __init__(self, district: str = None, street: str = None):
        self._district = district
        self._street = street
        self._district_id = None

    @staticmethod
    def map_district_id(district: str = None, street: str = None):
        """Map `street` or `district` to `district_id`, giving priority to `street`.

        Parameters must exactly be the same as visible in dropdowns on `URL`.
        """
        if not district and not street:
            raise ValueError("One of ['district', 'street'] is required.")

        r = requests.get(URL)
        r.raise_for_status()
        selects = BeautifulSoup(r.content, "html.parser").body.find_all("select")

        if street:
            strlist = next(iter([s for s in selects if s["id"] == "strlist"]))
            strdict = {option.text: option["value"] for option in strlist}

            try:
                return strdict[street]
            except KeyError:
                raise KeyError(
                    f"Unable to find street '{street}'. Please compare exact typing with {URL}"
                )

        if district:
            reglist = next(iter([s for s in selects if s["id"] == "reglist"]))
            regdict = {
                option.text: option.attrs["value"] for option in reglist.contents
            }

            try:
                return regdict[district]
            except KeyError:
                raise KeyError(
                    f"Unable to find district '{district}'. Please compare exact typing with {URL}"
                )

    def fetch(self):
        # Get & parse full HTML only on first call to fetch() to map district or street to district_id
        if not self._district_id:
            self._district_id = self.map_district_id(self._district, self._street)

        if not self._district_id:
            raise ValueError("'_district_id' is not set!")

        now = datetime.datetime.now().date()

        r = requests.get(
            URL,
            params={
                "_func": "evList",
                "_mod": "events",
                "ev[start]": str(now),
                "ev[end]": str(now + datetime.timedelta(days=365)),
                "ev[addr]": self._district_id,
            },
        )
        r.raise_for_status()

        entries = []
        for event in r.json()["contents"].values():
            entries.append(
                Collection(
                    datetime.datetime.fromisoformat(event["start"]).date(),
                    event["title"],
                    picture=event.get("thumb", {}).get("url"),
                )
            )

        return entries
