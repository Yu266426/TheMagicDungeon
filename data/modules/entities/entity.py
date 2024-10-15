import pygame
import pygbase


class Entity:
	def __init__(self, pos: pygame.typing.Point):
		self.pos = pygame.Vector2(pos)
		self.active = True
		self.visible = True

	def added(self):
		pass

	def removed(self):
		pass

	def interact(self, other: "Entity"):
		pass

	def enable(self):
		self.active = True

	def disable(self):
		self.active = False

	def update(self, delta: float):
		pass

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		pass

	def is_alive(self):
		return True
