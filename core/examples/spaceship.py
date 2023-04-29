from core.core import *
from core.tilemap import *
from core.shader import *
import os
class Spaceship(Engine):
    def awake(self):
        self.is_enabled = False
        self.priority_layer = 20

    def start(self):
        self.tile_map_drawer = self.core.get_engine_by_class(TileMapDrawer)
        self.tile_map_drawer.enable(True, tile_map_path=os.getcwd() + "/core/assets/space.tmx")
        self.line_effect = self.core.get_engine_by_class(Lines)
        self.line_effect.enable(True, width=self.tile_map_drawer.get_size()[0], height=self.tile_map_drawer.get_size()[1])
        self.camera = self.tile_map_drawer.get_camera()
        self.pos = (self.core.window_size[0]/2 + 50, self.core.window_size[1]/2)
        self.spaceship_image = pygame.image.load(os.getcwd() + "/core/assets/sprites/Spaceship/sprite_0.png")

    def update(self):
        self.handle_movement(speed=2)
        spaceship_center = (self.pos[0] - self.spaceship_image.get_width() / 2, self.pos[1] - self.spaceship_image.get_height() / 2)
        self.camera.look_at(self.pos)
        self.core.window.blit(self.spaceship_image, self.camera.apply_tuple(spaceship_center))
        self.line_effect.set_origin(self.camera.apply_tuple((0,0)))

    # handle movement of player
    def handle_movement(self, speed=1):
        move_direction = (0, 0)
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_a]:
            move_direction = (move_direction[0] - 1, move_direction[1])
        if keys[pygame.K_d]:
            move_direction = (move_direction[0] + 1, move_direction[1])

        # vertical movement
        if keys[pygame.K_w]:
            move_direction = (move_direction[0], move_direction[1] - 1)
        if keys[pygame.K_s]:
            move_direction = (move_direction[0], move_direction[1] + 1)

        if move_direction[0] == 0 and move_direction[1] == 0:
            return

        # normalize direction
        distance = math.sqrt(move_direction[0]**2+move_direction[1]**2)
        move_direction = (move_direction[0] / distance, move_direction[1] / distance)

        # apply direction
        self.pos = (
            round(self.pos[0] + (move_direction[0] * speed) * self.core.delta_time/10), # add new direction with speed to position, consider the different clock speeds of the cpu with deltaTime. fix a little jiggle with round
            round(self.pos[1] + (move_direction[1] * speed) * self.core.delta_time/10)
        )

        # check borders
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])

        if self.pos[0] > self.tile_map_drawer.get_size()[0]:
            self.pos = (self.tile_map_drawer.get_size()[0], self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)

        if self.pos[1] > self.tile_map_drawer.get_size()[1]:
            self.pos = (self.pos[0], self.tile_map_drawer.get_size()[1])

