
import math
import glm

# TODO: check if it will be better to
# add rendering data structure to be passed to those functions

def DebugNormals(u, v, obj, intersection):
    normal = intersection.surface_normal
    color = (normal + 1) * 0.5
    return color

def DebugUVCoordinates(u, v):
    length = math.sqrt(u * u + v * v + 1)
    tV = v / length
    t = 0.5 * (tV + 1.0)
    return glm.vec3(1.0, 1.0, 1.0) * (1.0 - t) + glm.vec3(0.5, 0.7, 1.0) * t

def DebugDepth(best_intersection):
    color = glm.vec3(1, 1, 1) * best_intersection.ray_origin_offset
    color = glm.normalize(color)
    return color

def ComputeFlatColor(obj, _intersection, _light_position):
    return obj.material.color.AsVec3()

# TODO: this should be refactored
def ComputeColor(obj, intersection, light_position):
    # intersection_position = intersection.position
    intersection_normal = intersection.surface_normal
    # light_direction = -light_position.normalize().xyz()
    light_direction = glm.normalize(light_position)
    albedo = obj.material.color.AsVec3() # * obj.material.ambient
    dot_product = max(0.0, glm.dot(light_direction, intersection_normal))
    color = albedo * dot_product
    return color
