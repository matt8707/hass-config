import datetime
from html.parser import HTMLParser

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Abfall Stuttgart"
DESCRIPTION = "Source for waste collections for the city of Stuttgart, Germany."
URL = "https://service.stuttgart.de/lhs-services/aws/"
TEST_CASES = {"Im Steinengarten 7": {"street": "Im Steinengarten", "streetnr": 7}}


# Parser for HTML checkbox
class InputCheckboxParser(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._value = []

    @property
    def value(self):
        return self._value

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            d = dict(attrs)
            if d.get("name", "") == self._name:
                self._value.append(d.get("value"))


# Parser for HTML table
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._within_table = False
        self._within_tr = False
        self._within_th = False
        self._within_td = False
        self._col_index = 0
        self._type = ""
        self._date = ""
        self._entries = []

    @property
    def entries(self):
        return self._entries

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "table":
            if d.get("id", "") == "awstable":
                self._within_table = True
        elif tag == "tr":
            if self._within_table:
                self._within_tr = True
        elif tag == "th":
            if self._within_tr:
                if self._col_index == 0:
                    self._type = ""
                self._within_th = True
                self._col_index += 1
        elif tag == "td":
            if self._within_tr:
                self._within_td = True
                self._col_index += 1

    def handle_endtag(self, tag):
        if tag == "table":
            self._within_table = False
            self._type = ""
            self._date = ""
        elif tag == "tr":
            if self._within_tr and len(self._date) > 0:
                date = datetime.datetime.strptime(self._date, "%d.%m.%Y").date()
                self._entries.append(Collection(date, self._type))
                self._date = ""
            self._within_tr = False
            self._within_th = False
            self._within_td = False
            self._col_index = 0
        elif tag == "th":
            self._within_th = False
            self._type = self._type.strip()
        elif tag == "td":
            self._within_td = False

    def handle_data(self, data):
        if self._within_th and self._col_index == 1:
            self._type += data
        elif self._within_td and self._col_index == 2:
            self._date += data


class Source:
    def __init__(self, street, streetnr):
        self._street = street
        self._streetnr = streetnr

    def fetch(self):
        # get waste types
        r = requests.get("https://service.stuttgart.de/lhs-services/aws/abfuhrtermine")
        wastetypes = InputCheckboxParser(name="calendar[wastetype][]")
        wastetypes.feed(r.text)

        now = datetime.datetime.now()
        args = [
            ("calendar[street]", self._street),
            ("calendar[streetnr]", self._streetnr),
            ("calendar[datefrom]", now.strftime("%d.%m.%Y")),
            ("calendar[dateto]", f"31.01.{now.year+1}"),
        ]
        for w in wastetypes.value:
            args.append(("calendar[wastetype][]", w))
        args.append(("calendar[submit]", ""))

        r = requests.post(
            "https://service.stuttgart.de/lhs-services/aws/abfuhrtermine", data=args
        )
        entries_parser = TableParser()
        entries_parser.feed(r.text)
        return entries_parser.entries
