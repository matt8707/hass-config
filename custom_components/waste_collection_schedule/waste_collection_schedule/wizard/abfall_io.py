#!/usr/bin/env python3

from html.parser import HTMLParser

import inquirer
import requests
import re

MODUS_KEY = "d6c5855a62cf32a4dadbc2831f0f295f"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# IDs of CONFIG VARIABLES
CONFIG_VARIABLES = ["f_id_kommune", "f_id_bezirk", "f_id_strasse", "f_id_strasse_hnr", "f_abfallarten"]

ACTION_EXTRACTOR_PATTERN = re.compile('(?<=awk-data-onchange-submit-waction=")[^\\n\\r"]+')

DISTRICT_CHOICES = [
    ("ALBA Berlin", "9583a2fa1df97ed95363382c73b41b1b"),
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


class OptionParser(HTMLParser):
    """Parser for HTML option list."""
    TEXTBOXES = "textboxes"

    def error(self, message):
        pass

    def __init__(self, target_var):
        super().__init__()
        self._target_var = target_var
        self._within_option = False
        self._option_name = ""
        self._option_value = "-1"
        self._choices = []
        self._is_selector = False
        self._is_text_input = False
        self._text_field_id = ""
        self._text_hint = ""
        self._text_name = ""
        self._label_for_id = ""
        self._label_contents = {}

    @property
    def choices(self):
        return self._choices

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if tag == "label":
            if "for" in attributes:
                self._label_for_id = attributes["for"]

        if tag == "input":
            if "type" in attributes:
                if attributes["type"] == "hidden":
                    if "name" in attributes and "value" in attributes and attributes["name"] == self._target_var:
                        # self._within_option = True
                        self._is_selector = True
                        self._option_value = attributes["value"]
                        self._choices.append((attributes["value"], attributes["value"]))
                elif self._target_var == OptionParser.TEXTBOXES and attributes["type"] == "text":
                    self._is_text_input = True
                    if "id" in attributes:
                        self._text_field_id = attributes["id"]
                    if "placeholder" in attributes:
                        self._text_hint = attributes["placeholder"]
                    if "name" in attributes:
                        self._text_name = attributes["name"]

        if tag == "select":
            if "name" in attributes and attributes["name"] == self._target_var:
                self._is_selector = True

        if tag == "option" and self._is_selector:
            self._within_option = True
            if "value" in attributes:
                self._option_value = attributes["value"]

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

        if len(self._label_for_id) > 0:
            self._label_contents[self._label_for_id] = data
            self._label_for_id = ""

    @property
    def is_selector(self):
        return self._is_selector

    @property
    def is_text_input(self):
        return self._is_text_input

    @property
    def text_name(self):
        return self._text_name

    @property
    def text_field_id(self):
        return self._text_field_id

    @property
    def label_contents(self):
        return self._label_contents

    @property
    def text_hint(self):
        return self._text_hint


def select_and_query(data, answers):
    relevant_config_vars = []
    for config_var in CONFIG_VARIABLES:
        if config_var not in answers and config_var in data:
            relevant_config_vars.append(config_var)

    for target_var in relevant_config_vars:
        # parser HTML option list
        parser = OptionParser(target_var)
        parser.feed(data)

        if parser.is_selector:
            questions = [
                inquirer.List(
                    target_var,
                    choices=parser.choices,
                    message=f"Select {target_var}",
                )
            ]
            answers.update(inquirer.prompt(questions))

    # Search for Textboxes (currently just supports one textbox per request)
    parser = OptionParser(OptionParser.TEXTBOXES)
    parser.feed(data)
    if parser.is_text_input:
        message = parser.label_contents[parser.text_field_id]
        if parser.text_hint != "":
            message = message + " (" + parser.text_hint + ")"

        questions = [inquirer.Text(parser.text_name, message=message)]
        answers.update(inquirer.prompt(questions))

    args = {"key": answers["key"], "modus": MODUS_KEY, "waction": ACTION_EXTRACTOR_PATTERN.findall(data)[0]}
    r = requests.post("https://api.abfall.io", params=args, data=answers, headers=HEADERS)
    return r.text


def main():
    questions = [
        inquirer.List(
            "key", choices=DISTRICT_CHOICES, message="Select service provider"
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
        if key in CONFIG_VARIABLES or key == "key":
            print(f"        {key}: {value}")


if __name__ == "__main__":
    main()
