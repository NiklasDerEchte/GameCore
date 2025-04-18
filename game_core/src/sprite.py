from .core import *
import os

####################
### Image slicer ###
####################

class Slicer:
    """
    Base class for slicing a surface into smaller sections.
    Provides a generic interface for subclasses to implement specific slicing behavior.
    """

    def slice(self, surface: pygame.Surface):
        """
        Placeholder function, returns the input surface without modification.

        :param surface: A `pygame.Surface` object to be sliced.
        :return: The original surface.
        """
        return surface


class SizeSlicer(Slicer):
    """
    Slices a surface into tiles of specified width and height, with optional gaps and padding.
    """
    def __init__(self,
                 width,
                 height,
                 x_gap=0,
                 y_gap=0,
                 top_padding=0,
                 left_padding=0,
                 right_padding=0,
                 bottom_padding=0):
        """
        Initializes a SizeSlicer instance with slicing dimensions and padding.

        :param width: Width of each tile.
        :param height: Height of each tile.
        :param x_gap: Horizontal gap between tiles.
        :param y_gap: Vertical gap between tiles.
        :param top_padding: Padding at the top of the image.
        :param left_padding: Padding at the left side of the image.
        :param right_padding: Padding at the right side of the image.
        :param bottom_padding: Padding at the bottom of the image.
        """
        super(Slicer, self).__init__()
        self._width = width
        self._height = height
        self._x_gap = x_gap
        self._y_gap = y_gap
        self._top_padding = top_padding
        self._left_padding = left_padding
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding

    def slice(self, surface: pygame.Surface):
        """
        Splits the surface into tiles based on the specified size and gaps.

        :param surface: A `pygame.Surface` to be sliced.
        :return: A list of `pygame.Surface` tiles.
        """
        width, height = surface.get_width(), surface.get_height()
        animation_content_rect = pygame.Rect(self._left_padding, self._top_padding, width - self._right_padding, height - self._bottom_padding)
        cols = round((animation_content_rect.width - animation_content_rect.x) / self._width)
        rows = round((animation_content_rect.height - animation_content_rect.y) / self._height)
        image_tiles = []
        for y in range(rows):
            for x in range(cols):
                selection_rect = pygame.Rect(
                    animation_content_rect.x + (x * self._width) + int(self._x_gap / 2.0),
                    animation_content_rect.y + (y * self._height) + int(self._y_gap / 2.0),
                    self._width - self._x_gap,
                    self._height - self._y_gap
                )
                tile = pygame.Surface((selection_rect.width, selection_rect.height), pygame.SRCALPHA, 32)
                tile.blit(surface, (0, 0), selection_rect)
                image_tiles.append(tile)
        return image_tiles

class AmountSlicer(Slicer):
    """
    Slices a surface into a specified number of rows and columns, with optional gaps and padding.
    """
    def __init__(
            self,
            rows=1,
            cols=1,
            x_gap=0,
            y_gap=0,
            top_padding=0,
            left_padding=0,
            right_padding=0,
            bottom_padding=0):
        """
        Initializes an AmountSlicer instance with slicing rows, columns, and padding.

        :param rows: Number of rows to divide the surface into.
        :param cols: Number of columns to divide the surface into.
        :param x_gap: Horizontal gap between tiles.
        :param y_gap: Vertical gap between tiles.
        :param top_padding: Padding at the top of the image.
        :param left_padding: Padding at the left side of the image.
        :param right_padding: Padding at the right side of the image.
        :param bottom_padding: Padding at the bottom of the image.
        """
        super(Slicer, self).__init__()
        self._rows = rows
        self._cols = cols
        self._x_gap = x_gap
        self._y_gap = y_gap
        self._top_padding = top_padding
        self._left_padding = left_padding
        self._right_padding = right_padding
        self._bottom_padding = bottom_padding

    def slice(self, surface: pygame.Surface):
        """
        Splits the surface into a grid of tiles based on the number of rows and columns.

        :param surface: A `pygame.Surface` to be sliced.
        :return: A list of `pygame.Surface` tiles.
        """
        width, height = surface.get_width(), surface.get_height()
        animation_content_rect = pygame.Rect(self._left_padding, self._top_padding, width - self._right_padding, height - self._bottom_padding)
        animation_frame_size = (
            (animation_content_rect.width - animation_content_rect.x) / self._cols,
            (animation_content_rect.height - animation_content_rect.y) / self._rows
        )
        image_tiles = []
        for y in range(self._rows):
            for x in range(self._cols):
                selection_rect = pygame.Rect(
                    animation_content_rect.x + (x * animation_frame_size[0]) + int(self._x_gap / 2.0),
                    animation_content_rect.y + (y * animation_frame_size[1]) + int(self._y_gap / 2.0),
                    animation_frame_size[0] - self._x_gap,
                    animation_frame_size[1] - self._y_gap
                )
                tile = pygame.Surface((selection_rect.width, selection_rect.height), pygame.SRCALPHA, 32)
                tile.blit(surface, (0, 0), selection_rect)
                image_tiles.append(tile)

        return image_tiles

############################################
### Simple color and image loader sprite ###
############################################

class SimpleSprite(pygame.sprite.Sprite):
    """
    A basic sprite that displays a colored rectangle.
    """
    def __init__(self,
                 color=(200, 200, 200, 255),
                 width=None,
                 height=None
                 ):
        """
        Initializes a sprite with a single color and optional dimensions.

        :param color: Color of the sprite as an RGBA tuple.
        :param width: Width of the sprite.
        :param height: Height of the sprite.
        """
        pygame.sprite.Sprite.__init__(self)
        if width is None:
            width = 32
        if height is None:
            height = 32
        self._image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self._rect = self._image.get_rect()
        self._image.fill(color)

    def get_image(self):
        """
        Returns the image surface of the sprite.

        :return: A `pygame.Surface` object representing the sprite.
        """
        return self._image

    def get_rect(self):
        """
        Returns the rectangular area of the sprite.

        :return: A `pygame.Rect` object.
        """
        return self._rect

    def update_rect(self, rect: pygame.Rect):
        """
        Updates the rectangular position and size of the sprite.

        :param rect: A `pygame.Rect` object.
        """
        self._rect = rect

class SimpleImageSprite(pygame.sprite.Sprite):
    """
    A sprite that displays an image, optionally sliced by a Slicer object.
    """
    def __init__(self, image_path, slicer: Slicer = None):
        """
        Initializes the sprite with an image and an optional slicer.

        :param image_path: Path to the image file.
        :param slicer: An optional Slicer object to slice the image.
        """
        pygame.sprite.Sprite.__init__(self)
        self._slicer = slicer
        self._image = pygame.image.load(image_path).convert_alpha()
        self._rect = self._image.get_rect()

    def flip(self, flip_x=False, flip_y=False):
        """
        Flips the image horizontally and/or vertically.

        :param flip_x: If True, flip the image horizontally.
        :param flip_y: If True, flip the image vertically.
        """
        self._image = pygame.transform.flip(self._image, flip_x, flip_y)

    def get_image(self) -> pygame.Surface:
        """
        Returns the image or a sliced version of it.

        :return: A `pygame.Surface` or list of surfaces if sliced.
        """
        if self._slicer is not None:
            return self._slicer.slice(self._image)
        return self._image

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangular area of the image.

        :return: A `pygame.Rect` object.
        """
        return self._rect

    def update_rect(self, rect: pygame.Rect):
        """
        Updates the rectangular position and size of the image.

        :param rect: A `pygame.Rect` object.
        """
        self._rect = rect


#######################
### Simple animator ###
#######################

class SimpleSpriteAnimator:
    """
    Manages animation states for sprites and cycles through frames based on time.
    """
    def __init__(self, anim_sprites: dict, start_state: str, anim_state_decision: callable, sprite_size: tuple, fps=30):
        """
        Initializes the animator with animations, state logic, and frame timing.

        :param anim_sprites: Dictionary mapping states to animation frames.
        :param start_state: The initial animation state.
        :param anim_state_decision: Callable to decide the current state.
        :param sprite_size: Size of the animation surface.
        :param fps: Frames per second for the animation.
        """
        ground_surface = pygame.surface.Surface(sprite_size, pygame.SRCALPHA, 32)
        self._surface = ground_surface.convert_alpha()
        self._rect = self._surface.get_rect()
        self._animation_sprites = anim_sprites
        self._active_sprite_index = 0
        self._active_animation_state = start_state
        self._cb_anim_state_decision = anim_state_decision
        self._fps = fps
        self._ft = 60/self._fps
        self._fwaiter = 0

    def get_size(self):
        """
        Returns the size of the animation surface.

        :return: Tuple representing the size (width, height).
        """
        return self._surface.get_size()

    def get_image(self, delta_time=None):
        """
        Returns the current animation frame.

        :param delta_time: Time since the last frame, used for timing animations.
        :return: A `pygame.Surface` of the current frame.
        """
        return self.animate(delta_time)

    def get_rect(self):
        """
        Returns the rectangular area of the animation surface.

        :return: A `pygame.Rect` object.
        """
        return self._rect

    def update_rect(self, rect: pygame.Rect):
        """
        Updates the rectangular position and size of the animation surface.

        :param rect: A `pygame.Rect` object.
        """
        self._rect = rect

    def animate(self, delta_time=None):
        """
        Cycles through animation frames based on time and state.

        :param delta_time: Time since the last frame, used for timing animations.
        :return: A `pygame.Surface` of the current frame.
        """
        if delta_time is not None:
            self._fwaiter = self._fwaiter - delta_time
            if self._fwaiter <= 0:
                self._fwaiter = self._ft
            else:
                return self._surface
        self._surface.fill((0, 0, 0, 0))
        anim_state = self._cb_anim_state_decision()
        if anim_state not in self._animation_sprites:
            print("animation state '{}' not found".format(anim_state))
            return self._surface
        if anim_state != self._active_animation_state:
            self._active_sprite_index = 0
            self._active_animation_state = anim_state

        active_sprite = self._animation_sprites[self._active_animation_state][self._active_sprite_index]

        if type(active_sprite) is list:
            for sprite in active_sprite:
                self._surface.blit(pygame.transform.scale(sprite, self.get_size()), (0, 0))
        else:
            self._surface.blit(pygame.transform.scale(active_sprite, self.get_size()), (0, 0))

        self._active_sprite_index = self._active_sprite_index + 1
        if self._active_sprite_index >= len(self._animation_sprites[self._active_animation_state]):
            self._active_sprite_index = 0

        return self._surface

###############################################
### Directory structure to animation parser ###
###############################################

class SpriteDirectoryAnimation:
    """
    Parses a directory structure to create animations for sprites.
    """
    def __init__(self, project_path, slicer: Slicer = None):
        """
        Initializes the parser with a project directory and an optional slicer.

        :param project_path: Path to the directory containing animations.
        :param slicer: An optional Slicer object to slice images.
        :type slicer: Slicer
        """
        self._project_path = project_path
        self._slicer = slicer

    def parse(self) -> dict[str, pygame.Surface]:
        """
        Parses the directory and loads animations.

        :return: A dictionary mapping animation names to frames.
        """
        if os.path.isfile(self._project_path):
            return {self._convert_filename(os.path.basename(self._project_path)): SimpleImageSprite(self._project_path, slicer=self._slicer).get_image()}
        elif os.path.isdir(self._project_path):
            return self._build()
        else:
            print("path '{}' not valid".format(self._project_path))
        return {}

    def _convert_filename(self, filename):
        """
        Converts a filename to an animation name.

        :param filename: The name of the file.
        :return: A string representing the animation name.
        """
        return os.path.splitext(filename)[0]

    def _build(self):
        """
        Builds an animation dictionary.

        :return: A dictionary mapping animation names to frames.
        """
        anim = {}
        animation_files = os.listdir(self._project_path)
        for animation_filename in animation_files:
            absolute_animation_path = os.path.join(self._project_path, animation_filename)
            animation_name = self._convert_filename(animation_filename)
            anim[animation_name] = []
            if os.path.isfile(absolute_animation_path):
                anim[animation_name] = SimpleImageSprite(absolute_animation_path, slicer=self._slicer).get_image()
            elif os.path.isdir(absolute_animation_path):
                for frame_filename in os.listdir(absolute_animation_path):
                    if os.path.isfile(os.path.join(absolute_animation_path, frame_filename)):
                        next_frames = SimpleImageSprite(os.path.join(absolute_animation_path, frame_filename), slicer=self._slicer).get_image()
                        current_frame = anim[animation_name]
                        if next_frames is not None:
                            if type(next_frames) is list:
                                anim[animation_name] = [*current_frame, *next_frames]
                            else:
                                anim[animation_name].append(next_frames)
        return anim