#!/usr/bin/env python3

import argparse
import importlib
import re
import site
import traceback
from pathlib import Path

import yaml

SECRET_FILENAME = "secrets.yaml"
SECRET_REGEX = re.compile(r"!secret\s(\w+)")


def main():
    parser = argparse.ArgumentParser(description="Test sources.")
    parser.add_argument(
        "-s", "--source", action="append", help="Test given source file"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List retrieved entries"
    )
    parser.add_argument(
        "-i", "--icon", action="store_true", help="Show waste type icon"
    )
    args = parser.parse_args()

    # read secrets.yaml
    secrets = {}
    try:
        with open(SECRET_FILENAME) as stream:
            try:
                secrets = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except FileNotFoundError:
        # ignore missing secrets.yaml
        pass

    package_dir = Path(__file__).resolve().parents[2]
    source_dir = package_dir / "waste_collection_schedule" / "source"

    # add module directory to path
    site.addsitedir(str(package_dir))

    if args.source is not None:
        files = args.source
    else:
        files = filter(
            lambda x: x != "__init__", map(lambda x: x.stem, source_dir.glob("*.py")),
        )

    for f in files:
        # iterate through all *.py files in waste_collection_schedule/source
        print(f"Testing source {f} ...")
        module = importlib.import_module(f"waste_collection_schedule.source.{f}")

        # get all names within module
        names = set(dir(module))

        # test if all mandatory names exist
        assert "TITLE" in names
        assert "DESCRIPTION" in names
        assert "URL" in names
        assert "TEST_CASES" in names

        # run through all test-cases
        for name, tc in module.TEST_CASES.items():
            # replace secrets in arguments
            replace_secret(secrets, tc)

            # create source
            source = module.Source(**tc)
            try:
                result = source.fetch()
                print(f"  found {len(result)} entries for {name}")
                if args.list:
                    for x in result:
                        icon_str = f" [{x.icon}]" if args.icon else ""
                        print(f"    {x.date.isoformat()}: {x.type}{icon_str}")
            except KeyboardInterrupt:
                exit()
            except Exception:
                print(traceback.format_exc())


def replace_secret(secrets, d):
    for key in d.keys():
        value = d[key]
        if isinstance(value, dict):
            replace_secret(secrets, value)
        elif isinstance(value, str):
            match = SECRET_REGEX.fullmatch(value)
            if match is not None:
                id = match.group(1)
                if id in secrets:
                    d[key] = secrets[id]
                else:
                    print(f"identifier '{id}' not found in {SECRET_FILENAME}")


if __name__ == "__main__":
    main()
