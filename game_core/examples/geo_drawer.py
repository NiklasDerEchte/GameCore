from game_core.src import *
class GeoDrawerPrefab(Engine):

    def awake(self):
        self.priority_layer = 99

    def start(self):
        self.border_color = (20, 20, 20)
        self.graph_root_pos = (round(self.core.window_size[0] / 2), round(self.core.window_size[1] / 2))
        self.zoom = 15
        self.surface = self.core.create_surface()
        self.draw_coord_system(raster_offset=1)
        self.draw_graph_by_function(lambda x: math.e**x)

    def update(self):
        self.core.draw_surface(self.surface)

    def fixed_update(self):
        pass

    def draw_coord_system(self, raster_offset = 20):
        pygame.draw.line(self.surface, self.border_color, (self.graph_root_pos[0], 0), (self.graph_root_pos[0], self.core.window_size[1]))
        pygame.draw.line(self.surface, self.border_color, (0, self.graph_root_pos[1]), (self.core.window_size[0], self.graph_root_pos[1]))

        raster_offset = raster_offset * self.zoom

        long_size = 5
        short_size = 3

        for x_offset in range(self.graph_root_pos[0], self.core.window_size[0], raster_offset):
            if (x_offset % 2) == 0:
                pygame.draw.line(self.surface, self.border_color, (x_offset, self.graph_root_pos[1]-long_size), (x_offset, self.graph_root_pos[1]+long_size))
            else:
                pygame.draw.line(self.surface, self.border_color, (x_offset, self.graph_root_pos[1] - short_size), (x_offset, self.graph_root_pos[1] + short_size))

        for x_offset in range(self.graph_root_pos[0], 0, -raster_offset):
            if (x_offset % 2) == 0:
                pygame.draw.line(self.surface, self.border_color, (x_offset, self.graph_root_pos[1]-long_size), (x_offset, self.graph_root_pos[1]+long_size))
            else:
                pygame.draw.line(self.surface, self.border_color, (x_offset, self.graph_root_pos[1] - short_size),(x_offset, self.graph_root_pos[1] + short_size))


        for y_offset in range(self.graph_root_pos[1], self.core.window_size[1], raster_offset):
            if (y_offset % 2) == 0:
                pygame.draw.line(self.surface, self.border_color, (self.graph_root_pos[0] - long_size, y_offset),(self.graph_root_pos[0] + long_size, y_offset))
            else:
                pygame.draw.line(self.surface, self.border_color, (self.graph_root_pos[0] - short_size, y_offset),(self.graph_root_pos[0] + short_size, y_offset))


        for y_offset in range(self.graph_root_pos[1], 0, -raster_offset):
            if (y_offset % 2) == 0:
                pygame.draw.line(self.surface, self.border_color, (self.graph_root_pos[0] - long_size, y_offset),(self.graph_root_pos[0] + long_size, y_offset))
            else:
                pygame.draw.line(self.surface, self.border_color, (self.graph_root_pos[0]-short_size, y_offset), (self.graph_root_pos[0]+short_size, y_offset))

    def draw_graph_by_function(self, f, segment_length = 1):
        last_point = None
        for screen_x in range(0, self.core.window_size[0], segment_length):
            coord_x = (screen_x - self.graph_root_pos[0]) / self.zoom
            try:
                coord_y = f(coord_x)
            except:
                continue
            screen_y = self.graph_root_pos[1] - (coord_y * self.zoom)
            if last_point != None:
                pygame.draw.line(self.surface, self.border_color, (last_point), (screen_x, screen_y))
            last_point = (screen_x, screen_y)
