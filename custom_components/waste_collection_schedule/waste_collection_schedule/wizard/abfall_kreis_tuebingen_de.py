#!/usr/bin/env python3

from html.parser import HTMLParser

import inquirer
import requests


# Parser for HTML option list
class OptionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._within_option = False
        self._option_name = ""
        self._option_value = "-1"
        self._choices = []

    @property
    def choices(self):
        return self._choices

    def handle_starttag(self, tag, attrs):
        if tag == "option":
            self._within_option = True
        for attr in attrs:
            if attr[0] == "value":
                self._option_value = attr[1]

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


def main():
    questions = [
        inquirer.List(
            "ort_id",
            choices=[
                ("Ammerbuch", 1),
                ("Bodelshausen", 2),
                ("Dettenhausen", 3),
                ("Dusslingen", 4),
                ("Gomaringen", 5),
                ("Hirrlingen", 6),
                ("Kirchentellinsfurt", 7),
                ("Kusterdingen", 8),
                ("Mössingen", 9),
                ("Nehren", 10),
                ("Neustetten", 11),
                ("Ofterdingen", 12),
                ("Rottenburg", 13),
                ("Rottenburger Teilgemeinden", 16),
                ("Starzach", 14),
                ("Tübingen", 15),
                ("Tübinger Teilorte", 17),
            ],
            message="Select municipality [Ort]",
        )
    ]
    answers1 = inquirer.prompt(questions)

    # retrieve street list
    args = {
        "action": "get_calendar_dropzones",
        "ort_id": answers1["ort_id"],
        "bin_type": "bin_standard",
    }
    r = requests.post(
        "https://www.abfall-kreis-tuebingen.de/wp-admin/admin-ajax.php", data=args
    )

    # parser HTML option list
    parser = OptionParser()
    parser.feed(r.text)

    # prompt for street list

    if len(parser.choices) > 1:
        questions = [
            inquirer.List("dropzone", choices=parser.choices, message="Select street")
        ]
        answers2 = inquirer.prompt(questions)
    else:
        answers2 = {"dropzone": parser.choices[0][1]}

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: abfall_kreis_tuebingen_de")
    print("      args:")
    print(f"        ort: {answers1['ort_id']}")
    print(f"        dropzone: {answers2['dropzone']}")


if __name__ == "__main__":
    main()
