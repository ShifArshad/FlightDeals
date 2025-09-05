import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

LOCATION_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
TOKEN_END_POINT = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["API_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Tye': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type':'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=TOKEN_END_POINT, headers=header, data=body)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']}")
        return response.json()['access_token']


    def get_destination_code(self, city_name):
        print(f"Using this token to get destination {self._token}")
        headers = {
                "Authorization": f"Bearer {self._token}"
       }

        query = {
           "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }

        response = requests.get(url=LOCATION_ENDPOINT, headers=headers, params=query)
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code