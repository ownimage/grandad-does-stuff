import json

from datetime import datetime, timedelta, time

start = (datetime.today() - timedelta(days=6)).date()
end = (datetime.today() - timedelta(days=1)).date()


# --- Load the Forecast JSON file ---
with open('solar_forecast_history.json') as f:
    raw_data = json.load(f)

forecast_total = 0 # kWh
forecast_count = 0
for date_str, entries in raw_data.items():
    for period in entries:
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
        if start <= d <= end:
            forecast_total += 0.5 * period['pv_estimate']
            forecast_count += 1
print(f'forecast total: {forecast_total} {forecast_count}')

# --- Load Actuals Data ---
with open('solar_actuals.json') as f:
    actual_data = json.load(f)['data']

actual_total = 0
actual_count = 0
for item in actual_data.values():
    d = datetime.strptime(item['start_time'], "%Y-%m-%d %H:%M").date()
    if start <= d <= end:
        actual_total += sum(item['data'].values())
        actual_count += 1
print(f'actual total: {actual_total} {actual_count}')

solar_forecast_multiplier = actual_total / forecast_total
print(f'solar forecast multiplier: {solar_forecast_multiplier}')

if actual_count == 288 and forecast_count == 288 and 0.5 <= solar_forecast_multiplier <= 1.5:
    with open("settings.json", "r") as f:
        settings = json.load(f)

    # Update the value
    settings["solar_forecast_multiplier"] = solar_forecast_multiplier

    # Save the updated settings
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

