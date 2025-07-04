import os
from datetime import datetime, time, timedelta

from common.json_store import JsonStore
from filenames import Filenames
from solarcontrolar.givenergy import GivEnergy


def get_givenergy():
    api_key = os.getenv("GIVENERGY_API_KEY")
    inverter_id = os.getenv("GIVENERGY_INVERTER_ID")
    return GivEnergy(api_key, inverter_id)


if __name__ == "__main__":
    end_date = datetime.combine(datetime.today(), time.min).date()
    print(f'{end_date.isoformat()}')
    givenergy = get_givenergy()
    generation_actuals = givenergy.get_generation_actuals_hh(end_date, 7)

    solar_actuals_store = JsonStore(Filenames.SOLAR_ACTUALS.value)
    existing = solar_actuals_store.read()
    solar_actuals_store.write({**existing, **generation_actuals})
