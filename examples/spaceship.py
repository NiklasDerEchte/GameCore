from core import *


class Spaceship(Engine, Prefab):
    """
    A class representing a spaceship in a 2D game. It handles the spaceship's movement,
    tile map rendering, camera control, and visual effects using shaders.

    Attributes:
        priority_layer (int): The priority layer for rendering.
        tile_map_surface (Surface): The surface used for rendering the background tile map.
        tile_map_drawer (TileMapDrawer): Responsible for drawing the tile map.
        line_effect (Lines): A shader effect applied to the scene.
        camera (Camera): The camera that follows the spaceship's movement.
        pos (tuple): The current position of the spaceship.
        spaceship_surface (Surface): The surface used for rendering the spaceship.
        simple_image_sprite (SimpleImageSprite): The sprite representing the spaceship image.
    """

    def awake(self):
        """
        Initializes the priority layer for the spaceship.

        This method is called when the spaceship object is created.
        """
        self.priority_layer = 20

    def start(self):
        """
        Initializes the spaceship's components, including the tile map, spaceship surface,
        shader effects, and camera.

        - Creates a tile map surface for the background.
        - Instantiates and enables a `TileMapDrawer` to render the tile map.
        - Initializes a `Lines` shader effect for visual enhancements.
        - Sets up the camera to follow the spaceship and positions the spaceship at the center of the screen.
        - Initializes the spaceship surface and sprite image.
        """
        # create background surface for the tilemap
        size = self.core.window_size
        self.tile_map_surface = self.core.create_layer_surface(
            name="_SpaceshipTileMap",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )

        # init tilemap
        self.tile_map_drawer = self.core.instantiate(TileMapDrawer)
        self.tile_map_drawer.enable(
            tile_map_path=os.getcwd() + "/examples/assets/space.tmx",
            surface=self.tile_map_surface
        )

        # init shader
        self.line_effect = self.core.instantiate(Lines)
        self.line_effect.enable(width=self.tile_map_drawer.get_size()[0], height=self.tile_map_drawer.get_size()[1])

        # set camera and initial spaceship position
        self.camera = self.tile_map_drawer.get_camera()
        self.pos = (self.core.window_size[0] / 2, self.core.window_size[1] / 2)

        # init spaceship surface
        self.spaceship_surface = self.core.create_layer_surface(
            name="_Spaceship",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=1,
            fill_after_draw=True
        )
        self.simple_image_sprite = SimpleImageSprite("/examples/assets/sprites/Spaceship/sprite_0.png")

    def update(self):
        """
        Updates the spaceship's movement, sprite position, camera view, and visual effects.

        - Handles player movement using the `handle_movement` method.
        - Updates the spaceship's position based on player input.
        - Makes the camera follow the spaceship's position.
        - Blits the spaceship sprite onto the spaceship surface.
        - Updates the origin for the line effect based on the camera's position.
        """
        self.handle_movement(speed=2)

        # calculate sprite position
        spaceship_center = get_center(
            self.pos,
            self.simple_image_sprite.get_rect().width,
            self.simple_image_sprite.get_rect().height
        )

        # update camera and draw spaceship
        self.camera.look_at(self.pos)
        self.spaceship_surface.blit(self.simple_image_sprite.get_image(), self.camera.apply_tuple(spaceship_center))

        # update line effect origin based on camera position
        self.line_effect.set_origin(self.camera.apply_tuple((0, 0)))

    def handle_movement(self, speed=1):
        """
        Handles the spaceship's movement based on player input.

        The spaceship can move in four directions (WASD) with speed adjustment.
        It also normalizes the movement direction and handles boundary checks.

        Parameters:
            speed (int): The movement speed of the spaceship (default is 1).
        """
        move_direction = (0, 0)
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_a]:
            move_direction = (move_direction[0] - 1, move_direction[1])
        if keys[pygame.K_d]:
            move_direction = (move_direction[0] + 1, move_direction[1])

        # vertical movement
        if keys[pygame.K_w]:
            move_direction = (move_direction[0], move_direction[1] - 1)
        if keys[pygame.K_s]:
            move_direction = (move_direction[0], move_direction[1] + 1)

        if move_direction[0] == 0 and move_direction[1] == 0:
            return

        # normalize direction
        distance = math.sqrt(move_direction[0] ** 2 + move_direction[1] ** 2)
        move_direction = (move_direction[0] / distance, move_direction[1] / distance)

        # apply direction
        self.pos = (
            round(self.pos[0] + (move_direction[0] * speed) * self.core.delta_time / 10),  # move along x-axis
            round(self.pos[1] + (move_direction[1] * speed) * self.core.delta_time / 10)  # move along y-axis
        )

        # check borders to prevent the spaceship from moving out of bounds
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])

        if self.pos[0] > self.tile_map_drawer.get_size()[0]:
            self.pos = (self.tile_map_drawer.get_size()[0], self.pos[1])

        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)

        if self.pos[1] > self.tile_map_drawer.get_size()[1]:
            self.pos = (self.pos[0], self.tile_map_drawer.get_size()[1])
