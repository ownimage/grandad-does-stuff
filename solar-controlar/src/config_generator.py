from datetime import datetime, timedelta

from common.dateHelper import DateHelper
from filenames import Filenames
from settings import Settings
from common.json_store import JsonStore


class ConfigGenerator:
    def __init__(self,
                 settings: Settings = Settings(),
                 solar_forecast_store: JsonStore = JsonStore(Filenames.SOLAR_FORECAST_FILE.value),
                 usage_forecast_store: JsonStore = JsonStore(Filenames.USAGE_FORECAST_FILE.value),
                 usage_actuals_store: JsonStore = JsonStore(Filenames.USAGE_ACTUALS.value),
                 config_store: JsonStore = JsonStore(Filenames.CONFIG.value),
                 datehelper=DateHelper(),
                 ):
        self.settings = settings
        self.solar_forecast = solar_forecast_store.read()
        self.usage_forecast = usage_forecast_store.read()
        self.usage_actuals = usage_actuals_store.read()
        self.config_store = config_store
        self.datehelper = datehelper

        self.battery_min_percentage = 100.0 * self.settings.battery_min_kwh() / self.settings.battery_capacity_kwh()

        self.tomorrow = (datetime.now(self.settings.timezone()) + timedelta(days=1)).date()
        self.tomorrow_iso = self.tomorrow.isoformat()
        self.tomorrow_day = self.tomorrow.strftime('%A')

    def get_min_max_estimate(self):
        usage1 = self.usage_actuals[self.datehelper.offset_iso(-6)]
        usage2 = self.usage_actuals[self.datehelper.offset_iso(-13)]
        solar = self.solar_forecast[self.datehelper.tomorrow_iso()]
        min_total = 0
        max_total = 0
        total = 0
        for key, solar_value in sorted(solar.items()):
            if "05:00" <= key <= "16:00":
                usage = (usage1[key] + usage2[key]) / 2
                total += solar_value["pv_estimate"] * self.settings.solar_forecast_multiplier() / 2 - usage
                min_total = min(min_total, total)
                max_total = max(max_total, total)
        return min_total, max_total

    def calculate_charge_percentage(self):
        min_total, max_total = self.get_min_max_estimate()

        kwh_for_100_peak = self.settings.battery_capacity_kwh() - max_total
        kwh_for_before_sun = self.settings.battery_min_kwh() - min_total
        kwh_requirement = max(kwh_for_100_peak, kwh_for_before_sun)

        percentage_unlimited = kwh_requirement * 100 / self.settings.battery_capacity_kwh()
        return int(max(self.battery_min_percentage, min(percentage_unlimited, 100)))

    def write_config(self):
        config = self.config_store.read()
        config["charge_to_percentage"] = self.calculate_charge_percentage()
        self.config_store.write(config)


# Example usage:
if __name__ == "__main__":
    config_generator = ConfigGenerator()
    config_generator.write_config()
