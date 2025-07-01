import json
import os
from datetime import datetime, time
from collections import defaultdict


from solarcontrolar.givenergy import GivEnergy


def get_givenergy():
    api_key = os.getenv('GIVENERGY_API_KEY')
    inverter_id = os.getenv('GIVENERGY_INVERTER_ID')
    return GivEnergy(api_key, inverter_id)

if __name__ == '__main__':
    filename = 'usage_actuals.json'
    
    with open(filename, 'r') as file:
        data = json.load(file)
    
    end_date = datetime.combine(datetime.today(), time.min).date()
    print(f'{end_date.isoformat()}')
    givenergy = get_givenergy()
    usage_actuals = givenergy.get_usage_actuals(end_date, 7)

    summary = defaultdict(dict)
    for item in usage_actuals['data'].values():
        date_key = item['start_time'].split()[0]
        start_time = item['start_time'].split()[1]
        usage = [item['data']['0'], item['data']['3'], item['data']['5']]
        # usage = sum(item['data'].values())
        summary[date_key][start_time] = usage

    # discard lowest value as it may not be fully populated
    oldest_date = min(summary)
    summary.pop(oldest_date)

    # discard highest value as it may not be fully populated
    newest_date = max(summary)
    summary.pop(newest_date)

    # for key in summary:
    #     print(f'{key}: {sum(summary[key].values())}')

    with open(filename, 'r') as f:
        data = json.load(f)

    # data |= summary
    for date, times in summary.items():
        if date not in data:
            data[date] = {}
        if isinstance(data[date], dict):
            last_values = [0, 0, 0]


            # this is to correct the values that are erroneously zeroed out in the API return value
            # this does lead to a better but not exact value
            sorted_times = dict(sorted(times.items()))
            for time in sorted_times:
                corrected_values = sorted_times[time]
                if corrected_values[0] == 0:
                    corrected_values[0] = last_values[0]
                if corrected_values[1] == 0:
                    corrected_values[1] = last_values[1]
                if corrected_values[2] == 0:
                    corrected_values[2] = last_values[2]
                last_values = corrected_values
                sorted_times[time] = sum(last_values) / 2

            data[date].update(sorted_times)
        else:
            print(f"Warning: existing entry at {date} is not a dict, skipping.")

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)



