#!/usr/bin/python3

import argparse
import importlib
import site
import traceback
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Test sources.")
    parser.add_argument(
        "-s", "--source", action="append", help="Test given source file"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List retrieved entries"
    )
    args = parser.parse_args()

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

        # create source
        for name, tc in module.TEST_CASES.items():
            # run through all test-cases
            source = module.Source(**tc)
            try:
                result = source.fetch()
                print(f"  found {len(result)} entries for {name}")
                if args.list:
                    for x in result:
                        print(f"    {x.date.isoformat()}: {x.type}")
            except KeyboardInterrupt:
                exit()
            except Exception:
                print(traceback.format_exc())


if __name__ == "__main__":
    main()
