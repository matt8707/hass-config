#!/usr/bin/env python3

import json

import inquirer
import requests


def main():
    # search for street
    questions = [inquirer.Text("street", message="Enter search string for street")]
    answers = inquirer.prompt(questions)

    # retrieve suggestions for street
    r = requests.get(
        "https://service.stuttgart.de/lhs-services/aws/strassennamen", params=answers
    )

    data = json.loads(r.text)
    street_choices = []
    for d in data["suggestions"]:
        street_choices.append((d["value"], d["data"]))

    # select street
    questions = [
        inquirer.List("street", choices=street_choices, message="Select street")
    ]
    results = inquirer.prompt(questions)

    # search for house number
    questions = [inquirer.Text("streetnr", message="Enter house number")]
    results.update(inquirer.prompt(questions))

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: stuttgart_de")
    print("      args:")
    for key, value in results.items():
        print(f"        {key}: {value}")


if __name__ == "__main__":
    main()
