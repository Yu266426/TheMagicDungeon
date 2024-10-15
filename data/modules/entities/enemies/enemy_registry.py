import logging

from data.modules.entities.enemies.basic_enemy import BasicEnemy
from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.enemies.test_enemy import TestEnemy


class EnemyRegistry:
	_registered_enemies: dict[str, type[Enemy]] = {}

	@classmethod
	def register_enemy_type(cls, enemy_type: str, enemy_class: type[Enemy]):
		if not issubclass(enemy_class, Enemy):
			raise TypeError(f"Provided type <{enemy_type} not subclass of <Enemy>")

		if enemy_type in cls._registered_enemies:
			raise ValueError(f"Enemy type {enemy_type} already in registered enemy types")

		cls._registered_enemies[enemy_type] = enemy_class

	@classmethod
	def get_enemy_type(cls, enemy_type: str) -> type[Enemy]:
		if enemy_type not in cls._registered_enemies:
			raise ValueError(f"Enemy type <{enemy_type}> not in registered enemy types")

		return cls._registered_enemies[enemy_type]

def register_enemies():
	logging.info("Registering enemies")

	EnemyRegistry.register_enemy_type("basic", BasicEnemy)
	EnemyRegistry.register_enemy_type("test", TestEnemy)
