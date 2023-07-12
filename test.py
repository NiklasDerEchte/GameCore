from core import *

class TestModule(Engine):
    def start(self):
        print("Module Started")
        # self.core.instantiate(SnowflakeEffect)
        # self.core.instantiate(MagGen)
        # self.core.instantiate(GeoDrawer)
        # self.core.instantiate(DebugFps)
        # self.core.instantiate(Projection)
        # self.core.instantiate(AiTownSpawner)
        # self.core.instantiate(ButtonExample)
        # self.core.instantiate(AiSimulationSpawner)
        # self.core.instantiate(Spaceship)


Core(background_color=(255, 255, 255, 0), fps=30)