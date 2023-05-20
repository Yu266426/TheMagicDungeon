from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
	from data.modules.entities.components.line_collider import LineCollider


class BoxCollider:
	def __init__(self, hitbox_size: tuple[int, int], pos: tuple = (0, 0)):
		self.pos = pygame.Vector2(pos)
		self._hitbox = pygame.FRect(self.pos, hitbox_size)

	def link_pos(self, pos: pygame.Vector2) -> "BoxCollider":
		self.pos = pos
		return self

	@property
	def rect(self):
		self._hitbox.midbottom = self.pos
		return self._hitbox

	def get_edge_lines(self) -> tuple["LineCollider", "LineCollider", "LineCollider", "LineCollider"]:
		from data.modules.entities.components.line_collider import LineCollider
		return (
			LineCollider(self.rect.topleft, 90, self.rect.width),
			LineCollider(self.rect.topleft, 180, self.rect.height),
			LineCollider(self.rect.bottomright, 0, self.rect.height),
			LineCollider(self.rect.bottomright, -90, self.rect.width)
		)

	def collides_with(self, collider):
		from data.modules.entities.components.line_collider import LineCollider

		if isinstance(collider, BoxCollider):
			return self.rect.colliderect(collider.rect)
		elif isinstance(collider, LineCollider):
			return collider.collides_with(self)
