from results import plotGPXdata.py
from STLgenerator import STLgenerator.py
from tkinter.filedialog import askopenfilename
import numpy as np
import math

filename = "./gpxfiles/Beten.gpx" #askopenfilename() ## mal relativer pfadname
latitude, longitude, elevation, time, velocity = [], [], [], [], []
ressistance_rolling, ressistance_air, power_elevation = [],[],[]


### Patterns to match 
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

### Function definition ###
def estimated_Performance(Gewicht, Geschwindigkeit, Hoehe1, Hoehe2):
    my_r =0.00404 ## Leifiphysik schaetzung
    rho = 1.2
    cwA = 0.28 
    P_roll = Gewicht*9,81*Geschwindigkeit*my_r
    ressistance_rolling.append(P_roll)
    P_air = 0.5*rho*cwA*Geschwindigkeit*Geschwindigkeit
    ressistance_air.append(P_air)
    k = Hoehe2-Hoehe1
    P_slope = (k*Geschwindigkeit)/(math.sqrt(1+k*k))
    power_elevation.append(P_slope)
    Power = ressistance_rolling + ressistance_air + power_elevation
    return Power  

def distance(lat, lon, ele):
    R = 6378137

    lat = np.radians(lat)
    lon = np.radians(lon)

    dlat = np.diff(lat)
    dlon = np.diff(lon)
    dele = np.diff(ele)

    a = np.sin(dlat/2)**2 + np.cos(lat[:-1]) * np.cos(lat[1:]) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    d = R * c
    return np.sqrt(d*d + dele*dele)

def get_elevation_from_Api_post(lat, lon):
    print("Elevationdata")

    lat_max = np.max(lat)
    lat_min = np.min(lat)
    lon_max = np.max(lon)
    lon_min = np.min(lon) 
    longitudenvektor = np.linspace(lon_min, lon_max, 150)
    latitudenvektor = np.linspace(lat_min, lat_max, 150)

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

    return longitudenvektor, latitudenvektor, elevation_data

################
### ANALYSIS ###
################

ele = list(map(float, elevation))
lat = list(map(float, latitude))
long = list(map(float, longitude))

time_seconds = np.array([
    datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    for t in time
])

delta_t = np.diff(time_seconds)
Distance = distance(lat, long, ele)
velocities = 3.6*(Distance / np.diff(time_seconds))
#Power = estimated_Performance(100, elevation)  ->> TODO
median_velo = np.median(velocities)
average_velo = np.average(velocities)
maximum_velo = np.max(velocities)
maximum_ele = np.max(ele)

print("maximum elevation: ")
print(maximum_ele)
print("maximum speed: ")
print(maximum_velo)
print("average speed: ")
print(average_velo)
print("median speed: ")
print(median_velo)