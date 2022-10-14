import json
import os
from collections import deque
from enum import Enum

import pygame.image

from data.modules.base.files import SPRITE_SHEET_DIR, IMAGE_DIR
from data.modules.graphics.sprite_sheet import SpriteSheet


class ResourceTypes(Enum):
	SPRITE_SHEET = 1
	IMAGE = 2


class ResourceManager:
	__max_load_per_update: int = 1

	__resources_to_load: deque[tuple[ResourceTypes, str, str]] = deque()
	__loaded_resources: dict = {}

	@staticmethod
	def __generate_sprite_sheet_config(config_path: str, file_name: str) -> None:
		"""
		Generates default config for a sprite_sheet if one does not exist

		:param config_path: Path of sprite sheet config
		:param file_name: Name of sprite sheet
		:return: None
		"""

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
	def __generate_image_config(config_path: str, file_name: str) -> None:
		"""
		Generates default config for an image if one does not exist

		:param config_path: Path of image config
		:param file_name: Name of image
		:return: None
		"""
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
	def init_load(cls):
		# * Sprite Sheets
		# Create default config for sprite_sheets, if none exist
		sprite_sheet_config_path = os.path.join(SPRITE_SHEET_DIR, "config.json")
		if not os.path.isfile(sprite_sheet_config_path):
			with open(sprite_sheet_config_path, "x") as sprite_sheet_config_file:
				sprite_sheet_data = {"sprite_sheets": {}}
				sprite_sheet_config_file.write(json.dumps(sprite_sheet_data))

		# Walk through sprite_sheets dir, appending all pngs for loading
		for dir_path, _, file_names in os.walk(SPRITE_SHEET_DIR):
			for file_name in file_names:
				if file_name.endswith(".png"):
					file_path = os.path.join(dir_path, file_name)

					cls.__generate_sprite_sheet_config(sprite_sheet_config_path, file_name)
					cls.__resources_to_load.append((ResourceTypes.SPRITE_SHEET, file_name[:-4], file_path))

		# * Images
		image_config_path = os.path.join(IMAGE_DIR, "config.json")
		if not os.path.isfile(image_config_path):
			with open(image_config_path, "x") as image_config_file:
				image_config_data = {"images": {}}
				image_config_file.write(json.dumps(image_config_data))

		for dir_path, _, file_names in os.walk(IMAGE_DIR):
			for file_name in file_names:
				if file_name.endswith(".png"):
					file_path = os.path.join(dir_path, file_name)

					cls.__generate_image_config(image_config_path, file_name)
					cls.__resources_to_load.append((ResourceTypes.IMAGE, file_name[:-4], file_path))

	@classmethod
	def load_update(cls):
		# If all resources are loaded
		if len(cls.__resources_to_load) == 0:
			print(f"Loaded {len(cls.__loaded_resources[ResourceTypes.SPRITE_SHEET])} sprite sheets")
			print(f"Loaded {len(cls.__loaded_resources[ResourceTypes.IMAGE])} images")
			return True

		# Load resources
		else:
			# Only loads max_load_per_update resources per update
			for _ in range(cls.__max_load_per_update):
				if len(cls.__resources_to_load) > 0:
					# Get resources info
					resource_info = cls.__resources_to_load.popleft()
					print(f"Loading: {resource_info[2]}")

					# * If resource is a sprite sheet
					if resource_info[0] == ResourceTypes.SPRITE_SHEET:
						# Ensure the key is present
						if ResourceTypes.SPRITE_SHEET not in cls.__loaded_resources:
							cls.__loaded_resources[ResourceTypes.SPRITE_SHEET] = {}

						# Read from sprite sheet config
						with open(os.path.join(SPRITE_SHEET_DIR, "config.json")) as config:
							data = json.load(config)
							data = data["sprite_sheets"][resource_info[1]]

						# Makes sure the config is initialized
						if data["scale"] != -1:
							cls.__loaded_resources[ResourceTypes.SPRITE_SHEET][resource_info[1]] = SpriteSheet(resource_info, data)
						else:
							print(f"WARNING: Skipping {resource_info[2]}, uninitialized config")

					# * If resource is an image
					if resource_info[0] == ResourceTypes.IMAGE:
						if ResourceTypes.IMAGE not in cls.__loaded_resources:
							cls.__loaded_resources[ResourceTypes.IMAGE] = {}

						with open(os.path.join(IMAGE_DIR, "config.json")) as config:
							data = json.load(config)
							data = data["images"][resource_info[1]]

						scale = data["scale"]

						image = pygame.image.load(resource_info[2]).convert_alpha()
						image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
						cls.__loaded_resources[ResourceTypes.IMAGE][resource_info[1]] = image

			return False

	@classmethod
	def get_resource(cls, resource_type: ResourceTypes, resource_name) -> SpriteSheet | pygame.Surface:
		return cls.__loaded_resources[resource_type][resource_name]
