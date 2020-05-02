
import math
from math_extentions import Vec3, Vec4

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
    return Vec3(1.0, 1.0, 1.0) * (1.0 - t) + Vec3(0.5, 0.7, 1.0) * t

def DebugDepth(best_intersection):
    color = Vec3(1, 1, 1) * best_intersection.ray_origin_offset
    color.i_normalize()
    return color

def ComputeFlatColor(obj, _intersection, _light_position):
    return Vec3(obj.material.color.r / 255, obj.material.color.g / 255, obj.material.color.b / 255)

# TODO: this should be refactored
def ComputeColor(obj, intersection, light_position):
    # intersection_position = intersection.position
    intersection_normal = intersection.surface_normal
    # light_direction = -light_position.normalize().xyz()
    light_direction = light_position.normalize().xyz()
    albedo = Vec3(obj.material.color.r / 255, obj.material.color.g / 255, obj.material.color.b / 255) # * obj.material.ambient
    dot_product = max(0.0, light_direction.dot(intersection_normal))
    color = albedo * dot_product
    return color
