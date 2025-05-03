#!/usr/bin/env python

import os
import datetime

import pytz

from solarcontrolar.config import Config
from solarcontrolar.givenergy import GivEnergy

tolerance = 1
config = Config()

api_key = os.getenv("GIVENERGY_API_KEY")
inverter_id = "FD2325G412"
givenergy = GivEnergy(api_key, inverter_id)

timezone_str = 'Europe/London'
local_tz = pytz.timezone(timezone_str)
now = datetime.datetime.now(local_tz)
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
hour = now.hour

if 2 <= hour < 5:
    charge_to_percentage = config.get_data()["charge_to_percentage"]
    battery_level = givenergy.battery_level()
    enabled = battery_level <= charge_to_percentage
    if abs(battery_level - charge_to_percentage) > tolerance:
        result = givenergy.set_timed_charge(enabled)
        print(f'{formatted_date} givenergy.set_timed_charge({result})')

elif 16 <= hour < 19:
    discharge_to_percentage = config.get_data()["discharge_to_percentage"]
    battery_level = givenergy.battery_level()
    enabled = battery_level >= discharge_to_percentage
    if abs(battery_level - discharge_to_percentage) > tolerance:
        result = givenergy.set_timed_export(enabled)
        print(f'{formatted_date} givenergy.set_timed_export({result})')

else:
    print(f'{formatted_date} No change')
