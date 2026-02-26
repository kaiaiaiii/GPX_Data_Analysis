import re
import matplotlib.pyplot as plt
import tkinter as tk
import math
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
import pyvista 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from tkinter.filedialog import askopenfilename
from datetime import datetime
from requests import post
import pandas as pd
from pandas import json_normalize


## TODO:
## Namingconvention, Iteration x,y gleichgross, bei Geschwindigkeit = 0 Daten loeschen
##Ziele:
    ## Histogram geschwindigkeit -> done
    ## Heatmap geschwindigkeit -> done
    ## Steigungen -> done
    ## trittfrequenz bei gegebener Uebersetzung -> Tacho wird gebraucht
    ## Errechnete Leistung 

### Variable definition ###
filename = "./gpxfiles/Beten.gpx" #askopenfilename() ## mal relativer pfadname
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

### Function definition ###
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
#Leistungen = Leistung_Geschaetzt(100, elevation)  ->> TODO
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

##################
### 3D-PRINTING###
##################
# define coordinates around the trail -> rastering in a rectangle, more shapes would be interesting. Also beeing able to use points according to some landmarks like sea etc
# points to stl -> TODO
# 3D-print the points -> TODO
#own implementation, looking for libraries later

def Meshing(lon, lat, ele): ## TODO: Muss noch funktionieren
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()
    ele_flat = np.array(ele)
    arraydata = np.column_stack((lat_flat, lon_flat, ele_flat))
    pointcloud = pyvista.PolyData(arraydata)
    mesh = pointcloud.reconstruct_surface()
    mesh.save("exports/mesh.stl")


###############
### plotten ###
###############
'''
plot_Data_Points(time_seconds[:-1], velocities, "red", "exports/velocity", "time", "velocity")
plot_Data_Points(time_seconds, ele, "red", "exports/Elevation", "time", "Elevation")
plot_Data_Points(time_seconds[:-1], np.diff(ele), "green", "exports/slope", "time", "Test") #TODO: Distance missing, right now only height change

###################################################
### plot map with track and elevation colorcode ###
###################################################

plt.figure(constrained_layout=True)
ax = plt.scatter(long, lat, c = ele, cmap = 'hot' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Track")
plt.colorbar(ax, label=r'$Elevation$')
plt.savefig("exports/Track")
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
plt.xlim([5, maximum_velo])#plt.legend()
plt.savefig("exports/Histogram")
plt.show()
plt.close()

#########################
### plot track in map ###
#########################
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
sc = ax.scatter(long, lat, c=velocities,  cmap='viridis', alpha=0.5, transform=ccrs.PlateCarree())
sc.set_clim(5, maximum_velo)
cbar = plt.colorbar(sc, label=r'$Velocity$')
plt.savefig("exports/Velocity")
plt.show()
plt.close()
'''
##############################################################
### plot track in map colorcode for elevation and velocity ###
##############################################################

Data_to_plot = get_elevation_from_Api_post(lat, long) 
lon_grid, lat_grid = np.meshgrid(Data_to_plot[0], Data_to_plot[1])
Meshing(lon_grid, lat_grid, Data_to_plot[2])

plt.figure(figsize=(8, 5)) # TODO: Automatic width and height
plt.scatter(lon_grid, lat_grid, c = Data_to_plot[2] , cmap = 'rainbow' )
ax = plt.scatter(long, lat, c = velocities, cmap = 'hot' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Height Profile")
cbar = plt.colorbar(ax, label=r'$Velocity$')
plt.savefig("exports/Height Profile")
plt.show()
plt.close()


