import random

import pygame.draw

from core.core import *

class Fog(Engine, Prefab):
    def awake(self):
        self.priority_layer = 80
        self.is_enabled = False

    def start(self, color=(230, 230, 230, 250)):
        self.surface = self.core.create_surface()
        self.surface.fill(color)

    def update(self):
        self.core.draw_surface(self.surface)

    def erase(self, position, size):
        pygame.draw.circle(self.surface, (255, 255, 255, 0), position, size)


class Lines(Engine, Prefab):
    def awake(self):
        self.priority_layer = 10
        self.is_enabled = False

        self.width = self.core.window_size[0]
        self.height = self.core.window_size[1]

    def on_enable(self, args=None):
        if args != None:
            if 'width' in args:
                self.width = args['width']
            if 'height' in args:
                self.height = args['height']

    def start(self):
        self.stripes = []
        self.surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.origin = (0,0)
        self.coroutines = [
            Coroutine(func=self.create_stripe_coroutine)
        ]

    def update(self):
        self.update_stripe()
        self.draw()
        self.core.window.blit(self.surface, self.origin)
        self.surface.fill(self.core.background_color)

    def draw(self):
        for stripe in self.stripes:
            if stripe['length'] > 0:
                if 'last_positions' in stripe:
                    stripe['last_positions'].append(stripe['position'])
                    if len(stripe['last_positions']) > stripe['length']: # remove positions
                        stripe['last_positions'].remove(stripe['last_positions'][0])

                    # draw tail
                    pygame.draw.lines(self.surface, (255, 255, 255), False, stripe['last_positions'], stripe['size'])
                else:
                    stripe['last_positions'] = []
                    stripe['last_positions'].append(stripe['position'])
            pygame.draw.circle(self.surface, (255, 255, 255), stripe['position'], math.ceil(stripe['size']/2))

    def update_stripe(self):
        for stripe in self.stripes:
            stripe_x = stripe['position'][0]
            stripe_y = stripe['position'][1]

            # handle next movement step
            stripe_x += stripe['speed'] * stripe['direction']
            stripe_y -= stripe['func'](stripe['speed']) # "add" delta to xn+1

            stripe['position'] = (stripe_x, stripe_y)

            # handle lifetime
            stripe['lifetime'] = stripe['lifetime'] - self.core.delta_time
            if stripe['lifetime'] <= 0 or stripe_x < 0 or stripe_y < 0:
                self.stripes.remove(stripe)

    def create_stripe_coroutine(self):
        m = random.randint(-2, 2)
        if m == 0:
            m = 1
        else:
            m = 1 / m

        stripe_config = {
            'position': (random.randint(0, self.width), random.randint(0, self.height)),
            'size': random.randint(1, 2),
            'length': random.randint(4, 10),
            'speed': random.randint(1, 6),
            'lifetime': random.randint(3000, 12000),
            'direction': [+1, -1][random.randint(0, 1)],
            'func': lambda x:  x * m
        }
        self.stripes.append(stripe_config)
        return {'interval': random.randint(2000, 5000)}


    def set_origin(self, position):
        self.origin = position