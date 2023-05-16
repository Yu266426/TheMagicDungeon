import pygame


class Hitbox:
	def __init__(self, hitbox_size: tuple[int, int], pos: tuple = (0, 0)):
		self.pos = pygame.Vector2(pos)
		self._hitbox = pygame.FRect(self.pos, hitbox_size)

	def link_pos(self, pos: pygame.Vector2) -> "Hitbox":
		self.pos = pos
		return self

	@property
	def rect(self):
		self._hitbox.midbottom = self.pos
		return self._hitbox

	def collides_with(self, collider):
		from data.modules.entities.components.line_collider import LineCollider

		if isinstance(collider, Hitbox):
			return self.rect.colliderect(collider.rect)
		elif isinstance(collider, LineCollider):
			return False
