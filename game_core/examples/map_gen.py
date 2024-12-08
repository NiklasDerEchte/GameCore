from perlin_noise import PerlinNoise
from game_core.core import *

class MagGen(Engine, Prefab):

    def awake(self):
        self.priority_layer = -1

    def start(self):
        self.noise = PerlinNoise()
        self.pixel_size = 3
        self.noise_scale = 15
        self.noise_offset_x = 0
        self.noise_offset_y = 0
        self.surface = self.core.create_surface()

        self.noise_map = [[]]
        self.update_noise_map()

        self.coroutines = [
            Coroutine(self.update_map, 3000)
        ]

    def update_noise_map(self):
        for x in range(int(self.core.window_size[0] / self.pixel_size)):
            colum = []
            for y in range(int(self.core.window_size[1] / self.pixel_size)):
                colum.append(self.noise([x / self.core.window_size[0] * self.noise_scale + self.noise_offset_x, y / self.core.window_size[1] * self.noise_scale + self.noise_offset_y]))
            self.noise_map.append(colum)

    def update(self):
        self.core.draw_surface(self.surface)

    def fixed_update(self):
        pass

    def update_map(self):
        self.surface.fill(self.core.background_color)
        for x in range(int(self.core.window_size[0] / self.pixel_size)):
            for y in range(int(self.core.window_size[1] / self.pixel_size)):
                color = (0, 0, 0)

                if (x == 0 or y == 0 or x == int(self.core.window_size[0] / self.pixel_size) - 1 or y == int(self.core.window_size[1] / self.pixel_size) - 1):
                    color = (255, 255, 255)
                else:
                    ret = self.noise_map[x][y]
                    ret = abs(ret)
                    color = self.get_color(ret)

                pygame.draw.rect(self.surface, color, (x * self.pixel_size, y * self.pixel_size, 10, 10))

    def get_color(self, f):
        color = (245, 66, 167)  # NO COLOR
        if f < .04:  # Water
            color = (random.randrange(27, 57), random.randrange(99, 120), random.randrange(171, 184))
        elif f < .07:  # Sand
            color = (219, 215, 99)
            if f < .05:
                color = (153, 151, 83)
        elif f < .3:  # Grass
            color = (random.randrange(5, 25), random.randrange(128, 140), random.randrange(33, 51))
        elif f < .4:  # Stone
            color = (148, 161, 151)
            if f < .32:
                color = (157, 189, 164)
        elif f < .5:  # Snow
            color = (223, 227, 242)
        else:  # Ice
            color = (129, 194, 224)
        return color