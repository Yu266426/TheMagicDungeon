import json
import os
from collections import deque
from enum import Enum
from typing import Any, Callable

import pygame

from .files import SPRITE_SHEET_DIR, IMAGE_DIR
from .graphics.sprite_sheet import SpriteSheet


class ResourceTypes(Enum):
	SPRITE_SHEET = 1
	IMAGE = 2


class ResourceManager:
	_max_load_per_update: int = 1

	_resources_to_load: deque[tuple[ResourceTypes, str, str]] = deque()
	_loaded_resources: dict[ResourceTypes, dict[str, Any]] = {}

	@staticmethod
	def _generate_sprite_sheet_config(config_path: str, file_name: str) -> None:
		with open(config_path, "r") as file:
			data = json.load(file)

		sprite_sheet_name = file_name[:-4]
		if sprite_sheet_name not in data["sprite_sheets"]:
			sprite_sheet_data = {
				"rows": 0,
				"columns": 0,
				"tile_width": 0,
				"tile_height": 0,
				"scale": -1
			}

			data["sprite_sheets"][sprite_sheet_name] = sprite_sheet_data

			with open(config_path, "w") as file:
				file.write(json.dumps(data))

	@staticmethod
	def _generate_image_config(config_path: str, file_name: str) -> None:
		with open(config_path, "r") as file:
			data = json.load(file)

		image_name = file_name[:-4]
		if image_name not in data["images"]:
			image_data = {
				"scale": 1
			}

			data["images"][image_name] = image_data

			with open(config_path, "w") as file:
				file.write(json.dumps(data))

	@classmethod
	def _init_for_resource(cls, resource_type: ResourceTypes, path: str, init_data: dict, generate_config_function: Callable[[str, str], None]):
		config_path = os.path.join(path, "config.json")

		# Create config if it does not exist
		if not os.path.isfile(config_path):
			with open(config_path, "x") as config_file:
				config_file.write(json.dumps(init_data))

		for dir_path, _, file_names in os.walk(path):
			for file_name in file_names:
				if file_name.endswith(".png"):
					file_path = os.path.join(dir_path, file_name)

					generate_config_function(config_path, file_name)
					cls._resources_to_load.append((resource_type, file_name[:-4], file_path))

		cls._loaded_resources[resource_type] = {}

	@classmethod
	def init_load(cls):
		# * Sprite Sheets
		cls._init_for_resource(ResourceTypes.SPRITE_SHEET, SPRITE_SHEET_DIR, {"sprite_sheets": {}}, cls._generate_sprite_sheet_config)

		# * Images
		cls._init_for_resource(ResourceTypes.IMAGE, IMAGE_DIR, {"images": {}}, cls._generate_image_config)

	@classmethod
	def load_update(cls):
		# If all resources are loaded
		if len(cls._resources_to_load) == 0:
			print(f"Loaded {len(cls._loaded_resources[ResourceTypes.SPRITE_SHEET])} sprite sheets")
			print(f"Loaded {len(cls._loaded_resources[ResourceTypes.IMAGE])} images")
			return True

		# Load resources
		else:
			# Only loads max_load_per_update resources per update
			for _ in range(cls._max_load_per_update):
				if len(cls._resources_to_load) > 0:
					# Get resources info
					resource_info = cls._resources_to_load.popleft()

					resource_type = resource_info[0]
					resource_name = resource_info[1]
					resource_path = resource_info[2]

					print(f"Loading: {resource_path}")

					# * If resource is a sprite sheet
					if resource_type == ResourceTypes.SPRITE_SHEET:
						# Ensure the key is present
						if ResourceTypes.SPRITE_SHEET not in cls._loaded_resources:
							cls._loaded_resources[ResourceTypes.SPRITE_SHEET] = {}

						# Read from sprite sheet config
						with open(os.path.join(SPRITE_SHEET_DIR, "config.json")) as config:
							data = json.load(config)
							data = data["sprite_sheets"][resource_name]

						# Makes sure the config is initialized
						if data["scale"] != -1:
							cls._loaded_resources[ResourceTypes.SPRITE_SHEET][resource_name] = SpriteSheet(resource_info, data)
						else:
							print(f"WARNING: Skipping {resource_path}, uninitialized config")

					# * If resource is an image
					elif resource_type == ResourceTypes.IMAGE:
						if ResourceTypes.IMAGE not in cls._loaded_resources:
							cls._loaded_resources[ResourceTypes.IMAGE] = {}

						with open(os.path.join(IMAGE_DIR, "config.json")) as config:
							data = json.load(config)
							data = data["images"][resource_name]

						scale = data["scale"]

						image = pygame.image.load(resource_path).convert_alpha()
						image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
						cls._loaded_resources[ResourceTypes.IMAGE][resource_name] = image

			return False

	@classmethod
	def get_resource(cls, resource_type: ResourceTypes, resource_name) -> SpriteSheet | pygame.Surface:
		return cls._loaded_resources[resource_type][resource_name]

	@classmethod
	def get_resources_of_type(cls, resource_type: ResourceTypes):
		return cls._loaded_resources[resource_type]
