#!/usr/bin/env python3

import json

import inquirer
import requests


def main():
    # get cookies
    r = requests.get("https://www.bsr.de/abfuhrkalender-20520.php")
    cookies = r.cookies

    while True:
        questions = [inquirer.Text("q", message="Enter search string for street")]
        answers = inquirer.prompt(questions)

        args = {"script": "dynamic_search", "step": 1, "q": answers["q"]}

        r = requests.get(
            "https://www.bsr.de/abfuhrkalender_ajax.php", params=args, cookies=cookies
        )

        data = json.loads(r.text)
        if (
            len(data) == 1 and data[0]["value"] == "Keine Adresse gefunden"
        ):  # {'value': 'Keine Adresse gefunden'}
            print("Search returned no result. Please try again.")
        else:
            break

    street_choices = []
    for d in data:
        street_choices.append(d["value"])

    # select street
    questions = [
        inquirer.List("abf_strasse", choices=street_choices, message="Select street")
    ]
    answers = inquirer.prompt(questions)

    # retrieve house number list
    args = {"script": "dynamic_search", "step": 2, "q": answers["abf_strasse"]}

    r = requests.get(
        "https://www.bsr.de/abfuhrkalender_ajax.php", params=args, cookies=cookies
    )

    # select house number
    data = json.loads(r.text)
    house_number_choices = []
    for d in data.values():
        house_number_choices.append((d["FullStreet"], d["HouseNo"]))

    questions = [
        inquirer.List(
            "abf_hausnr", choices=house_number_choices, message="Select house number"
        )
    ]
    answers.update(inquirer.prompt(questions))

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: bsr_de")
    print("      args:")
    for key, value in answers.items():
        print(f"        {key}: {value}")


if __name__ == "__main__":
    main()
