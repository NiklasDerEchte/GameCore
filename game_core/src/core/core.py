import sys
import random
import pygame
import string

from .engine import Engine
from .surface_stack import SurfaceStack, SurfaceStackElement
from .scene_manager import SceneManager, Scene, scene

class Core:
    """
    Main game framework for managing the game loop, rendering, and engines.

    :var window: main draw surface.
    :type window: pygame.Surface
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
            start_scene=None,
            size=(480, 480),
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
        self._fixed_update_interval_counter = 0
        self._scene_manager = SceneManager()
        self._display = display
        self._flags = window_flags
        self._depth = window_depth
        self._window_size = None
        self._start_scene = start_scene

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
        self.pressed_keys = []
        self.pressed_mouse = []
        self.mouse_position = (0, 0)
        pygame.init()
        pygame.display.set_caption(title)
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self._load_engines()
        self._game_loop()

    def _load_engines(self):
        for engine_class in Engine.__subclasses__():
            e = engine_class(self)  # init new engine class
    
    def get_scene_manager(self):
        """
        Retrieves the SceneManager instance.

        :returns: The SceneManager instance.
        :rtype: SceneManager
        """
        return self._scene_manager
    
    def _key_listener(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.pressed_mouse = pygame.mouse.get_pressed()
        self.pressed_keys = pygame.key.get_pressed()
        self.events = pygame.event.get()
        for key in self.events:
            if key.type == pygame.QUIT:
                self.is_running = False

    def _time_calculation(self):
        self.delta_time = self.clock.tick(self.locked_fps)
        self.elapsed_delta_time = self.elapsed_delta_time + self.delta_time
        self.elapsed_time_seconds = self.elapsed_delta_time / 1000 # ms to s
        self._fixed_update_interval_counter = self._fixed_update_interval_counter + self.delta_time

    def _game_loop(self):
        self.get_scene_manager().set_scene(self._start_scene)
        while self.is_running:
            self.window.fill(self.background_color)
            self._key_listener()
            self.get_scene_manager().scene()._update()
            if self._fixed_update_interval_counter >= self.fixed_update_interval:
                self._fixed_update_interval_counter = self._fixed_update_interval_counter - self.fixed_update_interval #add rest of interval_counter back
                self.get_scene_manager().scene()._fixed_update()
            self._scene_manager.scene().get_surface_stack().draw(self)
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
        return self._scene_manager.scene().get_surface_stack().get_surface(name)

    def remove_layer_surface(self, name):
        """
        Removes a layer and its associated surface by name.

        :param name: The name of the layer to remove.
        :type name: str
        """
        self._scene_manager.scene().get_surface_stack().remove_element(name)

    def move_layer_surface(self, name, position):
        """
        Updates the position of an existing layer's surface.

        :param name: The name of the layer whose surface position is to be updated.
        :type name: str
        :param position: The new top-left position of the surface in (x, y) coordinates.
        :type position: tuple[int, int]
        """
        self._scene_manager.scene().get_surface_stack().get_element(name).surface_render_position = position

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
        self._scene_manager.scene().get_surface_stack().add_element(name, img.convert_alpha(), render_layer, surface_render_position=(x, y), fill_after_draw=fill_after_draw)

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

    def instantiate(self, engine, **kwargs):
        """
        Creates and initializes a new instance of an engine class at runtime.
        This method is particularly suitable for creating **prefabs**, which are reusable templates as engines.

        :param engine: The engine class to instantiate. Must be a subclass of `Engine`.
        :type engine: type
        :param kwargs: Optional parameters to pass to the engine's `awake` method.
        :return: The instantiated and initialized engine instance.
        :rtype: Engine
        :raises TypeError: If the provided `engine` is not a subclass of `Engine`.
        """
        if isinstance(engine, Engine):    
            return self.get_scene_manager().scene().instantiate_engine(engine)
        return None


    def destroy(self, engine):
        """
        Destroys an engine instance and removes it from the list of active engines.

        :param engine: The engine instance to destroy.
        :type engine: Engine
        :raises TypeError: If the provided `engine` is not an instance of `Engine`.
        """
        if isinstance(engine, Engine):
            self.get_scene_manager().scene().destroy_engine(engine)