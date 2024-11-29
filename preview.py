from examples import *
from dimension_projection import *
# TODO: In dieser Version sind die physic.py und die animation.py neu
# TODO: Außerdem wird die Projektion ausgearbetet
# TODO: Es gibt auch neue Algorithmen wie die a_star
class PreviewModule(Engine):
    def start(self):
        print("PreviewModule started")
        # self.core.instantiate(SnowflakeEffect)
        # self.core.instantiate(MagGen)
        # self.core.instantiate(GeoDrawer)
        # self.core.instantiate(DebugFps)
        # self.core.instantiate(Projection)
        # self.core.instantiate(AiTownSpawner)
        # self.core.instantiate(ButtonExample)
        # self.core.instantiate(AiSimulationSpawner)
        # self.core.instantiate(Spaceship)
        # self.core.instantiate(Physics)# TODO <- Fühlt sich noch nicht ganz richtig an
        # self.core.instantiate(Test_Scene) # TODO <- arbeite gerade hier dran (perspective_projection 3D->2D) implement ModernGl
        # self.core.instantiate(Algo) # TODO <- Glaube ist noch was buggy
        # self.core.instantiate(GridView, grid_size=self.core.window_size)  # TODO <- Diese Parameterübergabe muss in die Dokumentation, eventuell auch die *args überneh



Core(background_color=(255, 255, 255, 0), fps=120)
