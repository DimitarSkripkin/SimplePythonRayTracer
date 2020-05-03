
import random
import math

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
