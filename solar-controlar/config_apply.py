#!/usr/bin/env python

import os
import datetime
import logging

import pytz
from tenacity import retry, stop_after_attempt, wait_fixed

from solarcontrolar.config import Config
from solarcontrolar.givenergy import GivEnergy

# Setup logger for better testability
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Configuration injection
def get_config():
    return Config()

def get_givenergy():
    api_key = os.getenv("GIVENERGY_API_KEY")
    inverter_id = os.getenv("GIVENERGY_INVERTER_ID")
    return GivEnergy(api_key, inverter_id)

# Time handling abstraction
def get_current_time(timezone_str="Europe/London"):
    local_tz = pytz.timezone(timezone_str)
    now = datetime.datetime.now(local_tz)
    return now, now.strftime("%Y-%m-%d %H:%M:%S")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
def charge_to_percentage(config, givenergy, tolerance, formatted_date):
    target_percentage = config.get_data()["charge_to_percentage"]
    battery_level = givenergy.battery_level()
    enabled = battery_level <= target_percentage

    if abs(battery_level - target_percentage) > tolerance:
        result = givenergy.set_timed_charge(enabled)
        if result:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} CHANGE set_timed_charge({enabled})"
        else:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} set_timed_charge({enabled})"
    else:
        msg = f"{formatted_date} battery_level={battery_level} is within tolerance={tolerance} of target_percentage={target_percentage} NO CHANGE"

    logger.info(msg)
    return msg  # Allows assertion in unit tests

def limit_timed_export(givenergy, hour, minute, tolerance, formatted_date):
    slot_duration = (19 - 16) * 60
    elapsed_minutes = (hour - 16) * 60 + minute
    target_percentage = int( (1 - (elapsed_minutes / slot_duration)) * 100)

    battery_level = givenergy.battery_level()
    enabled = battery_level >= target_percentage

    if abs(battery_level - target_percentage) > tolerance:
        result = givenergy.set_timed_export(enabled)
        if result:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} CHANGE set_timed_export({enabled})"
        else:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} set_timed_export({enabled})"
    else:
        msg = f"{formatted_date} battery_level={battery_level} is within tolerance={tolerance} of target_percentage={target_percentage} NO CHANGE"

    logger.info(msg)
    return msg  # Allows assertion in unit tests

# Main function for better testability
def main():
    config = get_config()
    givenergy = get_givenergy()
    tolerance = 1  # TODO should be in settings

    now, formatted_date = get_current_time()
    hour = now.hour
    minute = now.minute

    if 2 <= hour < 5:
        apply_config(config, givenergy, tolerance, formatted_date)
    elif 16 <= hour < 19:
        limit_timed_export(givenergy, hour, minute, tolerance, formatted_date)
    else:
        logger.info(f"{formatted_date} no action")

if __name__ == "__main__":
    main()