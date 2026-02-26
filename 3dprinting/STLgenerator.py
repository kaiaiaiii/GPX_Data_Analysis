import numpy as np
import pyvista

def Meshing(lon, lat, ele): ## TODO: Muss noch funktionieren
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()
    ele_flat = np.array(ele)
    arraydata = np.column_stack((lat_flat, lon_flat, ele_flat))
    pointcloud = pyvista.PolyData(arraydata)
    mesh = pointcloud.reconstruct_surface()
    mesh.save("exports/mesh.stl")
