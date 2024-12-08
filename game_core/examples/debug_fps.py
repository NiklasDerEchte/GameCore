from game_core.core import *

class DebugFps(Engine, Prefab):

    def awake(self):
        self.priority_layer = 1000

    def start(self):
        self.font = pygame.font.SysFont('Arial Black', 24)
        self.text_surface = None
        self.surface = self.core.create_layer_surface(render_layer=self.priority_layer)

    def fixed_update(self):
        self.text_surface = self.font.render("FPS: {}".format(round(self.core.fps)), False, (0, 0, 0), (200, 200, 200))

    def update(self):
        self.core.draw_surface(self.surface)
        if self.text_surface != None:
            self.surface.blit(self.text_surface, (10, 6))

