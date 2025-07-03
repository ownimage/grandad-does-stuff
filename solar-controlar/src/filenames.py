from enum import Enum


class Filenames(Enum):
    SOLAR_FORECAST_FILE = "solar_forecast_history.json"
    USAGE_FORECAST_FILE = "usage_forecast.json"
    USAGE_BASELINE_FILE = "usage_baseline.json"
    CONFIG = "config.json"
    SETTINGS = "settings.json"