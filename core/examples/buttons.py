from core.core import *
from core.ui import *
class ButtonExample(Engine, Prefab):
    def awake(self):
        self.priority_layer = 1000

    def start(self):
        self.surface = self.core.create_surface()

        self.b = Button(position=(self.core.window_size[0]/2, (self.core.window_size[1]/2)+100), anchor=CENTER_ANCHOR, title="Hello World!")
        self.ib = ImageButton(position=(20, 40))

    def update(self):
        # draw buttons
        self.b.draw(self.surface)
        self.ib.draw(self.surface)

        # main draw
        self.core.draw_surface(self.surface)
        self.surface.fill(self.core.background_color)