
import math

import glm
from ray_tracer import Ray

class Camera:
    def __init__(self, fov = 60, aspect_ratio = 16 / 9):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        # self.perspective = glm.perspective(self.fov, self.aspect_ratio, 0.001, 100.0)
        # self.perspective_view_matrix = glm.mat4() * self.perspective

        self.LookAt(glm.vec3(0, 0, 1), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0), fov, aspect_ratio)

    def LookAt(self, eye, center, up, fov = None, aspect_ratio = None):
        if fov:
            self.fov = fov
        if aspect_ratio:
            self.aspect_ratio = aspect_ratio
        if fov or aspect_ratio:
            self.half_height = math.tan(math.radians(self.fov) / 2)
            self.half_width = self.half_height * self.aspect_ratio

        self.origin = eye
        self.forward = glm.normalize(center - eye)
        self.right = glm.normalize(glm.cross(self.forward, up))
        self.up = glm.cross(self.right, self.forward)

        # view = glm.lookAt(eye, center, up)
        # self.perspective_view_matrix = (self.perspective * view)

        self.up = self.up * self.half_height * 2
        self.right = self.right * self.half_width

    def MakeRay(self, u, v):
        origin = self.origin
        direction = self.forward + self.right * u + self.up * v
        direction = glm.normalize(direction)

        ray = Ray(origin, direction)
        # ray.ApplyMatrix(self.perspective_view_matrix)
        return ray
