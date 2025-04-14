import pytmx
from .core.core import *

class TileMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.animated_tiles = []
        self.tiled_object_groups = []

    def render(self, surface):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    p = self.tmxdata.get_tile_properties_by_gid(gid)
                    if p is not None and len(p['frames']) > 0:
                        self.animated_tiles.append({
                            'grid_pos': (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight),
                            'animated_tiles': [frame for frame in p['frames']]
                        })
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                tiled_obj_group = {
                    "layer": layer,
                    "tiled_objs": []
                }
                for tiled_obj in layer:
                    tiled_obj_group["tiled_objs"].append(tiled_obj)
                self.tiled_object_groups.append(tiled_obj_group)

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return (temp_surface, self.animated_tiles)

class Camera:

    def __init__(self, camera_view_rect: pygame.Rect, camera_position=(0,0), camera_size=(0,0)):
        self.rect = pygame.Rect(camera_position[0], camera_position[1], camera_size[0], camera_size[1])
        self.camera_view_rect = camera_view_rect

    def look_at(self, target=(0,0)):
        x = -target[0] + int(self.rect.width / 2)
        y = -target[1] + int(self.rect.height / 2)

        x = min(self.camera_view_rect.x, x)
        y = min(self.camera_view_rect.y, y)

        x = max(-(self.camera_view_rect.width - self.rect.width), x)
        y = max(-(self.camera_view_rect.height - self.rect.height), y)
        self.rect.x, self.rect.y = x, y

    def apply(self, rect):
        return rect.move(self.rect.topleft)

    def apply_coord(self, x, y):
        rect = pygame.Rect(x, y, 0, 0)
        rect = self.apply(rect)
        return (rect.x, rect.y)

    def apply_tuple(self, d):
        rect = pygame.Rect(d[0], d[1], 0, 0)
        rect = self.apply(rect)
        return (rect.x, rect.y)


class TileMapDrawerPrefab(Engine):
    def awake(self):
        self.is_enabled = False
        self.priority_layer = -2
        self.tile_map_path = None
        self._draw_surface = None

    def on_enable(self, inject=None):
        if inject is None:
            return
        if 'tile_map_path' in inject:
            self.tile_map_path = inject['tile_map_path']
        if 'surface' in inject:
            self._draw_surface = inject['surface']
        else:
            self._draw_surface = self.core.window

    def start(self):
        if self.tile_map_path is None:
            s = """ tile_map_path cant be None!

            did u miss?
            .enable(True, tile_map_path='...')"""
            raise ValueError(s)

        self.tile_map = None
        self.camera = None

        self.tile_map = TileMap(self.tile_map_path)
        self.map, self.animated_tiles = self.tile_map.make_map()

        self.camera = Camera(
            camera_position=(0, 0),
            camera_size=self.core.window_size,
            camera_view_rect=pygame.Rect(0, 0, self.map.get_width(), self.map.get_height())
        )

    def update(self):
        if self.tile_map_path is None or self.tile_map is None:
            return

        # calculate animation tiles
        for animated_tile in self.animated_tiles:
            if 'active_animation_index' not in animated_tile: # set first tile if not set
                animated_tile['active_animation_index'] = 0
                animated_tile['active_animation_time_left'] = animated_tile['animated_tiles'][animated_tile['active_animation_index']].duration

                # draw tile
                gid = animated_tile['animated_tiles'][animated_tile['active_animation_index']].gid
                self.map.blit(self.tile_map.tmxdata.get_tile_image_by_gid(gid), animated_tile['grid_pos'])

            else:
                animated_tile['active_animation_time_left'] = animated_tile['active_animation_time_left'] - self.core.delta_time # calculate time of current animated tile
                if animated_tile['active_animation_time_left'] <= 0: # change tile
                    if animated_tile['active_animation_index']+1 >= len(animated_tile['animated_tiles']): # reset to first tile index
                        animated_tile['active_animation_index'] = 0
                        animated_tile['active_animation_time_left'] = animated_tile['animated_tiles'][animated_tile['active_animation_index']].duration
                    else: # choose next index
                        animated_tile['active_animation_index'] = animated_tile['active_animation_index'] + 1
                        animated_tile['active_animation_time_left'] = animated_tile['animated_tiles'][animated_tile['active_animation_index']].duration

                    # draw tile
                    gid = animated_tile['animated_tiles'][animated_tile['active_animation_index']].gid
                    self.map.blit(self.tile_map.tmxdata.get_tile_image_by_gid(gid), animated_tile['grid_pos'])

        self._draw_surface.blit(self.map, self.camera.apply(self.map.get_rect()))

    def get_camera(self):
        return self.camera

    def get_size(self):
        if self.tile_map == None:
            return None
        return (self.tile_map.width, self.tile_map.height)