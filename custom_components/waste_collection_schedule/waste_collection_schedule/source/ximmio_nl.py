from datetime import datetime, timedelta

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Ximmio"
DESCRIPTION = "Source for Ximmio B.V. waste collection."
URL = "https://www.ximmio.nl"
TEST_CASES = {
    "ACV Group": {"company": "acv", "post_code": "6721MH", "house_number": 1},
    "Meerlanden": {"company": "meerlanden", "post_code": "1435BX", "house_number": 650},
    "Almere": {"company": "almere", "post_code": "1318NG", "house_number": 15},
}


SERVICE_URLS = {
    "meerlanden": "https://wasteprod2api.ximmio.com",
    "rad": "https://wasteprod2api.ximmio.com",
}

SERVICE_IDS = {
    "acv": "f8e2844a-095e-48f9-9f98-71fceb51d2c3",
    "almere": "53d8db94-7945-42fd-9742-9bbc71dbe4c1",
    "areareiniging": "adc418da-d19b-11e5-ab30-625662870761",
    "avri": "78cd4156-394b-413d-8936-d407e334559a",
    "bar": "bb58e633-de14-4b2a-9941-5bc419f1c4b0",
    "hellendoorn": "24434f5b-7244-412b-9306-3a2bd1e22bc1",
    "meerlanden": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
    "meppel": "b7a594c7-2490-4413-88f9-94749a3ec62a",
    "rad": "13a2cad9-36d0-4b01-b877-efcb421a864d",
    "reinis": "9dc25c8a-175a-4a41-b7a1-83f237a80b77",
    "twentemilieu": "8d97bb56-5afd-4cbc-a651-b4f7314264b4",
    "waardlanden": "942abcf6-3775-400d-ae5d-7380d728b23c",
    "ximmio": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
}


class Source:
    def __init__(self, company, post_code, house_number):
        self._post_code = post_code
        self._house_number = house_number
        self._url = SERVICE_URLS.get(company, "https://wasteapi.ximmio.com")
        self._company_code = SERVICE_IDS[company]

    def fetch(self):
        data = {
            "postCode": self._post_code,
            "houseNumber": self._house_number,
            "companyCode": self._company_code,
        }
        r = requests.post(f"{self._url}/api/FetchAdress", data=data)
        d = r.json()

        dataList = d["dataList"][0]
        data = {
            "uniqueAddressID": dataList["UniqueId"],
            "startDate": datetime.now().strftime("%Y-%m-%d"),
            "endDate": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "companyCode": self._company_code,
            "community": dataList.get("Community", ""),
        }
        r = requests.post(f"{self._url}/api/GetCalendar", data=data)
        d = r.json()

        entries = []
        for wasteType in d["dataList"]:
            for date in wasteType["pickupDates"]:
                entries.append(
                    Collection(
                        date=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").date(),
                        t=wasteType["_pickupTypeText"],
                    )
                )
        return entries
