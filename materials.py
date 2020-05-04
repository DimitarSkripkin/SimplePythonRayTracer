
from math_extentions import *
from ray_tracer import Ray

class Color:
    def __init__(self, r = 0, g = 0, b = 0, alpha = 1):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def AsVec3(self):
        return glm.vec3(self.r, self.g, self.b)

    def AsVec4(self):
        return glm.vec4(self.r, self.g, self.b, self.alpha)

    @classmethod
    def RandomColor(cls):
        min_color_value = 0
        max_color_value = 1
        return cls(random_in_range(min_color_value, max_color_value),
            random_in_range(min_color_value, max_color_value),
            random_in_range(min_color_value, max_color_value))

class Material:
    def __init__(self):
        self.color = Color(0.250, 0.5, 1)

class ScatterResult:
    def __init__(self, attenuation, scattered):
        self.attenuation = attenuation
        self.scattered = scattered

class Lambertian(Material):
    def __init__(self):
        super().__init__()

    def Scatter(self, ray, hit_record):
        # bounce_target = best_intersection.world_position + best_intersection.surface_normal + random_unit_vector()
        # bounce_target = best_intersection.world_position + best_intersection.surface_normal + random_in_unit_sphere()
        bounce_target = hit_record.world_position + random_in_hemisphere(hit_record.surface_normal)
        bounce_direction = glm.normalize(bounce_target - hit_record.world_position)
        bounce_ray = Ray(hit_record.world_position, bounce_direction)
        return ScatterResult(self.color.AsVec4(), bounce_ray)

class Reflective(Material):
    def __init__(self):
        super().__init__()

    def Scatter(self, ray, hit_record):
        ray_direction = glm.vec3(ray.direction)
        # v - 2*dot(v, n)*n;
        reflection_direction = glm.reflect(ray_direction, hit_record.surface_normal)
        if glm.dot(reflection_direction, hit_record.surface_normal) <= 0:
            return None

        reflected_ray = Ray(hit_record.world_position, reflection_direction)
        return ScatterResult(self.color.AsVec4(), reflected_ray)

def RandomMaterial():
    material_index = random.randint(0, 1)
    materials = {
        0: Lambertian,
        1: Reflective
    }

    return materials.get(material_index)()
