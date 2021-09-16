import numpy as np
import math
import trimesh
import copy
from robot import Robot
from heart import model_loader

R = Robot([0.3, 0.25, .2, 0.1])
R.set_base_location(location = np.array([[3,0, 0]]).T)
R.apply_bending([math.pi/20000, math.pi/2, math.pi/3, math.pi])
R.apply_roll([0.0, math.pi/4, math.pi/4, math.pi/4])
R.apply_extension([10.0, 20.0, 10.0, 5.0])
R.generate_path()

heart = model_loader('Model/3DBenchy.stl')
meshes = [heart, R.mesh]
trimesh.Scene(meshes).show()

for i in R.mesh:

    coll_man = trimesh.collision.CollisionManager()

    coll_man.add_object(name = "Robot", mesh = i, transform=None)
    coll_man.add_object(name = "heart", mesh = heart, transform=None)

    print(coll_man.in_collision_internal())
