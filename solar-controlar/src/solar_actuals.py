import json
import os
from datetime import datetime, time

from solarcontrolar.givenergy import GivEnergy


def get_givenergy():
    api_key = os.getenv("GIVENERGY_API_KEY")
    inverter_id = os.getenv("GIVENERGY_INVERTER_ID")
    return GivEnergy(api_key, inverter_id)


end_date = datetime.combine(datetime.today(), time.min).date()
print(f'{end_date.isoformat()}')
givenergy = get_givenergy()
generation_actuals = givenergy.get_generation_actuals(end_date, 7)

with open("solar_actuals.json", "w") as f:
    json.dump(generation_actuals, f, indent=2)


