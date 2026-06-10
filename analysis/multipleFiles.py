import os
import fnmatch
from results.plotGPXdata import plot_Data_Points
from analysis.analysis import read_from_file, data_cleansing, data_calculations
from APIrequest import get_elevation_from_Api_post
from tkinter import filedialog

def get_file_list(folderpath):
    file_list = []
    for filenames in os.walk(folderpath):
        for filename in filenames:
            file_list.append({filename})
    return file_list

def get_data_from_all_files(file_list):
    for file in file_list:
        long, lat, ele, time = read_from_file(file)
        longitude, latitude, elevation_along_path, time_seconds = data_cleansing(long, lat, ele, time)
        velocities, median_velo, average_velo, maximum_velo, maximum_ele = data_calculations(longitude, latitude, elevation_along_path, time_seconds)
        longitude_vector, latitude_vector, elevation_map = get_elevation_from_Api_post(longitude, latitude)
        lon_grid, lat_grid = np.meshgrid(longitude_vector, latitude_vector)


def multiple_file_analysis():
    folder_path = filedialog.askdirectory()
    number_of_files = fnmatch.filter(os.listdir(folder_path), '*.gpx') 
    for i in range(number_of_files):
         