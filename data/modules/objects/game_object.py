import json
import logging
import os

import pygame
import pygbase
from pygbase import Camera

from data.modules.base.paths import OBJECT_DIR
from data.modules.entities.entity import Entity


class GameObject(Entity):
	def __init__(self, name: str, pos: tuple, sprite: pygbase.Image | pygbase.Animation, custom_hitbox: pygame.Rect | None = None):
		super().__init__(pos)
		self.name = name

		self.sprite = sprite
		self.is_animation = isinstance(self.sprite, pygbase.Animation)
		if self.is_animation:
			self.rect = self.sprite.get_current_image().get_image(0).get_rect(midbottom=self.pos)
		else:
			self.rect = self.sprite.get_image(0).get_rect(midbottom=self.pos)

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def animate(self, frame_time: float):
		if self.is_animation:
			self.sprite.change_frame(frame_time)

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, flags=0):
		if self.is_animation:
			self.sprite.draw_at_pos(display, self.pos, camera, flags=flags)
		else:
			self.sprite.draw(display, camera.world_to_screen(self.pos), flags=flags)


class ObjectLoader:
	# object_name: (sprite, hitbox, behaviour)
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

		# Shared data
		sprite_sheet_name = data["sprite_sheet_name"]

		# Optional data
		if "hitbox" in data:
			hitbox = data["custom_hitbox"]
		else:
			hitbox = None

		# TODO: Make behaviour do something
		if "behaviour" in data:
			behaviour = data["behaviour"]
		else:
			behaviour = None

		# Type-dependent data
		object_type: str = data["type"]
		if object_type == "static":
			cls.objects[object_name] = (
				object_type,
				pygbase.ResourceManager.get_resource(pygbase.Common.get_resource_type("sprite_sheet"), sprite_sheet_name).get_image(data["image_index"]),
				hitbox,
				behaviour
			)
		elif object_type == "animated":
			cls.objects[object_name] = (
				object_type,
				(sprite_sheet_name, data["animation_start_index"], data["animation_length"], data["animation_looping"]),
				hitbox,
				behaviour
			)
		else:
			raise ValueError(f"{object_name} object file has invalid type <{type}>")

	@classmethod
	def create_object(cls, name: str, pos) -> GameObject:
		object_data = cls.objects[name]
		if object_data[0] == "static":
			return GameObject(name, pos, object_data[1], custom_hitbox=object_data[2])
		else:
			return GameObject(name, pos, pygbase.Animation(*object_data[1]), custom_hitbox=object_data[2])
