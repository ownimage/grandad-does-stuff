import os

from solarcontrolar.givenergy import GivEnergy

# solcast = SolCast(os.getenv("SOLCAST_API_KEY"), os.getenv("SOLCAST_SITE_ID"))
# formatted_json = json.dumps(solcast.forecast(), indent=4, sort_keys=True)
# print(formatted_json)

api_key = os.getenv("GIVENERGY_API_KEY")
inverter_id = "FD2325G412"
givenergy = GivEnergy(api_key, inverter_id)
# setting_write = givenergy.setting_write(41, "00:00")
value = givenergy.battery_level()
print(value)
# formatted_json = json.dumps(setting_read, indent=4, sort_keys=True)
# print(json.dumps(formatted_json, indent=4, sort_keys=True))

