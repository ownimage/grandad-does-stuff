import os
import json
from datetime import datetime, timedelta

import pytz

from solarcontrolar.solcast import SolCast

local_tz = pytz.timezone('Europe/London') # TODO put in settings
tomorrow = (datetime.now(local_tz) + timedelta(days=1)).date()
tomorrow_key = tomorrow.isoformat()

def fetch_forecast():
    solcast = SolCast(os.getenv('SOLCAST_API_KEY'), os.getenv('SOLCAST_SITE_ID'))
    return solcast.forecast()

def check_already_exists(key):
    file_name = 'solar_forecast.json' # TODO put as constant
    with open(file_name, 'r+') as file:
        forecast = json.load(file)
        return key in forecast

def add_to_forecast(summary):
    file_name = 'solar_forecast.json' # TODO put as constant
    with open(file_name, 'r+') as file:
        forecast = json.load(file)
        forecast[summary['date']] = summary['data']
        file.seek(0)
        json.dump(forecast, file, indent=4)

def add_to_history(data):
    file_name = 'solar_forecast_history.json' # TODO put as constant
    with open(file_name, 'r+') as file:
        history = json.load(file)
        history[data['date']] = data['data']
        file.seek(0)
        json.dump(history, file, indent=4)


def summarise_forecast(data):
    day = sum(
        entry['pv_estimate'] for entry in data['forecasts']
        if datetime.fromisoformat(entry['period_end'].split('.')[0]).date() == tomorrow
        and datetime.fromisoformat(entry['period_end'].split('.')[0]).hour < 16
    ) / 2

    peak = sum(
        entry['pv_estimate'] for entry in data['forecasts']
        if datetime.fromisoformat(entry['period_end'].split('.')[0]).date() == tomorrow
        and 16 < datetime.fromisoformat(entry['period_end'].split('.')[0]).hour < 19
    ) / 2

    late = sum(
        entry['pv_estimate'] for entry in data['forecasts']
        if datetime.fromisoformat(entry['period_end'].split('.')[0]).date() == tomorrow
        and datetime.fromisoformat(entry['period_end'].split('.')[0]).hour > 19
    ) / 2

    return {'date': f'{tomorrow}', 'data': {'day':  day, 'peak': peak, 'late': late}}

def half_hourly_forecast(data):
    half_hourly_values = []
    for entry in data['forecasts']:
        entry_date = datetime.fromisoformat(entry['period_end'].split('.')[0]) - timedelta(minutes=30)
        if entry_date.date() == tomorrow:
            formatted_entry = {
                "period_start":  entry_date.strftime("%H:%M"),
                "pv_estimate": entry['pv_estimate'],
                "pv_estimate10": entry['pv_estimate10'],
                "pv_estimate90": entry['pv_estimate90'],
            }
            half_hourly_values.append(formatted_entry)
    return {'date': f'{tomorrow}', 'data': half_hourly_values}

if __name__ == '__main__':
    if not check_already_exists(tomorrow_key):
        forecast = fetch_forecast()

        summary = summarise_forecast(forecast)
        add_to_forecast(summary)

        hhf = half_hourly_forecast(forecast)
        add_to_history(hhf)

