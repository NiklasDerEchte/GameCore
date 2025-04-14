from game_core.src import *

class Field:
    def __init__(self, grid_position, size, margin, is_wall=False):
        self._grid_position = grid_position
        self._size = size
        self._screen_position = (
        self._grid_position[0] * (self._size[0] + margin), self._grid_position[1] * (self._size[1] + margin))
        self._color = (52, 73, 235)
        self._wall_color = (56, 56, 56)
        self._margin = margin

        self._is_wall = is_wall

    def set_color(self, color):
        self._color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self._color if not self._is_wall else self._wall_color, (
        self._screen_position[0] + self._margin, self._screen_position[1] + self._margin, self._size[0], self._size[1]))

    def get_grid_position(self):
        return self._grid_position

    def __eq__(self, other):
        return self._grid_position == other._grid_position

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Grid_Position=[X:{}|Y:{}] Screen_Position=[X:{}|Y:{}] Size=[X:{}|Y:{}]".format(
            self._grid_position[0], self._grid_position[1],
            self._screen_position[0] + self._margin, self._screen_position[1] + self._margin,
            self._size[0],
            self._size[1]
        )
    
class GridNavigationPrefab(Engine):

    def awake(self, grid_size=(300, 300), cell_size=(20, 20), margin=5, priority_layer=-1, field_class=Field):
        self.priority_layer = priority_layer
        self._grid_size = grid_size
        self._cell_size = cell_size
        self._margin = margin
        self._current_path = None
        self._field_class = field_class

    def start(self):
        print("Grid example started...")
        self._cell_amount = (
            int(self._grid_size[0] / (self._cell_size[0] + self._margin)),
            int(self._grid_size[1] / (self._cell_size[1] + self._margin))
        )
        self._colors = {
            "wall": (56, 56, 56),
            "player": (145, 71, 255),
            "field": (52, 73, 235),
            "path": (255, 0, 0)
        }
        self._fields = [[self._field_class((x, y), self._cell_size, self._margin) for x in range(self._cell_amount[0])] for y in range(self._cell_amount[1])]
        self._player = self._field_class(
            (random.randint(0, self._cell_amount[0]), random.randint(0, self._cell_amount[1])),
            (self._cell_size[0], self._cell_size[1]),
            self._margin
        )
        self._player.set_color(self._colors["player"])
        self.surface = self.core.create_layer_surface()
        self._nav_grid = Grid(self._cell_amount)

    def xy_cell_amount(self):
        return self._cell_amount

    def update(self):
        for event in self.core.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid_position = self.window_to_grid(event.pos)
                if event.button == 1:
                    self.clear_path()
                    player_node = self._nav_grid.get_node(self._player.get_grid_position())
                    destination_node = self._nav_grid.get_node(grid_position)
                    self._current_path = self._nav_grid.get_path(player_node, destination_node)
                    if self._current_path is not None:
                        for path_node in self._current_path.get_path():
                            self.get_field(path_node.get_position()).set_color(self._colors["path"])
                elif event.button == 3:
                    self.clear_path()
                    self._nav_grid.get_node(grid_position).set_accessibility(False) # set as "wall"
                    self.get_field(self.window_to_grid(event.pos)).set_color(self._colors["wall"])
                    
        self.draw(self.surface)

    def clear_path(self):
        if self._current_path is not None:
            self._current_path = None
            for field_row in self._fields:
                for field in field_row:
                    if self._nav_grid.get_node(field.get_grid_position()).is_accessible():
                        field.set_color(self._colors["field"])
                    else:
                        field.set_color(self._colors["wall"])

    def window_to_grid(self, window_position):
        return (
            int(window_position[0] / (self._cell_size[0] + self._margin)),
            int(window_position[1] / (self._cell_size[1] + self._margin))
        )

    def get_field(self, grid_position):
        if grid_position[0] < 0 or grid_position[1] < 0 or grid_position[0] > self._grid_size[0] or grid_position[1] > self._grid_size[1]:
            return None
        try:
            return self._fields[grid_position[1]][grid_position[0]]
        except IndexError:
            return None

    def draw(self, surface):
        for field_row in self._fields:
            for field in field_row:
                field.draw(surface)
        self._player.draw(surface)