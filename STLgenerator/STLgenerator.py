import numpy as np
import pyvista
from stl import mesh

def Meshing(lon, lat, ele):
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()
    ele_flat = (np.array(ele).flatten())*0.0005
    arraydata = np.column_stack((lat_flat, lon_flat, ele_flat))
    pointcloud = pyvista.PolyData(arraydata)
    pointcloud.plot(style = "points", point_size = 10.0) ## 
    mesh = pointcloud.reconstruct_surface().triangulate()
    mesh.save("exports/mesh.stl")


'''
def data_to_stl(lon, lat, ele, filename="export/terrain.stl", z_scale=10.005): #, base_height, model_size_mm):
    lon_flat = lon.flatten()
    lat_flat = lat.flatten()
    ele_flat = np.array(ele).flatten()* z_scale
    rows, cols = ele.shape
    n_faces = (rows - 1) * (cols - 1) * 2
    terrain_mesh = mesh.Mesh(np.zeros(n_faces, dtype=mesh.Mesh.dtype))
    face = 0
    for i in range(rows - 1):
        for j in range(cols - 1):
            p1 = [lon[i,j],   lat[i,j],   ele[i,j]]
            p2 = [lon[i+1,j], lat[i+1,j], ele[i+1,j]]
            p3 = [lon[i,j+1], lat[i,j+1], ele[i,j+1]]
            p4 = [lon[i+1,j+1], lat[i+1,j+1], ele[i+1,j+1]]
            terrain_mesh.vectors[face] = np.array([p1, p2, p3])
            face += 1
            terrain_mesh.vectors[face] = np.array([p2, p4, p3])
            face += 1

    terrain_mesh.save(filename)
    print("Triangles:", n_faces)

'''
'''
def ShowStlFile(filename):
    mesh = o3d.io.read_triangle_mesh(filename)
    mesh = mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], window_name="STL", left=1000, top=200, width=800, height=650)


ShowStlFile("../exports/mesh.stl")
'''