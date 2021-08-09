import datetime
import logging
from pathlib import Path

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "ICS"
DESCRIPTION = "Source for ICS based schedules."
URL = None
TEST_CASES = {
    "Dortmund, Dudenstr. 5": {
        "url": "https://www.edg.de/ical/kalender.ics?Strasse=Dudenstr.&Hausnummer=5&Erinnerung=-1&Abfallart=1,2,3,4"
    },
    "Leipzig, Sandgrubenweg 27": {
        "url": "https://stadtreinigung-leipzig.de/wir-kommen-zu-ihnen/abfallkalender/ical.ics?position_nos=38296&name=Sandgrubenweg%2027"
    },
    "Ludwigsburg": {
        "url": "https://www.avl-ludwigsburg.de/fileadmin/Files/Abfallkalender/ICS/Privat/Privat_{%Y}_Ossweil.ics"
    },
    "Esslingen, Bahnhof": {
        "url": "https://api.abfall.io/?kh=DaA02103019b46345f1998698563DaAd&t=ics&s=1a862df26f6943997cef90233877a4fe"
    },
    "Test File": {
        # Path is used here to allow to call the Source from any location.
        # This is not required in a yaml configuration!
        "file": Path(__file__)
        .resolve()
        .parents[1]
        .joinpath("test/test.ics")
    },
    "Test File (recurring)": {
        # Path is used here to allow to call the Source from any location.
        # This is not required in a yaml configuration!
        "file": Path(__file__)
        .resolve()
        .parents[1]
        .joinpath("test/recurring.ics")
    },
    "München, Bahnstr. 11": {
        "url": "https://www.awm-muenchen.de/entsorgen/abfuhrkalender?tx_awmabfuhrkalender_abfuhrkalender%5Bhausnummer%5D=11&tx_awmabfuhrkalender_abfuhrkalender%5Bleerungszyklus%5D%5BB%5D=1%2F2%3BU&tx_awmabfuhrkalender_abfuhrkalender%5Bleerungszyklus%5D%5BP%5D=1%2F2%3BG&tx_awmabfuhrkalender_abfuhrkalender%5Bleerungszyklus%5D%5BR%5D=001%3BU&tx_awmabfuhrkalender_abfuhrkalender%5Bsection%5D=ics&tx_awmabfuhrkalender_abfuhrkalender%5Bsinglestandplatz%5D=false&tx_awmabfuhrkalender_abfuhrkalender%5Bstandplatzwahl%5D=true&tx_awmabfuhrkalender_abfuhrkalender%5Bstellplatz%5D%5Bbio%5D=70024507&tx_awmabfuhrkalender_abfuhrkalender%5Bstellplatz%5D%5Bpapier%5D=70024507&tx_awmabfuhrkalender_abfuhrkalender%5Bstellplatz%5D%5Brestmuell%5D=70024507&tx_awmabfuhrkalender_abfuhrkalender%5Bstrasse%5D=bahnstr.&tx_awmabfuhrkalender_abfuhrkalender%5Byear%5D={%Y}"
    },
    "Buxtehude, Am Berg": {
        "url": "https://abfall.landkreis-stade.de/api_v2/collection_dates/1/ort/10/strasse/90/hausnummern/1/abfallarten/R02-R04-B02-D04-D12-P04-R12-R14-W0-R22-R24-R31/kalender.ics"
    },
    #    "Hausmüllinfo: ASR Chemnitz": {
    #        "url": "https://asc.hausmuell.info/ics/ics.php",
    #        "method": "POST",
    #        "params": {
    #            "hidden_id_egebiet": 439087,
    #            "input_ort": "Chemnitz",
    #            "input_str": "Straße der Nationen",
    #            "input_hnr": 2,
    #            "hidden_send_btn": "ics",
    #            # "hiddenYear": 2021,
    #            "hidden_id_ort": 10,
    #            "hidden_id_ortsteil": 0,
    #            "hidden_id_str": 17814,
    #            "hidden_id_hnr": 5538100,
    #            "hidden_kalenderart": "privat",
    #            "showBinsBio": "on",
    #            "showBinsRest": "on",
    #            "showBinsRest_rc": "on",
    #            "showBinsPapier": "on",
    #            "showBinsOrganic": "on",
    #            "showBinsXmas": "on",
    #            "showBinsDsd": "on",
    #            "showBinsProb": "on",
    #        },
    #        "year_field": "hiddenYear",
    #    },
    "Abfall Zollernalbkreis, Ebingen": {
        "url": "https://www.abfallkalender-zak.de",
        "params": {
            "city": "2,3,4",
            "street": "3",
            "types[]": [
                "restmuell",
                "gelbersack",
                "papiertonne",
                "biomuell",
                "gruenabfall",
                "schadstoffsammlung",
                "altpapiersammlung",
                "schrottsammlung",
                "weihnachtsbaeume",
                "elektrosammlung",
            ],
            "go_ics": "Download",
        },
        "year_field": "year",
    },
}


HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(
        self,
        url=None,
        file=None,
        offset=None,
        params=None,
        year_field=None,
        method="GET",
    ):
        self._url = url
        self._file = file
        if bool(self._url is not None) == bool(self._file is not None):
            raise RuntimeError("Specify either url or file")
        self._ics = ICS(offset)
        self._params = params
        self._year_field = year_field  # replace this field in params with current year
        self._method = method  # The method to send the params

    def fetch(self):
        if self._url is not None:
            if "{%Y}" in self._url or self._year_field is not None:
                # url contains wildcard or params contains year field
                now = datetime.datetime.now()

                # replace year in url
                url = self._url.replace("{%Y}", str(now.year))

                # replace year in params
                if self._year_field is not None:
                    if self._params is None:
                        raise RuntimeError("year_field specified without params")
                    self._params[self._year_field] = str(now.year)

                entries = self.fetch_url(url, self._params)

                if now.month == 12:
                    # also get data for next year if we are already in december
                    url = self._url.replace("{%Y}", str(now.year + 1))
                    self._params[self._year_field] = str(now.year + 1)

                    try:
                        entries.extend(self.fetch_url(url), self._params)
                    except Exception:
                        # ignore if fetch for next year fails
                        pass
                return entries
            else:
                return self.fetch_url(self._url, self._params)
        elif self._file is not None:
            return self.fetch_file(self._file)

    def fetch_url(self, url, params=None):
        # get ics file
        if self._method == "GET":
            r = requests.get(url, params=params, headers=HEADERS)
        elif self._method == "POST":
            r = requests.post(url, data=params, headers=HEADERS)
        else:
            _LOGGER.error(
                "Error: unknown method to fetch URL, use GET or POST; got %s"
                % self._method
            )
            return "error"
        r.encoding = "utf-8"  # requests doesn't guess the encoding correctly

        # check the return code
        if not r.ok:
            _LOGGER.error(
                "Error: the response is not ok; need code 200, but got code %s"
                % r.status_code
            )
            return "error"

        return self._convert(r.text)

    def fetch_file(self, file):
        f = open(file)
        return self._convert(f.read())

    def _convert(self, data):
        dates = self._ics.convert(data)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
