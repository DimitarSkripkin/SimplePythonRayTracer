
import math

from math_extentions import *
from scene_data import Object
from materials import Color, DefaultMaterial
from ray_tracer import IntersectionResult

class Sphere(Object):
    def __init__(self, radius, position, material):
        super().__init__('3D_OBJECT_SPHERE', position, material)
        self.radius = radius

    def Intersect(self, ray):
        ray_origin = ray.origin.xyz()
        ray_direction = ray.direction.xyz()
        sphere_center = self.position.xyz()
        oc = ray_origin - sphere_center

        a = ray_direction.dot(ray_direction)
        # b = 2.0 * oc.dot(ray_direction)
        half_b = oc.dot(ray_direction)
        c = oc.dot(oc) - self.radius * self.radius
        # discriminant = b*b - 4*a*c
        discriminant = half_b*half_b - a*c

        if discriminant > 0:
            # ray_intersection_offset = (-b - math.sqrt(discriminant)) / (2 * a)
            ray_intersection_offset = (-half_b - math.sqrt(discriminant)) / a
            if ray_intersection_offset < ray.t_max and ray_intersection_offset > ray.t_min:
                intersection_point = ray.PointAtOffset(ray_intersection_offset)
                surface_normal = (intersection_point - sphere_center).normalize()
                intersection_result = IntersectionResult(self, intersection_point, ray_intersection_offset, surface_normal)
                return intersection_result

            # ray_intersection_offset = (-b + math.sqrt(discriminant)) / (2 * a)
            ray_intersection_offset = (-half_b + math.sqrt(discriminant)) / a
            if ray_intersection_offset < ray.t_max and ray_intersection_offset > ray.t_min:
                intersection_point = ray.PointAtOffset(ray_intersection_offset)
                surface_normal = (intersection_point - sphere_center).normalize()
                intersection_result = IntersectionResult(self, intersection_point, ray_intersection_offset, surface_normal)
                return intersection_result

        return None

    # TODO: compare both approaches
    def IntersectOld(self, ray):
        position = self.position
        radius = self.radius

        ray_origin = ray.origin.xyz()
        ray_direction = ray.direction.xyz()
        sphere_center = position.xyz()
        t = (sphere_center - ray_origin).dot(ray_direction)

        pos = ray.PointAtOffset(t) # ray_direction * t + ray_origin

        intersection_distance = (sphere_center - pos).magnitude()
        if intersection_distance == radius:
            intersection_result = IntersectionResult(self, pos, t, (pos - sphere_center).normalize())
            return intersection_result
        elif intersection_distance < radius:
            tHc = math.sqrt(radius * radius - intersection_distance * intersection_distance)
            ray_collision_offset = t - tHc
            intersection1 = ray_origin + (ray_direction * ray_collision_offset)
            intersection_result = IntersectionResult(self, intersection1, ray_collision_offset, (intersection1 - sphere_center).normalize())
            return intersection_result
            # ray_collision_offset = t + tHc
            # intersection2 = ray_origin + (ray_direction * ray_collision_offset)
            # intersection_result = IntersectionResult(intersection2, ray_collision_offset, (intersection2 - sphere_center).normalize())
        return None

    @classmethod
    def GenerateRandomSphere(cls):
        radius = random_in_range(2, 5)
        position = Vec4(random_in_range(-5, 5), random_in_range(-5, 5), random_in_range(-5, 5), 1)
        material = DefaultMaterial()
        material.color = Color.RandomColor()
        return cls(radius, position, material)
