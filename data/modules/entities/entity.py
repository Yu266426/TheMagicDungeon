import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE
from data.modules.base.level import Level
from data.modules.base.utils import get_1d_pos


class Entity:
	def __init__(self, pos: tuple[int, int], image, hitbox: tuple[int, int] | None = None):
		self.pos = pygame.Vector2(pos)

		self.image: pygame.Surface = image
		self._hitbox_override = hitbox

	@property
	def hitbox(self):
		if self._hitbox_override is None:
			return pygame.Rect(self.image.get_rect(midbottom=self.pos))
		else:
			hitbox = pygame.Rect((0, 0), self._hitbox_override)
			hitbox.midbottom = self.pos
			return hitbox

	def move(self, direction: pygame.Vector2, level: Level):
		is_collision = False

		self.pos.x += direction.x
		hitbox = self.hitbox
		if 0 < direction.x:
			top_right_tile = level.get_tile(hitbox.topright)
			if top_right_tile:
				self.pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
				is_collision = True

			bottom_right_tile = level.get_tile(hitbox.bottomright)
			if bottom_right_tile:
				self.pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
				is_collision = True
		elif direction.x < 0:
			top_left_tile = level.get_tile(hitbox.topleft)
			if top_left_tile:
				self.pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
				is_collision = True

			bottom_left_tile = level.get_tile(hitbox.bottomleft)
			if bottom_left_tile:
				self.pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
				is_collision = True

		self.pos.y += direction.y
		hitbox = self.hitbox
		if 0 < direction.y:
			bottom_left_tile = level.get_tile(hitbox.bottomleft)
			if bottom_left_tile:
				self.pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
				is_collision = True

			bottom_right_tile = level.get_tile(hitbox.bottomright)
			if bottom_right_tile:
				self.pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
				is_collision = True
		elif direction.y < 0:
			top_left_tile = level.get_tile(hitbox.topleft)
			if top_left_tile:
				self.pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
				is_collision = True

			top_right_tile = level.get_tile(hitbox.topright)
			if top_right_tile:
				self.pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
				is_collision = True

		return is_collision

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface, camera: Camera):
		pass
