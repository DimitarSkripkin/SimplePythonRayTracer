
import random
import math
from enum import Enum

import glm

def random_in_range(min_value, max_value):
    return min_value + random.random() * (max_value - min_value)

def random01():
    return random.random()

def random_unit_vector():
    a = random_in_range(0, 2 * math.pi)
    z = random_in_range(-1, 1)
    r = math.sqrt(1 - z*z)
    return glm.vec3(r * math.cos(a), r * math.sin(a), z)

def random_in_unit_sphere():
    while True:
        p = glm.vec3(random_in_range(-1, 1), random_in_range(-1, 1), random_in_range(-1, 1))
        if glm.length2(p) > 1:
            continue

        return p

def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if glm.dot(in_unit_sphere, normal) > 0: # in the same hemisphere as the normal
        return in_unit_sphere
    else:
        return -in_unit_sphere

def get_squared_distance(vecA, vecB):
    return glm.distance2(vecA, vecB)

class RefractionIndices(Enum):
    Vacuum = 1.0
    AirAtSeaLevel = 1.00029
    Ice = 1.31
    # at 20 degrees C
    Water = 1.333
    FusedQuartz = 1.46
    # from 1.5 to 1.6
    Glass = 1.5
    Sapphire = 1.77
    Diamond = 2.42

def refract(uv, n, etaI_over_etaT):
    cos_theta = glm.dot(-uv, n)
    r_out_parallel =  etaI_over_etaT * (uv + cos_theta * n)
    r_out_perp = n * (-math.sqrt(1.0 - glm.length2(r_out_parallel)))
    return r_out_parallel + r_out_perp

def schlick_approximation(cosine, ref_idx):
    # r0 = (air_refraction_index - ref_idx) / (air_refraction_index + ref_idx)
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0)*math.pow((1 - cosine), 5)
