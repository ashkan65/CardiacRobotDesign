# This calss generates mesh (trimesh extrude) of a sheath.
import trimesh
import numpy as np
import math


class Sheath:
    SegmentsLength = None
    Length = None
    SegmentsNum = None
    Radius = None
    BaseTransform = None
    Path = []
    ThetaMax = None
    polygon = None

    # parameterized constructor
    def __init__(self, Radius, Length, SegmentsLength, ThetaMax):
        self.SegmentsLength = SegmentsLength
        self.Length = Length
        self.SegmentsNum = int(Length / SegmentsLength)
        self.ThetaMax = ThetaMax

    def display(self):
        print("SegmentsLength = " + str(self.SegmentsLength))
        print("SegmentsNum = " + str(self.SegmentsNum))
        print("ThetaMax = " + str(self.ThetaMax))
        print("Length = " + str(self.Length))

    def transform(self, transform):
        self.answer = self.first + self.second

    def set_cross(self, radius, SegmentsNum=100, show=False):
        self.Radius = radius
        angles = np.arange(0, 2 * math.pi, 2 * math.pi / SegmentsNum)
        vertices = np.array([radius * np.sin(angles), radius * np.cos(angles)]).T
        # print (vertices)
        end_edge = np.array([[SegmentsNum - 1, 0]])
        edges = np.array([np.arange(0, SegmentsNum - 1), np.arange(1, SegmentsNum)]).T
        # print (edges)
        # print(end_edge)
        edges = np.concatenate((edges, end_edge), axis=0)
        # print(a)
        # v = [[2.0, 0.0], [2.0, 2.0], [0.0, 2.0], [-2.0, 2.0], [-2.0, 0.0], [-2.0, -2.0],
        #      [0.0, -2.0], [2.0, -2.0], [2.0, 0.0]]
        # v = np.array(v)
        # e = np.array([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]])
        self.polygon = trimesh.path.polygons.edges_to_polygons(edges, vertices)
        if show: trimesh.path.polygons.plot(self.polygon)
        path = np.array([np.arange(0, 10, 1), np.zeros(10), np.zeros(10)]).T.reshape(10, 3)
        # print(path)

    def path_gen(self):
        self.path = np.array([np.arange(0, 10, 1), np.zeros(10), np.zeros(10)]).T.reshape(10, 3)
        # for i in range(self.SegmentsNum):
        #     self.Path.append(1)

    def mesh_gen(self):
        self.mesh = trimesh.creation.sweep_polygon(self.polygon[0], np.array([np.arange(0, 10, 1), np.zeros(10),
                                                                              np.zeros(10)]).T.reshape(10, 3))
        return self.mesh
# # creating object of the class
# # this will invoke parameterized constructor
# obj = Addition(1000, 2000)

# # perform Addition
# obj.calculate()

# # display result
# obj.display()
