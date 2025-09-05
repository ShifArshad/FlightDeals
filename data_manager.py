from pprint import pprint
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
SHEETY_END_POINT = "https://api.sheety.co/328088ca2019df72e735477a0a289fc3/myFlightDeals/prices"

class DataManager:
    def __init__(self):
        self._user = os.environ["SHEETY_USRENAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_END_POINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        pprint(data)
        return self.destination_data

    def update_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            response = requests.put(url=f"{SHEETY_END_POINT}/{city['id']}", json=new_data, auth=self._authorization)
            print(response.text)


