import requests
import pandas as pd
import math

API_KEY = "AIzaSyCirvfY5a3RQOdTnRTMHJZZE5f3TgOiEig"
ADDRESS = "1c/149 McCredie Rd, Smithfield NSW 2164"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
R_EARTH = 6371.0  # Earth radius in kilometers

def get_lat_lng(address):
    response = requests.get(BASE_URL, params={"address": address, "key": API_KEY})
    if response.status_code == 200:
        json = response.json()
        location = json['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

def get_postcode_for_lat_lng(lat, lng):
    response = requests.get(BASE_URL, params={"latlng": f"{lat},{lng}", "key": API_KEY})
    if response.status_code == 200:
        json = response.json()
        for result in json['results']:
            for component in result['address_components']:
                if 'postal_code' in component['types']:
                    return component['short_name']
    return None

def haversine_distance(lat1, lng1, lat2, lng2):
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_EARTH * c

# Reduce the step size for greater precision
step = 0.04  # Reduced from 0.1

def get_postcodes_in_radius(center_lat, center_lng, radius):
    postcodes = set()
    extended_radius = radius + 10  # Extend the search radius
    lat_range = extended_radius / 111.32  # Approximate conversion from km to degrees of latitude
    lng_range = extended_radius / (40075 * math.cos(math.radians(center_lat)) / 360)  # Approx conversion for longitude

    for lat in frange(center_lat - lat_range, center_lat + lat_range, step):
        for lng in frange(center_lng - lng_range, center_lng + lng_range, step):
            if haversine_distance(center_lat, center_lng, lat, lng) <= radius:
                postcode = get_postcode_for_lat_lng(lat, lng)
                if postcode:
                    postcodes.add(postcode)
    return postcodes

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

lat, lng = get_lat_lng(ADDRESS)

ranges = {
    "Metro": 30,
    "O1": 50,
    "O2": 80,
    "O3": 150
}

all_postcodes = set()
results = {}

for range_name, radius in ranges.items():
    postcodes = get_postcodes_in_radius(lat, lng, radius) - all_postcodes
    all_postcodes.update(postcodes)
    results[range_name] = ', '.join(postcodes)

    # Print the results as they are obtained
    print(f"{range_name}: {results[range_name]}")

df = pd.DataFrame(list(results.items()), columns=["Range", "Postcodes"])
df.to_excel("postcodes.xlsx", index=False, engine='openpyxl')
