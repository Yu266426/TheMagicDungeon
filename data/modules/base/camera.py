import pygame


class Camera:
	def __init__(self, pos: tuple[int | float, int | float] = (0, 0)):
		self.target = pygame.Vector2(pos)

	def set_target(self, target: pygame.Vector2):
		self.target = target.copy()

	def screen_to_world(self, pos: pygame.Vector2 | tuple):
		return pygame.Vector2(pos[0] + self.target.x, pos[1] + self.target.y)
