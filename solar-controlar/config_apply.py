#!/usr/bin/env python

import os
import datetime

import pytz
from tenacity import retry, stop_after_attempt, wait_fixed

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

@retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
def process_timed_action(config_key, comparator, action):
    # Get the target percentage from your configuration
    target_percentage = config.get_data()[config_key]

    # Retrieve the current battery level
    battery_level = givenergy.battery_level()

    # Decide whether to enable the action based on the comparator function
    enabled = comparator(battery_level, target_percentage)

    # Check if the difference exceeds tolerance, then call the action function
    if abs(battery_level - target_percentage) > tolerance:
        result = action(enabled)
        if result:
            print(f'{formatted_date} battery_leval={battery_level} target_percentage={target_percentage} CHANGE {action.__name__}({enabled})')
        else:
            print(f'{formatted_date} battery_leval={battery_level} target_percentage={target_percentage} {action.__name__}({enabled})')



# Then, in your scheduling logic, you can simply do:
if 2 <= hour < 5:
    process_timed_action(
        config_key="charge_to_percentage",
        comparator=lambda level, target: level <= target,
        action=givenergy.set_timed_charge
    )
elif 16 <= hour < 19:
    process_timed_action(
        config_key="discharge_to_percentage",
        comparator=lambda level, target: level >= target,
        action=givenergy.set_timed_export
    )

else:
    print(f'{formatted_date} no action')
