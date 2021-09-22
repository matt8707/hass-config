import json
from datetime import datetime
from html.parser import HTMLParser

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Berline Recycling"
DESCRIPTION = "Source for Berlin Recycling waste collection."
URL = "https://berlin-recycling.de"
TEST_CASES = {
    "Germanenstrasse": {
        "username": "!secret berlin_recycling_username",
        "password": "!secret berlin_recycling_password",
    },
}


# Parser for HTML input (hidden) text
class HiddenInputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._args = {}

    @property
    def args(self):
        return self._args

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            d = dict(attrs)
            if str(d["type"]).lower() == "hidden":
                self._args[d["name"]] = d["value"] if "value" in d else ""


SERVICE_URL = "https://kundenportal.berlin-recycling.de/"


class Source:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def fetch(self):
        session = requests.session()

        # first get returns session specific url
        r = session.get(SERVICE_URL, allow_redirects=False)

        # get session id's
        r = session.get(r.url)

        parser = HiddenInputParser()
        parser.feed(r.text)
        args = parser.args
        args["__EVENTTARGET"] = "btnLog"
        args["__EVENTARGUMENT"] = None
        args["Username"] = self._username
        args["Password"] = self._password

        # login
        r = session.post(r.url, data=args)
        serviceUrl = r.url

        request_data = {"withhtml": "true"}
        r = session.post(serviceUrl + "/GetDashboard", json=request_data)

        request_data = {"datasettable": "ENWIS_ABFUHRKALENDER"}
        r = session.post(serviceUrl + "/ChangeDatasetTable", json=request_data)

        request_data = {
            "datasettablecode": "ENWIS_ABFUHRKALENDER",
            "startindex": 0,
            "searchtext": "",
            "rangefilter": "",
            "ordername": "",
            "orderdir": "",
            "ClientParameters": "",
            "headrecid": "",
        }
        r = session.post(serviceUrl + "/GetDatasetTableHead", json=request_data)

        data = json.loads(r.text)
        # load json again, because response is double coded
        data = json.loads(data["d"])

        entries = []
        for d in data["data"]:
            date = datetime.strptime(d["Task Date"], "%Y-%m-%d").date()
            entries.append(Collection(date, d["Material Description"]))
        return entries
