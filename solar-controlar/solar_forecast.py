import json
from datetime import datetime, timedelta

# Load the JSON data
with open("solar_forecast.json", "r") as file:
    data = json.load(file)

# Dictionary to store daily sums
daily_sums = {}

tomorrow = (datetime.utcnow() + timedelta(days=1)).date()

# Sum up pv_estimate values for tomorrow from 00:00 until 16:00
early_pv_estimate = sum(
    entry["pv_estimate"] for entry in data["forecasts"]
    if datetime.fromisoformat(entry["period_end"].split('.')[0]).date() == tomorrow
    and datetime.fromisoformat(entry["period_end"].split('.')[0]).hour < 16
) / 2

total_pv_estimate = sum(
    entry["pv_estimate"] for entry in data["forecasts"]
    if datetime.fromisoformat(entry["period_end"].split('.')[0]).date() == tomorrow
) / 2

late_pv_estimate = sum(
    entry["pv_estimate"] for entry in data["forecasts"]
    if datetime.fromisoformat(entry["period_end"].split('.')[0]).date() == tomorrow
    and datetime.fromisoformat(entry["period_end"].split('.')[0]).hour > 19
) / 2

print(f"Total pv_estimate for {tomorrow} until 16:00: {early_pv_estimate:.2f}")
print(f"Total pv_estimate for {tomorrow}: {total_pv_estimate:.2f}")
print(f"Total pv_estimate for {tomorrow} from 19:00: {late_pv_estimate:.2f}")
