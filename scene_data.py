
import glm
from math_extentions import random_in_range, get_squared_distance
from camera import Camera
from materials import Color, Lambertian, Reflective, Glossy, Transparent, RandomMaterial

class Object:
    def __init__(self, obj_type, position = glm.vec4(0, 0, 0, 1), material = None):
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
        self.camera.LookAt(glm.vec3(30, 30, 30), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        # self.camera.LookAt(glm.vec3(15, 10, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

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
        self.camera.LookAt(glm.vec3(0, 1, 1.5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0), 45)
        # self.camera.LookAt(glm.vec3(-2, 2, 1), glm.vec3(0, 0, -1), glm.vec3(0, 1, 0), 15)

        from objects import Sphere
        material = Lambertian()
        material.color = Color(0.1, 0.2, 0.5)
        sphere = Sphere(0.5, glm.vec4(-2, 0, -1, 1), material)
        self.AddObject(sphere)

        material = Reflective()
        material.color = Color(0.8, 0.8, 0.8)
        sphere = Sphere(0.5, glm.vec4(-1, 0, -1, 1), material)
        sphere.material = material
        self.AddObject(sphere)

        material = Glossy(0.3)
        material.color = Color(0.8, 0.6, 0.2)
        sphere = Sphere(0.5, glm.vec4(0, 0, -1, 1), material)
        sphere.material = material
        self.AddObject(sphere)

        material = Transparent(1.5)
        material.color = Color(0.8, 0.8, 0.8)
        sphere = Sphere(0.5, glm.vec4(1, 0, -1, 1), material)
        sphere.material = material
        self.AddObject(sphere)

        material = Transparent(1.5)
        material.color = Color(0.8, 0.8, 0.8)
        sphere = Sphere(-0.45, glm.vec4(1, 0, -1, 1), material)
        sphere.material = material
        self.AddObject(sphere)

        material = Lambertian()
        material.color = Color(0.5, 0.25, 0.125)
        sphere = Sphere(0.5, glm.vec4(2, 0, -1, 1), material)
        self.AddObject(sphere)

        material = Lambertian()
        material.color = Color(0.8, 0.8, 0.0)
        sphere = Sphere(100, glm.vec4(0, -100.5, -1, 1), material)
        self.AddObject(sphere)

        light = LightSource(glm.vec4(-10, 5, 0, 1))
        self.AddObject(light)

        # to debug if GetClosestLight method works
        # light = LightSource(glm.vec4(10, 0, -5, 1))
        # self.AddObject(light)

    def InitDemoScene(self):
        self.camera.LookAt(glm.vec3(10, 10, 20), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        from objects import Sphere, Plane

        min_sphere_radius = 2
        max_sphere_radius = 3
        cell_size = 2 * max_sphere_radius + 1
        for x in range(-1, 2):
            for y in range(-1, 2):
                sphere = Sphere.GenerateRandomSphere()
                sphere.radius = random_in_range(min_sphere_radius, max_sphere_radius)
                sphere.position = glm.vec4(x * cell_size + random_in_range(2, 4), random_in_range(2, 4), y * cell_size + random_in_range(2, 4), 1)
                self.AddObject(sphere)

        material = Lambertian()
        plane = Plane(glm.vec3(0, 1, 0), glm.vec3(0, 0, 0), material)
        self.AddObject(plane)

        light = LightSource(glm.vec4(-10, 10, 10, 1))
        self.AddObject(light)

        # to be used when there is support for multiple lights
        # light = LightSource(glm.vec4(1, 10, 0, 1))
        # self.AddObject(light)
