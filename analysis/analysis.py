import re
import math
from datetime import datetime
import numpy as np
from requests import post


latitude, longitude, elevation, time, velocity = [], [], [], [], []
ressistance_rolling, ressistance_air, power_elevation = [],[],[]


def read_from_file(filename):
    pattern_longitude = r'lon="(\d+\.?\d*)'
    pattern_latitude = r'lat="(\d+\.?\d*)'
    pattern_elevation = r'<ele>(\d+\.?\d*)'
    pattern_time = r'<time>(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})'

    with open(filename, 'r') as file:
        for line in file:
            longitude.extend(re.findall(pattern_longitude, line))
            latitude.extend(re.findall(pattern_latitude, line))
            elevation.extend(re.findall(pattern_elevation, line))
            time.extend(re.findall(pattern_time, line))
    return longitude, latitude, elevation, time

def estimated_Performance(mass, velocity, elevation1, elevation2):
    my_r =0.00404 ## more or less educated guess
    rho = 1.2
    cwA = 0.28 
    P_roll = mass*9,81*velocity*my_r
    ressistance_rolling.append(P_roll)
    P_air = 0.5*rho*cwA*velocity*velocity
    ressistance_air.append(P_air)
    k = elevation2-elevation1
    P_slope = (k*velocity)/(math.sqrt(1+k*k))
    power_elevation.append(P_slope)
    Power = ressistance_rolling + ressistance_air + power_elevation
    return Power  

def distance_between_coordinates(longitude, latitude, elevation):
    R = 6378137

    longitude = np.radians(longitude)
    latitude = np.radians(latitude)

    dlongitude = np.diff(longitude)
    dlatitude = np.diff(latitude)
    delevation = np.diff(elevation)

    a = np.sin(dlatitude/2)**2 + np.cos(latitude[:-1]) * np.cos(latitude[1:]) * np.sin(dlongitude/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    d = R * c
    return np.sqrt(d*d + delevation*delevation)

def get_elevation_from_Api_post(longitude, latitude):
    print("Elevationdata")

    lat_max = np.max(latitude)
    lat_min = np.min(latitude)
    lon_max = np.max(longitude)
    lon_min = np.min(longitude) 
    longitude_vector = np.linspace(lon_min, lon_max, 150)
    latitude_vector = np.linspace(lat_min, lat_max, 150)

    elevation_data = []
    lats_and_lons = []

    for latitude in latitude_vector:
        for longitude in longitude_vector:
            lats_and_lons.append((latitude, longitude))

    lats_and_lons_list = lats_and_lons
    for idx, lat_lon in enumerate(lats_and_lons):
        lats_and_lons_list[idx] ={
            "latitude": lat_lon[0],
            "longitude": lat_lon[1]
        }

    payload = {
    "locations":
    lats_and_lons_list
    }

    headers = {'Accept': 'application/json','Content-Type': 'application/json'}
    query = f"https://api.open-elevation.com/api/v1/lookup"
    response = post(url=query, json=payload, headers=headers)


    result = response.json()

    print(f"Full response: {response}")


    for entry in result['results']:
        elevation_data.append(entry['elevation'])

    return longitude_vector, latitude_vector, elevation_data

def data_cleansing(longitude, latitude, elevation, time):
    ele = list(map(float, elevation))
    lat = list(map(float, latitude))
    long = list(map(float, longitude))

    time_seconds = np.array([
        datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
        for t in time
    ])
    return long, lat, ele, time_seconds

def data_calculations(longitude, latitude, elevation, time_seconds):
    delta_t = np.diff(time_seconds)
    Distance = distance_between_coordinates(longitude, latitude, elevation)
    velocities = 3.6*(Distance / np.diff(time_seconds))
    #Power = estimated_Performance(100, elevation)  ->> TODO
    median_velo = np.median(velocities)
    average_velo = np.average(velocities)
    maximum_velo = np.max(velocities)
    maximum_ele = np.max(elevation)
    print("maximum elevation: ")
    print(maximum_ele)
    print("maximum speed: ")
    print(maximum_velo)
    print("average speed: ")
    print(average_velo)
    print("median speed: ")
    print(median_velo)
    return velocities, median_velo, average_velo, maximum_velo, maximum_ele

def data_analysis(filename):
    longitude, latitude, elevation_along_path, time_seconds = data_cleansing(read_from_file(filename))
    velocities, median_velo, average_velo, maximum_velo, maximum_ele = data_calculations(longitude, latitude, elevation, time_seconds)
    longitude_vector, latitude_vector, elevation_map = get_elevation_from_Api_post(longitude, latitude)
    return longitude_vector, latitude_vector, elevation_along_path, elevation_map, time_seconds