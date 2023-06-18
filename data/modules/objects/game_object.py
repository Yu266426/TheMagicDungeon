import pygame
import pygbase
from pygbase import Camera

from data.modules.entities.entity import Entity


class GameObject(Entity):
	def __init__(self, name: str, pos: tuple, sprite: pygbase.Image | pygbase.Animation, custom_hitbox: pygame.Rect | None = None):
		super().__init__(pos)
		self.name = name

		self.sprite = sprite
		self.is_animated = isinstance(self.sprite, pygbase.Animation)
		if self.is_animated:
			self.rect = self.sprite.get_current_image().get_image(0).get_rect(midbottom=self.pos)
		else:
			self.rect = self.sprite.get_image(0).get_rect(midbottom=self.pos)

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def removed(self):
		pass

	def animate(self, frame_time: float):
		if self.is_animated:
			self.sprite.change_frame(frame_time)

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, flags=0):
		if self.is_animated:
			self.sprite.draw_at_pos(display, self.pos, camera, flags=flags)
		else:
			self.sprite.draw(display, camera.world_to_screen(self.pos), flags=flags)
