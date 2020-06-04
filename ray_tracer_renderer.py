
import math
import threading
import queue
import logging

import glm
from math_extentions import random01, random_unit_vector, random_in_unit_sphere, random_in_hemisphere
from frame import Frame
from ray_data import Ray
import shaders

class RenderJob:
    def __init__(self, frame, scene, fromX, toX, fromY, toY):
        self.frame = frame
        self.scene = scene
        self.fromX = fromX
        self.toX = toX
        self.fromY = fromY
        self.toY = toY

    def Render(self):
        width = self.frame.width
        height = self.frame.height

        # render_func = self.FastRender
        render_func = self.AntiAliasedRender
        # render_func = self.DebugRender

        for y in range(self.fromY, self.toY):
            for x in range(self.fromX, self.toX):
                color = render_func(x, y, width, height)
                self.frame.SetFloatingColorAt(x, y, color)

    def FastRender(self, x, y, width, height):
        color = glm.vec3(0, 0, 0)

        u = (4 * x / width) - 2
        v = (2 * y / height) - 1

        ray = self.scene.camera.MakeRay(u, v)
        color = self.ComputeColor(ray)

        return color

    def AntiAliasedRender(self, x, y, width, height):
        anti_aliasing_samples_count = 4

        color = glm.vec3(0, 0, 0)

        for i in range(anti_aliasing_samples_count):
            u = ((4 * x + random01()) / width) - 2
            v = ((2 * y + random01()) / height) - 1

            ray = self.scene.camera.MakeRay(u, v)
            try:
                color += self.ComputeColor(ray)
            except:
                logging.error(f"failed to process job for coordinates - {u}x{v}")

        # Divide the color total by the number of samples and gamma-correct
        # for a gamma value of 2.0.
        scale = 1.0 / anti_aliasing_samples_count
        r = math.sqrt(scale * color[0])
        g = math.sqrt(scale * color[1])
        b = math.sqrt(scale * color[2])
        return glm.vec3(r, g, b)

    def ComputeColor(self, ray, bounce_limit = 15):
        if bounce_limit <= 0:
            return glm.vec3(0, 0, 0)

        best_intersection = self.scene.CastRay(ray)

        ray_direction = glm.vec3(ray.direction)
        if best_intersection:
            # closest_light = self.scene.GetClosestLight(glm.vec4(best_intersection.world_position, 1))
            # light_position = glm.vec3(closest_light.position)

            # return shaders.ComputeColor(best_intersection.obj, best_intersection, light_position)
            # return shaders.ComputeFlatColor(best_intersection.obj, best_intersection, light_position)

            material = best_intersection.obj.material
            scatter_result = material.Scatter(ray, best_intersection)
            if not scatter_result:
                return material.emitted.AsVec3()

            material_color = glm.vec3(scatter_result.attenuation)
            return (
                material.emitted.AsVec3()
                + material_color * self.ComputeColor(scatter_result.scattered, bounce_limit - 1)
            )
        else:
            return glm.vec3(0, 0, 0)

    def DebugRender(self, x, y, width, height):
        debug_frame_orientation = False
        debug_uv_coordinates = False
        debug_normals = True
        debug_depth = False

        color = glm.vec3(0, 0, 0)

        u = (4 * x / width) - 2
        v = (2 * y / height) - 1

        if debug_frame_orientation:
            color.x = x / width
            color.y = y / height
            color.z = 0.2
        elif debug_uv_coordinates:
            color = shaders.DebugUVCoordinates(u, v)
        else:
            ray = self.scene.camera.MakeRay(u, v)
            best_intersection = self.scene.CastRay(ray)

            if best_intersection:
                if debug_normals:
                    color = shaders.DebugNormals(u, v, best_intersection.obj, best_intersection)
                elif debug_depth:
                    color = shaders.DebugDepth(best_intersection)

        return color

def RenderThread(thread_number, render_queue, stop_rendering_event):
    logging.info(f"starting rendering thread - {thread_number}")
    while not stop_rendering_event.is_set():
        try:
            item = render_queue.get(False)
        except queue.Empty:
            logging.info(f"no more jobs, stopping rendering thread - {thread_number}")
            return

        item.Render()
        render_queue.task_done()

    logging.info(f"force stopping rendering thread - {thread_number}")

# TODO: check if this could be refactored to use ThreadPoolExecutor
class RayTracerRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = Frame(self.width, self.height)
        self.preparation_for_rendering = False

        self.render_queue = queue.Queue()
        self.render_threads = []
        self.stop_rendering_event = threading.Event()

    # expected Frame orientation:
    # x = 0 to be Left side of the image
    # y = 0 to be Bottom side of the image
    def Render(self, scene):
        if self.preparation_for_rendering or self.IsRendering():
            return

        self.preparation_for_rendering = True
        # TODO: remove when there is no need for visual indication if new rendering is started
        self.frame = Frame(self.width, self.height)

        horizontal_frame_step = 16
        vertical_frame_step = 16
        self.JobsWithSpiralRenderPattern(scene, horizontal_frame_step, vertical_frame_step)
        # self.JobsWithBottomToTopRenderPattern(scene, horizontal_frame_step, vertical_frame_step)

        # create and start worker threads
        self.render_threads = []
        worker_threads_count = 1
        for thread_number in range(0, worker_threads_count):
            render_thread_args = (thread_number, self.render_queue, self.stop_rendering_event)
            render_thread = threading.Thread(target=RenderThread, args=render_thread_args)
            self.render_threads.append(render_thread)
            render_thread.start()

        self.preparation_for_rendering = False

    def StopRendering(self):
        self.stop_rendering_event.set()
        for render_thread in self.render_threads:
            render_thread.join()

    def IsRendering(self):
        for render_thread in self.render_threads:
            if render_thread.is_alive():
                return True

        return False

    def JobsWithBottomToTopRenderPattern(self, scene, horizontal_frame_step, vertical_frame_step):
        # generate worker jobs
        for y in range(0, self.height, vertical_frame_step):
            for x in range(0, self.width, horizontal_frame_step):
                from_x = x
                to_x = from_x + horizontal_frame_step
                if to_x > self.width:
                    to_x = self.width
                from_y = y
                to_y = from_y + vertical_frame_step
                if to_y > self.height:
                    to_y = self.height
                # logging.debug(f"new rendering job for {from_x} - {to_x}, {from_y} - {to_y}")
                render_job = RenderJob(self.frame, scene, from_x, to_x, from_y, to_y)
                self.render_queue.put(render_job)

    def JobsWithSpiralRenderPattern(self, scene, horizontal_frame_step, vertical_frame_step):
        # generate worker jobs
        frame_step = glm.vec2(horizontal_frame_step, vertical_frame_step)
        origin = glm.vec2(self.width / 2, self.height / 2) - frame_step
        for (x, y) in spiral(int(self.width / horizontal_frame_step) + 1, int(self.height / vertical_frame_step) + 1):
            from_point = glm.vec2(x, y) * frame_step + origin
            to_point = from_point + frame_step

            from_point.x = glm.clamp(from_point.x, 0, self.width)
            from_point.y = glm.clamp(from_point.y, 0, self.height)
            to_point.x = glm.clamp(to_point.x, 0, self.width)
            to_point.y = glm.clamp(to_point.y, 0, self.height)

            render_job = RenderJob(self.frame, scene, int(from_point.x), int(to_point.x), int(from_point.y), int(to_point.y))
            self.render_queue.put(render_job)

def spiral(width, height):
    x = 0
    y = 0
    dx = 0
    dy = -1
    half_width = width / 2
    half_height = height / 2
    for i in range(max(width, height)**2):
        if (-half_width < x <= half_width) and (-half_height < y <= half_height):
            yield (x, y)
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy
