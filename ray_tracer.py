
import math

from math_extentions import *

class IntersectionResult:
    def __init__(self, obj, world_position, ray_origin_offset, surface_normal):
        self.obj = obj
        self.world_position = world_position
        self.surface_normal = surface_normal
        self.ray_origin_offset = ray_origin_offset

class Ray:
    def __init__(self, origin, direction):
        self.intensity = 1
        self.origin = origin
        self.direction = direction
        self.t_min = 0.0
        self.t_max = float("inf")

    # TODO: this should be refactored
    # def ApplyMatrix(self, matrix):
    #     self.origin = matrix * self.origin
    #     self.direction = (matrix * self.direction).normalize()

    def PointAtOffset(self, offset):
        return self.origin + self.direction * offset
