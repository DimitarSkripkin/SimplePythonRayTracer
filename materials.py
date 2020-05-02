
from math_extentions import *

class Color:
    def __init__(self, r = 0, g = 0, b = 0, alpha = 255):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    @classmethod
    def RandomColor(cls):
        min_color_value = 64
        max_color_value = 230
        return cls(random_in_range(min_color_value, max_color_value),
            random_in_range(min_color_value, max_color_value),
            random_in_range(min_color_value, max_color_value))

class DefaultMaterial:
    def __init__(self):
        self.ambient = 0.1
        self.diffuse = 0.9
        self.specular = 0.9
        self.shininess = 200
        self.reflectivity = 0
        self.transparency = 0
        self.refractive_index = 1
        self.color = Color(32, 128, 255)
