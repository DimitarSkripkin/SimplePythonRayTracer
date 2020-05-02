
from math_extentions import *
from camera import Camera
from materials import DefaultMaterial, Color

class Object:
    def __init__(self, obj_type, position = Vec4(0, 0, 0, 1), material = None):
        self.obj_type = obj_type
        self.position = position
        self.material = material

class LightSource(Object):
    def __init__(self, position, light_color = Color.RandomColor(), light_type = 'POINT_LIGHT'):
        super().__init__(light_type, position)
        # self.light_type = light_type

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.camera = Camera()
        self.camera.LookAt(Vec3(30, 30, 30), Vec3(0, 0, 0), Vec3(0, 1, 0))
        # self.camera.LookAt(Vec3(15, 10, 5), Vec3(0, 0, 0), Vec3(0, 1, 0))

    def AddObject(self, obj):
        if obj.obj_type == 'POINT_LIGHT':
            self.lights.append(obj)
        else:
            self.objects.append(obj)

    def CastRay(self, ray):
        best_intersection = None
        for obj in self.objects:
            intersection_result = obj.Intersect(ray)
            if not best_intersection:
                best_intersection = intersection_result
            elif intersection_result and intersection_result.ray_origin_offset < best_intersection.ray_origin_offset:
                best_intersection = intersection_result

        return best_intersection

    def GetClosestLight(self, point):
        current_closest = self.lights[0]
        current_closest_squared_distance = get_squared_distance(current_closest.position, point)
        for light in self.lights[1:]:
            squared_distance = get_squared_distance(light.position, point)
            if squared_distance < current_closest_squared_distance:
                current_closest_squared_distance = squared_distance
                current_closest = light
        return current_closest

    def InitDebugScene(self):
        self.camera.LookAt(Vec3(0, 0, 1), Vec3(0, 0, 0), Vec3(0, 1, 0))

        from objects import Sphere
        material = DefaultMaterial()
        material.color = Color(225, 225, 225)
        sphere = Sphere(0.5, Vec4(0, 0, -1), material)
        self.AddObject(sphere)

        light = LightSource(Vec4(-10, 5, 0, 1))
        self.AddObject(light)

        # to debug if GetClosestLight method works
        # light = LightSource(Vec4(10, 0, -5, 1))
        # self.AddObject(light)

    def InitDemoScene(self):
        from objects import Sphere

        min_sphere_radius = 2
        max_sphere_radius = 3
        for x in range(-16, 16, 2 * max_sphere_radius + 1):
            for y in range(-16, 16, 2 * max_sphere_radius + 1):
                sphere = Sphere.GenerateRandomSphere()
                sphere.radius = random_in_range(min_sphere_radius, max_sphere_radius)
                sphere.position = Vec4(x + random_in_range(2, 4), random_in_range(2, 4), y + random_in_range(2, 4), 1)
                self.AddObject(sphere)

        light = LightSource(Vec4(1, 10, 0, 1))
        self.AddObject(light)