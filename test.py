from core import *

class TestModule(Engine):
    def awake(self):
        self.is_enabled = True

    def start(self):
        print("Module Started")
        self.core.get_engine_by_class(SnowflakeEffect).enable(False)
        self.core.get_engine_by_class(MagGen).enable(True)
        self.core.get_engine_by_class(GeoDrawer).enable(False)
        self.core.get_engine_by_class(DebugFps).enable(True)
        self.core.get_engine_by_class(Projection).enable(False)
        self.core.get_engine_by_class(AiTownSpawner).enable(False)
        self.core.get_engine_by_class(AiSimulationSpawner).enable(True)


Core(background_color=(255, 255, 255, 0), fps=30, headless=False)