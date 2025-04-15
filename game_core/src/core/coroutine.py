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
        :param interval: The time interval (in milliseconds) between executions.
        :type interval: float
        :param loop_condition: A function returning a boolean that determines if the coroutine should continue.
        :type loop_condition: callable
        :param call_delay: Initial delay before the first execution (in milliseconds).
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
