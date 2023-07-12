import sys
import random
import math
import time
import pygame
from perlin_noise import PerlinNoise
from pygame.locals import QUIT
import inspect
import numpy as np
import pytmx

class Coroutine:
    """ main Coroutine logic """
    def __init__(self, func, interval=None, loop_condition=lambda: True, call_delay=None, func_args=None, func_kwargs=None):
        self.is_dead = False
        self._func_args = func_args
        self._func_kwargs = func_kwargs
        self._func = func
        self._interval = interval
        if not callable(loop_condition):
            raise TypeError("loop_condition parameter must be a function")
        self._condition = loop_condition
        self._countdown = call_delay if call_delay != None else 0

    def _tick(self, dt):
        if self._condition() and not self.is_dead:
            self._countdown = self._countdown - dt
            if self._countdown <= 0:
                ret = None
                if self._func_args is not None or self._func_kwargs is not None:
                    if self._func_args is not None and self._func_kwargs is not None:
                        ret = self._func(*self._func_args, **self._func_kwargs)
                    elif self._func_args is not None and self._func_kwargs is None:
                        ret = self._func(*self._func_args)
                    elif self._func_args is None and self._func_kwargs is not None:
                        ret = self._func(**self._func_kwargs)
                else:
                    ret = self._func()
                if ret != None and isinstance(ret, dict):
                    if 'interval' in ret:
                        self._interval = ret['interval']
                    if 'func_args' in ret:
                        self._func_args = ret['func_args']
                    if 'func_kwargs' in ret:
                        self._func_kwargs = ret['func_kwargs']

                if self._interval == None:
                    self.is_dead = True
                else:
                    self._countdown = self._interval
        else:
            self.is_dead = True

class Engine:
    def __init__(self, core):
        # public properties
        self.core = core
        self.is_enabled = True
        self.priority_layer = 0

        # jobs
        self.coroutines = []
        self.state_machines = []

        # private intern properties
        self._is_started = False

    def _check_dead_jobs(self):
        if len(self.coroutines) > 0:
            for c in self.coroutines:
                if c.is_dead:
                    self.coroutines.remove(c)


    def _update_jobs(self):
        if len(self.coroutines) > 0:
            for c in self.coroutines:
                c._tick(self.core.delta_time)

        if len(self.state_machines) > 0:
            for sm in self.state_machines:
                sm._tick()

    def enable(self, value, **kwargs):
        data = None
        if len(kwargs.items()) > 0:
            data = kwargs
        if value and not self.is_enabled:
            if 'args' in inspect.getargspec(self.on_enable).args:
                self.on_enable(args=data)
            else:
                self.on_enable()
            if not self._is_started:
                self.start()
                self._is_started = True

        self.is_enabled = value

    def start_func_as_coroutine(self, func, **kwargs):
        if not callable(func):
            raise TypeError("coroutine parameter must be a function")
        c = Coroutine(func, **kwargs)
        self.coroutines.append(c)

    def start_coroutine(self, coroutine):
        if not isinstance(coroutine, Coroutine):
            raise TypeError("coroutine parameter must be a Coroutine instance")
        self.coroutines.append(coroutine)


    def awake(self):
        """is called once at the beginning to set properties"""
        pass

    def on_enable(self, args=None):
        """is always called when the engine has been enabled"""
        pass

    def start(self):
        """is called once at the beginning or after first enable"""
        pass

    def update(self):
        """is constantly called"""
        pass

    def fixed_update(self):
        """is called in a certain tick rate"""
        pass


class Prefab:
    """parent class for Engine classes, to avoid insta load on start"""
    pass

class Core:
    def __init__(self, title='GameCore', size=(480, 480), update=None, start=None, fixed_update=None, background_color=(0,0,0,0), fps=30, headless=False):
        # private properties
        self._update_func = update
        self._start_func = start
        self._fixed_update_func = fixed_update
        self._fixed_update_interval_counter = 0
        self._engines = []
        self._is_headless = headless

        # config able properties
        self.window_size = size
        self.background_color = background_color
        self.is_running = True
        self.fixed_update_interval = 1000/100 # every 100ms = 0.1s
        self.locked_fps = fps

        # init main vars and loop
        self.delta_time = 1
        self.elapsed_delta_time = 0
        self.elapsed_time_seconds = 0
        self.fps = 0
        self.events = []
        pygame.init()
        pygame.display.set_caption(title)
        pygame.font.init()
        self.clock = pygame.time.Clock()
        if not self._is_headless:
            self.window = pygame.display.set_mode(self.window_size)
        self.__load_engines()
        self.__game_loop()

    def __load_engines(self):
        for engine_class in Engine.__subclasses__():
            if not Prefab in engine_class.__bases__:
                e = engine_class(self)  # init new engine class
                self._engines.append(e)


    def __key_listener(self):
         self.events = pygame.event.get()
         for key in self.events:
            if key.type == pygame.QUIT:
                self.is_running = False

    def __time_calculation(self):
        self.delta_time = self.clock.tick(self.locked_fps)
        self.elapsed_delta_time = self.elapsed_delta_time + self.delta_time
        self.elapsed_time_seconds = self.elapsed_delta_time / 1000 # ms to s
        self._fixed_update_interval_counter = self._fixed_update_interval_counter + self.delta_time

    def __call_awake_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                 engine.awake()

    def __call_start_func(self):
        if self._start_func != None:
            self._start_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled and not engine._is_started:
                    engine.start()
                    engine._is_started = True

    def __call_update_func(self):
        if self._update_func != None:
            self._update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.update()
                    engine._check_dead_jobs()
                    engine._update_jobs()

    def __call_fixed_update_func(self):
        if self._fixed_update_func != None:
            self._fixed_update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.fixed_update()

    def __game_loop(self):
        self.__call_awake_func()
        self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
        self.__call_start_func()
        while self.is_running:
            if not self._is_headless:
                self.window.fill(self.background_color)
            self.__key_listener()
            self.__call_update_func()
            if self._fixed_update_interval_counter >= self.fixed_update_interval:
                self._fixed_update_interval_counter = self._fixed_update_interval_counter - self.fixed_update_interval #add rest of interval_counter back
                self.__call_fixed_update_func()
            self.fps = round(self.clock.get_fps(), 2)
            if not self._is_headless:
                pygame.display.update()
                pygame.display.flip()
            self.__time_calculation()
        pygame.quit()
        sys.exit()

    def create_surface(self):
        """
        create a fullscreen surface
        :return Surface:
        """
        img = pygame.surface.Surface((self.window_size[0], self.window_size[1]), pygame.SRCALPHA, 32)
        if self._is_headless:
            return img
        return img.convert_alpha()

    def draw_surface(self, surface):
        """
        draw surface on (0,0) point (perfect for fullscreen)
        :param surface:
        :return:
        """
        if not self._is_headless:
            self.window.blit(surface, (0, 0))

    def get_engine_by_class(self, searchClass):
        """
        find one engine by class type
        :param searchClass:
        :return engine or null:
        """
        if inspect.isclass(searchClass):
            for engine in self._engines:
                if engine.__class__.__name__ == searchClass.__name__:
                    return engine
        else:
            raise Exception("value must be a class")
        return None

    def get_engines_by_class(self, searchClass):
        """
        get all engines from class type
        :param searchClass:
        :return list or empty list:
        """
        engine_list = []
        if inspect.isclass(searchClass):
            for engine in self._engines:
                if engine.__class__.__name__ == searchClass.__name__:
                    engine_list.append(engine)
        else:
            raise Exception("value must be a class")
        return engine_list

    def instantiate(self, engine):
        """
        create engine while runtime
        :param engine:
        :return engine clone:
        """
        if issubclass(engine, Engine):
            e = engine(self)
            e.awake()
            if e.is_enabled:
                e.start()
                e._is_started = True

            self._engines.append(e)
            self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
            return e
        return None


    def destroy(self, engine):
        if isinstance(engine, Engine):
            for e in self._engines:
                if id(e) == id(engine):
                    self._engines.remove(e)
                    del e

