import re
import matplotlib.pyplot as plt
import tkinter as tk
import math
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from tkinter.filedialog import askopenfilename
from datetime import datetime
from requests import get
import pandas as pd
from pandas import json_normalize
tk.Tk().withdraw() ##??

## TODO:
## Namingconvention, Iteration x,y gleichgross
##Ziele:
    ## Histogram geschwindigkeit -> done
    ## Heatmap geschwindigkeit -> done
    ## Steigungen -> done
    ## trittfrequenz bei gegebener Uebersetzung -> Tacho wird gebraucht
    ## Errechnete Leistung 

### Variable definition ###
filename = "./FileName.gpx" #askopenfilename() ## mal relativer pfadname
latitude, longitude, elevation, time, velocity = [], [], [], [], []
Leistung_Rollwiderstand, Leistung_Luftwiderstand, Leistung_Steigung = [],[],[]
velocity = []

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

### Funktionen ###
def plot_Data_Points(x, y, color, Name, xlabel, ylabel):
    plt.figure(figsize=(8, 5))
    plt.plot(np.asarray(x, float), y, color=color, label=Name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(Name)
    plt.legend()
    plt.savefig(Name + xlabel + ylabel)
    plt.show()
    plt.close()

def estimated_Performance(Gewicht, Geschwindigkeit, Hoehe1, Hoehe2):
    my_r =0.00404 ## Leifiphysik schaetzung
    rho = 1.2
    cwA = 0.28 
    P_Rolle = Gewicht*9,81*Geschwindigkeit*my_r
    Leistung_Rollwiderstand.append(P_Rolle)
    P_Luft = 0.5*rho*cwA*Geschwindigkeit*Geschwindigkeit
    Leistung_Luftwiderstand.append(P_Luft)
    k = Hoehe2-Hoehe1
    P_Steigung = (k*Geschwindigkeit)/(math.sqrt(1+k*k))
    Leistung_Steigung.append(P_Steigung)
    Leistung = Leistung_Luftwiderstand + Leistung_Rollwiderstand + Leistung_Steigung
    return Leistung  

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
    longitudenvektor = np.linspace(lon_min, lon_max, 10)
    latitudenvektor = np.linspace(lat_min, lat_max, 10)

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

    return elevation_data

####################
### AUSWERTUNGEN ###
####################

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
#Leistungen = Leistung_Geschaetzt(100, elevation)  ->> TODO
median_velo = np.median(velocities)
average_velo = np.average(velocities)

###############
### plotten ###
###############

plot_Data_Points(time_seconds, ele, "red", "Elevation", "Zeit", "Elevation")
plot_Data_Points(time_seconds[:-1], np.diff(ele), "green", "slope", "Zeit", "Test") #TODO: Distance missing, right now only height change

###################################################
### plot map with track and elevation colorcode ###
###################################################

plt.figure(figsize=(8, 5))                  # TODO: Automatic width and height
plt.scatter(long, lat, c = ele, cmap = 'viridis' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Track")
plt.legend()
plt.savefig("Track")
plt.show()
plt.close()

###############################
### Histogram of velocities ###
###############################

plt.figure(figsize=(8, 5))
plt.hist(velocities, 500)
plt.xlabel("Velocity")
plt.ylabel("frequency")
plt.title("velocity over time")
plt.xlim([0, 60])#plt.legend()
plt.savefig("Histogram")
plt.show()
plt.close()


#########################
### plot track in map ###
#########################
### das velocities lang genug ist, aber etwas pfuschig
velocities = np.append(velocities, velocities[-1])
fig = plt.figure(figsize=(8, 8))
proj = ccrs.LambertConformal(central_latitude=np.average(lat),central_longitude=np.average(long))
ax = plt.axes(projection=proj)
extent = [np.min(long), np.max(long),np.min(lat), np.max(lat)]
ax.set_extent(extent, crs=ccrs.PlateCarree())
ax.stock_img()
ax.add_feature(cfeature.COASTLINE, edgecolor='gray')
ax.add_feature(cfeature.BORDERS, edgecolor='gray')
ax.add_feature(cfeature.STATES, edgecolor='gray')
sc = ax.scatter(long, lat, c=ele, s=ele, cmap='viridis', alpha=0.5, transform=ccrs.PlateCarree())
cbar = plt.colorbar(sc, label=r'$Velocity$')
sc.set_clim(3, 7)
plt.savefig("Velocity")
plt.show()
plt.close()

##################
### 3D-PRINTING###
##################
# min, max of lat, long -> done
# define coordinates around the trail -> rastering in a rectangle, more shapes would be interesting. Also beeing able to use points according to some landmarks like sea etc
# api request to get elevation -> save in vector done
# points to stl -> TODO
# 3D-print the points -> TODO
#own implementation, looking for libraries later#

Data_to_plot = get_elevation_from_Api_post(lat, long) ## maybe have lat, long, ele separated

plt.figure(figsize=(8, 5)) # TODO: Automatic width and height
plt.scatter(Data_to_plot[0], Data_to_plot[1], c = Data_to_plot[2] , cmap = 'viridis' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Track")
plt.legend()
plt.savefig("Track")
plt.show()
plt.close()


'''
        ### extend to values
        longitude.extend(match_lon)
        latitude.extend(match_lat)
        elevation.extend(match_ele)
        time.extend(match_time)
Abhaengig von umgebung
ax = plt.axes(projection=cimgt.OSM().crs)
ax.set_extent([np.min(long), np.max(long), np.min(lat), np.max(lat)])
ax.add_image(cimgt.OSM(), 3)
plt.scatter(long, lat, transform=ccrs.PlateCarree())

leider depreceated:
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='f', lat_0=np.average(lat), lon_0=np.average(long), width= 1E5, height=1.2E5) # TODO: Better resolution, automatic with and height
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')
m.scatter(long, lat, latlon=True, c=ele, s=velocities, cmap='viridis', alpha=0.5)
plt.colorbar(label=r'$Velocity$')
plt.clim(3, 7)
def shape(lat, long, size):
    lat_max = np.max(lat) + size
    lat_min = np.min(lat) - size
    lon_max = np.max(long) + size
    lon_min = np.min(long) - size
  return lat_max, lat_min, lon_max, lon_min



def ElevationData(lat, lon):
    print("Elevationdata")
    latitudenvektor, longitudenvektor = coordinates(lat, lon)

    elevation_data = []

    for latitude in latitudenvektor:
        for longitude in longitudenvektor:
            elevation = getElevationfromAPI(latitude, longitude)
            elevation_data.append(elevation)

    return elevation_data 

def getElevationfromAPI(lat, long): ## open elevation, need to look for other apis maybe
    query = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{long}"
    r = get(query, timeout = 20)
    if r.status_code in (200, 201):
            elevation = pd.json_normalize(
                r.json(), 'results'
            )['elevation'].values[0]
    return elevation

'''