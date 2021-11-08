import datetime
from html.parser import HTMLParser

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Auckland council"
DESCRIPTION = "Source for Auckland council."
URL = "https://aucklandcouncil.govt.nz"
TEST_CASES = {
    "429 Sea View Road": {"area_number": "12342453293"},  # Monday
    "8 Dickson Road": {"area_number": "12342306525"},  # Thursday
}

MONTH = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def toDate(formattedDate):
    items = formattedDate.split()
    return datetime.date(int(items[3]), MONTH[items[2]], int(items[1]))


# Parser for <div> element with class wasteSearchResults
class WasteSearchResultsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._entries = []
        self._wasteType = None
        self._withinWasteDateSpan = False
        self._withinHouseholdDiv = False
        self._withinRubbishLinks = False
        self._todaysDate = None
        self._workingWasteDate = None

    @property
    def entries(self):
        return self._entries

    def handle_endtag(self, tag):
        if tag == "span" and self._withinWasteDateSpan:
            self._withinWasteDateSpan = False
        if tag == "div" and self._withinRubbishLinks:
            self._withinRubbishLinks = False
            self._workingWasteDate = None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            d = dict(attrs)
            id = d.get("id", "")
            if id.endswith("HouseholdBlock"):
                self._withinHouseholdDiv = True
            if id.endswith("CommercialBlock"):
                self._withinHouseholdDiv = False

        if self._withinHouseholdDiv:
            s = dict(attrs)
            className = s.get("class", "")
            if tag == "div":
                if className == "links":
                    self._withinRubbishLinks = True
                else:
                    self._withinRubbishLinks = False

            if tag == "span":
                if className.startswith("m-r-1"):
                    self._withinWasteDateSpan = True

                if self._workingWasteDate is not None:
                    if className.startswith("icon-rubbish") or className.startswith(
                        "icon-recycle"
                    ):
                        type = s["class"][5:]  # remove "icon-"
                        self._entries.append(Collection(self._workingWasteDate, type))

    def handle_data(self, data):
        # date span comes first, doesn't have a year
        if self._withinWasteDateSpan:
            todays_date = datetime.date.today()
            # use current year, unless Jan is in data, and we are still in Dec
            year = todays_date.year
            if "January" in data and todays_date.month == 12:
                # then add 1
                year = year + 1
            fullDate = data + " " + f"{year}"
            self._workingWasteDate = toDate(fullDate)


class Source:
    def __init__(
        self, area_number,
    ):
        self._area_number = area_number

    def fetch(self):
        # get token
        params = {"an": self._area_number}

        r = requests.get(
            "https://www.aucklandcouncil.govt.nz/rubbish-recycling/rubbish-recycling-collections/Pages/collection-day-detail.aspx",
            params=params,
            verify=False,
        )
        p = WasteSearchResultsParser()
        p.feed(r.text)
        return p.entries
