import os
from datetime import datetime, timedelta
from typing import Any

import pytz

from solarcontrolar.solcast import SolCast
from common.json_store import JsonStore

class SolarForecastGenerator:
    LOCAL_TZ = pytz.timezone('Europe/London')
    FORECAST_FILE = 'solar_forecast.json'
    HISTORY_FILE = 'solar_forecast_history.json'

    def __init__(self, api_key: str = None, site_id: str = None,
                 forecast_store: JsonStore = JsonStore(FORECAST_FILE),
                 history_store = JsonStore(HISTORY_FILE),
                 tz: Any = None):
        self.api_key = api_key or os.getenv("SOLCAST_API_KEY")
        self.site_id = site_id or os.getenv("SOLCAST_SITE_ID")
        self.local_tz = tz or self.LOCAL_TZ
        self.tomorrow = (datetime.now(self.local_tz) + timedelta(days=1)).date()
        self.tomorrow_key = self.tomorrow.isoformat()
        self.forecast_store = forecast_store
        self.history_store = history_store

    #TODO need to be able to inject SolCast
    def fetch_forecast(self):
        solcast = SolCast(self.api_key, self.site_id)
        return solcast.forecast()

    def check_already_exists(self, forecast) -> bool:
        return self.tomorrow_key in forecast

    def summarise_forecast(self, data):
        day, peak, late = 0.0, 0.0, 0.0

        for entry in data['forecasts']:
            dt = datetime.fromisoformat(entry['period_end'].split('.')[0])
            if dt.date() != self.tomorrow:
                continue
            hour = dt.hour
            estimate = entry['pv_estimate']
            if hour < 16:
                day += estimate
            elif 16 < hour < 19:
                peak += estimate
            elif hour > 19:
                late += estimate

        return {
            'date': self.tomorrow_key,
            'data': {'day': day / 2, 'peak': peak / 2, 'late': late / 2}
        }

    def half_hourly_forecast(self, data):
        result = []
        for entry in data['forecasts']:
            dt = datetime.fromisoformat(entry['period_end'].split('.')[0]) - timedelta(minutes=30)
            if dt.date() == self.tomorrow:
                result.append({
                    'period_start': dt.strftime("%H:%M"),
                    'pv_estimate': entry['pv_estimate'],
                    'pv_estimate10': entry['pv_estimate10'],
                    'pv_estimate90': entry['pv_estimate90'],
                })
        return {'date': self.tomorrow_key, 'data': result}

    def add_to_forecast(self, forecast, summary):
        forecast[summary['date']] = summary['data']
        self.forecast_store.write(forecast)

    def add_to_history(self, summary):
        history = self.history_store.read()
        history[summary['date']] = summary['data']
        self.history_store.write(history)

    def run(self):
        forecast = self.forecast_store.read()
        if not self.check_already_exists(forecast):
            new_forecast = self.fetch_forecast()
            summary = self.summarise_forecast(new_forecast)
            self.add_to_forecast(forecast, summary)

            half_hour = self.half_hourly_forecast(new_forecast)
            self.add_to_history(half_hour)

if __name__ == '__main__':
        manager = SolarForecastGenerator()
        manager.run()


