'''
    This file generates the forward kinematics and mesh of steerable sheaths.
    This file has two classes sheath and robot. Sheath generates a curved mesh with a constant cross section
    Robot stacks multiple of sheaths to form a steerable sheaths.
    File name: robot.py
    Author: Ashkan Pourkand
    Date created: 9/2/2021
    Date last modified: 9/21/2021
    Python Version: 3.8.10
    Needs numpy, trimeshtransforms3d
    to install deps in lunix:
        pip3 install numpy
        pip3 install trimesh
        pip3 install transforms3d

'''
import trimesh
import numpy as np
import math
from transforms3d.euler import euler2mat
from transforms3d.axangles import axangle2mat



class Sheath:
    SegmentsLength = None
    Length = None
    SegmentsNum = None
    Radius = None
    BaseTransform = None
    ThetaMax = None
    polygon = None
    mesh = None
    R = None
    L = None
    sheath = None
    # parameterized constructor
    def __init__(self, radius, Length, SegmentsLength, ThetaMax):
        # Const:
        #   - radius of the sheath
        #   - length of the sheath
        #   - segment's length : smaller is more accurate but slower
        #   - Theta: how much bending the sheath has (assuming the constant curvature).

        self.radius = radius
        self.SegmentsLength = SegmentsLength
        self.Length = Length
        self.SegmentsNum = int(Length / SegmentsLength)
        self.ThetaMax = ThetaMax
        self.r = self.Length / self.ThetaMax
        self.Path = []
        self.set_cross()
        self.path_gen()
        self.mesh_gen()
        self.sheath = []

    def display(self):
        print("SegmentsLength = " + str(self.SegmentsLength))
        print("SegmentsNum = " + str(self.SegmentsNum))
        print("ThetaMax = " + str(self.ThetaMax))
        print("Length = " + str(self.Length))

    def set_cross(self, SegmentsNum=100, show=False):
        angles = np.arange(0, 2 * math.pi, 2 * math.pi / SegmentsNum)
        vertices = np.array([self.radius * np.sin(angles), self.radius * np.cos(angles)]).T
        end_edge = np.array([[SegmentsNum - 1, 0]])
        edges = np.array([np.arange(0, SegmentsNum - 1), np.arange(1, SegmentsNum)]).T
        edges = np.concatenate((edges, end_edge), axis=0)
        self.polygon = trimesh.path.polygons.edges_to_polygons(edges, vertices)
        if show: trimesh.path.polygons.plot(self.polygon)
        path = np.array([np.arange(0, 10, 1), np.zeros(10), np.zeros(10)]).T.reshape(10, 3)

    def path_gen(self):
        self.Path = []
        for i in range(self.SegmentsNum):
            theta = i * (self.ThetaMax / self.SegmentsNum)
            self.Path.append([self.r * (1 - math.cos(theta)), 0.0, self.r * math.sin(theta)])
        self.Path = np.array([self.Path])[0]

    def mesh_gen(self):
        self.mesh = trimesh.creation.sweep_polygon(self.polygon[0], self.Path)
        return self.mesh

    def apply_transformation_H(self, H, show=False):
        self.mesh.vertices = trimesh.transform_points(self.mesh.vertices, H)
        self.Path = trimesh.transform_points(self.Path, H)
        if show:
            trimesh.Scene(self.mesh).show()

    def apply_transformation(self, location, orientation, show=False):
        print("location", location)
        #   orientation = [x_angle, z_angle, y_angle]
        self.R = euler2mat(orientation[0], orientation[1], orientation[2], 'sxzy')
        self.L = np.array([location])
        self.BaseTransform = (np.concatenate((np.concatenate((self.R, self.L.T), axis=1),
                                              np.array([[0.0, 0.0, 0.0, 1.0]])), axis=0))
        self.apply_transformation_H(self.BaseTransform, show=show)

    def get_tail_pose(self):
        return (self.Path[-1, :]).T


class Robot:
    # This class generates the trimesh.mesh type soft robot that can be use for collision detection and path planning.
    # the robot has an array of steerable sheaths each capable of twisting, bending, and extending
    # you can apply the actuation commands via vectors of new parameters
    sectionsRadius = None
    baseLocation = None
    baseOrientation = None
    mesh = []
    numSections = None
    sheaths = []
    origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
    frames = []
    bending = None
    roll = None
    extension = None

    def __init__(self, sectionsRadius):
        # sectionsRadius : array of radiuses of the steerable sheaths in mm
        # self.baseLocation = baseLocation
        self.numSections = len(sectionsRadius)
        self.sectionsRadius = sectionsRadius

    def apply_bending(self, bending):
        # bending is a vectors of bending angles used in
        if len(bending) != self.numSections:
            raise Exception("Number of inputs does not match with the number of steerable sections")
        self.bending = bending

    def apply_roll(self, roll):
        if len(roll) != self.numSections:
            raise Exception("Number of inputs does not match with the number of steerable sections")
        self.roll = roll

    def apply_extension(self, extension):
        if len(extension) != self.numSections:
            raise Exception("Number of inputs does not match with the number of steerable sections")
        self.extension = extension

    def set_base_location(self, location):
        self.baseLocation = location

    def generate_path(self):
        # Doing FK and generating the path and mesh for the current configuration
        # First we generate frames at the base of each sheath (each one has a rot_Z followed by a roz_Y and a
        # translation to the end of tail):
        self.frames = []
        local_frame_T = []
        local_frame_R = []
        local_frame_H = []
        global_frame_H = []
        for i in range(self.numSections):
            sheath = Sheath(self.sectionsRadius[i], self.extension[i], 0.1, self.bending[i])
            # Rotation and translation due ot bending:
            local_frame_T.append(np.concatenate([sheath.get_tail_pose(), [1]], axis=0))
            local_frame_R.append(np.concatenate([axangle2mat([0, 1, 0], self.bending[i]),
                                                 np.array([[0, 0, 0]])], axis=0))

            zero_T = np.array([0.0, 0.0, 0.0, 1.0]).reshape(4,1)
            local_roll = np.concatenate([axangle2mat([0, 0, 1], self.roll[i]),
                                                 np.array([[0, 0, 0]])], axis=0)
            local_roll_T = np.concatenate([local_roll,zero_T], axis = 1)
            local_frame_H.append(np.column_stack([local_frame_R[i], local_frame_T[i]]))
            if i == 0:
                global_frame_H.append(np.dot(local_roll_T, local_frame_H[0]))
                self.sheaths.append(sheath.apply_transformation_H(local_roll_T))
            else:
                global_frame_H.append(np.dot(global_frame_H[i-1], np.dot(local_roll_T,local_frame_H[i])))
                self.sheaths.append(sheath.apply_transformation_H(np.dot(global_frame_H[i-1],local_roll_T)))
            self.mesh.append(sheath.mesh)

