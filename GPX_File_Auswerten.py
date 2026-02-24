import re
import matplotlib.pyplot as plt
import tkinter as tk
import math
#import rasterio
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from mpl_toolkits.basemap import Basemap
from tkinter.filedialog import askopenfilename
from datetime import datetime
from requests import get
from pandas import json_normalize
tk.Tk().withdraw()

#fn = askopenfilename()
'''
<?xml version='1.0' encoding='UTF-8'?>
<gpx version="1.1" creator="https://www.komoot.de" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>Sonntagsausfahrt</name>
    <author>
      <link href="https://www.komoot.de">
        <text>komoot</text>
        <type>text/html</type>
      </link>
    </author>
  </metadata>
  <trk>
    <name>Sonntagsausfahrt</name>
    <trkseg>
      <trkpt lat="50.585320" lon="18.018161">
        <ele>336.461315</ele>
        <time>2025-06-15T06:27:21.112Z</time>
      </trkpt>
      <trkpt lat="50.585558" lon="18.018229">
        <ele>336.461315</ele>
        <time>2025-06-15T06:29:36.120Z</time>
      </trkpt>
'''

##Ziele:
    ## Histogram geschwindigkeit -> done
    ## Heatmap geschwindigkeit -> done
    ## Steigungen -> done
    ## trittfrequenz bei gegebener Uebersetzung -> Tacho wird gebraucht
    ## Errechnete Leistung 
    ## 3D-Druckbar?

### Variablen Definitionen ###
filename = "/nishome/kai/Documents/repos/privat/DataScience/GPX_Auswertungen/2025-10-10_2626219759_Tag 2 - Entscheidungsschwierigkeiten.gpx"  #askopenfilename()
latitude, longitude, elevation, time, velocity = [], [], [], [], []
Leistung_Rollwiderstand, Leistung_Luftwiderstand, Leistung_Steigung = [],[],[]
velocity = []

### Pattern Matching
pattern_longitude = r'lon="(\d+\.?\d*)'
pattern_latitude = r'lat="(\d+\.?\d*)'
pattern_elevation = r'<ele>(\d+\.?\d*)'
pattern_time = r'<time>(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})'

with open(filename, 'r') as file:
    for line in file:
        ### Match patterns 
        match_lon = re.findall(pattern_longitude, line)
        match_lat = re.findall(pattern_latitude, line)
        match_ele = re.findall(pattern_elevation, line)
        match_time = re.findall(pattern_time, line)
        ### extend to values
        longitude.extend(match_lon)
        latitude.extend(match_lat)
        elevation.extend(match_ele)
        time.extend(match_time)


ele = list(map(float, elevation))
lat = list(map(float, latitude))
long = list(map(float, longitude))

time_seconds = np.array([
    datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    for t in time
])

### Funktionen ###
def plotDataPoints(x, y, color, Name, xlabel, ylabel):
    plt.figure(figsize=(8, 5))
    plt.plot(np.asarray(x, float), y, color=color, label=Name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(Name)
    plt.legend()
    plt.show()

def Leistung_Geschaetzt(Gewicht, Geschwindigkeit, Hoehe1, Hoehe2):
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

####################
### AUSWERTUNGEN ###
####################

delta_t = np.diff(time_seconds)
Distance = distance(lat, long, ele)
velocities = 3.6*(Distance / np.diff(time_seconds))
#Leistungen = Leistung_Geschaetzt(100, elevation)
median_velo = np.median(velocities)
average_velo = np.average(velocities)

print(lat)
print(long)
print(median_velo)
print(average_velo)
###############
### plotten ###
###############

plotDataPoints(time_seconds, ele, "red", "Elevation", "Zeit", "Elevation")
plotDataPoints(time_seconds[:-1], np.diff(ele), "green", "slope", "Zeit", "Test") #TODO: Distance missing, right now only height change

plt.figure(figsize=(8, 5)) # TODO: Automatic width and height
plt.scatter(long, lat, c = ele, cmap = 'viridis' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Track")
plt.legend()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(velocities, 500)
plt.xlabel("Velocity")
plt.ylabel("frequency")
plt.title("velocity over time")
plt.xlim([0, 60])
plt.legend()
plt.show()

''' Abhaengig von umgebung
ax = plt.axes(projection=cimgt.OSM().crs)
ax.set_extent([np.min(long), np.max(long), np.min(lat), np.max(lat)])
ax.add_image(cimgt.OSM(), 3)
plt.scatter(long, lat, transform=ccrs.PlateCarree())
'''

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='f', lat_0=np.average(lat), lon_0=np.average(long), width= 1E5, height=1.2E5) # TODO: Better resolution, automatic with and height
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')
m.scatter(long, lat, latlon=True, c=ele, s=velocities, cmap='viridis', alpha=0.5)
plt.colorbar(label=r'$Velocity$')
plt.clim(3, 7)

##################
### 3D-PRINTING###
##################
# min, max of lat, long -> done
# define coordinates around the trail -> rastering in a rectangle, more shapes would be interesting. Also beeing able to use points according to some landmarks like sea etc
# api request to get elevation -> save in vector
# points to stl 
# 3D-print the points
'''
def shape(lat, long, size):
    lat_max = np.max(lat) + size
    lat_min = np.min(lat) - size
    lon_max = np.max(long) + size
    lon_min = np.min(long) - size
  return lat_max, lat_min, lon_max, lon_min

'''

#own implementation, looking for libraries later#


def coordinates(lat, lon):
  lat_max = np.max(lat)
  lat_min = np.min(lat)
  lon_max = np.max(lon)
  lon_min = np.min(lon) 

  longitudenvektor, latitudenvektor = [], []  
  for i in range(len(lat_min), len(lat_max), 0.00001):
    latitude = i
    latitudenvektor.append(latitude)

  for j in range(len(lon_min), len(lon_max), 0.00001):
    longitude = j
    longitudenvektor.append(longitude)
  return latitudenvektor, longitudenvektor

          
def getElevationfromAPI(lat, long): ## open elevation, need to look for other apis maybe
  query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
  r = get(query, timeout = 20)
  if r.status_code == 200 or r.status_code == 201:
        elevation = json_normalize(r.json(), 'results')['elevation'].values[0]
  return elevation

def ElevationData(lat, long):
   latitudenvektor, longitudenvektor = coordinates(lat, long)
   ElevationData = []
   for latitude in latitudenvektor:
      for longitude in longitudenvektor:
        Elevation = getElevationfromAPI(latitude, longitude)
        ElevationData.append(Elevation)      

'''

def get_elevation(lat,lon):
    coords = ((lat,lon),(lat,lon))
    with rasterio.test
def STL_File(lat, lon, ele):
    num_triangles = len(lat)*len(lat)
    data = np.zeroes(num_triangles, dtype=mesh.Mesh.dtype)
'''