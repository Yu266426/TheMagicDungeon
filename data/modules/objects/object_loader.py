import json
import logging
import os

import pygame
import pygbase

from data.modules.base.paths import OBJECT_DIR
from data.modules.base.registry.registry import Registry
from data.modules.objects.game_object import GameObject


# TODO: Conform to Loader
class ObjectLoader:
	# object_name: (object_type, sprite, hitbox, behaviour, tags) for static and animated
	# object_name: (object_type, object_class, tags) for custom
	object_data: dict[str, tuple] = {}

	@classmethod
	def init(cls):
		for object_file in os.listdir(OBJECT_DIR):
			name, extension = object_file.split(".")

			if extension == "json":
				cls._load_object(name)
			else:
				logging.warning(f"Non .json file \"{object_file}\" found in objects directory")

		logging.info(f"Loaded {len(cls.object_data)} objects")

	@classmethod
	def _load_object(cls, object_name: str):
		json_path = OBJECT_DIR / f"{object_name}.json"

		with open(json_path) as json_file:
			data = json.load(json_file)

		# Shared optional data
		hitbox = None
		behaviour = None
		tags = ()

		if "hitbox" in data:
			hitbox = data["custom_hitbox"]

		# TODO: Make behaviour do something
		if "behaviour" in data:
			behaviour = data["behaviour"]

		if "tags" in data:
			tags = tuple(data["tags"])

		# Type-dependent data
		object_type: str = data["type"]
		if object_type == "static":
			sprite_sheet_name = data["sprite_sheet"]

			cls.object_data[object_name] = (
				object_type,
				pygbase.ResourceManager.get_resource("sprite_sheets", sprite_sheet_name).get_image(data["image_index"]),
				hitbox,
				behaviour,
				tags
			)
		elif object_type == "animated":
			sprite_sheet_name = data["sprite_sheet"]

			cls.object_data[object_name] = (
				object_type,
				("sprite_sheets", sprite_sheet_name, data["animation_start_index"], data["animation_length"], data["animation_looping"]),
				hitbox,
				behaviour,
				tags
			)
		elif object_type == "custom":
			cls.object_data[data["name"]] = (
				object_type,
				Registry.get_type(data["name"], GameObject),
				tags
			)
		else:
			raise ValueError(f"{object_name} object file has invalid type <{type}>")

	@classmethod
	def create_object(cls, name: str, pos: pygame.typing.Point, is_pixel: bool = False) -> tuple[GameObject, tuple[str, ...]]:
		"""
		Creates an object based on inputs

		:param name: Name of object
		:param pos: Position to spawn object at
		:param is_pixel: If position is in tiles or pixels
		:return: tuple[object, tags]
		"""
		object_data = cls.object_data[name]
		if object_data[0] == "static":
			return GameObject(
				name,
				pos,
				is_pixel,
				object_data[1],  # Sprite
				custom_hitbox=object_data[2]
			), object_data[4]

		elif object_data[0] == "animated":
			return (GameObject(
				name,
				pos,
				is_pixel,
				pygbase.Animation(*object_data[1]),  # Animation data
				custom_hitbox=object_data[2]
			), object_data[4])

		elif object_data[0] == "custom":
			return object_data[1](pos, is_pixel), object_data[2]
