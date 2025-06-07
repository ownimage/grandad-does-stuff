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
def apply_config(config, givenergy, config_key, comparator, action, tolerance, now, formatted_date):
    target_percentage = config.get_data()[config_key]
    battery_level = givenergy.battery_level()
    enabled = comparator(battery_level, target_percentage)

    if abs(battery_level - target_percentage) > tolerance:
        result = action(enabled)
        if result:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} CHANGE {action.__name__}({enabled})"
        else:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage={target_percentage} {action.__name__}({enabled})"
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

    if 2 <= hour < 5:
        apply_config(config, givenergy, "charge_to_percentage", lambda lvl, tgt: lvl <= tgt, givenergy.set_timed_charge, tolerance, now, formatted_date)
    elif 16 <= hour < 19:
        apply_config(config, givenergy, "discharge_to_percentage", lambda lvl, tgt: lvl >= tgt, givenergy.set_timed_export, tolerance, now, formatted_date)
    else:
        logger.info(f"{formatted_date} no action")

if __name__ == "__main__":
    main()