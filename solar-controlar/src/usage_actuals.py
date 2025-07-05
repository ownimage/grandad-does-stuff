import json
from datetime import datetime, time
from collections import defaultdict
from dateutil import parser
import pytz

from common.json_store import JsonStore
from filenames import Filenames
from settings import Settings
from solarcontrolar.givenergy import GivEnergy


class UsageActuals:
    def __init__(self,
                 usage_store=JsonStore(Filenames.USAGE_ACTUALS.value),
                 timezone = Settings().timezone(),
                 days: int = 28
                 ):
        self.usage_store = usage_store
        self.timezone = timezone
        self.days = days

    def summarize(self, data_points):
        entries = sorted([
            (parser.parse(ts), value)
            for ts, value in data_points.items()
        ])

        # Initialize nested dictionary for the summary
        summary = defaultdict(dict)

        for i in range(1, len(entries)):
            current_dt, current_val = entries[i]
            _, previous_val = entries[i - 1]
            delta = round(current_val - previous_val, 3)

            # Round to nearest half hour
            minute = current_dt.minute
            rounded_minute = 0 if minute < 30 else 30
            rounded_dt = current_dt.replace(
                minute=rounded_minute, second=0, microsecond=0
            )

            date_str = rounded_dt.strftime("%Y-%m-%d")
            time_str = rounded_dt.strftime("%H:%M")

            # Accumulate deltas into their half-hour bins
            summary[date_str][time_str] = summary[date_str].get(time_str, 0) + delta
        return summary

    def fetch(self):
        data = GivEnergy().get_meter_data(datetime.strptime("2025-07-03", "%Y-%m-%d").date(), 1)
        # Extract relevant fields
        summary = {
            datetime.fromisoformat(entry["time"])
            .astimezone(self.timezone)
            .strftime("%Y-%m-%d %H:%M:%S %Z%z"): entry["today"]["consumption"]
            for entry in data["data"]
        }

        usage_store.write(dict(sorted(summary.items())))


if __name__ == '__main__':
    ua = UsageActuals()

    usage_store = JsonStore(Filenames.USAGE_ACTUALS.value)
    raw_data = ua.usage_store.read()
    day_data = ua.summarize(raw_data)

    import pprint
    pprint.pprint(dict(day_data), sort_dicts=False)

