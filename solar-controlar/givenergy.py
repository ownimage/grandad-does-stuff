import requests

class GivEnergy:
    def __init__(self, api_key, inverter_id):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Please supply api_key")

        self.inverter_id = inverter_id
        if not self.inverter_id:
            raise ValueError("Please supply inverter_id")

        self.base_url = "https://api.givenergy.cloud/v1"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }


    def get(self, url):
        # Set up headers with authorization
        response = requests.get(url, headers=self.headers,)

        if response.status_code == 200:
            return response.json()
        else:
            raise response.raise_for_status()


    def post(self, url, payload=None):
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise response.raise_for_status()


    def events(self):
        return self.get(f"{self.base_url}/inverter/{self.inverter_id}/events")

    def data(self):
        return self.get(f"{self.base_url}/inverter/{self.inverter_id}/data-points/2025-04-25?page=1")

    def energy_flows(self):
        payload = {
            "start_time": "2025-04-25",
            "end_time": "2025-04-26",
            "grouping": 1
        }
        return self.post(f"{self.base_url}/inverter/{self.inverter_id}/energy-flows", payload)