import json
import logging
import os

import pygame

from data.modules.base.paths import ENEMY_DIR
from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.enemies.enemy_registry import EnemyRegistry
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_registry import EntityStateRegistry
from data.modules.level.level import Level


class EnemyLoader:
	# enemy_name: (enemy_type, health, hitbox, animations_data, states_data)
	# animations_data: {animation_name: (sprite_sheet, start_index, length, speed)}
	# states_data: {state_name: (depends on state)}
	_enemy_data: dict[str, tuple] = {}

	@classmethod
	def init(cls):
		for enemy_file in os.listdir(ENEMY_DIR):
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
		try:
			enemy_type = EnemyRegistry.get_enemy_type(enemy_type_name)
		except ValueError:
			raise ValueError(f"Loading {enemy_name}: enemy_type <{enemy_type_name}> not in registered enemies")

		data_to_save = {
			"type": enemy_type_name,
			"health": -1,
			"hitbox": [-1, -1],
			"animations": {},
			"states": {}
		}

		animations = data_to_save["animations"]
		for animation in enemy_type.REQUIRED_ANIMATIONS:
			animations[animation] = {
				"sprite_sheet": "",
				"start_index": -1,
				"length": -1,
				"speed": -1
			}

		states = data_to_save["states"]
		for state_name in enemy_type.REQUIRED_STATES:
			state = EntityStateRegistry.get_state_type(state_name)

			states[state_name] = {}
			for data_name, data_type in state.REQUIRED_DATA:
				if data_type is int:
					initial_value = -1
				elif data_type is float:
					initial_value = -1.0
				else:
					raise ValueError(f"Data type <{data_type}> for entity state \"{state_name}\".{data_name} not supported")

				states[state_name][data_name] = initial_value

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
		state_data = {}
		for state_name, state in states_data.items():
			state_data[state_name] = state

		cls._enemy_data[enemy_name] = (
			enemy_type,
			health,
			hitbox,
			animation_data,
			state_data
		)

	@classmethod
	def create_enemy(cls, enemy_name: str, pos: pygame.typing.Point, level: Level, entity_manager: EntityManager) -> "Enemy":
		enemy_data = cls._enemy_data[enemy_name]

		return EnemyRegistry.get_enemy_type(enemy_data[0])(
			pos,
			level,
			entity_manager,
			enemy_data[2],  # Hitbox
			enemy_data[1],  # Health,
			enemy_data[3],  # Animation data
			enemy_data[4]  # State data
		)
