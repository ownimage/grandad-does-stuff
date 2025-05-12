#!/usr/bin/env python

import os
import datetime

import pytz
from tenacity import retry, stop_after_attempt, wait_fixed

from solarcontrolar.config import Config
from solarcontrolar.givenergy import GivEnergy

tolerance = 1 # TODO should be in settings
config = Config()

api_key = os.getenv("GIVENERGY_API_KEY")
inverter_id = os.getenv("GIVENERGY_INVERTER_ID")
givenergy = GivEnergy(api_key, inverter_id)

timezone_str = 'Europe/London' # TODO should be in settings
local_tz = pytz.timezone(timezone_str)
now = datetime.datetime.now(local_tz)
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
hour = now.hour

@retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
def apply_config(config_key, comparator, action):
    target_percentage = config.get_data()[config_key]
    battery_level = givenergy.battery_level()
    enabled = comparator(battery_level, target_percentage)

    if abs(battery_level - target_percentage) > tolerance:
        result = action(enabled)
        if result:
            print(f'{formatted_date} battery_leval={battery_level} target_percentage={target_percentage} CHANGE {action.__name__}({enabled})')
        else:
            print(f'{formatted_date} battery_leval={battery_level} target_percentage={target_percentage} {action.__name__}({enabled})')
    else:
        print(f'{formatted_date} battery_leval={battery_level} is within tolerance={tolerance} of target_percentage={target_percentage} NO CHANGE')



# Then, in your scheduling logic, you can simply do:
if 2 <= hour < 5:
    apply_config(
        config_key="charge_to_percentage",
        comparator=lambda level, target: level <= target,
        action=givenergy.set_timed_charge
    )
elif 16 <= hour < 19:
    apply_config(
        config_key="discharge_to_percentage",
        comparator=lambda level, target: level >= target,
        action=givenergy.set_timed_export
    )
else:
    print(f'{formatted_date} no action')
