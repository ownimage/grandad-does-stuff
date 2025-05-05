import os
import json
from datetime import datetime, timedelta

import pytz

from solarcontrolar.solcast import SolCast

local_tz = pytz.timezone('Europe/London')
tomorrow = (datetime.now(local_tz) + timedelta(days=1)).date()
tomorrow_key = tomorrow.isoformat()

def fetch_forecast():
    solcast = SolCast(os.getenv('SOLCAST_API_KEY'), os.getenv('SOLCAST_SITE_ID'))
    return solcast.forecast()

def check_already_exists(key):
    file_name = 'solar_forecast.json'
    with open(file_name, 'r+') as file:
        history = json.load(file)
        return key in history

def add_to_history(data):
    file_name = 'solar_forecast.json'
    with open(file_name, 'r+') as file:
        history = json.load(file)
        history[data['date']] = data['data']
        file.seek(0)
        json.dump(history, file, indent=4)


def summarise(data):
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

    return {'date': f'{tomorrow}', 'data': {'day': day, 'peak': peak, 'late': late}}

if not check_already_exists(tomorrow_key):
    forecast = fetch_forecast()
    summary = summarise(forecast)
    add_to_history(summary)

