Coroutine
=========

The ``Coroutine`` class is a helper class that provides a way to execute a function at regular intervals. It is an optimal function to create health regeneration or enemy spawns, for example. To use the ``Coroutine`` object, create an instance of it and provide it with the necessary parameters:

.. code:: python

    from game_core.core import *

    class FooBar(Engine):
        """
        A custom engine class inheriting from `Engine`.
        """

        def start(self):
            """
            Initializes the FooBar engine by setting up a coroutine to execute `my_func` repeatedly.

            - Sets `self.counter` to 5 as a loop condition counter.
            - Starts a coroutine to call `my_func`:
                - Executes after an initial delay of 1200 ms.
                - Repeats every 1000 ms while `self.counter > 0`.
            """
            self.counter = 5
            self.start_coroutines([
                Coroutine(func=self.my_func, interval=1000, call_delay=1200, loop_condition=lambda: self.counter > 0)
            ])

        def my_func(self):
            """
            A task executed by the coroutine:

            - Prints "Hello World" to the console.
            - Decrements `self.counter` to manage the loop condition.
            - Dynamically adjusts the interval for the next execution with a random value between 1000 and 2000 ms.

            :return: A dictionary updating the interval for the coroutine.
            """
            print("Hello World")
            self.counter = self.counter - 1
            return {'interval': random.randint(1000, 2000)}

.. code-block::

    Output: 5x Hello World#

The ``ScreenBlink`` class demonstrates the integration of a coroutine to create a dynamic screen-blinking effect by periodically changing the background color.
The ``ScreenBlink`` class can also be easily tested using `preview.py <https://github.com/NiklasDerEchte/GameCore/blob/master/preview.py>`__.

.. code:: python

    from game_core.core import *

    class ScreenBlink(Engine, Prefab):
        """
        A class combining `Engine` and `Prefab` functionalities to create a screen-blinking effect by changing the background color periodically.
        """

        def start(self):
            """
            Initializes the ScreenBlink engine by setting up a coroutine to execute `change`:

            - Coroutine is triggered after an initial delay of 30 ms.
            - Repeats every 15,000 ms (15 seconds).
            """
            self.coroutines = [
                Coroutine(
                    func=self.change,
                    interval=15*1000,
                    call_delay=30,
                )
            ]

        def random_color(self):
            """
            Generates a random RGB color:

            - Red, green, and blue components are randomly selected between 0 and 255.

            :return: A tuple (r, g, b) representing the random color.
            """
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return (r, g, b)

        def change(self):
            """
            Changes the background color of the core engine:

            - Sets `core.background_color` to a randomly generated color using `random_color`.
            """
            self.core.background_color = self.random_color()


