
import random
from gem import matrix, vector

def random_in_range(min_value, max_value):
    return min_value + random.random() * (max_value - min_value)

def random01():
    return random.random()

def get_squared_distance(vecA, vecB):
    return (vecA.vector[0] - vecB.vector[0])**2 + (vecA.vector[1] - vecB.vector[1])**2 + (vecA.vector[2] - vecB.vector[2])**2

class Mat4(matrix.Matrix):
    def __init__(self, data = None):
        super().__init__(4, data=data)

class Vec3(vector.Vector):
    def __init__(self, *data):
        super().__init__(3, data=list(data))

    @property
    def x(self):
        return self.vector[0]

    @x.setter
    def x(self, value):
        self.vector[0] = value

    @property
    def y(self):
        return self.vector[1]

    @y.setter
    def y(self, value):
        self.vector[1] = value

    @property
    def z(self):
        return self.vector[2]

    @z.setter
    def z(self, value):
        self.vector[2] = value

    def __setitem__(self, index, data):
        self.vector[index] = data

    def __getitem__(self, index):
        return self.vector[index]

    @classmethod
    def FromVec3(cls, vec3):
        return cls(*vec3.vector)

class Vec4(vector.Vector):
    def __init__(self, *data):
        super().__init__(4, data=list(data))

    @property
    def x(self):
        return self.vector[0]

    @x.setter
    def x(self, value):
        self.vector[0] = value

    @property
    def y(self):
        return self.vector[1]

    @y.setter
    def y(self, value):
        self.vector[1] = value

    @property
    def z(self):
        return self.vector[2]

    @z.setter
    def z(self, value):
        self.vector[2] = value

    @property
    def w(self):
        return self.vector[3]

    @w.setter
    def w(self, value):
        self.vector[3] = value

    def __setitem__(self, index, data):
        self.vector[index] = data

    def __getitem__(self, index):
        return self.vector[index]

    @classmethod
    def FromVec3(cls, vec3, w):
        return cls(*vec3.vector, w)
