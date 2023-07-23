import json
import logging
import os

import pygame
import pygbase

from data.modules.base.paths import OBJECT_DIR
from data.modules.objects.game_object import GameObject
from data.modules.objects.object_registry import ObjectRegistry


class ObjectLoader:
	# object_name: (object_type, sprite, hitbox, behaviour) for static and animated
	# object_name: (object_type, object_class) for custom
	objects: dict[str, tuple] = {}

	@classmethod
	def init(cls):
		for object_file in os.listdir(OBJECT_DIR):
			cls.load_object(object_file[:-5])

		logging.info(f"Loaded {len(cls.objects)} objects")

	@classmethod
	def load_object(cls, object_name: str):
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
			sprite_sheet_name = data["sprite_sheet_name"]

			cls.objects[object_name] = (
				object_type,
				pygbase.ResourceManager.get_resource("sprite_sheet", sprite_sheet_name).get_image(data["image_index"]),
				hitbox,
				behaviour,
				tags
			)
		elif object_type == "animated":
			sprite_sheet_name = data["sprite_sheet_name"]

			cls.objects[object_name] = (
				object_type,
				("sprite_sheet", sprite_sheet_name, data["animation_start_index"], data["animation_length"], data["animation_looping"]),
				hitbox,
				behaviour,
				tags
			)
		elif object_type == "custom":
			cls.objects[data["name"]] = (
				object_type,
				ObjectRegistry.get_object_type(data["name"]),
				tags
			)
		else:
			raise ValueError(f"{object_name} object file has invalid type <{type}>")

	@classmethod
	def create_object(cls, name: str, pos: pygame.Vector2 | tuple, pixel_pos: bool = False) -> tuple[GameObject, tuple[str, ...]]:
		object_data = cls.objects[name]
		if object_data[0] == "static":
			return GameObject(name, pos, pixel_pos, object_data[1], custom_hitbox=object_data[2]), object_data[4]
		elif object_data[0] == "animated":
			return GameObject(name, pos, pixel_pos, pygbase.Animation(*object_data[1]), custom_hitbox=object_data[2]), object_data[4]
		elif object_data[0] == "custom":
			return object_data[1](pos, pixel_pos), object_data[2]
