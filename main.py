from results.plotGPXdata import plot_Data_Points
from analysis.analysis import read_from_file, data_cleansing, data_calculations
from analysis.APIrequest import get_elevation_from_Api_post
from analysis.cadence import cadence_from_data
from STLgenerator.STLgenerator import Meshing
from tkinter.filedialog import askopenfilename
import numpy as np
import math


gpxfilename = "./inputdata/FileName.gpx" #askopenfilename()
cadencefilename = "./inputdata/CadenceData.txt" #askopenfilename()

#########################
### GPX File Analysis ###
#########################

long, lat, ele, time = read_from_file(gpxfilename)
longitude, latitude, elevation_along_path, time_seconds = data_cleansing(long, lat, ele, time)
velocities, median_velo, average_velo, maximum_velo, maximum_ele = data_calculations(longitude, latitude, elevation_along_path, time_seconds)
longitude_vector, latitude_vector, elevation_map = get_elevation_from_Api_post(longitude, latitude)
lon_grid, lat_grid = np.meshgrid(longitude_vector, latitude_vector)


###############################
### Bike Parameter Analysis ###
###############################

cadence_from_data(cadencefilename)

###################
### 3D-Printing ###
###################

Meshing(lon_grid, lat_grid, elevation_map)

################
### Plotting ###
################


plot_Data_Points(time_seconds[:-1], velocities, "red", "exports/velocity", "time", "velocity")
plot_Data_Points(time_seconds, elevation_map, "red", "export/Elevation", "time", "Elevation")
plot_Data_Points(time_seconds[:-1], np.diff(elevation_along_path), "green", "export/slope", "time", "Test")

plt.figure(constrained_layout=True)
ax = plt.scatter(long, lat, c = ele, s = 0.2, cmap = 'plasma' )
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Track")
plt.colorbar(ax, label=r'$Elevation$')
plt.savefig("export/Track")
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
plt.xlim([5, 2*average_velo])#plt.legend()
plt.savefig("export/Histogram")
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
sc = ax.scatter(long, lat, c=velocities,  cmap='plasma', s=0.2, transform=ccrs.PlateCarree(), vmax= 2*average_velo, vmin=5)
cbar = plt.colorbar(sc, label=r'$Velocity$')
plt.savefig("export/Velocity")
plt.show()
plt.close()

##############################################################
### plot track in map colorcode for elevation and velocity ###
##############################################################

Data_to_plot = get_elevation_from_Api_post(lat, long) 
lon_grid, lat_grid = np.meshgrid(Data_to_plot[0], Data_to_plot[1])
Meshing(lon_grid, lat_grid, Data_to_plot[2])

plt.figure(figsize=(8, 5)) # TODO: Automatic width and height
plt.scatter(lon_grid, lat_grid, c = Data_to_plot[2] , cmap = 'rainbow' )
ax = plt.scatter(long, lat, c = velocities, s = 0.1, cmap = 'plasma' , vmax= 2*average_velo, vmin=5)
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Height Profile")
cbar = plt.colorbar(ax, label=r'$Velocity$')
plt.savefig("export/Height Profile")
plt.show()
plt.close()

##############################################################
### plot track in elevation profile colorcode for velocity ###
##############################################################
# Data_to_plot = get_elevation_from_Api_post(lat, long) 
# lon_grid, lat_grid = np.meshgrid(Data_to_plot[0], Data_to_plot[1])
# Meshing(lat_grid, lon_grid, Data_to_plot[2])
# data_to_stl(lat_grid, lon_grid, Data_to_plot[2])

plt.figure(figsize=(8, 5)) # TODO: Automatic width and height
ax = plt.scatter(time_seconds[:-1], ele[:-1], c = velocities, s = 0.2, cmap = 'plasma' , vmax= 3*median_velo, vmin=0)
plt.xlabel("time")
plt.ylabel("elevation")
plt.title("Height Profile")
plt.savefig("export/Height_Velo")
cbar = plt.colorbar(ax, label=r'$Velocity$')
plt.show()
plt.close()