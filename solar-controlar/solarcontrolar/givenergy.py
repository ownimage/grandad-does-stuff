import requests
from datetime import datetime, timedelta
from collections import defaultdict

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

    def get(self, url, payload=None):
        # Set up headers with authorization
        response = requests.request("GET", url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise response.raise_for_status()

    def post(self, url, payload=None):
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200 or response.status_code == 201:
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

    def settings(self):
        return self.get(f"{self.base_url}/inverter/{self.inverter_id}/settings")

    def setting_read(self, setting_id):
        return self.post(f"{self.base_url}/inverter/{self.inverter_id}/settings/{setting_id}/read")

    def setting_write(self, setting_id, value):
        payload = {"value": value}
        return self.post(f"{self.base_url}/inverter/{self.inverter_id}/settings/{setting_id}/write", payload)

    def setting_write_validate(self, setting_id, value, function_name):
        self.setting_write(setting_id, value)
        new_value = self.setting_read(setting_id)['data']['value']
        if new_value != value:
            raise RuntimeError(f'Givnergy::{function_name}({value} failed')
        return new_value


    def get_timed_charge(self):
        return self.setting_read(66)

    def set_timed_charge(self, value):
        return self.setting_write_validate(66, value, 'set_enable_ac_charge')

    def get_timed_export(self):
        return self.setting_read(56)

    def set_timed_export(self, value):
        return self.setting_write_validate(56, value, 'set_enable_dc_discharge')

    def get_day_usage(self, days_ago):
        today = datetime.today()
        start_time = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        end_time = (today - timedelta(days=days_ago-1)).strftime("%Y-%m-%d")
        payload = {"start_time": start_time, "end_time": end_time, "grouping": 0}
        return self.post(f"{self.base_url}/inverter/{self.inverter_id}/energy-flows", payload)

    def last_4_weeks_usage(self):
        weekly_usage = defaultdict(float)  # Dictionary to store sums per day of the week

        # Iterate over the last 28 days
        for days_ago in range(1, 8):
            daily_data = self.get_day_usage(days_ago)  # Get usage for the given day
            date_obj = datetime.today() - timedelta(days=days_ago)
            day_of_week = date_obj.strftime("%A")  # Convert to full weekday name

            daily_usage_sum = sum(entry["data"].get("0", 0) for entry in daily_data["data"].values())
            daily_usage_sum += sum(entry["data"].get("3", 0) for entry in daily_data["data"].values())
            daily_usage_sum += sum(entry["data"].get("5", 0) for entry in daily_data["data"].values())
            weekly_usage[day_of_week] += daily_usage_sum

        return dict(weekly_usage)

    def battery_level(self):
        return self.get(f"{self.base_url}/inverter/{self.inverter_id}/system-data/latest")['data']['battery']['percent']


