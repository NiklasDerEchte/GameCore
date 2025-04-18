from game_core import *

@scene("preview")
class PreviewModule(Engine):
    def start(self):
        print("PreviewModule started")
        # self.core.instantiate(SnowflakeEffectPrefab)
        # self.core.instantiate(MagGenPrefab)
        # self.core.instantiate(GeoDrawerPrefab)
        # self.core.instantiate(DebugFpsPrefab)
        # self.core.instantiate(ProjectionPrefab)
        # self.core.instantiate(AiTownSpawnerPrefab)
        # self.core.instantiate(AiSimulationSpawnerPrefab)
        # self.core.instantiate(SpaceshipPrefab)
        # self.core.instantiate(GridViewPrefab, grid_size=self.core.window_size)
        # self.core.instantiate(GridNavigationPrefab, grid_size=self.core.window_size)
        # self.core.instantiate(ScreenBlinkPrefab)
        # self.core.instantiate(DrawSystemPrefab)
        # self.core.instantiate(DrawSystemImagePrefab)
        # self.core.instantiate(DrawSystemAnimationImagePrefab)
        # self.core.instantiate(DrawSystemAnimationImageSlicedPrefab)
        # self.core.instantiate(DrawSystemAnimationImageSlicedWithPaddingsPrefab)
        # self.core.instantiate(DrawSystemDirectoryAnimationImageSlicedPrefab)
        # self.core.instantiate(PowderSimulationPrefab, width=self.core.window_size[0], height=self.core.window_size[1])
        # self.core.instantiate(PlatformCharacterPrefab)

Core(
    background_color=(255, 255, 255, 0), 
    fps=60
)