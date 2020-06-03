
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
    def __init__(self, color = Color(0.250, 0.5, 1), emitted = Color(0, 0, 0)):
        self.color = color
        self.emitted = emitted

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
        # v - 2*dot(v, n)*n
        reflection_direction = glm.reflect(ray_direction, hit_record.surface_normal)
        if glm.dot(reflection_direction, hit_record.surface_normal) <= 0:
            return None

        reflected_ray = Ray(hit_record.world_position, reflection_direction)
        return ScatterResult(self.color.AsVec4(), reflected_ray)

class Glossy(Material):
    def __init__(self, roughness = 0.8):
        super().__init__()
        self.roughness = roughness

    def Scatter(self, ray, hit_record):
        ray_direction = glm.vec3(ray.direction)
        # v - 2*dot(v, n)*n
        reflection_direction = glm.reflect(ray_direction, hit_record.surface_normal)
        if glm.dot(reflection_direction, hit_record.surface_normal) <= 0:
            return None

        reflected_ray = Ray(hit_record.world_position, reflection_direction + random_in_unit_sphere() * self.roughness)
        return ScatterResult(self.color.AsVec4(), reflected_ray)

class Transparent(Material):
    def __init__(self, refraction_index = 1.5):
        super().__init__()
        self.refraction_index = refraction_index

    def Scatter(self, ray, hit_record):
        self.color = Color(1, 1, 1)
        ray_direction = glm.vec3(ray.direction)
        surface_normal = hit_record.surface_normal

        # refract
        etaI_over_etaT = 1.0 / self.refraction_index
        ray_surface_dot = glm.dot(surface_normal, ray_direction)
        is_front_face = ray_surface_dot < 0
        if not is_front_face:
            # it's backside of the surface
            etaI_over_etaT = self.refraction_index
            surface_normal = -surface_normal
            ray_surface_dot = -ray_surface_dot

        cos_theta = glm.fmin(-ray_surface_dot, 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        if etaI_over_etaT * sin_theta > 1.0:
            # ray can't be refracted so should be reflected
            reflection_direction = glm.reflect(ray_direction, surface_normal)
            reflected_ray = Ray(hit_record.world_position, reflection_direction)
            return ScatterResult(self.color.AsVec4(), reflected_ray)

        reflect_prob = schlick_approximation(cos_theta, etaI_over_etaT)
        if random01() < reflect_prob:
            reflection_direction = glm.reflect(ray_direction, surface_normal)
            reflected_ray = Ray(hit_record.world_position, reflection_direction)
            return ScatterResult(self.color.AsVec4(), reflected_ray)

        refraction_direction = refract(ray_direction, surface_normal, etaI_over_etaT)
        refracted_ray = Ray(hit_record.world_position, refraction_direction)
        return ScatterResult(self.color.AsVec4(), refracted_ray)

class LightEmitting(Material):
    def __init__(self):
        super().__init__(emitted = Color(1, 1, 1))

    def Scatter(self, ray, hit_record):
        return None

def RandomMaterial():
    material_index = random.randint(0, 4)
    materials = {
        0: Lambertian,
        1: Reflective,
        2: Glossy,
        3: Transparent,
        4: LightEmitting
    }

    return materials.get(material_index)()
