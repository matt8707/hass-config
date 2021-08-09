import urllib.parse

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "BSR"
DESCRIPTION = "Source for Berliner Stadtreinigungsbetriebe waste collection."
URL = "bsr.de"
TEST_CASES = {
    "Bahnhofstr., 12159 Berlin (Tempelhof-Schöneberg)": {
        "abf_strasse": "Bahnhofstr., 12159 Berlin (Tempelhof-Schöneberg)",
        "abf_hausnr": 1,
    },
    "Am Ried, 13467 Berlin (Reinickendorf)": {
        "abf_strasse": "Am Ried, 13467 Berlin (Reinickendorf)",
        "abf_hausnr": "11G",
    },
}


def myquote(s):
    # bsr uses strange quoting
    return urllib.parse.quote(s, safe=",()")


class Source:
    def __init__(self, abf_strasse, abf_hausnr):
        self._abf_strasse = abf_strasse
        self._abf_hausnr = abf_hausnr
        self._ics = ICS()

    def fetch(self):
        # get cookie
        r = requests.get("https://www.bsr.de/abfuhrkalender-20520.php")
        cookies = r.cookies

        # get street name only (without PLZ)
        street = self._abf_strasse.split(",")[0]

        # start search using string name (without PLZ)
        args = {"script": "dynamic_search", "step": 1, "q": street}
        r = requests.get(
            "https://www.bsr.de/abfuhrkalender_ajax.php", params=args, cookies=cookies
        )

        # retrieve house number list
        args = {"script": "dynamic_search", "step": 2, "q": self._abf_strasse}
        r = requests.get(
            "https://www.bsr.de/abfuhrkalender_ajax.php", params=args, cookies=cookies
        )

        args = {
            "abf_strasse": street,
            "abf_hausnr": self._abf_hausnr,
            "tab_control": "Jahr",
            "abf_config_weihnachtsbaeume": "",
            "abf_config_restmuell": "on",
            "abf_config_biogut": "on",
            "abf_config_wertstoffe": "on",
            "abf_config_laubtonne": "on",
            # "abf_selectmonth": "5 2020",
            # "abf_datepicker": "28.04.2020",
            # "listitems":7,
        }
        r = requests.post(
            "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_kalender_ajax",
            data=args,
            cookies=cookies,
        )

        args = {
            "script": "dynamic_iCal_ajax",
            "abf_strasse": self._abf_strasse,
            "abf_hausnr": self._abf_hausnr,
            "tab_control": "Jahr",
            "abf_config_weihnachtsbaeume": "",
            "abf_config_restmuell": "on",
            "abf_config_biogut": "on",
            "abf_config_wertstoffe": "on",
            "abf_config_laubtonne": "on",
            # "abf_selectmonth": "5 2020",
            # "listitems":7,
        }

        # create url using private url encoding
        encoded = map(lambda key: f"{key}={myquote(str(args[key]))}", args.keys())
        url = "https://www.bsr.de/abfuhrkalender_ajax.php?" + "&".join(encoded)
        r = requests.get(url, cookies=cookies)

        # parse ics file
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
