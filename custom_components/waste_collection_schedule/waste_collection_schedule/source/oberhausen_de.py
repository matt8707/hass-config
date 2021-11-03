import datetime
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Oberhausen.de"
DESCRIPTION = "Source for Oberhausen waste collection."
URL = "https://www.oberhausen.de/abfallkalender"

TEST_CASES = {
    "Max-Planck-Ring": {
        "street": "Max-Planck-Ring",
    },
    "Mülheimer Straße 1": {
        "street": "Mülheimer Straße 1",
    },
}

# Parser for HTML input (hidden) text
class ICSLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._args = {}

    @property
    def args(self):
        return self._args

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            if "href" in d and 'abfallkalender_ical.php' in str(d["href"]):
                self._args["href"] = urljoin(URL, d["href"])

class Source:
    def __init__(self, street):
        self._street = street
        self._ics = ICS()

    def fetch(self):
        now = datetime.datetime.now()
        entries = self.fetch_year(now.year)

        if now.month == 12:
            # also get data for next year if we are already in december
            try:
                entries.extend(self.fetch_year(now.year + 1))
            except Exception:
                # ignore if fetch for next year fails
                pass
        return entries

    def fetch_year(self, year):
        with requests.Session() as s:
            # get session id
            s.get("https://www.oberhausen.de/abfallkalender")

            # update session with filters and get ICS link
            r = s.post("https://www.oberhausen.de/abfallkalender", data={
                "abfall_searchstring": self._street,
                "abfall_jahr": year,
                "actbio": "on",
                "actdeckgruen": "on",
                "actdeckrot": "on",
                "actdeckblau": "on",
                "actgelb": "on",
                "actpapier": "on",
                "submit_search": ""
            })

            # extract ICS link
            parser = ICSLinkParser()
            parser.feed(r.text)

            if not "href" in parser.args or parser.args["href"] == "":
                raise Exception(
                   "Error: could not extract ICS download link for year / street: {}, '{}'".format(
                       year,
                       self._street
                   )
               )

            # download ICS file
            r = s.get(parser.args['href'])

            # check the return code
            if not r.ok:
                raise Exception(
                    "Error: the response is not ok; need code 200, but got code {}".format(
                        r.status_code
                    )
                )

        # parse ics file
        r.encoding = "utf-8"
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
