import logging

from data.modules.entities.enemies.melee_enemy import MeleeEnemy
from data.modules.entities.enemies.enemy import Enemy


class EnemyRegistry:
	_registered_enemies: dict[str, type[Enemy]] = {}

	@classmethod
	def register_enemies(cls):
		logging.info("Registering enemies")

		cls._register_enemy_type("melee", MeleeEnemy)

	@classmethod
	def _register_enemy_type(cls, enemy_type: str, enemy_class: type[Enemy]):
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
