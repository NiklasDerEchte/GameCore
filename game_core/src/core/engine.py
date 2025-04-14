import sys
import random
import pygame
import inspect
import string

from .coroutine import Coroutine

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
        Triggered when the engine is enabled via the enable() method.

        :param inject: Optional data to be injected during the enabling process.
        :type inject: dict
        """
        pass

    def on_disable(self):
        """
        Called when the engine is disabled, via the disable() method.
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
        This method is called when the engine is about to be destroyed or when a scene change occurs.
        """
        pass
