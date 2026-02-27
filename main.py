from results.plotGPXdata.py import plot_Data_Points
from analysis.analysis.py import data_analysis
from STLgenerator/STLgenerator.py import Meshing
from tkinter.filedialog import askopenfilename
import numpy as np
import math


filename = "./gpxfiles/Beten.gpx" #askopenfilename() ## mal relativer pfadname
longitude_vector, latitude_vector, elevation_path, elevation_map, time_seconds = data_analysis(filename)

plot_Data_Points(time_seconds[:-1], velocities, "red", "exports/velocity", "time", "velocity")
plot_Data_Points(time_seconds, elevation_map, "red", "exports/Elevation", "time", "Elevation")
plot_Data_Points(time_seconds[:-1], np.diff(elevation_path), "green", "exports/slope", "time", "Test")