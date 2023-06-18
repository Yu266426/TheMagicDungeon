from data.modules.objects.game_object import GameObject
from data.modules.objects.torch import Torch, EditorTorch


class ObjectRegistry:
	_registered_objects: dict[str, type[GameObject]] = {}

	@classmethod
	def register_object(cls, name, game_object: type[GameObject]):
		if issubclass(game_object, GameObject):
			if name not in cls._registered_objects:
				cls._registered_objects[name] = game_object
			else:
				raise ValueError(f"Name <{name}> already in registered objects")
		else:
			raise TypeError(f"Provided type <{game_object} not subclass of <GameObject>")

	@classmethod
	def get_object_type(cls, name: str) -> type[GameObject]:
		if name in cls._registered_objects:
			return cls._registered_objects[name]
		else:
			raise ValueError(f"Name <{name}> not in registered objects")


ObjectRegistry.register_object("torch", Torch)
ObjectRegistry.register_object("editor_torch", EditorTorch)
