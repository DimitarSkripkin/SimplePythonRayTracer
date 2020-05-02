
from math_extentions import Vec3

def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    return value

def clamp_color(color):
    new_color = Vec3.FromVec3(color)
    new_color[0] = clamp(new_color[0], 0, 255)
    new_color[1] = clamp(new_color[1], 0, 255)
    new_color[2] = clamp(new_color[2], 0, 255)
    return new_color

class Frame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bpp = 4  # bytes per pixel
        self.bytes = bytearray(self.width * self.height * self.bpp)

    def SetFloatingColorAt(self, x, y, normalized_color):
        normalized_color = clamp_color(normalized_color * 255)
        bytes_offset = (y * self.width + x) * self.bpp
        self.bytes[bytes_offset + 0] = int(normalized_color[0])
        self.bytes[bytes_offset + 1] = int(normalized_color[1])
        self.bytes[bytes_offset + 2] = int(normalized_color[2])
        self.bytes[bytes_offset + 3] = 255
