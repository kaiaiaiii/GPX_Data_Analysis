import numpy as np
import pyvista
import open3d as o3d
from stl import mesh

def Meshing(lon, lat, ele): ## TODO: Muss noch funktionieren
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()
    ele_flat = np.array(ele).flatten()
    arraydata = np.column_stack((lat_flat, lon_flat, ele_flat))
    pointcloud = pyvista.PolyData(arraydata)
    mesh = pointcloud.reconstruct_surface().triangulate()
    mesh.save("exports/mesh.stl")

'''
def ShowStlFile(filename):
    mesh = o3d.io.read_triangle_mesh(filename)
    mesh = mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], window_name="STL", left=1000, top=200, width=800, height=650)


ShowStlFile("../exports/mesh.stl")
'''