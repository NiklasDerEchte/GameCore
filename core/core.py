import sys
import random
import math
import time
import pygame
from perlin_noise import PerlinNoise
from pygame.locals import QUIT
import inspect
import numpy as np

class Coroutine:
    def __init__(self, func, interval):
        self._func = func
        self._interval = interval
        self._countdown = 0

    def _tick(self, dt):
        self._countdown = self._countdown - dt
        if self._countdown <= 0:
            self._countdown = self._interval
            self._func()

class Engine:
    is_enabled = True
    core = None
    priority_layer = 0
    coroutines = []

    _is_started = False

    def _update_coroutine(self):
        if len(self.coroutines) > 0:
            for c in self.coroutines:
                c._tick(self.core.delta_time)

    def enable(self, value):
        if value and not self.is_enabled:
            if not self._is_started:
                self.start()
                self._is_started = True
            self.on_enable()

        self.is_enabled = value

    def start(self):
        """is called once at the beginning or after first enable"""
        pass

    def on_enable(self):
        """is always called when the engine has been enabled"""
        pass

    def update(self):
        """is constantly called"""
        pass

    def fixed_update(self):
        """is called in a certain tick rate"""
        pass

class Core:
    def __init__(self, size=(480, 480), update=None, start=None, fixed_update=None, background_color=(0,0,0,0), fps=30):
        # private properties
        self._update_func = update
        self._start_func = start
        self._fixed_update_func = fixed_update
        self._fixed_update_interval_counter = 0
        self._engines = []

        # config able properties
        self.window_size = size
        self.background_color = background_color
        self.is_running = True
        self.delta_time = 1
        self.elapsed_delta_time = 0
        self.elapsed_time_seconds = 0
        self.fixed_update_interval = 1000/100 # every 100ms = 0.1s
        self.locked_fps = fps
        self.fps = 0

        # init main vars and loop
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.window_size)
        self.__load_engines()
        self.__game_loop()

    def __load_engines(self):
        for engine_class in Engine.__subclasses__():
            engine_class.core = self
            e = engine_class() # init new engine class
            self._engines.append(e)
        self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)

    def __key_listener(self):
         events = pygame.event.get()
         for key in events:
            if key.type == pygame.QUIT:
                self.is_running = False

    def __time_calculation(self):
        self.delta_time = self.clock.tick(self.locked_fps)
        self.elapsed_delta_time = self.elapsed_delta_time + self.delta_time
        self.elapsed_time_seconds = self.elapsed_delta_time / 1000 # ms to s
        self._fixed_update_interval_counter = self._fixed_update_interval_counter + self.delta_time

    def __call_start_func(self):
        if self._start_func != None:
            self._start_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.start()
                    engine._is_started = True

    def __call_update_func(self):
        if self._update_func != None:
            self._update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.update()
                    engine._update_coroutine()

    def __call_fixed_update_func(self):
        if self._fixed_update_func != None:
            self._fixed_update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.fixed_update()

    def __game_loop(self):
        self.__call_start_func()
        while self.is_running:
            self.window.fill(self.background_color)
            self.__key_listener()
            self.__call_update_func()
            if self._fixed_update_interval_counter >= self.fixed_update_interval:
                self._fixed_update_interval_counter = self._fixed_update_interval_counter - self.fixed_update_interval #add rest of interval_counter back
                self.__call_fixed_update_func()
            self.fps = round(self.clock.get_fps(), 2)
            pygame.display.update()
            self.__time_calculation()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def create_surface(self):
        img = pygame.surface.Surface((self.window_size[0], self.window_size[1]), pygame.SRCALPHA, 32)
        return img.convert_alpha()

    def draw_surface(self, surface):
        self.window.blit(surface, (0, 0))

    def get_engine_by_class(self, searchClass):
        if inspect.isclass(searchClass):
            for engine in self._engines:
                if engine.__class__.__name__ == searchClass.__name__:
                    return engine
        else:
            raise Exception("value must be a class")
        return None

