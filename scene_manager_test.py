from game_core import *

@scene("SampleScene")
class PreviewModule(Engine):
    def start(self):
        print("PreviewModule started")

Core(
    background_color=(255, 255, 255, 0), 
    fps=120,
)
# TODO: Die Scenen scheinen zu funktionieren, könnte man jetzt nicht die prefabs abschaffen weil Engines ohne Scene nicht mehr automatisch gesartet werden?