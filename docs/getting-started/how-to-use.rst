How to use GameCore
===================

Core object
^^^^^^^^^^^

The ``Core`` class is responsible for creating the game window, managing the game loop, and handling input events. To use the Core object, simply create an instance of it and provide it with the necessary parameters:

.. code-block:: python

    Core(
        size=(640, 480),
        background_color=(255, 255, 255),
        fps=60
    )

simple runtime environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of how you can use the engine to create a simple game loop:

.. code-block:: python

    from game_core.core import *

    def start(core): # <- here u get the core object
        # initialize game objects here
        pass

    def update():
        # update game objects here
        pass

    Core(update=update, start=start)

what is an Engine?
^^^^^^^^^^^^^^^^^^

The ``Engine`` class is a base class that you can inherit from to create your own custom runtime controlled object. Engines are started after the Core class has been invoked. The following methods are available for you to override:

* ``awake`` Is called once at the beginning to set properties.
* ``start`` Called once at the beginning or after first enable.
* ``on_enable`` Called when the engine has been enabled. This is the perfect method to pass params, to init or recalculate attributes.
* ``on_disable`` Called when the engine has been disabled.
* ``update`` Constantly called.
* ``fixed_update`` Called in a certain tick rate.
* ``on_destroy`` Called once after engine got destroyed

To create your own engine, you can simply inherit from the ``Engine`` class and override any of the above methods as necessary.

.. code-block:: python

    from game_core.core import *

    class MyEngine(Engine):
        def start(self):
            print("MyEngine started")

        def update(self):
            print("MyEngine updated")

    Core(background_color=(255, 255, 255, 0), fps=60)

What is a Prefab Engine?
^^^^^^^^^^^^^^^^^^^^^^^^

The lifecycle can be completely controlled and engines created dynamically via the parent ``Prefab``.

.. code-block:: python

    from game_core.core import *

    class MyPrefab(Engine, Prefab):
        def start(self):
            print("MyPrefab started")

    class MyEngine(Engine):
        def start(self):
            print("MyEngine started")
            self.core.instantiate(MyPrefab) # starts lifecycle

    Core(background_color=(255, 255, 255, 0), fps=60)

enable / disable Engine
^^^^^^^^^^^^^^^^^^^^^^^

``Engine``.enable(``**kwargs`` inject...)

* ``inject`` You can pass properties to the ``Engine``

``Engine``.disable()

.. code-block:: python

    from game_core.core import *

    class MyPrefab(Engine, Prefab):
        def awake(self): # set pre configs
            self.is_enabled = False # Disable the start of the lifecycle at the instantiation and allow them to be enabled dynamically.

        def start(self):
            self.start_time = self.core.elapsed_delta_time
            print("MyPrefab started")

        def on_enable(self, inject=None):
            print("MyPrefab enabled")
            print(inject['info'])

        def on_disable(self):
            alive_time = self.core.elapsed_delta_time - self.start_time
            print("MyPrefab disabled after {}s".format(round(alive_time/1000)))

    class MyEngine(Engine):
        def start(self):
            print("MyEngine started")
            self.prefab_engine = self.core.instantiate(MyPrefab)
            print("Wait three seconds...")
            self.wait_ms = 3000 # wait three seconds

        def update(self):
            self.wait_ms = self.wait_ms - self.core.delta_time
            if self.wait_ms <= 0 and not self.prefab_engine.is_enabled:
                self.prefab_engine.enable(info="This prefab will dies in 10 seconds. This is the perfect method to pass params, to init or recalculate attributes.")
                self.wait_ms = 10000
            if self.wait_ms <= 0 and self.prefab_engine.is_enabled:
                self.is_enabled = False
                self.prefab_engine.disable()


    Core(background_color=(255, 255, 255, 0), fps=60)

Output:

.. code-block::

    MyEngine started
    Wait three seconds...
    MyPrefab enabled
    This prefab will dies in 10 seconds. This is the perfect method to pass params, to init or recalculate attributes.
    MyPrefab started
    MyPrefab disabled after 10s

destroy Engine
^^^^^^^^^^^^^^

``Engine``.destroy(Engine engine)

* ``engine`` The ``Engine`` to destroy, calls the ``on_destroy``

.. code-block:: python

    from game_core.core import *

    class MyEngine(Engine):
        def start(self):
            print("MyEngine started")
            self.core.destroy(self)

        def on_destroy(self):
            print("MyEngine stopped")
            exit()

    Core(background_color=(255, 255, 255, 0), fps=60)

