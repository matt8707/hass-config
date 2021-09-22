#!/usr/bin/env python3

from html.parser import HTMLParser

import inquirer
import requests

MODUS_KEY = "d6c5855a62cf32a4dadbc2831f0f295f"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


class OptionParser(HTMLParser):
    """Parser for HTML option list."""

    def __init__(self):
        super().__init__()
        self._within_option = False
        self._option_name = ""
        self._option_value = "-1"
        self._choices = []
        self._select_name = ""
        self._waction = ""

    @property
    def choices(self):
        return self._choices

    @property
    def select_name(self):
        return self._select_name

    @property
    def waction(self):
        return self._waction

    def handle_starttag(self, tag, attrs):
        if tag == "option":
            self._within_option = True
            for attr in attrs:
                if attr[0] == "value":
                    self._option_value = attr[1]
        elif tag == "select":
            for attr in attrs:
                if attr[0] == "name":
                    self._select_name = attr[1]
                elif attr[0] == "awk-data-onchange-submit-waction":
                    self._waction = attr[1]

    def handle_endtag(self, tag):
        if (
            self._within_option
            and len(self._option_name) > 0
            and self._option_value != "-1"
        ):
            self._choices.append((self._option_name, self._option_value))
        self._within_option = False
        self._option_name = ""
        self._option_value = "-1"

    def handle_data(self, data):
        if self._within_option:
            self._option_name += data


def select_and_query(data, answers):
    # parser HTML option list
    parser = OptionParser()
    parser.feed(data)

    questions = [
        inquirer.List(
            parser.select_name,
            choices=parser.choices,
            message=f"Select {parser.select_name}",
        )
    ]
    answers.update(inquirer.prompt(questions))

    args = {"key": answers["key"], "modus": MODUS_KEY, "waction": parser.waction}
    r = requests.post(
        "https://api.abfall.io", params=args, data=answers, headers=HEADERS
    )
    return r.text


def main():
    # select district
    district_choices = [
        ("Böblingen", "8215c62763967916979e0e8566b6172e"),
        ("Kitzingen", "594f805eb33677ad5bc645aeeeaf2623"),
        ("Freudenstadt", "595f903540a36fe8610ec39aa3a06f6a"),
        ("Göppingen", "365d791b58c7e39b20bb8f167bd33981"),
        ("Landsberg am Lech", "7df877d4f0e63decfb4d11686c54c5d6"),
        ("Landshut", "bd0c2d0177a0849a905cded5cb734a6f"),
        ("Rotenburg (Wümme)", "645adb3c27370a61f7eabbb2039de4f1"),
        ("Sigmaringen", "39886c5699d14e040063c0142cd0740b"),
        ("MüllALARM / Schönmackers", "e5543a3e190cb8d91c645660ad60965f"),
        ("Unterallgäu", "c22b850ea4eff207a273e46847e417c5"),
        ("Westerwaldkreis", "248deacbb49b06e868d29cb53c8ef034"),
        ("Calw", "690a3ae4906c52b232c1322e2f88550c"),
    ]
    questions = [
        inquirer.List(
            "key", choices=district_choices, message="Select service provider"
        )
    ]
    answers = inquirer.prompt(questions)

    # prompt for first level
    args = {"key": answers["key"], "modus": MODUS_KEY, "waction": "init"}
    r = requests.get("https://api.abfall.io", params=args, headers=HEADERS)

    data = r.text
    while True:
        data = select_and_query(data, answers)

        if "f_id_abfalltyp" in data:
            break

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: abfall_io")
    print("      args:")
    for key, value in answers.items():
        print(f"        {key}: {value}")


if __name__ == "__main__":
    main()
