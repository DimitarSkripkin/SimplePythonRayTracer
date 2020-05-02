
import logging
import wx

from scene_data import Scene
from ray_tracer_renderer import RayTracerRenderer

class RayTracerUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(RayTracerUI, self).__init__(*args, **kw)
        self.InitRayTracer()
        self.InitUI()

    def InitUI(self):
        self.image_width = 1280
        self.image_height = 720
        self.aspect_ratio = self.image_width / self.image_height

        pnl = wx.Panel(self)
        # font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        # heading = wx.StaticText(pnl, label='Stats', pos=(105, 10))
        # heading.SetFont(font)

        self.renderBtn = wx.Button(pnl, label='Render', pos=(self.image_width - 85, 10))
        self.renderBtn.Bind(wx.EVT_BUTTON, self.OnStartRender)
        # refreshBtn = wx.Button(pnl, label='Manual Refresh', pos=(self.image_width / 2, 10))
        # refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefreshRender)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnRefreshTimer, self.timer)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.resized = False # the dirty flag
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.bitmap = self.MakeBitmap(self.ray_tracer_renderer.frame, self.image_width, self.image_height)
        self.img = wx.StaticBitmap(pnl, 0, self.bitmap, pos=(5, 42))

        windowSize = (self.image_width + 25, self.image_height + 100)
        self.SetSize(windowSize)
        self.SetTitle('RayTracer')
        self.Centre()
        self.Show(True)

        self.img.SetBitmap(self.bitmap)

    def RecalculateUIElements(self):
        if not self.IsShown():
            return

        pos = (self.ClientSize.width - 95, 10)
        self.renderBtn.SetPosition(pos)

        offset_x = (self.ClientSize.width - self.image_width) / 2 - 1
        offset_y = (self.ClientSize.height - self.image_height) / 2 + 21
        imagePos = (offset_x, offset_y)
        self.img.SetPosition(imagePos)

    def OnClose(self, event):
        self.ray_tracer_renderer.StopRendering()
        event.Skip()

    def OnSize(self, event):
        self.resized = True # set dirty
        event.Skip()

    def OnIdle(self, event):
        if self.resized:
            # take action if the dirty flag is set
            new_width, new_height = self.GetSize()
            logging.info(f"w: {new_width}, h: {new_height}")

            new_width -= 25
            new_height -= 100

            # self.aspect_ratio = w / h
            new_ratio = new_width / new_height
            if new_ratio < self.aspect_ratio:
                self.image_width = new_width
                self.image_height = self.image_width / self.aspect_ratio
            else:
                self.image_height = new_height
                self.image_width = self.image_height * self.aspect_ratio

            self.RecalculateUIElements()
            self.OnRefreshRender(event)
            self.Refresh()
            self.resized = False # reset the flag

    def InitRayTracer(self):
        # 80, 40, 20, 10, 8, 4, 2, 1
        scale_down_factor = 2
        self.ray_tracer_width = int(1280 / scale_down_factor)
        self.ray_tracer_height = int(720 / scale_down_factor)
        self.scene = Scene()
        # self.scene.InitDemoScene()
        self.scene.InitDebugScene()
        self.ray_tracer_renderer = RayTracerRenderer(self.ray_tracer_width, self.ray_tracer_height)

    def OnStartRender(self, event):
        if self.ray_tracer_renderer.IsRendering():
            event.Skip()
            return

        self.timer.Start(100)
        self.ray_tracer_renderer.Render(self.scene)

    def OnRefreshTimer(self, event):
        # logging.debug('OnRefreshTimer')
        if not self.ray_tracer_renderer.IsRendering():
            self.timer.Stop()

        self.OnRefreshRender(event)

    def OnRefreshRender(self, _event):
        self.bitmap = self.MakeBitmap(self.ray_tracer_renderer.frame, self.image_width, self.image_height)
        self.img.SetBitmap(self.bitmap)

    def MakeBitmap(self, frame, target_width, target_height):
        # Make a bitmap using an array of RGBA bytes
        bitmap = wx.Bitmap.FromBufferRGBA(frame.width, frame.height, frame.bytes)
        image = bitmap.ConvertToImage().Mirror(False)
        # image = image.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)
        image = image.Scale(target_width, target_height, wx.IMAGE_QUALITY_NEAREST)
        return wx.Bitmap(image)


def main():
    rtApp = wx.App()
    RayTracerUI(None)
    rtApp.MainLoop()

if __name__ == '__main__':
    loggingHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')
    loggingHandler.setFormatter(logFormatter)
    logging.basicConfig(level=logging.DEBUG, handlers=[loggingHandler])
    main()
