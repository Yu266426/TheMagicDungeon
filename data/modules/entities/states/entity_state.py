import pygame
from pygbase import Camera


class EntityState:
	def update(self, delta: float):
		pass

	def next_state(self) -> str:
		return ""

	def draw(self, screen: pygame.Surface, camera: Camera):
		pass
