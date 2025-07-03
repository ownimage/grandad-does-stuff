import json
from datetime import datetime, timedelta

from filenames import Filenames
from settings import Settings
from common.json_store import JsonStore


class ConfigGenerator:
    def __init__(self,
                 settings: Settings = Settings(),
                 solar_forecast_store: JsonStore = JsonStore(Filenames.SOLAR_FORECAST_FILE.value),
                 usage_forecast_store: JsonStore = JsonStore(Filenames.USAGE_FORECAST_FILE.value),
                 usage_baseline_store: JsonStore = JsonStore(Filenames.USAGE_BASELINE_FILE.value),
                 config_store: JsonStore = JsonStore(Filenames.CONFIG.value)
                 ):
        self.settings = settings
        self.solar_forecast = solar_forecast_store.read()
        self.usage_forecast = usage_forecast_store.read()
        self.usage_baseline = usage_baseline_store.read()
        self.config_store = config_store

        self.battery_min_percentage = 100.0 * self.settings.battery_min_kwh() / self.settings.battery_capacity_kwh()

        self.tomorrow = (datetime.now(self.settings.timezone()) + timedelta(days=1)).date()
        self.tomorrow_iso = self.tomorrow.isoformat()
        self.tomorrow_day = self.tomorrow.strftime('%A')

    def get_usage_forecast(self):
        try:
            return self.usage_forecast[self.tomorrow_iso]
        except KeyError:
            return self.usage_baseline[self.tomorrow_day]

    def calculate_charge_percentage(self):
        usage = self.get_usage_forecast()

        solar_forecast_before_4 = {k: v for k, v in self.solar_forecast[self.tomorrow_iso].items() if k < "16:00"}
        solar_total_before_4 = sum(d.get("pv_estimate", 0) for d in solar_forecast_before_4.values()) / 2.0

        charge_for_100_peak = self.settings.battery_capacity_kwh() - self.settings.solar_forecast_multiplier() * solar_total_before_4 + usage['day']
        charge_for_before_sun = usage['early']
        charge_requirement = max(charge_for_100_peak, charge_for_before_sun)

        charge_to_unlimited = charge_requirement * 100 / self.settings.battery_capacity_kwh()
        return int(max(self.battery_min_percentage, min(charge_to_unlimited, 100)))

    def write_config(self, output_path="config.json"):
        config = {"charge_to_percentage": self.calculate_charge_percentage()}
        self.config_store.write(config)


# Example usage:
if __name__ == "__main__":
    config_generator = ConfigGenerator()
    config_generator.write_config()
