from results.plotGPXdata import plot_Data_Points
from analysis.analysis import data_analysis
from analysis.cadence import cadence_from_data
from STLgenerator.STLgenerator import Meshing
from tkinter.filedialog import askopenfilename
import numpy as np
import math


gpxfilename = "./FileName.gpx" #askopenfilename()
cadencefilename = "./inputdata/CadenceData.txt" #askopenfilename()
longitude_vector, latitude_vector, elevation_path, elevation_map, time_seconds = data_analysis(gpxfilename)

#plot_Data_Points(time_seconds[:-1], velocities, "red", "exports/velocity", "time", "velocity")
#plot_Data_Points(time_seconds, elevation_map, "red", "export/Elevation", "time", "Elevation")
plot_Data_Points(time_seconds[:-1], np.diff(elevation_path), "green", "export/slope", "time", "Test")