
import logging
import time
from datetime import datetime

import wx

from ray_tracer_renderer import RayTracerRenderer
from scene_data import Scene

class ControlsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        self.renderBtn = wx.Button(self, label='Render')
        self.saveBtn = wx.Button(self, label='Save')
        self.stats = wx.StaticText(self, label='Stats: ')

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(self.stats, 1, wx.ALL | wx.EXPAND, 5)
        h_sizer.Add(self.renderBtn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        h_sizer.Add(self.saveBtn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.SetSizerAndFit(h_sizer)

    def UpdateStats(self, stats):
        label = f'Stats: {", ".join(stats)}'
        self.stats.SetLabel(label)

class RenderPanel(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent)

        self.bitmap = self.MakeBitmap(frame, frame.width, frame.height)
        self.img = wx.StaticBitmap(self, 0, self.bitmap)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.img, 1, wx.ALL | wx.SHAPED, 0)

        self.SetSizerAndFit(sizer)

    def UpdateRender(self, frame):
        virtual_size = self.GetVirtualSize()
        self.bitmap = self.MakeBitmap(frame, virtual_size.width, virtual_size.height)
        self.img.SetBitmap(self.bitmap)

    def MakeBitmap(self, frame, target_width, target_height):
        if target_width <= 0:
            target_width = 1
        if target_height <= 0:
            target_height = 1

        # Make a bitmap using an array of RGBA bytes
        bitmap = wx.Bitmap.FromBufferRGBA(frame.width, frame.height, frame.bytes)
        image = bitmap.ConvertToImage().Mirror(False)
        # image = image.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)
        image = image.Scale(target_width, target_height, wx.IMAGE_QUALITY_NEAREST)
        return wx.Bitmap(image)

class RayTracerUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(RayTracerUI, self).__init__(*args, **kw)
        self.InitRayTracer()
        self.InitUI()

    def InitUI(self):
        self.image_width = 640
        self.image_height = 360
        windowSize = (self.image_width + 25, self.image_height + 100)

        self.SetSize(windowSize)
        self.SetTitle('RayTracer')
        self.SetAutoLayout(1)

        self.controls = ControlsPanel(self)
        self.controls.renderBtn.Bind(wx.EVT_BUTTON, self.OnStartRender)
        self.controls.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)

        self.render_view = RenderPanel(self, self.ray_tracer_renderer.frame)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.controls, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.render_view, 1, wx.ALL | wx.ALIGN_CENTER | wx.SHAPED, 0)
        self.SetSizer(sizer)

        # refresh render result
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnRefreshTimer, self.timer)

        # handle window close event
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # handle window resize event
        self.resized = False # the dirty flag
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.Centre()
        self.Show(True)

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

            self.OnRefreshRender(event)
            self.Refresh()
            self.resized = False # reset the flag

    def InitRayTracer(self):
        # 80, 40, 20, 10, 8, 4, 2, 1
        scale_down_factor = 4
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

        self.started_render_time = time.perf_counter()
        self.timer.Start(1000)
        self.ray_tracer_renderer.Render(self.scene)

    def OnRefreshTimer(self, event):
        # logging.debug('OnRefreshTimer')
        self.controls.UpdateStats([
            f'render time - {time.perf_counter() - self.started_render_time:0.4f}',
            f'resolution - {self.ray_tracer_width}x{self.ray_tracer_height}'
        ])
        if not self.ray_tracer_renderer.IsRendering():
            self.timer.Stop()

        self.OnRefreshRender(event)

    def OnRefreshRender(self, _event):
        self.render_view.UpdateRender(self.ray_tracer_renderer.frame)

    def OnSave(self, event):
        today = datetime.today()
        default_file_name = f'rt_{int(time.mktime(today.timetuple()))}'
        # wildcard = "JPEG files (*.jpg)|*.jpg|BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png"
        wildcard = "PNG files (*.png)|*.png"

        dialog = wx.FileDialog(self,
            "Save as...",
            defaultFile = default_file_name,
            wildcard = wildcard,
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK: # Save button was pressed
            self.render_view.bitmap.SaveFile(dialog.GetPath(), wx.BITMAP_TYPE_PNG)
            dialog.Destroy()

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
