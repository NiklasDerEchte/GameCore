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
import string

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

    def enable(self, **kwargs):
        data = None
        if len(kwargs.items()) > 0:
            data = kwargs
        if not self.is_enabled:
            if 'inject' in inspect.getfullargspec(self.on_enable).args:
                self.on_enable(inject=data)
            else:
                self.on_enable()
            if not self._is_started:
                self.start()
                self._is_started = True

        self.is_enabled = True

    def disable(self):
        self.on_disable()
        self.is_enabled = False


    def start_func_as_coroutine(self, func, **kwargs):
        if not callable(func):
            raise TypeError("coroutine parameter must be a function")
        c = Coroutine(func, **kwargs)
        self.coroutines.append(c)

    def start_coroutine(self, coroutine):
        if not isinstance(coroutine, Coroutine):
            raise TypeError("coroutine parameter must be a Coroutine instance")
        self.coroutines.append(coroutine)

    def start_coroutines(self, coroutines):
        for coroutine in coroutines:
            self.start_coroutine(coroutine)

    def awake(self):
        """is called once at the beginning to set properties"""
        pass

    def on_enable(self, inject=None):
        """is always called when the engine has been enabled"""
        pass

    def on_disable(self):
        """is always called when the engine has been disabled"""
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

    def on_destroy(self):
        """called before the engine is destroyed"""
        pass


class Prefab:
    """parent class for Engine classes, to avoid insta load on start"""
    pass

class SurfaceStackElement:
    def __init__(self):
        self.name = None
        self.surface = None
        self.render_layer = 0
        self.surface_render_position = (0, 0)
        self.auto_fill = False

    def print(self):
        print("Surface {} with layer: {}".format(self.name, self.render_layer))

class SurfaceStack:
    def __init__(self):
        self._stack = []

    def add_element(self, name, surface, render_layer: int, surface_render_position: tuple, fill_after_draw=True):
        for element in self._stack:
            if element.name == name:
                s = "surface name \'{}\' already exists".format(name)
                raise ValueError(s)
            if element.render_layer == render_layer:
                render_layer = render_layer + 1

        surface_stack_element = SurfaceStackElement()
        surface_stack_element.name = name
        surface_stack_element.surface = surface
        surface_stack_element.render_layer = render_layer
        surface_stack_element.surface_render_position = surface_render_position
        surface_stack_element.auto_fill = fill_after_draw
        self._stack.append(surface_stack_element)
        self._stack = sorted(self._stack, key=lambda x: x.render_layer, reverse=False)

    def remove_element(self, name):
        for element in self._stack:
            if element.name == name:
                self._stack.remove(element)
                break

    def get_surface(self, name):
        return self.get_element(name).surface

    def get_element(self, name):
        for element in self._stack:
            if element.name == name:
                return element

    def draw(self, core):
        counter = 0
        for element in self._stack:
            # print("Draw {} at {} by {}/{}]".format(element.name, element.surface_render_position, counter, len(self.stack)-1))
            core.window.blit(element.surface, element.surface_render_position)
            if element.auto_fill:
                element.surface.fill(core.background_color)
            counter = counter + 1

    def print(self):
        for element in self._stack:
            element.print()

class Core:

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        if self.window is not None:
            pygame.display.quit()
        self.window = pygame.display.set_mode(value, flags=self._flags, depth=self._depth, display=self._display)
        self._window_size = value

    def __init__(self,
            title='GameCore',
            size=(480, 480),
            update=None,
            start=None,
            fixed_update=None,
            background_color=(0,0,0,0),
            fps=30,
            display=0,
            window_flags=pygame.DOUBLEBUF,
            window_depth=32):

        # private properties
        self._update_func = update
        self._start_func = start
        self._fixed_update_func = fixed_update
        self._fixed_update_interval_counter = 0
        self._engines = []
        self._display = display
        self._flags = window_flags
        self._depth = window_depth
        self._window_size = None
        self._surface_stack = SurfaceStack()

        # config able properties
        self.window = None
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
        self._load_engines()
        self._game_loop()

    def _load_engines(self):
        for engine_class in Engine.__subclasses__():
            if not Prefab in engine_class.__bases__:
                e = engine_class(self)  # init new engine class
                self._engines.append(e)


    def _key_listener(self):
         self.events = pygame.event.get()
         for key in self.events:
            if key.type == pygame.QUIT:
                self.is_running = False

    def _time_calculation(self):
        self.delta_time = self.clock.tick(self.locked_fps)
        self.elapsed_delta_time = self.elapsed_delta_time + self.delta_time
        self.elapsed_time_seconds = self.elapsed_delta_time / 1000 # ms to s
        self._fixed_update_interval_counter = self._fixed_update_interval_counter + self.delta_time

    def _call_awake_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                 engine.awake()

    def _call_start_func(self):
        if self._start_func != None:
            self._start_func(self)
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled and not engine._is_started:
                    engine.start()
                    engine._is_started = True

    def _call_update_func(self):
        if self._update_func != None:
            self._update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.update()
                    engine._check_dead_jobs()
                    engine._update_jobs()

    def _call_fixed_update_func(self):
        if self._fixed_update_func != None:
            self._fixed_update_func()
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.fixed_update()

    def _game_loop(self):
        self._call_awake_func()
        self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
        self._call_start_func()
        while self.is_running:
            self.window.fill(self.background_color)
            self._key_listener()
            self._call_update_func()
            if self._fixed_update_interval_counter >= self.fixed_update_interval:
                self._fixed_update_interval_counter = self._fixed_update_interval_counter - self.fixed_update_interval #add rest of interval_counter back
                self._call_fixed_update_func()
            self._surface_stack.draw(self)
            self.fps = round(self.clock.get_fps(), 2)
            pygame.display.update()
            pygame.display.flip()
            self._time_calculation()
        pygame.quit()
        sys.exit()

    def get_layer_surface(self, name):
        return self._surface_stack.get_surface(name)

    def remove_layer_surface(self, name):
        self._surface_stack.remove_element(name)

    def move_layer_surface(self, name, position):
        """
        move existing layer surface
        """
        self._surface_stack.get_element(name).surface_render_position = position

    def create_layer_surface(self, name=None, width=0, height=0, x=0, y=0, render_layer: int = 0, fill_after_draw=True):
        """
        create auto draw surface with own render position
        :return Surface:
        """
        if width == 0:
            width = self.window_size[0]
        if height == 0:
            height = self.window_size[1]
        if name == None:
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        img = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32)
        self._surface_stack.add_element(name, img.convert_alpha(), render_layer, surface_render_position=(x, y), fill_after_draw=fill_after_draw)

        return self.get_layer_surface(name)

    def create_surface(self, size=None):
        """
        create a surface
        :return Surface:
        """
        if size is None:
            size = self.window_size
        img = pygame.surface.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        return img.convert_alpha()

    def draw_surface(self, surface, position=None):
        """
        manually draw surface
        :param surface: position = topleft
        :return:
        """
        if position is None:
            position = (0, 0)
        self.window.blit(surface, position)

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
                    e.on_destroy()
                    self._engines.remove(e)
                    del e