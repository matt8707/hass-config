import datetime

from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Example Source"
DESCRIPTION = "Source for example waste collection."
URL = None
TEST_CASES = {"Example": {"days": 10}}


class Source:
    def __init__(self, days=20, per_day=2, types=5):
        self._days = days
        self._per_day = per_day
        self._types = types

    def fetch(self):
        now = datetime.datetime.now().date()

        entries = []
        ap_type = 0

        for day in range(self._days):
            for idx in range(self._per_day):
                entries.append(
                    Collection(
                        now + datetime.timedelta(days=day + 7),
                        f"Type{(ap_type % self._types) + 1}",
                    )
                )
                ap_type = ap_type + 1

        return entries
