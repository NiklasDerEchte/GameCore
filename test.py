import pygame.font

from core import *

class TestModule(Engine):

    def start(self):
        print("Module Started")
        sf = self.core.get_engine_by_class(SnowflakeEffect)
        mg = self.core.get_engine_by_class(MagGen)
        gd = self.core.get_engine_by_class(GeoDrawer)
        df = self.core.get_engine_by_class(DebugFps)
        pr = self.core.get_engine_by_class(Projection)

        sf.enable(True)
        mg.enable(True)
        gd.enable(True)
        df.enable(True)
        pr.enable(True)


Core(background_color=(255, 255, 255, 0), fps=30)
