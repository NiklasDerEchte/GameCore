from core import *
from bridson import poisson_disc_samples


class Algo(Engine, Prefab):

    def awake(self):
        self.priority_layer = -1

    def start(self):
        self.noise = PerlinNoise()
        self.pixel_size = 3
        self.noise_scale = 15
        self.noise_offset_x = 0
        self.noise_offset_y = 0
        self.noise_map = [[]]
        self.update_noise_map()

        self.voronoi_targets = []
        self.voronoi_targets_colors = {}
        self.voronoi_distance = 10
        self.update_voronoi_targets()

        self.surface = self.core.create_surface()
        self.update_map()

    def update_noise_map(self):
        for x in range(int(self.core.window_size[0] / self.pixel_size)):
            colum = []
            for y in range(int(self.core.window_size[1] / self.pixel_size)):
                colum.append(self.noise([x / self.core.window_size[0] * self.noise_scale + self.noise_offset_x,
                                         y / self.core.window_size[1] * self.noise_scale + self.noise_offset_y]))
            self.noise_map.append(colum)

    def update_voronoi_targets(self):
        self.voronoi_targets.clear()
        temp_targets = poisson_disc_samples(width=self.core.window_size[0], height=self.core.window_size[1], r=50)
        for i in temp_targets:
            self.voronoi_targets.append((int(i[0]), int(i[1])))
        self.voronoi_targets = list(dict.fromkeys(self.voronoi_targets))
        for i in self.voronoi_targets:
            self.voronoi_targets_colors[i] = (
            random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.voronoi_distance = self.voronoi_distance + 1
            self.update_map()
        if keys[pygame.K_s]:
            self.voronoi_distance = self.voronoi_distance - 1
            self.update_map()

    def update(self):
        self.handle_keys()
        if self.voronoi_distance > 255:
            self.voronoi_distance = 255

        if self.voronoi_distance < 0:
            self.voronoi_distance = 0

        self.core.draw_surface(self.surface)

    def fixed_update(self):
        pass

    def update_map(self):
        self.surface.fill(self.core.background_color)
        #for target in self.voronoi_targets:
        #    pygame.draw.rect(self.surface, (157, 189, 164), (target[0], target[1], 3, 3))
        for x in range(int(self.core.window_size[0] / self.pixel_size)):
            for y in range(int(self.core.window_size[1] / self.pixel_size)):
                color = (0, 0, 0)
                next_target, distance = self.getNextTargetWithDistance((x, y))
                color = self.voronoi_targets_colors[next_target]
                alpha = (255 - (distance * self.voronoi_distance)) if (255 - (distance * self.voronoi_distance)) > 0 else 0
                color = (color[0], color[1], color[2], alpha)

                pygame.draw.rect(self.surface, color,
                                 (x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))

        #        if (x == 0 or y == 0 or x == int(self.core.window_size[0] / self.pixel_size) - 1 or y == int(self.core.window_size[1] / self.pixel_size) - 1):
        #            color = (255, 255, 255)
        #        else:
        #            ret = self.noise_map[x][y]
        #            ret = abs(ret)
        #            color = self.get_color(ret)
        #        pygame.draw.rect(self.surface, color, (x * self.pixel_size, y * self.pixel_size, 10, 10))

    def getNextTargetWithDistance(self, position):
        next_target = None
        next_distance = 0
        for target in self.voronoi_targets:
            delta_vec = (target[0] - position[0], target[1] - position[1])
            distance = math.sqrt(((delta_vec[0] * delta_vec[0]) + (delta_vec[1] * delta_vec[1])))
            if next_target is None or distance < next_distance:
                next_distance = distance
                next_target = target
        return next_target, next_distance

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
