from core.core import *

class DebugFps(Engine):
    is_enabled = False
    priority_layer = 1000
    def start(self):
        self.font = pygame.font.SysFont('Arial Black', 24)
        self.text_surface = None

    def fixed_update(self):
        self.text_surface = self.font.render("FPS: {}".format(round(self.core.fps)), False, (0, 0, 0), (200, 200, 200))

    def update(self):
        if self.text_surface != None:
            self.core.window.blit(self.text_surface, (10, 6))

