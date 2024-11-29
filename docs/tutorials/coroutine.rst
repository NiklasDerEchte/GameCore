Coroutine
=========

The ``Coroutine`` class is a helper class that provides a way to execute a function at regular intervals. It is an optimal function to create health regeneration or enemy spawns, for example. To use the ``Coroutine`` object, create an instance of it and provide it with the necessary parameters:

.. code-block:: python

    from core import *
    class FooBar(Engine):
        def start(self):
            self.counter = 5
            self.start_coroutines([
                Coroutine(func=self.my_func, interval=1000, call_delay=1200, loop_condition=lambda: self.counter > 0) # runs my_func in 1200 ms every 1000 ms
            ])

        def my_func(self):
            print("Hello World")
            self.counter = self.counter - 1
            return {'interval': random.randint(1000, 2000)} # interval is optionally adjustable every tick

.. code-block::

    Output: 5x Hello World

