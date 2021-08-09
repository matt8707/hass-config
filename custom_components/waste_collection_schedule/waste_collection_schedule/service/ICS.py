import datetime
import logging
import re

import icalendar
import recurring_ical_events

_LOGGER = logging.getLogger(__name__)


class ICS:
    def __init__(self, offset=None, regex=None):
        self._offset = offset
        self._regex = None
        if regex is not None:
            self._regex = re.compile(regex)

    def convert(self, ics_data):
        # parse ics file
        try:
            calendar = icalendar.Calendar.from_ical(ics_data)
        except Exception as err:
            _LOGGER.error(f"Parsing ics data failed:{str(err)}")
            _LOGGER.debug(ics_data)
            return []

        # calculate start- and end-date for recurring events
        start_date = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        if self._offset is not None:
            start_date -= datetime.timedelta(days=self._offset)
        end_date = start_date.replace(year=start_date.year + 1)

        events = recurring_ical_events.of(calendar).between(start_date, end_date)

        entries = []
        for e in events:
            if e.name == "VEVENT":
                # calculate date
                dtstart = None
                if type(e.get("dtstart").dt) == datetime.date:
                    dtstart = e.get("dtstart").dt
                elif type(e.get("dtstart").dt) == datetime.datetime:
                    dtstart = e.get("dtstart").dt.date()
                if self._offset is not None:
                    dtstart += datetime.timedelta(days=self._offset)

                # calculate waste type
                summary = str(e.get("summary"))
                if self._regex is not None:
                    match = self._regex.match(summary)
                    if match:
                        summary = match.group(1)

                entries.append((dtstart, summary))
        return entries
