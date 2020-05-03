
import math

import glm
from ray_tracer import Ray

class Camera:
    def __init__(self, fov = 60, aspect_ratio = 16 / 9):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.perspective = glm.perspective(self.fov, self.aspect_ratio, 0.001, 100.0)
        self.perspective_view_matrix = glm.mat4() * self.perspective

    def LookAt(self, eye, center, up):
        self.origin = eye
        self.forward = glm.normalize(center - eye)
        self.right = glm.normalize(glm.cross(self.forward, up))
        self.up = glm.cross(self.right, self.forward)

        self.height = math.tan(self.fov)
        self.width = self.height * self.aspect_ratio

        view = glm.lookAt(eye, center, up)
        self.perspective_view_matrix = (self.perspective * view)

    def MakeRay(self, u, v):
        origin = self.origin
        direction = self.forward + self.right * u * self.width + self.up * v * self.height * 2
        direction = glm.normalize(direction)

        ray = Ray(origin, direction)
        # ray.ApplyMatrix(self.perspective_view_matrix)
        return ray
