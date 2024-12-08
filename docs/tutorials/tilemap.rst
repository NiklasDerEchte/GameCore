Tilemap 2D
==========

The ``TileMap`` class is responsible for loading a ``.tmx`` file, which contains the information about the tileset and the map made of these tiles. It uses the ``pytmx`` library to load the ``.tmx`` file and render the tiles onto a surface. It also supports animated tiles. The ``make_map()`` method returns the rendered map surface and a list of animated tiles with their position and frames.

.. hint::

   You can easily edit `.tmx` tilemap files using the `Tiled <https://www.mapeditor.org/>`__ map editor.

Camera
^^^^^^

The ``Camera`` class represents the viewable area of the game world. It takes a target position as input and sets its own position accordingly. The target is usually the player's position, and the camera follows the player around the game world. The ``look_at()`` method calculates the position of the camera based on the target position, and the ``apply()`` method returns the position of a rectangle in the camera view.

TileMapDrawer
^^^^^^^^^^^^^

.. code-block:: python

    from game_core.core import *

    class MyEngine(Engine):

        def start(self):
            self.tile_map_drawer = self.core.instantiate(TileMapDrawer) # create TileMapDrawer engine
            self.tile_map_drawer.enable(tile_map_path="map.tmx") # enable engine, load and draw map
            self.camera = self.tile_map_drawer.get_camera()

        def update(self):
            player_position = (player.x, player.y) # player position in world space not window space
            self.camera.look_at(player_position)
            self.core.window.blit(player_image, self.camera.apply_tuple(player_position)) # draw player sprite on camera

    Core(background_color=(255, 255, 255, 0), fps=30)

Examples
^^^^^^^^

`Spaceship <https://github.com/NiklasDerEchte/GameCore/blob/master/examples/spaceship.py>`_
-------------------------------------------------------------------------------------------

.. image:: ../_images/spaceship-example.png
   :alt: spaceship example image
   :scale: 100%

`code <https://github.com/NiklasDerEchte/GameCore/blob/master/examples/spaceship.py>`__
