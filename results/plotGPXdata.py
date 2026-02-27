import matplotlib.pyplot as plt
import numpy as np

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


 #TODO: Distance missing, right now only height change

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
