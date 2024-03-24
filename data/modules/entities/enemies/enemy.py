import math

import pygame
import pygbase

from data.modules.entities.components.box_collider import BoxCollider
from data.modules.entities.components.health import Health
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.level import Level


class Enemy(Entity):
	ENEMY_TYPES: dict[str, type] = {}

	@classmethod
	def register_enemy(cls, enemy_type: str, enemy_class: type):
		if enemy_type in cls.ENEMY_TYPES:
			raise ValueError("Enemy type already exists")

		cls.ENEMY_TYPES[enemy_type] = enemy_class

	@classmethod
	def create_enemy(cls, enemy_type: str, pos: tuple | pygame.Vector2, level: Level, entity_manager: EntityManager):
		return cls.ENEMY_TYPES[enemy_type](pos, level, entity_manager)

	def __init__(self, pos: tuple | pygame.Vector2, level: Level, entity_manager: EntityManager, collider_size: tuple[int, int], health: int):
		super().__init__(pos)

		self.collider = BoxCollider(collider_size).link_pos(self.pos)
		self.movement = Movement(3000, 10, level, self.collider)

		self.health = Health(health)
		self.damage_timer = pygbase.Timer(0.6, True, False)

		self.visible = True

		self.entity_manager = entity_manager

	def damaged(self):
		pass

	def update(self, delta: float):
		self.damage_timer.tick(delta)

		if self.damage_timer.done():
			damage_entities = self.entity_manager.get_entities_of_tag("damage")
			for entity in damage_entities:
				if self.collider.collides_with(entity.collider):
					# print(entity)
					self.health.damage(entity.damage)

					dir_vec = entity.pos - self.pos
					if dir_vec.length() != 0:
						dir_vec.normalize_ip()

					self.movement.velocity -= dir_vec * 2000

					self.damage_timer.start()

					self.damaged()
					break

		# Flashing hit effect
		self.visible = self.damage_timer.done() or not math.sin(pygame.time.get_ticks() / 25) > 0

	def is_alive(self):
		return self.health.is_alive()
