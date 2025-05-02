import os
import requests

# Define the API endpoint
url = "https://api.solcast.com.au/rooftop_sites/7efd-fd73-fba3-cc46/forecasts?format=json"

# Your bearer token
token = os.getenv("SOLCAST_API_KEY")

# Set up headers with authorization
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("Hello, World!")

# Make the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())  # Parse JSON response
else:
    print("Error:", response.status_code, response.text)

