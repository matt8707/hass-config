#!/usr/bin/env python3

import json

import inquirer
import requests


def main():
    questions = [
        inquirer.Text("street_name", message="Enter search string for street"),
        inquirer.Text(
            "building_number", message="Enter search string for house number"
        ),
    ]
    answers = inquirer.prompt(questions)

    args = answers
    args["form"] = "json"
    r = requests.get("https://www.awbkoeln.de/api/streets", params=args)

    # "data":[{"street_name":"Bahnhofplatz","building_number":"5","building_number_plain":"5","building_number_addition":"","street_code":"4270",
    # "district":"Gremberghoven","zipcode":"51149","district_code":"4","area_code":"7","user_street_name":"Bahnhofplatz","user_building_number":"1"}
    data = json.loads(r.text)
    if len(data["data"]) == 0:
        print("no matching address found")
        return

    choices = []
    for d in data["data"]:
        value = {
            "street_code": d["street_code"],
            "building_number": d["building_number"],
        }
        choices.append(
            (
                f"{d['user_street_name']} {d['user_building_number']}, {d['zipcode']} Köln - {d['district']}",
                value,
            )
        )

    questions = [inquirer.List("data", choices=choices, message="Select address")]
    answers = inquirer.prompt(questions)

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: awbkoeln_de")
    print("      args:")
    print(f"        street_code: {answers['data']['street_code']}")
    print(f"        building_number: {answers['data']['building_number']}")


if __name__ == "__main__":
    main()
