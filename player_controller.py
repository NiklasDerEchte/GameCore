from game_core import *

# TODO - unfertig
#      - Eine alternative zum PlatformerCharacterControllerPrefab aus der src/character_controller.py

class TopDownCharacterControllerPrefab(Engine):
    def start(self):
        self.pos = (self.core.window_size[0] / 2, self.core.window_size[1] / 2)

    def update(self):
        self.handle_movement(speed=2)

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
        distance = math.sqrt(move_direction[0] ** 2 + move_direction[1] ** 2)
        move_direction = (move_direction[0] / distance, move_direction[1] / distance)

        # apply direction
        self.pos = (
            round(self.pos[0] + (move_direction[0] * speed) * self.core.delta_time / 10),  # move along x-axis
            round(self.pos[1] + (move_direction[1] * speed) * self.core.delta_time / 10)  # move along y-axis
        )

        # check borders to prevent the spaceship from moving out of bounds
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])

        if self.pos[0] > self.tile_map_drawer.get_size()[0]:
            self.pos = (self.tile_map_drawer.get_size()[0], self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)

        if self.pos[1] > self.tile_map_drawer.get_size()[1]:
            self.pos = (self.pos[0], self.tile_map_drawer.get_size()[1])
