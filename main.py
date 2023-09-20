import requests
import pandas as pd

API_KEY = "AIzaSyCirvfY5a3RQOdTnRTMHJZZE5f3TgOiEig"
ADDRESS = "1c/149 McCredie Rd, Smithfield NSW 2164"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def get_lat_lng(address):
    response = requests.get(BASE_URL, params={"address": address, "key": API_KEY})
    if response.status_code == 200:
        json = response.json()
        location = json['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

def get_postcodes_in_radius(lat, lng, radius):
    postcodes = set()
    for i in range(0, radius, 5):
        location_str = f"{lat},{lng + i / 100.0}"
        response = requests.get(BASE_URL, params={"latlng": location_str, "key": API_KEY})
        if response.status_code == 200:
            json = response.json()
            for result in json['results']:
                for component in result['address_components']:
                    if 'postal_code' in component['types']:
                        postcodes.add(component['short_name'])
    return postcodes

lat, lng = get_lat_lng(ADDRESS)

ranges = {
    "Metro": (0, 30),
    "O1": (30, 50),
    "O2": (50, 80),
    "O3": (80, 150)
}

all_postcodes = set()
results = {}

for range_name, (start, end) in ranges.items():
    postcodes = get_postcodes_in_radius(lat, lng, end) - all_postcodes
    all_postcodes.update(postcodes)
    results[range_name] = ', '.join(postcodes)

# Saving to Excel using pandas
df = pd.DataFrame(list(results.items()), columns=["Range", "Postcodes"])
df.to_excel("postcodes.xlsx", index=False, engine='openpyxl')
