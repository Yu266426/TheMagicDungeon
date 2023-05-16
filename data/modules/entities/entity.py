import pygame
import pygbase


class Entity:
	def __init__(self, pos):
		self.pos = pygame.Vector2(pos)

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		pass

	def is_alive(self):
		return True
