from core.core import *
from core.math import *

class NavAgent:
    def __init__(self, position, speed=1):
        self.position = position
        self.speed = speed
        self.distance = 0

    def move(self, destination):
        delta_vec = (destination[0] - self.position[0], destination[1] - self.position[1])
        self.distance = math.sqrt((delta_vec[0] ** 2) + (delta_vec[1] ** 2))
        if self.distance > 0:
            new_pos_x = self.position[0] + (min(self.speed, round(self.distance)) * delta_vec[0] / self.distance)
            new_pos_y = self.position[1] + (min(self.speed, round(self.distance)) * delta_vec[1] / self.distance)
            self.position = (new_pos_x, new_pos_y)


class SimpleSpriteAnimator:
    def __init__(self, anim_sprites: dict, start_state: str, anim_state_decision: callable, sprite_size: tuple, fps=None):
        ground_surface = pygame.surface.Surface(sprite_size, pygame.SRCALPHA, 32)
        self._surface = ground_surface.convert_alpha()
        self._animation_sprites = anim_sprites
        self._active_sprite_index = 0
        self._active_animation_state = start_state
        self._cb_anim_state_decision = anim_state_decision
        self._fps = fps
        self._ft = 60/self._fps
        self._fwaiter = 0

    def get_size(self):
        return self._surface.get_size()
    def animate(self, delta_time=None):
        if delta_time is not None:
            self._fwaiter = self._fwaiter - delta_time
            if self._fwaiter <= 0:
                self._fwaiter = self._ft
            else:
                return self._surface
        self._surface.fill((0, 0, 0, 0))
        anim_state = self._cb_anim_state_decision()
        if anim_state not in self._animation_sprites:
            print("animation state '{}' not found".format(anim_state))
            return self._surface
        if anim_state != self._active_animation_state:
            self._active_sprite_index = 0
            self._active_animation_state = anim_state

        active_sprite = self._animation_sprites[self._active_animation_state][self._active_sprite_index]

        if type(active_sprite) is list:
            for sprite in active_sprite:
                self._surface.blit(pygame.transform.scale(sprite, self.get_size()), (0, 0))
        else:
            self._surface.blit(pygame.transform.scale(active_sprite, self.get_size()), (0, 0))

        self._active_sprite_index = self._active_sprite_index + 1
        if self._active_sprite_index >= len(self._animation_sprites[self._active_animation_state]):
            self._active_sprite_index = 0

        return self._surface