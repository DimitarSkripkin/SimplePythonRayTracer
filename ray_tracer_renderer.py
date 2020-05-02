
import math
import threading
import queue
import logging

from math_extentions import Vec3, Vec4, matrix, random01
from frame import Frame
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

        render_func = self.FastRender
        # render_func = self.AntiAliasedRender
        # render_func = self.DebugRender

        for y in range(self.fromY, self.toY):
            for x in range(self.fromX, self.toX):
                color = render_func(x, y, width, height)
                self.frame.SetFloatingColorAt(x, y, color)

    def FastRender(self, x, y, width, height):
        color = Vec3(0, 0, 0)

        u = (4 * x / width) - 2
        v = (2 * y / height) - 1

        ray = self.scene.camera.MakeRay(u, v)
        color = self.ComputeColor(u, v, ray)

        return color

    def AntiAliasedRender(self, x, y, width, height):
        anti_aliasing_samples_count = 8

        color = Vec3(0, 0, 0)

        for i in range(anti_aliasing_samples_count):
            u = ((4 * x + random01()) / width) - 2
            v = ((2 * y + random01()) / height) - 1

            ray = self.scene.camera.MakeRay(u, v)
            color += self.ComputeColor(u, v, ray)

        return color / anti_aliasing_samples_count

    def ComputeColor(self, u, v, ray):
        best_intersection = self.scene.CastRay(ray)

        if best_intersection:
            closest_light = self.scene.GetClosestLight(best_intersection.world_position)
            light_position = closest_light.position.xyz()

            return shaders.ComputeColor(best_intersection.obj, best_intersection, light_position)
            # return shaders.ComputeFlatColor(best_intersection.obj, best_intersection, light_position)
        else:
            return shaders.DebugUVCoordinates(u, v)

    def DebugRender(self, x, y, width, height):
        debug_frame_orientation = False
        debug_uv_coordinates = False
        debug_normals = True
        debug_depth = False

        color = Vec3(0, 0, 0)

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

        # generate worker jobs
        horizontal_frame_step = 16
        vertical_frame_step = 16
        for y in range(0, self.height, vertical_frame_step):
            for x in range(0, self.width, horizontal_frame_step):
                fromX = x
                toX = fromX + horizontal_frame_step
                if toX > self.width:
                    toX = self.width
                fromY = y
                toY = fromY + vertical_frame_step
                if toY > self.height:
                    toY = self.height
                # logging.debug(f"new rendering job for {fromX} - {toX}, {fromY} - {toY}")
                render_job = RenderJob(self.frame, scene, fromX, toX, fromY, toY)
                self.render_queue.put(render_job)

        # create and start worker threads
        self.render_threads = []
        worker_threads_count = 16
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
