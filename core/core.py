import sys
import random
import pygame
import inspect
import string

class Coroutine:
    """
    Represents a coroutine that periodically executes a function.

    :var is_dead: Indicates whether the coroutine is inactive.
    :type is_dead: bool
    """
    def __init__(self, func, interval=None, loop_condition=lambda: True, call_delay=None, func_args=None, func_kwargs=None):
        """
         Initializes the Coroutine.

        :param func: The function to execute periodically. The function can update the 'interval', 'func_args', and 'func_kwargs' by returning them in a dictionary.
        :type func: callable
        :param interval: The time interval (in seconds) between executions.
        :type interval: float
        :param loop_condition: A function returning a boolean that determines if the coroutine should continue.
        :type loop_condition: callable
        :param call_delay: Initial delay before the first execution.
        :type call_delay: float
        :param func_args: Positional arguments to pass to `func`.
        :type func_args: tuple
        :param func_kwargs: Keyword arguments to pass to `func`.
        :type func_kwargs: dict
        """
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
    """
     Represents a game engine responsible for managing coroutines and state machines.

     :var core: Reference to the Core instance managing the game loop.
     :type core: Core
     :var is_enabled: Indicates whether the engine is active.
     :type is_enabled: bool
     :var priority_layer: Determines the order of engine execution.
     :type priority_layer: int
     :var state_machines: List of state machines managed by the engine.
     :type state_machines: list
     """
    def __init__(self, core):
        """
        Initializes the Engine.

        :param core: The Core instance managing the game loop.
        :type core: Core
        """
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
        """
        Enables the engine and triggers related events.

        :param kwargs: Additional data passed to the `on_enable` method.
        :type kwargs: dict
        """
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
        """
        Disables the engine and triggers related events.
        """
        self.on_disable()
        self.is_enabled = False


    def start_func_as_coroutine(self, func, **kwargs):
        """
        Starts a function as a coroutine.

        :param func: The function to execute as a coroutine.
        :type func: callable
        :param kwargs: Arguments for the coroutine, including interval, call_delay, and all other parameters of the Coroutine class.
        :type kwargs: dict
        """
        if not callable(func):
            raise TypeError("coroutine parameter must be a function")
        c = Coroutine(func, **kwargs)
        self.coroutines.append(c)

    def start_coroutine(self, coroutine):
        """
        Adds a Coroutine instance to the list of active coroutines.

        :param coroutine: The Coroutine instance to start.
        :type coroutine: Coroutine
        """
        if not isinstance(coroutine, Coroutine):
            raise TypeError("coroutine parameter must be a Coroutine instance")
        self.coroutines.append(coroutine)

    def start_coroutines(self, coroutines):
        """
        Adds multiple Coroutine instances to the list of active coroutines.

        :param coroutines: List of Coroutine instances to start.
        :type coroutines: list
        """
        for coroutine in coroutines:
            self.start_coroutine(coroutine)

    def awake(self, **kwargs):
        """
        Called once at the beginning of the engine's lifecycle for initialization.

        :param kwargs: Optional arguments for initialization.
        :type kwargs: dict
        """
        pass

    def on_enable(self, inject=None):
        """
        Called when the engine is enabled.

        :param inject: Optional data to inject during enabling.
        :type inject: dict
        """
        pass

    def on_disable(self):
        """
        Called when the engine is disabled.
        """
        pass

    def start(self):
        """
        Called when the engine starts.
        """
        pass

    def update(self):
        """
        Called continuously during the game loop.
        """
        pass

    def fixed_update(self):
        """
        Called at fixed intervals during the game loop.
        """
        pass

    def on_destroy(self):
        """
        Called before the engine is destroyed.
        """
        pass


class Prefab:
    """
    Base class for engine-related components, preventing immediate execution.
    """
    pass

class SurfaceStackElement:
    """
    Represents an individual element in a stack of rendering surfaces.

    :var name: Name identifier for the surface.
    :type name: str
    :var surface: The surface object to render.
    :type surface: pygame.Surface
    :var render_layer: The rendering order for the surface.
    :type render_layer: int
    :var surface_render_position: Position of the surface in the window.
    :type surface_render_position: tuple
    :var auto_fill: Indicates if the surface should auto-fill after rendering.
    :type auto_fill: bool
    """
    def __init__(self):
        """
        Initializes a SurfaceStackElement.
        """
        self.name = None
        self.surface = None
        self.render_layer = 0
        self.surface_render_position = (0, 0)
        self.auto_fill = False

    def print(self):
        """
        Prints information about the surface element.
        """
        print("Surface {} with layer: {}".format(self.name, self.render_layer))

class SurfaceStack:
    """
    Manages a stack of rendering surfaces for organized layer-based rendering.
    """
    def __init__(self):
        """
        Initializes a SurfaceStack.
        """
        self._stack = []

    def add_element(self, name, surface, render_layer: int, surface_render_position: tuple, fill_after_draw=True):
        """
        Adds a new surface element to the stack.

        :param name: Unique name for the surface.
        :type name: str
        :param surface: The surface to add.
        :type surface: pygame.Surface
        :param render_layer: The rendering order.
        :type render_layer: int
        :param surface_render_position: Position of the surface in the window.
        :type surface_render_position: tuple
        :param fill_after_draw: Indicates if the surface should auto-fill after rendering.
        :type fill_after_draw: bool
        """
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
        """
        Removes a surface element from the stack.

        :param name: Name of the surface to remove.
        :type name: str
        """
        for element in self._stack:
            if element.name == name:
                self._stack.remove(element)
                break

    def get_surface(self, name):
        """
        Retrieves a surface by name.

        :param name: Name of the surface.
        :type name: str

        :returns: The requested surface.
        :rtype: pygame.Surface
        """
        return self.get_element(name).surface

    def get_element(self, name):
        """
        Retrieves a SurfaceStackElement by name.

        :param name: Name of the element.
        :type name: str

        :returns: The requested element.
        :rtype: SurfaceStackElement:
        """
        for element in self._stack:
            if element.name == name:
                return element

    def draw(self, core):
        """
        Draws all surfaces in the stack.

        :param core: Reference to the Core instance for rendering.
        :type core: Core
        """
        counter = 0
        for element in self._stack:
            # print("Draw {} at {} by {}/{}]".format(element.name, element.surface_render_position, counter, len(self.stack)-1))
            core.window.blit(element.surface, element.surface_render_position)
            if element.auto_fill:
                element.surface.fill(core.background_color)
            counter = counter + 1

    def print(self):
        """
        Prints information about all surfaces in the stack.
        """
        for element in self._stack:
            element.print()

class Core:
    """
    Main game framework for managing the game loop, rendering, and engines.

    :var window_size: (X,Y) Dimensions of the game window.
    :type window_size: tuple
    :var background_color: Background color of the game window.
    :type background_color: tuple
    :var is_running: Indicates if the game is running.
    :type is_running: bool
    :var locked_fps: Target frames per second for the game loop.
    :type locked_fps: int
    """

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
            title='GameCore <3',
            size=(480, 480),
            update=None,
            start=None,
            fixed_update=None,
            background_color=(0,0,0,0),
            fps=30,
            display=0,
            window_flags=pygame.DOUBLEBUF,
            window_depth=32):

        """
        Initializes the Core framework.

        :param title: Title of the game window.
        :type title: str
        :param size: Dimensions of the game window.
        :type size: tuple
        :param update: Update function for the game loop.
        :type update: callable
        :param start: Start function executed at the beginning.
        :type start: callable
        :param fixed_update: Function executed at fixed intervals.
        :type fixed_update: callable
        :param background_color: Background color of the window.
        :type background_color: tuple
        :param fps: Target frames per second.
        :type fps: int
        :param display: Display index for the game window.
        :type display: int
        :param window_flags: Pygame flags for the window.
        :type window_flags: int
        :param window_depth: Bit depth for the window.
        :type window_depth: int
        """

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
        """
        Retrieves the surface associated with a specific layer by its name.

        :param name: The name of the layer whose surface is to be retrieved.
        :type name: str
        :return: The surface object of the specified layer.
        :rtype: pygame.Surface
        """
        return self._surface_stack.get_surface(name)

    def remove_layer_surface(self, name):
        """
        Removes a layer and its associated surface by name.

        :param name: The name of the layer to remove.
        :type name: str
        """
        self._surface_stack.remove_element(name)

    def move_layer_surface(self, name, position):
        """
        Updates the position of an existing layer's surface.

        :param name: The name of the layer whose surface position is to be updated.
        :type name: str
        :param position: The new top-left position of the surface in (x, y) coordinates.
        :type position: tuple[int, int]
        """
        self._surface_stack.get_element(name).surface_render_position = position

    def create_layer_surface(self, name=None, width=0, height=0, x=0, y=0, render_layer: int = 0, fill_after_draw=True):
        """
        Creates a new rendering layer surface.

        :param name: Name of the surface.
        :type name: str
        :param width: Width of the surface.
        :type width: int
        :param height: Height of the surface.
        :type height: int
        :param x: X-coordinate of the surface.
        :type x: int
        :param y: Y-coordinate of the surface.
        :type y: int
        :param render_layer: Rendering order of the surface.
        :type render_layer: int
        :param fill_after_draw: Auto-fill the surface after drawing.
        :type fill_after_draw: bool

        :returns: The created surface.
        :rtype: pygame.Surface
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
        Creates a new surface with specified dimensions.

        :param size: The size of the surface as a (width, height) tuple.
                     Defaults to the size of the main window if not specified.
        :type size: tuple[int, int], optional
        :return: A new surface object with the specified or default size.
        :rtype: pygame.Surface
        """
        if size is None:
            size = self.window_size
        img = pygame.surface.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        return img.convert_alpha()

    def draw_surface(self, surface, position=None):
        """
        Draws a surface onto the main window at a specified position.

        :param surface: The surface to draw.
        :type surface: pygame.Surface
        :param position: The top-left position where the surface will be drawn,
                         specified as a (x, y) tuple. Defaults to (0, 0).
        :type position: tuple[int, int], optional
        """
        if position is None:
            position = (0, 0)
        self.window.blit(surface, position)

    def get_engine_by_class(self, searchClass):
        """
        Finds and returns the first engine of a specific class type.

        :param searchClass: The class type of the engine to search for.
        :type searchClass: type
        :return: The first engine instance matching the specified class type, or None if no match is found.
        :rtype: Engine or None
        :raises TypeError: If the provided `searchClass` is not a class.
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
        Retrieves all engines of a specific class type.

        :param searchClass: The class type of engines to search for.
        :type searchClass: type
        :return: A list of all engines matching the specified class type.
        :rtype: list[Engine]
        :raises TypeError: If the provided `searchClass` is not a class.
        """
        engine_list = []
        if inspect.isclass(searchClass):
            for engine in self._engines:
                if engine.__class__.__name__ == searchClass.__name__:
                    engine_list.append(engine)
        else:
            raise Exception("value must be a class")
        return engine_list

    def instantiate(self, engine, **kwargs):
        """
        Creates and initializes a new instance of an engine class at runtime.
        This method is particularly suitable for creating **prefabs**, which are reusable templates for engines.

        :param engine: The engine class to instantiate. Must be a subclass of `Engine`.
        :type engine: type
        :param kwargs: Optional parameters to pass to the engine's `awake` method.
        :return: The instantiated and initialized engine instance.
        :rtype: Engine
        :raises TypeError: If the provided `engine` is not a subclass of `Engine`.
        """
        if issubclass(engine, Engine):
            e = engine(self)
            if len(kwargs.items()) > 0:
                e.awake(**kwargs)
            else:
                e.awake()
            if e.is_enabled:
                e.start()
                e._is_started = True

            self._engines.append(e)
            self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
            return e
        return None


    def destroy(self, engine):
        """
        Destroys an engine instance and removes it from the list of active engines.

        :param engine: The engine instance to destroy.
        :type engine: Engine
        :raises TypeError: If the provided `engine` is not an instance of `Engine`.
        """
        if isinstance(engine, Engine):
            for e in self._engines:
                if id(e) == id(engine):
                    e.on_destroy()
                    self._engines.remove(e)
                    del e