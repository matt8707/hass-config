import datetime
import re
from html.parser import HTMLParser

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Wastenet"
DESCRIPTION = "Source for Wastenet.org.nz."
URL = "http://www.wastenet.org.nz"
TEST_CASES = {
    "166 Lewis Street": {"address": "166 Lewis Street INVERCARGILL"},  # Monday
    "199 Crawford Street": {"address": "199 Crawford Street INVERCARGILL"},  # Tuesday
    "156 Tay Street": {"address": "156 Tay Street INVERCARGILL"},  # Wednesday
    "31 Conyers Street": {"address": "31 Conyers Street INVERCARGILL"},  # Thursday
    "67 Chesney Street": {"address": "67 Chesney Street INVERCARGILL"},  # Friday
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


def toDate(match):
    # match is based on following input string: 21 April 2021
    # regex: (\d+) (\w+) (\d+)
    return datetime.date(
        int(match.group(3)), MONTH[match.group(2)], int(match.group(1))
    )


# Parser for <div> element with class wasteSearchResults
class WasteSearchResultsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._entries = []
        self._wasteType = None
        self._withinCollectionDay = False
        self._todaysDate = None

    @property
    def entries(self):
        return self._entries

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            d = dict(attrs)
            if d.get("class", "").startswith("wasteSearchResults "):
                self._wasteType = d["class"][19:]  # remove "wasteSearchResults "

    def handle_data(self, data):
        match = re.search(r"Todays Date: \w+, (\d+) (\w+) (\d+)", data)
        if match:
            self._todaysDate = toDate(match)
        elif data == "Next Collection Day":
            self._withinCollectionDay = True
        elif self._withinCollectionDay:
            date = None
            if data.strip().lower() == "today":
                date = self._todaysDate
            elif data.strip().lower() == "tomorrow":
                date = self._todaysDate + datetime.timedelta(days=1)
            else:
                date = toDate(re.search(r"(\d+) (\w+) (\d+)", data))

            if self._wasteType is not None:
                self._entries.append(Collection(date, self._wasteType))

            self._withinCollectionDay = False


class Source:
    def __init__(
        self, address,
    ):
        self._address = address

    def fetch(self):
        # get token
        params = {"view": 1, "address": self._address}

        r = requests.get(
            "http://www.wastenet.org.nz/RecycleRubbish/WasteCollectionSearch.aspx",
            params=params,
        )

        p = WasteSearchResultsParser()
        p.feed(r.text)
        return p.entries
