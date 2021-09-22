#!/usr/bin/env python3

from html.parser import HTMLParser

import inquirer
import requests


# Parser for HTML input (hidden) text
class InputTextParser(HTMLParser):
    def __init__(self, **identifiers):
        super().__init__()
        self._identifiers = identifiers
        self._value = None

    @property
    def value(self):
        return self._value

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            d = dict(attrs)
            for key, value in self._identifiers.items():
                if key not in d or d[key] != value:
                    return
            self._value = d.get("value")


# Parser for HTML input select list
class InputSelectParser(HTMLParser):
    def __init__(self, **identifiers):
        super().__init__()
        self._identifiers = identifiers
        self._within_select = False
        self._within_option = False
        self._option_name = ""
        self._option_value = "-1"
        self._choices = []

    @property
    def choices(self):
        return self._choices

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "select":
            for key, value in self._identifiers.items():
                if key not in d or d[key] != value:
                    return
            self._within_select = True
        elif tag == "option" and self._within_select:
            self._within_option = True
            self._option_value = d.get("value")

    def handle_endtag(self, tag):
        if tag == "select":
            self._within_select = False
        elif tag == "option":
            if (
                self._within_select
                and self._within_option
                and len(self._option_name) > 0
                and self._option_value != ""
            ):
                self._choices.append((self._option_name, self._option_value))
            self._within_option = False
            self._option_name = ""
            self._option_value = "-1"

    def handle_data(self, data):
        if self._within_option:
            self._option_name += data


def main():
    results = {}

    # select service
    service_choices = [
        ("Frankfurt", "Fes"),
        ("Düsseldorf", "Dus"),
        ("Rhein-Sieg-Kreis", "Rsa"),
        ("Bochum", "Usb"),
        ("Münster", "Awm"),
        ("Mainz", "Ebm"),
        ("Entsorgungsverband Saar (EVS)", "Evs"),
        ("Landkreis Gießen", "Lkg"),
        ("Hamm", "Ash"),
        ("Darmstadt", "Ead"),
        ("Kaiserslautern", "Ask"),
        ("Hanau", "His"),
        ("Maintal", "Mai"),
        ("Haltern am See", "Hal"),
        ("Friedberg", "Efb"),
    ]
    questions = [
        inquirer.List(
            "service",
            choices=service_choices,
            message="Select service provider for district",
        )
    ]
    answers = inquirer.prompt(questions)
    results.update(answers)

    mm_ses = InputTextParser(type="hidden", name="mm_ses")

    url = f"https://www.muellmax.de/abfallkalender/{answers['service'].lower()}/res/{answers['service']}Start.php"
    r = requests.get(url)
    mm_ses.feed(r.text)

    # select "Abfuhrtermine", returns ort or an empty street search field
    args = {"mm_ses": mm_ses.value, "mm_aus_ort.x": 0, "mm_aus_ort.x": 0}
    r = requests.post(url, data=args)
    mm_ses.feed(r.text)

    # check if last request returns a list of cities
    mm_frm_ort_sel = InputSelectParser(name="mm_frm_ort_sel")
    mm_frm_ort_sel.feed(r.text)
    if len(mm_frm_ort_sel.choices) > 0:
        # select city
        questions = [
            inquirer.List(
                "mm_frm_ort_sel", choices=mm_frm_ort_sel.choices, message="Select city"
            )
        ]
        answers = inquirer.prompt(questions)
        results.update(answers)

        # get list of streets
        args = {
            "mm_ses": mm_ses.value,
            "xxx": 1,
            "mm_frm_ort_sel": answers["mm_frm_ort_sel"],
            "mm_aus_ort_submit": "weiter",
        }
        r = requests.post(url, data=args)
        mm_ses.feed(r.text)

    # get list of streets
    args = {
        "mm_ses": mm_ses.value,
        "xxx": 1,
        "mm_frm_str_name": "",
        "mm_aus_str_txt_submit": "suchen",
    }
    r = requests.post(url, data=args)
    mm_ses.feed(r.text)

    mm_frm_str_sel = InputSelectParser(name="mm_frm_str_sel")
    mm_frm_str_sel.feed(r.text)

    # select street
    questions = [
        inquirer.List(
            "mm_frm_str_sel", choices=mm_frm_str_sel.choices, message="Select street"
        )
    ]
    answers = inquirer.prompt(questions)
    results.update(answers)

    # get list of house numbers
    args = {
        "mm_ses": mm_ses.value,
        "xxx": 1,
        "mm_frm_str_sel": answers["mm_frm_str_sel"],
        "mm_aus_str_sel_submit": "weiter",
    }
    r = requests.post(url, data=args)
    mm_ses.feed(r.text)

    mm_frm_hnr_sel = InputSelectParser(name="mm_frm_hnr_sel")
    mm_frm_hnr_sel.feed(r.text)

    # select house number
    if len(mm_frm_hnr_sel.choices) > 0:
        questions = [
            inquirer.List(
                "mm_frm_hnr_sel",
                choices=mm_frm_hnr_sel.choices,
                message="Select house number",
            )
        ]
        answers = inquirer.prompt(questions)
        results.update(answers)

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: muellmax_de")
    print("      args:")
    for key, value in results.items():
        print(f"        {key}: {value}")


if __name__ == "__main__":
    main()
