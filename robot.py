# This calss generates mesh (trimesh extrude) of a sheath.
import trimesh
import numpy as np

class Sheath:
    SegmentsLength = None
    Length = None
    SegmentsNum = None
    Radius = None
    BaseTransform = None 
    Path = []
    ThetaMax = None
    # parameterized constructor
    def __init__(self, Radius, Length, SegmentsLength, ThetaMax):
        self.SegmentsLength = SegmentsLength
        self.Length = Length
        self.SegmentsNum =  int(Length/SegmentsLength)
        self.ThetaMax = ThetaMax
    def display(self):
        print("SegmentsLength = " + str(self.SegmentsLength))
        print("SegmentsNum = " + str(self.SegmentsNum))
        print("ThetaMax = " + str(self.ThetaMax))
        print("Length = " + str(self.Length))
 
    def transform(self, transform):
        self.answer = self.first + self.second
    def set_cross(self,Radius ):
        self.Radius = Radius
        
    def path_gen(self):
        for i in range(self.SegmentsNum):
            self.Path.append(1)
# # creating object of the class
# # this will invoke parameterized constructor
# obj = Addition(1000, 2000)
 
# # perform Addition
# obj.calculate()
 
# # display result
# obj.display()