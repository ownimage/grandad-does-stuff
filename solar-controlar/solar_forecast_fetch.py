import os
import json

from solarcontrolar.solcast import SolCast  # Import the SolCast class

solcast = SolCast(os.getenv("SOLCAST_API_KEY"), os.getenv("SOLCAST_SITE_ID"))
formatted_json = json.dumps(solcast.forecast(), indent=4, sort_keys=True)
print(formatted_json)

