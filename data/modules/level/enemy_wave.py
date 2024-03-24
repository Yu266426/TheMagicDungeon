from typing import TYPE_CHECKING

from data.modules.entities.entity_manager import EntityManager

if TYPE_CHECKING:
	from data.modules.level.level import Level
	from data.modules.level.room import Room


class EnemyWave:
	def __init__(self, wave_data: dict, entity_manager: EntityManager):
		self.entity_manager = entity_manager

		self.wave_data: dict = wave_data
		self.enemies = []

		self.wave_in_progress = False

	def spawn_wave(self, level: "Level", room: "Room"):
		from data.modules.entities.enemies.enemy import Enemy

		if not self.wave_in_progress:
			for enemy_type, num_enemies in self.wave_data.items():
				for _ in range(num_enemies):
					enemy = Enemy.create_enemy(enemy_type, room.generate_spawn_pos(), level, self.entity_manager)

					self.enemies.append(enemy)
					self.entity_manager.add_entity(enemy)

		self.wave_in_progress = True
