import numpy as np
import math
import trimesh
# import networkx as nx
# from shapely.geometry import LineString
from robot import Sheath
# from Polygons import plot
# load a file by name or from a buffer
# mesh = trimesh.load_mesh('Model/BaseXSection.stl')
mesh = trimesh.load_mesh('Model/3DBenchy.stl')

a = np.random.rand(3)
b = np.random.rand(3)
c = np.random.rand(3)
mesh2 = trimesh.Trimesh(vertices=[100.*a, 100.0*b, 100.0*c],
                       faces=[[0, 1, 2]])

a = np.random.rand(3)
b = np.random.rand(3)
c = np.random.rand(3)
mesh3 = trimesh.Trimesh(vertices=[100.0*a, 100.0*b, 100.0*c],
                       faces=[[0, 1, 2]])

sh = Sheath(Radius = 2.0, Length = 100.0, SegmentsLength = 0.1, ThetaMax = 182.0)
sh.display()
# to keep the raw data intact, disable any automatic processing
#mesh = trimesh.load_mesh('../models/featuretype.STL', process=False)
# is the current mesh watertight?
mesh.is_watertight
# what's the euler number for the mesh?
mesh.euler_number
# the convex hull is another Trimesh object that is available as a property
# lets compare the volume of our mesh with the volume of its convex hull
np.divide(mesh.volume, mesh.convex_hull.volume)
# since the mesh is watertight, it means there is a
# volumetric center of mass which we can set as the origin for our mesh
mesh.vertices -= mesh.center_mass
# what's the moment of inertia for the mesh?
mesh.moment_inertia
# if there are multiple bodies in the mesh we can split the mesh by
# connected components of face adjacency
# since this example mesh is a single watertight body we get a list of one mesh
# mesh.split()
meshes = [mesh, mesh2, mesh3]
# trimesh.Scene(meshes).show()

v = [[2.0, 0.0], [2.0, 2.0], [0.0, 2.0], [-2.0, 2.0], [-2.0, 0.0], [-2.0, -2.0], [0.0, -2.0], [2.0, -2.0], [2.0, 0.0]]
v = np.array(v)
e = np.array([[0, 1], [1, 2], [6, 3], [6, 4]])
polygon = trimesh.path.polygons.edges_to_polygons(e, v)
# Polygon.plot(polygon)
for i in range (10):
    # print("here")
    mesh3 = trimesh.Trimesh(vertices=[100.0*a+float(i), 100.0*b, 100.0*c],
                       faces=[[0, 1, 2]])
    meshes = [mesh,mesh2,mesh3]
    # trimesh.Scene(meshes).show()

sh.set_cross(1)
sh.path_gen()
mesh4 = sh.mesh_gen()
# trimesh.Scene(mesh4).show()
# mesh2 = trimesh.Trimesh(vertices=[[110, 0, 0], [110, 0, 1], [110, 1, 0],[100,10,10]],
#                        faces=[[0, 1, 2],[0,1,3]])
# # preview mesh in a pyglet window from a terminal, or inline in a notebook
# mesh4.visual.face_colors = [200, 200, 250, 100]
mesh4.show()
# trimesh.Scene(meshes).show()
# coll_man = trimesh.collision.CollisionManager()
# coll_man.add_object(name = "Benchy", mesh = mesh, transform=None)
# coll_man.add_object(name = "randobj", mesh = mesh2, transform=None)
# for i in range(1000):
# 	a = np.random.rand(3)
# 	b = np.random.rand(3)
# 	c = np.random.rand(3)
# 	mesh2 = trimesh.Trimesh(vertices=[10.0*a, 10.0*a+b, 10.0*a+c],
#                        faces=[[0, 1, 2]])
# 	# print(len(mesh2.vertices))
# 	coll_man.add_object(name = "randobj", mesh = mesh2, transform=None)
# 	print(coll_man.in_collision_internal())
# 	if coll_man.in_collision_internal()==False:
# 		print(mesh2.vertices)
# 		print(mesh2.faces)
# get a single cross section of the mesh
# slice = mesh.section(plane_origin=mesh.centroid, 
                     # plane_normal=[0,0,1])

# the section will be in the original mesh frame
# slice.show()
                    
# # we can sample the volume of Box primitives
# points = mesh.bounding_box_oriented.sample_volume(count=1000)

# # find the closest point on the mesh to each random point
# (closest_points,distances,triangle_id) = mesh.nearest.on_surface(points)
# # print('Distance from point to surface of mesh:\n{}'.format(distances))



# # create a PointCloud object out of each (n,3) list of points
# cloud_original = trimesh.points.PointCloud(points)
# cloud_close    = trimesh.points.PointCloud(closest_points)

# # create a unique color for each point
# cloud_colors = np.array([trimesh.visual.random_color() for i in points])

# # set the colors on the random point and its nearest point to be the same
# cloud_original.vertices_color = cloud_colors
# cloud_close.vertices_color    = cloud_colors

# # create a scene containing the mesh and two sets of points
# scene = trimesh.Scene([mesh,
#                        cloud_original,
#                        cloud_close])

# # show the scene wusing 
# scene.show()
