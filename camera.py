
import math

from math_extentions import matrix, vector, Vec4, Vec3
from ray_tracer import Ray

class Camera:
    def __init__(self, fov = 60, aspect_ratio = 16 / 9):
        self.perspective_view_matrix = matrix.identity(4)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.perspective = matrix.perspective(self.fov, self.aspect_ratio, 0.001, 100.0)

    def LookAt(self, eye, center, up):
        self.origin = eye
        self.forward = (center - eye).normalize()
        self.right = vector.cross(self.forward, up).normalize()
        self.up = vector.cross(self.right, self.forward)

        self.height = math.tan(self.fov)
        self.width = self.height * self.aspect_ratio

        view = matrix.lookAt(eye, center, up)
        self.perspective_view_matrix = (self.perspective * view)

    def MakeRay(self, u, v):
        origin = self.origin
        direction = self.forward + self.right * u * self.width + self.up * v * self.height * 2
        direction.normalize()

        ray = Ray(origin, direction)
        # ray.ApplyMatrix(self.perspective_view_matrix)
        return ray
