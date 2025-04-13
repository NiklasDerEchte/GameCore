from .engine import Engine
import inspect

def scene(name):
    """
    Decorator to register a engine to scene class with a name.
    """
    def decorator(cls):
        original_init = cls.__init__

        def _init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            core = args[0]
            core.get_scene_manager().setup_engine(name, self)
            print(f"[Scene-Init] Szene '{name}' wurde initialisiert für Instanz: {self}")

        cls.__init__ = _init
        return cls

    return decorator

class Scene:
    def __init__(self, name, engines=None):
        self._name = name
        self._engines = engines if engines is not None else []
        
    def instantiate_engine(self, engine, **kwargs):
        """
        Adds an engine instance to the scene.

        :param engine: The engine instance to add.
        :type engine: Engine
        :raises TypeError: If the provided `engine` is not an instance of `Engine`.
        """
        if isinstance(engine, Engine):
            e = engine(self)
            if len(kwargs.items()) > 0:
                e.awake(**kwargs)
            else:
                e.awake()
            if e.is_enabled:
                e.start()
                e._is_started = True
            self._engines.append(engine)
            self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
        else:
            raise TypeError("value must be an instance of Engine")

    def destroy_engine(self, engine):
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

    def _on_enter(self):
        self._call_awake_func()
        self._engines = sorted(self._engines, key=lambda x: x.priority_layer, reverse=False)
        self._call_start_func()

    def exit(self):
        for engine in self._engines:
            engine.on_exit()

    def _update(self):
        self._call_update_func()
    
    def _fixed_update(self):
        self._call_fixed_update_func()
    
    def _call_awake_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                 engine.awake()

    def _call_start_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled and not engine._is_started:
                    engine.start()
                    engine._is_started = True

    def _call_update_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.update()
                    engine._check_dead_jobs()
                    engine._update_jobs()

    def _call_fixed_update_func(self):
        if len(self._engines) > 0:
            for engine in self._engines:
                if engine.is_enabled:
                    engine.fixed_update()

class SceneManager:
    def __init__(self):
        self._scenes = []
        self._current_scene = None
        
    def setup_engine(self, scene_name, engine):
        for scene in self._scenes:
            if scene._name == scene_name:
                scene.instantiate_engine(engine)
                return
        self._scenes.append(Scene(scene_name, [engine]))

    def set_scene(self, scene_name):
        if len(self._scenes) == 0:
            raise Exception("No scenes available")
        for scene in self._scenes:
            if scene._name == scene_name:
                self._current_scene = scene
                self.current_scene._on_enter()
                return
        if scene_name == None:
            self._current_scene = self._scenes[0]
            self._current_scene._on_enter()
        
    def scene(self) -> Scene:
        """
        Retrieves the current scene.
        """
        return self._current_scene