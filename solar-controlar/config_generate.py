import os
import json
from datetime import datetime, timedelta

import pytz

# TODO need to pass these in somehow
battery_capacity = 9.6
battery_min = 0.4

battery_min_percentage = 100.0 * battery_min / battery_capacity

def get_solar_forecast(key):
    with open('solar_forecast.json', 'r') as file:
        return json.load(file)[key]

def get_usage_forecast(key):
    with open('usage_forecast.json', 'r') as file:
        return json.load(file)[key]

local_tz = pytz.timezone('Europe/London')
tomorrow = (datetime.now(local_tz) + timedelta(days=1)).date().isoformat()

solar_forecast = get_solar_forecast(tomorrow)
usage_forecast = get_usage_forecast(tomorrow)

# KWh
charge_for_100_peak = battery_capacity - solar_forecast['day'] + usage_forecast['day']
charge_for_before_sun = usage_forecast['early']
charge_requirement = max(charge_for_100_peak, charge_for_before_sun)

charge_to_unlimited = charge_requirement * 100/battery_capacity
charge_to_percentage = int(max(battery_min_percentage, min(charge_to_unlimited, 100)))

discharge_to_unlimited = (battery_min - solar_forecast['late'] + usage_forecast['late']) * 100/battery_capacity
discharge_to_percentage = int(max(battery_min_percentage, min(discharge_to_unlimited, 100)))

config = {
  "charge_to_percentage": charge_to_percentage,
  "discharge_to_percentage": discharge_to_percentage
}

with open("config.json", "w") as file:
    json.dump(config, file, indent=4)