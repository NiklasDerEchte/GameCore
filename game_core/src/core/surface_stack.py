import sys
import random
import pygame
import inspect
import string

class SurfaceStackElement:
    """
    Represents an individual element in a stack of rendering surfaces.

    :var name: Name identifier for the surface.
    :type name: str
    :var surface: The surface object to render.
    :type surface: pygame.Surface
    :var render_layer: The rendering order for the surface.
    :type render_layer: int
    :var surface_render_position: Position of the surface in the window.
    :type surface_render_position: tuple
    :var auto_fill: Indicates if the surface should auto-fill after rendering.
    :type auto_fill: bool
    """
    def __init__(self):
        """
        Initializes a SurfaceStackElement.
        """
        self.name = None
        self.surface = None
        self.render_layer = 0
        self.surface_render_position = (0, 0)
        self.auto_fill = False

    def print(self):
        """
        Prints information about the surface element.
        """
        print("Surface {} with layer: {}".format(self.name, self.render_layer))

class SurfaceStack:
    """
    Manages a stack of rendering surfaces for organized layer-based rendering.
    """
    def __init__(self):
        """
        Initializes a SurfaceStack.
        """
        self._stack = []

    def add_element(self, name, surface, render_layer: int, surface_render_position: tuple, fill_after_draw=True):
        """
        Adds a new surface element to the stack.

        :param name: Unique name for the surface.
        :type name: str
        :param surface: The surface to add.
        :type surface: pygame.Surface
        :param render_layer: The rendering order.
        :type render_layer: int
        :param surface_render_position: Position of the surface in the window.
        :type surface_render_position: tuple
        :param fill_after_draw: Indicates if the surface should auto-fill after rendering.
        :type fill_after_draw: bool
        """
        for element in self._stack:
            if element.name == name:
                s = "surface name \'{}\' already exists".format(name)
                raise ValueError(s)
            if element.render_layer == render_layer:
                render_layer = render_layer + 1

        surface_stack_element = SurfaceStackElement()
        surface_stack_element.name = name
        surface_stack_element.surface = surface
        surface_stack_element.render_layer = render_layer
        surface_stack_element.surface_render_position = surface_render_position
        surface_stack_element.auto_fill = fill_after_draw
        self._stack.append(surface_stack_element)
        self._stack = sorted(self._stack, key=lambda x: x.render_layer, reverse=False)

    def remove_element(self, name):
        """
        Removes a surface element from the stack.

        :param name: Name of the surface to remove.
        :type name: str
        """
        for element in self._stack:
            if element.name == name:
                self._stack.remove(element)
                break

    def get_surface(self, name):
        """
        Retrieves a surface by name.

        :param name: Name of the surface.
        :type name: str

        :returns: The requested surface.
        :rtype: pygame.Surface
        """
        return self.get_element(name).surface

    def get_element(self, name):
        """
        Retrieves a SurfaceStackElement by name.

        :param name: Name of the element.
        :type name: str

        :returns: The requested element.
        :rtype: SurfaceStackElement:
        """
        for element in self._stack:
            if element.name == name:
                return element

    def draw(self, core):
        """
        Draws all surfaces in the stack.

        :param core: Reference to the Core instance for rendering.
        :type core: Core
        """
        counter = 0
        for element in self._stack:
            # print("Draw {} at {} by {}/{}]".format(element.name, element.surface_render_position, counter, len(self.stack)-1))
            core.window.blit(element.surface, element.surface_render_position)
            if element.auto_fill:
                element.surface.fill(core.background_color)
            counter = counter + 1

    def print(self):
        """
        Prints information about all surfaces in the stack.
        """
        for element in self._stack:
            element.print()