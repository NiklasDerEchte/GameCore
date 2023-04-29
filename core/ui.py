import pygame.draw

from core.core import *
import os

TOP_LEFT_ANCHOR = 'topleft'
CENTER_ANCHOR = 'center'

class Button:
	def __init__(self, position=None, anchor=TOP_LEFT_ANCHOR, border_color=(100, 100, 100), border_width=3, size=(85, 35), title='Button', click=None, release=None, hover=None, title_color=(60, 60, 60), color=(152, 181, 212), hover_color=(203,223,245), click_color=(65,65,65, 200)):
		self._title = title
		self._border_color = border_color
		self._border_width = border_width

		self._title_color = title_color
		self._color = color
		self._hover_color = hover_color
		self._click_color = click_color

		self._click_func = click
		self._release_func = release
		self._hover_func = hover

		self._clicked = False
		self._font = pygame.font.SysFont('arialblack', 12)

		if position is not None:
			if anchor == TOP_LEFT_ANCHOR:
				self._rect = pygame.Rect((position[0], position[1], size[0], size[1]))
				self._rect.topleft = position
			elif anchor == CENTER_ANCHOR:
				self._rect = pygame.Rect((position[0] - size[0] / 2, position[1] - size[1] / 2, size[0], size[1]))
				self._rect.center = position
		else:
			self._rect = pygame.Rect((0, 0, size[0], size[1]))

	def get_size(self):
		return self._rect.size

	def get_position(self, anchor=TOP_LEFT_ANCHOR):
		if anchor == TOP_LEFT_ANCHOR:
			return self._rect.topleft
		if anchor == CENTER_ANCHOR:
			return self._rect.center

	def draw(self, surface):
		text_surface = self._font.render(' {} '.format(self._title), False, self._title_color)
		pos = pygame.mouse.get_pos()
		color = self._color
		if self._rect.collidepoint(pos[0],pos[1]):
			if self._hover_func is not None:
				self._hover_func()
			color = self._hover_color

			if pygame.mouse.get_pressed()[0] == 1 and not self._clicked:
				if self._click_func is not None:
					self._click_func()
				self._clicked = True
				color = self._click_color

			if pygame.mouse.get_pressed()[0] == 0 and self._clicked:
				if self._release_func is not None:
					self._release_func()
				self._clicked = False
		pygame.draw.rect(surface, color, self._rect)
		pygame.draw.rect(surface, self._border_color, self._rect, self._border_width)
		surface.blit(text_surface, (self._rect.x + (self._rect.width-text_surface.get_width())/2, self._rect.y + (self._rect.height-text_surface.get_height())/2)) # center anchor


class ImageButton:
	def __init__(self, position=None, anchor=TOP_LEFT_ANCHOR, scale=1, image_path=None, hover_image_path=None, title='Button', click=None, release=None, hover=None, title_color=(60, 60, 60)):

		self._scale = scale

		self.image = self._get_image_from_image_path(os.getcwd() + "/core/assets/button.png" if image_path is None else image_path)
		self.hover_image = self._get_image_from_image_path(os.getcwd() + "/core/assets/button-hover.png" if hover_image_path is None else hover_image_path)

		self.image_rect = self.image.get_rect()
		self.hover_image_rect = self.hover_image.get_rect()

		self._title = title
		self._title_color = title_color

		if self.image_rect is None or self.hover_image_rect is None:
			raise ValueError("image problem")

		if position is not None:
			if anchor == TOP_LEFT_ANCHOR:
				self.image_rect.topleft = position
				self.hover_image_rect.topleft = position
			elif anchor == CENTER_ANCHOR:
				self.image_rect.center = position
				self.hover_image_rect.center = position

		self.clicked = False

		self._click_func = click
		self._release_func = release
		self._hover_func = hover

		self._font = pygame.font.SysFont('arialblack', 12)

	def _get_image_from_image_path(self, image_path):
		if image_path is None:
			return None
		image = pygame.image.load(image_path)
		width = image.get_width()
		height = image.get_height()
		return pygame.transform.scale(image, (int(width * self._scale), int(height * self._scale)))


	def draw(self, surface):
		text_surface = self._font.render(' {} '.format(self._title), False, self._title_color)
		pos = pygame.mouse.get_pos()

		drawing_image = self.image
		drawing_rect = self.image_rect
		if self.image_rect.collidepoint(pos):
			if self._hover_func is not None:
				self._hover_func()
			drawing_image = self.hover_image
			drawing_rect = self.hover_image_rect

			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				if self._click_func is not None:
					self._click_func()
				self.clicked = True

			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				if self._release_func is not None:
					self._release_func()
				self.clicked = False

		surface.blit(drawing_image, (drawing_rect.x, drawing_rect.y))
		surface.blit(text_surface, (drawing_rect.x + (drawing_rect.width-text_surface.get_width())/2, drawing_rect.y + (drawing_rect.height-text_surface.get_height())/2)) # center anchor