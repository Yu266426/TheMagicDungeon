import random

import pygame

from data.modules.base.constants import TILE_SIZE
from data.modules.base.level import Level
from data.modules.entities.components.movement import Movement
from data.modules.entities.states.entity_state import EntityState


class WanderState(EntityState):
	def __init__(self, pos: pygame.Vector2, movement: Movement, level: Level, wander_range: int):
		self.pos = pos
		self.level = level

		self.movement = movement

		self.wander_range = (-wander_range * TILE_SIZE, wander_range * TILE_SIZE)

		self.target = None
		self.find_target()

		self.time_since_target = 0.0
		self.time_to_new_target = 2.0

	def find_target(self):
		random_target = (
			self.pos.x + random.randint(*self.wander_range),
			self.pos.y + random.randint(*self.wander_range)
		)

		tile = self.level.get_tile(random_target)
		if tile is not None:
			if tile.sprite_sheet_name != "walls":
				self.target = pygame.Vector2(random_target)
				self.time_since_target = 0
		else:
			if self.level.get_room(random_target) is not None:
				self.target = pygame.Vector2(random_target)
				self.time_since_target = 0

	def update(self, delta: float):
		if self.target is not None:
			self.movement.move_in_direction(self.pos, self.target - self.pos, delta)

			if self.pos.distance_to(self.target) < 20 or self.time_since_target > self.time_to_new_target:
				self.find_target()
				self.time_since_target = 0
				self.time_to_new_target = random.uniform(2, 4)
		else:
			self.find_target()

		self.time_since_target += delta
