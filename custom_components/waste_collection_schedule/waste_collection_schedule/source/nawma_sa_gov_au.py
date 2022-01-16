import datetime
import requests
from html.parser import HTMLParser
from waste_collection_schedule import Collection


TITLE = "North Adelaide Waste Management Authority"
DESCRIPTION = "Source for nawma.sa.gov.au (Salisbury, Playford, and Gawler South Australia)."
URL = "http://www.nawma.sa.gov.au"
TEST_CASES = {
    "128 Bridge Road": {"street_number": "128", "street_name": "Bridge Road", "suburb": "Pooraka"}, # Monday
    "226 Bridge Road": {"street_number": "226", "street_name": "Bridge Road", "suburb": "Pooraka"}, # Monday reverse
    "Whites Road": {"street_name": "Whites Road", "suburb": "Paralowie"}, # Tuesday
    "Hazel Avenue": {"street_name": "Hazel Avenue", "suburb": "Angle Value"}, # Wednesday
    "155 Murray St": {"street_name": "Murray Street (sec between Ayers and the railway line", "suburb": "Gawler"}, # Thursday
    "Edward Crescent": {"street_name": "Edward Crescent", "suburb": "Evanston Park"}, # Friday
}


class CollectionResultsParser(HTMLParser):
    """
    Parser for the collection results <div> element returned by the API.
    """

    def __init__(self):
        super().__init__()
        self._entries = []

        self._current_type = None

        # State machine
        self._in_entry = False
        self._read_type = True
        self._cell_count = 0

    @property
    def entries(self):
        return self._entries

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("class") == "coll-content":
            self._in_entry = True
            self._cell_count = 0
        elif tag == "h6" and self._in_entry:
            self._read_type = True
        elif tag == "td":
            self._cell_count = self._cell_count + 1

    def handle_endtag(self, tag):
        if tag == "div":
            self._in_entry = False

    def handle_data(self, data):
        if self._read_type:
            self._current_type = data
            self._read_type = False

        elif self._in_entry and self._cell_count == 6:
            date = datetime.datetime.strptime(data.strip(), '%d %B %Y').date()

            icon = "mdi:trash-can"
            if "yellow" in self._current_type:
                icon = "mdi:recycle"
            elif "green" in self._current_type:
                icon = "mdi:leaf"

            self._entries.append(Collection(date, self._current_type, icon))

            # We're finished with this entry
            self._in_entry = False


class Source:
    def __init__(self, street_name, suburb, street_number="", pid="2444"):
        self._street_number = street_number  # Optional
        self.street_name = street_name
        self._suburb = suburb
        self._pid = pid  # Not really sure what this is!

    def fetch(self):
        params = {
            "action": "collection_day",
            "street_no": self._street_number,
            "street": self.street_name,
            "area": self._suburb,
            "pid": self._pid,
        }

        r = requests.post(
            "http://www.nawma.sa.gov.au/wp-admin/admin-ajax.php",
            data=params,  # The parameters are sent as the body of the post
        )

        p = CollectionResultsParser()
        p.feed(r.text)
        return p.entries
