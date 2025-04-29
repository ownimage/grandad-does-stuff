import os
import json

from solcast import SolCast  # Import the SolCast class
from givenergy import GivEnergy

solcast = SolCast(os.getenv("SOLCAST_API_KEY"), os.getenv("SOLCAST_SITE_ID"))
formatted_json = json.dumps(solcast.forecast(), indent=4, sort_keys=True)
print(formatted_json)

