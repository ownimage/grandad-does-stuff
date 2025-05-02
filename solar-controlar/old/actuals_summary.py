import json
from datetime import datetime
from collections import defaultdict

def load_actuals(file_path):
    """Load JSON data from the given file."""
    with open(file_path, "r") as file:
        return json.load(file)

def summarize_daily(actuals_data):
    """Summarize pv_estimate values by date."""
    daily_summary = defaultdict(float)

    for entry in actuals_data["estimated_actuals"]:
        date = datetime.fromisoformat(entry["period_end"].split(".")[0]).date()
        daily_summary[date] += entry["pv_estimate"]  # Sum up estimates per day

    return daily_summary


def save_summary(summary, output_file):
    """Save the daily summary as a JSON file with string keys."""
    formatted_summary = {str(date): pv_estimate for date, pv_estimate in summary.items()}  # Convert keys to strings

    with open(output_file, "w") as file:
        json.dump(formatted_summary, file, indent=4)

if __name__ == "__main__":
    file_path = "actuals.json"  # Replace with your actual file path
    output_file = "actuals_summary.json"

    actuals_data = load_actuals(file_path)
    daily_summary = summarize_daily(actuals_data)
    save_summary(daily_summary, output_file)

    print(f"Daily summary saved to {output_file}")
