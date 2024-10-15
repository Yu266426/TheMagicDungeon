import logging

from data.modules.objects.altars import RuneAltar
from data.modules.objects.game_object import GameObject
from data.modules.objects.torch import Torch


class ObjectRegistry:
	_registered_objects: dict[str, type[GameObject]] = {}

	@classmethod
	def register_object(cls, object_name: str, game_object: type[GameObject]):
		if not issubclass(game_object, GameObject):
			raise TypeError(f"Provided type <{game_object} not subclass of <GameObject>")

		if object_name in cls._registered_objects:
			raise ValueError(f"Object <{object_name}> already in registered objects")

		cls._registered_objects[object_name] = game_object

	@classmethod
	def get_object_type(cls, object_name: str) -> type[GameObject]:
		if object_name not in cls._registered_objects:
			raise ValueError(f"Object <{object_name}> not in registered objects")

		return cls._registered_objects[object_name]

def register_objects():
	logging.info("Registering objects")

	ObjectRegistry.register_object("torch", Torch)
	ObjectRegistry.register_object("rune_altar", RuneAltar)
