import pygame

from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.level import Level


class EnemyBuilder:
	ENEMY_TYPES: dict[str, type] = {}

	@classmethod
	def register_enemy(cls, enemy_type: str, enemy_class: type):
		if enemy_type in cls.ENEMY_TYPES:
			raise ValueError("Enemy type already exists")

		cls.ENEMY_TYPES[enemy_type] = enemy_class

	@classmethod
	def create_enemy(cls, enemy_type: str, pos: tuple | pygame.Vector2, level: Level, entity_manager: EntityManager) -> "Enemy":
		return cls.ENEMY_TYPES[enemy_type](pos, level, entity_manager)
