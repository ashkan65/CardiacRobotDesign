import math
import trimesh

# Function that loads the model, moves if to the origin and has the option to make is transparent
# Author: Ashkan Pourkand
def model_loader(name, origin=[0.0, 0.0, 0.0], transparent= True):
    mesh = trimesh.load_mesh(name)
    mesh.vertices -= mesh.center_mass + origin
    if transparent :  mesh.visual.face_colors = [200, 200, 250, 130]
    return mesh

