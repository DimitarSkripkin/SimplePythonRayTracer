
import math

import glm
from math_extentions import random_in_range
from scene_data import Object
from materials import Color, RandomMaterial
from ray_tracer import IntersectionResult

class Sphere(Object):
    def __init__(self, radius, position, material):
        super().__init__('3D_OBJECT_SPHERE', position, material)
        self.radius = radius

    def Intersect(self, ray):
        ray_origin = ray.origin
        ray_direction = ray.direction
        sphere_center = glm.vec3(self.position)
        oc = ray_origin - sphere_center

        a = glm.dot(ray_direction, ray_direction)
        # b = 2.0 * glm.dot(oc, ray_direction)
        half_b = glm.dot(oc, ray_direction)
        c = glm.dot(oc, oc) - self.radius * self.radius
        # discriminant = b*b - 4*a*c
        discriminant = half_b*half_b - a*c

        if discriminant > 0:
            # ray_intersection_offset = (-b - math.sqrt(discriminant)) / (2 * a)
            ray_intersection_offset = (-half_b - math.sqrt(discriminant)) / a
            if ray_intersection_offset < ray.t_max and ray_intersection_offset > ray.t_min:
                intersection_point = ray.PointAtOffset(ray_intersection_offset)
                surface_normal = glm.normalize(intersection_point - sphere_center)
                intersection_result = IntersectionResult(self, intersection_point, ray_intersection_offset, surface_normal)
                return intersection_result

            # ray_intersection_offset = (-b + math.sqrt(discriminant)) / (2 * a)
            ray_intersection_offset = (-half_b + math.sqrt(discriminant)) / a
            if ray_intersection_offset < ray.t_max and ray_intersection_offset > ray.t_min:
                intersection_point = ray.PointAtOffset(ray_intersection_offset)
                surface_normal = glm.normalize(intersection_point - sphere_center)
                intersection_result = IntersectionResult(self, intersection_point, ray_intersection_offset, surface_normal)
                return intersection_result

        return None

    # TODO: compare both approaches
    def IntersectOld(self, ray):
        position = self.position
        radius = self.radius

        ray_origin = ray.origin
        ray_direction = ray.direction
        sphere_center = position
        t = glm.dot(sphere_center - ray_origin, ray_direction)

        pos = ray.PointAtOffset(t) # ray_direction * t + ray_origin

        intersection_distance = glm.length(sphere_center - pos)
        if intersection_distance == radius:
            intersection_result = IntersectionResult(self, pos, t, glm.normalize(pos - sphere_center))
            return intersection_result
        elif intersection_distance < radius:
            tHc = math.sqrt(radius * radius - intersection_distance * intersection_distance)
            ray_collision_offset = t - tHc
            intersection1 = ray_origin + (ray_direction * ray_collision_offset)
            intersection_result = IntersectionResult(self, intersection1, ray_collision_offset, glm.normalize(intersection1 - sphere_center))
            return intersection_result
            # ray_collision_offset = t + tHc
            # intersection2 = ray_origin + (ray_direction * ray_collision_offset)
            # intersection_result = IntersectionResult(intersection2, ray_collision_offset, glm.normalize(intersection2 - sphere_center))
        return None

    @classmethod
    def GenerateRandomSphere(cls):
        radius = random_in_range(2, 5)
        position = glm.vec4(random_in_range(-5, 5), random_in_range(-5, 5), random_in_range(-5, 5), 1)
        material = RandomMaterial()
        material.color = Color.RandomColor()
        return cls(radius, position, material)

class Plane(Object):
    def __init__(self, normal, position, material):
        super().__init__('3D_OBJECT_PLANE', position, material)
        self.normal = normal

    def Intersect(self, ray):
        ray_direction = ray.direction
        denominator = glm.dot(self.normal, ray_direction)
        # possible collision
        # plane normal and ray direction are not in the same direction
        if denominator < 0:
            plane_position = self.position
            ray_origin = ray.origin
            oc = ray_origin - plane_position
            ray_intersection_offset = glm.dot(oc, self.normal) / -denominator
            # ray_intersection_offset > ray.t_min plane is in front of the ray
            if ray_intersection_offset < ray.t_max and ray_intersection_offset > ray.t_min:
                intersection_point = ray.PointAtOffset(ray_intersection_offset)
                intersection_result = IntersectionResult(self, intersection_point, ray_intersection_offset, self.normal)
                return intersection_result

        return None
