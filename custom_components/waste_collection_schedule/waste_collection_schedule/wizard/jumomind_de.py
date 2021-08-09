#!/usr/bin/python3

import json

import inquirer
import requests


def main():
    # select service
    service_choices = [
        ("Altötting", "aoe"),
        ("Aurich", "lka"),
        ("Bad Homburg vdH", "hom"),
        ("Barnim", "bdg"),
        ("Darmstadt-Dieburg", "zaw"),
        # ("Groß-Gerau", "aws"),
        ("Hattersheim am Main", "hat"),
        ("Ingolstadt", "ingol"),
        ("Lübbecke", "lue"),
        ("Minden", "sbm"),
        ("MyMüll App", "mymuell"),
        ("Recklinghausen", "ksr"),
        ("Rhein-Hunsrück", "rhe"),
        ("Uckermark", "udg"),
    ]
    questions = [
        inquirer.List(
            "service_id",
            choices=service_choices,
            message="Select service provider for district",
        )
    ]
    answers = inquirer.prompt(questions)

    # get list of city by service
    args = {"r": "cities"}
    r = requests.get(
        f"https://{answers['service_id']}.jumomind.com/mmapp/api.php", params=args
    )
    cities = json.loads(r.text)

    # select city from list
    city_choices = []
    cityData = {}
    for city in cities:
        # {'name': 'Altötting', '_name': 'Altötting', 'id': '24', 'region_code': '02', 'area_id': '24', 'img': None, 'has_streets': True}
        city_choices.append((city["name"], city["id"]))
        cityData[city["id"]] = {
            "area_id": city["area_id"],
            "has_streets": city["has_streets"],
        }

    questions = [
        inquirer.List(
            "city_id", choices=city_choices, message="Select municipality [Kommune/Ort]"
        )
    ]
    answers.update(inquirer.prompt(questions))

    selected_city = cityData[answers["city_id"]]
    if not selected_city["has_streets"]:
        # city has no street, therefore use area_id directly
        answers["area_id"] = selected_city["area_id"]
    else:
        # city has streets, therefore get list of streets
        args = {"r": "streets", "city_id": answers["city_id"]}
        r = requests.get(
            f"https://{answers['service_id']}.jumomind.com/mmapp/api.php", params=args
        )
        streets = json.loads(r.text)

        # select street from list
        street_choices = []
        house_numbers = {}
        for street in streets:
            # {'name': 'Adalbert-Stifter-Str.', '_name': 'Adalbert-Stifter-Str.', 'id': '302', 'area_id': '48'}
            # {"name":"ACHATWEG","_name":"ACHATWEG","id":"355008","area_id":"085080001","houseNumberFrom":"0001","houseNumberTo":"0001","comment":"","houseNumbers":[["0001","085080001"],["0003","085080003"],["0004","085080004"],["0005","085080005"],["0006","085080006"]]},
            street_choices.append((street["name"], street["area_id"]))
            house_number_choices = []
            if "houseNumbers" in street:
                for hnr in street["houseNumbers"]:
                    house_number_choices.append((hnr[0], hnr[1]))
                house_numbers[street["area_id"]] = house_number_choices

        questions = [
            inquirer.List("area_id", choices=street_choices, message="Select street")
        ]
        answers.update(inquirer.prompt(questions))

        if answers["area_id"] in house_numbers:
            questions = [
                inquirer.List(
                    "area_id",
                    choices=house_numbers[answers["area_id"]],
                    message="Select house number",
                )
            ]
            answers.update(inquirer.prompt(questions))

    print("Copy the following statements into your configuration.yaml:\n")
    print("# waste_collection_schedule source configuration")
    print("waste_collection_schedule:")
    print("  sources:")
    print("    - name: jumomind_de")
    print("      args:")
    print(f"        service_id: {answers['service_id']}")
    print(f"        city_id: {answers['city_id']}")
    print(f"        area_id: {answers['area_id']}")


if __name__ == "__main__":
    main()
