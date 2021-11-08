import datetime
import json

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Seattle Public Utilities"
DESCRIPTION = "Source for Seattle Public Utilities waste collection."
URL = "https://myutilities.seattle.gov/eportal/#/accountlookup/calendar"
TEST_CASES = {
    "City Hall": {"street_address": "600 4th Ave"},
    "Ballard Builders": {"street_address": "7022 12th Ave NW"},
    "Carmona Court": {"street_address": "1127 17th Ave E"},
}


def get_service_icon(service_name):
    switcher = {"Garbage": "trash-can", "Recycle": "recycle", "Food/Yard Waste": "leaf"}
    return switcher.get(service_name, "trash-can")


class Source:
    def __init__(self, street_address):
        self._street_address = street_address

    def fetch(self):

        # Mimicking the same API calls the calendar lookup page uses:
        # 1. find account code
        # 2. find account ID for a given address
        # 3. get token (uses basic auth and the customerID = guest
        # 4. get account summary
        # 5. get calendar

        # step 1
        find_address_payload = {
            "address": {"addressLine1": self._street_address, "city": "", "zip": ""}
        }

        r = requests.post(
            "https://myutilities.seattle.gov/rest/serviceorder/findaddress",
            json=find_address_payload,
        )

        address_info = json.loads(r.text)
        prem_code = address_info["address"][0]["premCode"]

        # step 2
        find_account_payload = {"address": {"premCode": prem_code}}

        r = requests.post(
            "https://myutilities.seattle.gov/rest/serviceorder/findAccount",
            json=find_account_payload,
        )

        account_info = json.loads(r.text)
        account_number = account_info["account"]["accountNumber"]

        # step 3
        token_payload = {
            "grant_type": "password",
            "username": "guest",
            "password": "guest",
        }

        r = requests.post(
            "https://myutilities.seattle.gov/rest/auth/guest", data=token_payload
        )

        token_info = json.loads(r.text)
        token = token_info["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # step 4
        swsummary_payload = {
            "customerId": "guest",
            "accountContext": {
                "accountNumber": account_number,
                "personId": None,
                "companyCd": None,
                "serviceAddress": None,
            },
        }

        r = requests.post(
            "https://myutilities.seattle.gov/rest/guest/swsummary",
            json=swsummary_payload,
            headers=headers,
        )

        summary_info = json.loads(r.text)
        # the description property in each service in swServices it's either 'Garbage', 'Recycle', or 'Food/Yard Waste'

        swServices = summary_info["accountSummaryType"]["swServices"][0]["services"]
        personId = summary_info["accountContext"]["personId"]
        companyCd = summary_info["accountContext"]["companyCd"]

        # step 5
        waste_calendar_payload = {
            "customerId": "guest",
            "accountContext": {
                "accountNumber": account_number,
                "personId": personId,
                "companyCd": companyCd,
            },
            "servicePoints": [],
        }

        # fill out payload
        for service in swServices:
            waste_calendar_payload["servicePoints"].append(service["servicePointId"])

        r = requests.post(
            "https://myutilities.seattle.gov/rest/solidwastecalendar",
            json=waste_calendar_payload,
            headers=headers,
        )

        calendar_info = json.loads(r.text)

        # output
        entries = []

        for service in swServices:
            name = service["description"]
            servicePointId = service["servicePointId"]

            for collection_date in calendar_info["calendar"][servicePointId]:
                next_date = datetime.datetime.strptime(
                    collection_date, "%m/%d/%Y"
                ).date()
                service_icon = "mdi:" + get_service_icon(name)

                entries.append(Collection(date=next_date, t=name, icon=service_icon))

        return entries
