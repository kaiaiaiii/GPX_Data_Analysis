import numpy as np
from requests import post

def get_elevation_from_Api_post(lat, lon):
    print("Elevationdata")
    
    max_payload_size = 100*100 # number of points per request

    lat_max = np.max(lat)
    lat_min = np.min(lat)
    lon_max = np.max(lon)
    lon_min = np.min(lon) 
    longitudenvektor = np.linspace(lon_min, lon_max, 100)
    latitudenvektor = np.linspace(lat_min, lat_max, 100)

    elevation_data = []
    lats_and_lons = []

    for latitude in latitudenvektor:
        for longitude in longitudenvektor:
            lats_and_lons.append((latitude, longitude))

    lats_and_lons_list = lats_and_lons
    for idx, lat_lon in enumerate(lats_and_lons):
        lats_and_lons_list[idx] ={
            "latitude": lat_lon[0],
            "longitude": lat_lon[1]
        }
        
    for idx in range(0, len(lats_and_lons_list), max_payload_size):
        batch = lats_and_lons_list[idx:idx + max_payload_size]

        payload = {
        "locations":
        batch
        }

        query = f"https://api.open-elevation.com/api/v1/lookup"
        response = post(url=query, json=payload)


        result = response.json()

        print(f"Full response: {response}")


        for entry in result['results']:
            elevation_data.append(entry['elevation'])

    return longitudenvektor, latitudenvektor, elevation_data
