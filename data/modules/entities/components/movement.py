import pygame
from data.modules.base.constants import TILE_SIZE
from data.modules.map.level import Level
from data.modules.base.utils import get_1d_tile_pos
from data.modules.entities.components.boxcollider import BoxCollider


# class Movement:
# 	def __init__(self, speed: float, level: Level, hitbox: Hitbox):
# 		self.speed = speed
#
# 		self.level = level
# 		self.hitbox = hitbox
#
# 	def move_in_direction(self, pos: pygame.Vector2, direction: pygame.Vector2, delta: float):
# 		normalized_direction = direction.copy()
# 		if normalized_direction.length() != 0:
# 			normalized_direction.normalize_ip()
#
# 		is_collision = [False, False]
#
# 		pos.x += normalized_direction.x * self.speed * delta
# 		hitbox = self.hitbox.rect
# 		if 0 < normalized_direction.x:
# 			top_right_tile = self.level.get_tile(hitbox.topright)
# 			if top_right_tile:
# 				pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
# 				is_collision[0] = True
#
# 			bottom_right_tile = self.level.get_tile(hitbox.bottomright)
# 			if bottom_right_tile:
# 				pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
# 				is_collision[0] = True
# 		elif normalized_direction.x < 0:
# 			top_left_tile = self.level.get_tile(hitbox.topleft)
# 			if top_left_tile:
# 				pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
# 				is_collision[0] = True
#
# 			bottom_left_tile = self.level.get_tile(hitbox.bottomleft)
# 			if bottom_left_tile:
# 				pos.x = (get_1d_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
# 				is_collision[0] = True
#
# 		pos.y += normalized_direction.y * self.speed * delta
# 		hitbox = self.hitbox.rect
# 		if 0 < normalized_direction.y:
# 			bottom_left_tile = self.level.get_tile(hitbox.bottomleft)
# 			if bottom_left_tile:
# 				pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
# 				is_collision[1] = True
#
# 			bottom_right_tile = self.level.get_tile(hitbox.bottomright)
# 			if bottom_right_tile:
# 				pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
# 				is_collision[1] = True
# 		elif normalized_direction.y < 0:
# 			top_left_tile = self.level.get_tile(hitbox.topleft)
# 			if top_left_tile:
# 				pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
# 				is_collision[1] = True
#
# 			top_right_tile = self.level.get_tile(hitbox.topright)
# 			if top_right_tile:
# 				pos.y = (get_1d_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
# 				is_collision[1] = True
#
# 		return is_collision

class Movement:
	def __init__(self, speed: float, drag: float, level: Level, hitbox: BoxCollider):
		self.speed = speed
		self.drag = drag

		self.velocity = pygame.Vector2()

		self.level = level
		self.hitbox = hitbox

	def move_in_direction(self, pos: pygame.Vector2, direction: pygame.Vector2, delta: float):
		normalized_direction = direction.copy()
		if normalized_direction.length() != 0:
			normalized_direction.normalize_ip()

		acceleration = normalized_direction * self.speed

		is_collision = [False, False]

		pos.x += self.velocity.x * delta + 0.5 * acceleration.x * delta ** 2
		hitbox = self.hitbox.rect
		if 0 < self.velocity.x:
			top_right_tile = self.level.get_tile(hitbox.topright)
			if top_right_tile:
				pos.x = (get_1d_tile_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
				is_collision[0] = True

			bottom_right_tile = self.level.get_tile(hitbox.bottomright)
			if bottom_right_tile:
				pos.x = (get_1d_tile_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE - hitbox.width / 2 - 1
				is_collision[0] = True
		elif self.velocity.x < 0:
			top_left_tile = self.level.get_tile(hitbox.topleft)
			if top_left_tile:
				pos.x = (get_1d_tile_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
				is_collision[0] = True

			bottom_left_tile = self.level.get_tile(hitbox.bottomleft)
			if bottom_left_tile:
				pos.x = (get_1d_tile_pos(hitbox.x, TILE_SIZE) + 1) * TILE_SIZE + hitbox.width / 2 + 1
				is_collision[0] = True

		if is_collision[0]:
			self.velocity.x = 0

		pos.y += self.velocity.y * delta + 0.5 * acceleration.y * delta ** 2
		hitbox = self.hitbox.rect
		if 0 < self.velocity.y:
			bottom_left_tile = self.level.get_tile(hitbox.bottomleft)
			if bottom_left_tile:
				pos.y = (get_1d_tile_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
				is_collision[1] = True

			bottom_right_tile = self.level.get_tile(hitbox.bottomright)
			if bottom_right_tile:
				pos.y = (get_1d_tile_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE - 1
				is_collision[1] = True
		elif self.velocity.y < 0:
			top_left_tile = self.level.get_tile(hitbox.topleft)
			if top_left_tile:
				pos.y = (get_1d_tile_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
				is_collision[1] = True

			top_right_tile = self.level.get_tile(hitbox.topright)
			if top_right_tile:
				pos.y = (get_1d_tile_pos(hitbox.y, TILE_SIZE) + 1) * TILE_SIZE + hitbox.height + 1
				is_collision[1] = True

		if is_collision[1]:
			self.velocity.y = 0

		self.velocity += (acceleration - self.velocity * self.drag) * delta

		return is_collision
