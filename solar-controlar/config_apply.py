import os
import datetime
import logging
import json

import pytz
from tenacity import retry, stop_after_attempt, wait_fixed

from solarcontrolar.config import Config
from solarcontrolar.givenergy import GivEnergy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

class ConfigApply:
    def __init__(self, Config=Config(), os=os, json=json, GivEnergy=GivEnergy, pytz=pytz, datetime=datetime, logger=logger ):
        self.__Config = Config
        self.__os = os
        self.__json = json
        self.__GivEnergy = GivEnergy
        self.__pytz = pytz
        self.__datetime = datetime
        self.__logger = logger

    def get_config(self):
        return self.__Config.get_data()

    def get_settings(self):
        with open("settings.json", "r") as file:
            return self.__json.load(file)

    def get_givenergy(self):
        api_key = self.__os.getenv("GIVENERGY_API_KEY")
        inverter_id = self.__os.getenv("GIVENERGY_INVERTER_ID")
        return self.__GivEnergy(api_key, inverter_id)

    def get_current_time(self, timezone_str="Europe/London"):
        local_tz = self.__pytz.timezone(timezone_str)
        now = self.__datetime.datetime.now(local_tz)
        return now, now.strftime("%Y-%m-%d %H:%M:%S")

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def charge_to_percentage(self, givenergy, tolerance, formatted_date):
        target_percentage = self.get_config()["charge_to_percentage"]
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

        self.__logger.info(msg)
        return msg  # Allows assertion in unit tests

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def limit_timed_export(self, givenergy, target_percentage, tolerance, formatted_date):
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

        self.__logger.info(msg)
        return msg  # Allows assertion in unit tests

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def full_discharge(self, givenergy, formatted_date):
        battery_level = givenergy.battery_level()

        result = givenergy.set_timed_export(True)
        if result:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage=0 CHANGE set_timed_export(True)"
        else:
            msg = f"{formatted_date} battery_level={battery_level} target_percentage=0 set_timed_export(True)"

        self.__logger.info(msg)
        return msg  # Allows assertion in unit tests

# Main function for better testability
    def main(self):
        config = self.get_config()
        givenergy = self.get_givenergy()
        settings = self.get_settings()
        tolerance = settings["tolerance_percent"]
        init_discharge_target = settings["last_30mins_discharge_target"]

        now, formatted_date = self.get_current_time()
        hour = now.hour
        minute = now.minute

        if 2 <= hour < 5:
            return self.charge_to_percentage(givenergy, tolerance, formatted_date)
        elif 16 <= hour < 19:
            if hour < 18 or minute < 30: # not last half-hour drain immediately to init_discharge_target
                return self.limit_timed_export(givenergy, init_discharge_target, tolerance, formatted_date)
            else: # last half-hour drain to floor
                return self.full_discharge(givenergy, formatted_date)

        else:
            msg = f"{formatted_date} no action"
            self.__logger.info(msg)
            return msg

if __name__ == "__main__":
    ConfigApply().main()