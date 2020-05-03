
import glm

def clamp(value, min_value, max_value):
    return glm.clamp(value, min_value, max_value)

def clamp_color(color):
    return glm.clamp(color, 0, 255)

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
