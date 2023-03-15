import pygame


class Hitbox:
	def __init__(self, hitbox_size: tuple[int, int]):
		self.pos = pygame.Vector2()
		self._hitbox = pygame.Rect(self.pos, hitbox_size)

	def link_pos(self, pos: pygame.Vector2) -> "Hitbox":
		self.pos = pos
		return self

	@property
	def rect(self):
		self._hitbox.midbottom = self.pos
		return self._hitbox
