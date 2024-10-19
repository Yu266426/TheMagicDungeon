import json
import logging
import os

import pygame

from data.modules.base.paths import ENEMY_DIR
from data.modules.base.registry import Registry
from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.level import Level


class EnemyLoader:
	# enemy_name: (enemy_type, health, hitbox, dict[animations, states])
	# animations: {animation_name: (sprite_sheet, start_index, length, speed)}
	# states: {state_name: (depends on state)}
	_enemy_data: dict[str, tuple[str, int, tuple[int, int], dict[str, ...]]] = {}

	@classmethod
	def init(cls):
		for enemy_file in os.listdir(ENEMY_DIR):
			if "." not in enemy_file:
				continue

			name, extension = enemy_file.split(".")

			if extension == "start":
				cls._init_file(name)
			elif extension == "json":
				cls._load(name)
			else:
				logging.warning(f"Non .start or .json file \"{enemy_file}\" found in enemy directory")

	@classmethod
	def _init_file(cls, enemy_name: str):
		"""
		Processes any .start files in enemy directory into a .json file to be edited
		"""

		starter_file_path = ENEMY_DIR / f"{enemy_name}.start"

		with open(starter_file_path) as starter_file:
			data_name = json.load(starter_file)

		enemy_type_name = data_name["type"]
		required_data = Registry.get_required_data(enemy_type_name, Enemy)

		data_to_save = {
			"type": enemy_type_name,
			"health": -1,
			"hitbox": [-1, -1],
			"animations": required_data["animations"],
			"states": required_data["states"]
		}

		# Save to .json file, and delete starter file
		json_file_path = ENEMY_DIR / f"{enemy_name}.json"
		with open(json_file_path, "x") as json_file:
			json_file.write(json.dumps(data_to_save, indent=2))

		os.remove(starter_file_path)

	@classmethod
	def _load(cls, enemy_name: str):
		json_file_path = ENEMY_DIR / f"{enemy_name}.json"

		with open(json_file_path) as json_file:
			data = json.load(json_file)

		enemy_type = data["type"]
		health = data["health"]
		hitbox = data["hitbox"]
		enemy_data = {}

		animations_data = data["animations"]
		animation_data = {}
		for animation_name, animation in animations_data.items():
			animation_data[animation_name] = (
				animation["sprite_sheet"],
				animation["start_index"],
				animation["length"],
				animation["speed"]
			)

		states_data = data["states"]

		enemy_data["animations"] = animation_data
		enemy_data["states"] = states_data

		cls._enemy_data[enemy_name] = (
			enemy_type,
			health,
			hitbox,
			enemy_data
		)

	@classmethod
	def create_enemy(cls, enemy_name: str, pos: pygame.typing.Point, level: Level, entity_manager: EntityManager) -> "Enemy":
		enemy_data = cls._enemy_data[enemy_name]

		return Registry.get_type(enemy_data[0], Enemy)(
			pos,
			level,
			entity_manager,
			enemy_data[2],  # Hitbox
			enemy_data[1],  # Health,
			enemy_data[3],  # Data
		)
