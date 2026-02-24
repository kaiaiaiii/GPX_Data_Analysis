import numpy as np
### sketch
'''
calculate medium coordinate
calculate max in all directions from medium
get shape around it
draw map with shape around it
get height of shape map around it
do surface mesh out of the elevation data -> Blender
add coordinates of the points (scatter plot)

'''

ele = list(map(float, elevation))
lat = list(map(float, latitude))
long = list(map(float, longitude))


def medium_coordinate(latitude_coordinates, longitude_coordinates):
    medium_lat = np.average(latitude_coordinates)
    medium_long = np.average(longitude_coordinates)
    return medium_lat, medium_long

def extreme_coordinates(latitude_coordinates, longitude_coordinates):
    maximum_lat = np.max(latitude_coordinates)
    maximum_long = np.max(longitude_coordinates)
    minimum_lat = np.min(latitude_coordinates)
    minimum_long = np.min(longitude_coordinates)
    return maximum_lat, maximum_long, minimum_lat, minimum_long


def shape(avg_lat, avg_long):

#

    