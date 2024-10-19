import logging

from typing_extensions import get_origin

from data.modules.base.animation_data import AnimationData
from data.modules.base.registrable import Registrable


class Registry[T: Registrable]:
	_registered_types: dict[type, dict[str, type[T]]] = {}
	_pure_registered_types: set[type] = set()
	_required_data: dict[type, dict[str, dict[str, ...]]] = {}

	@classmethod
	def init(cls):
		cls.register_type(AnimationData)

	@classmethod
	def register_type(cls, type_to_register: type[T]):
		# Pure type (Used only to provide data)
		if type_to_register.get_is_pure():
			base_class = type_to_register
			cls._pure_registered_types.add(type_to_register)
		else:
			base_class = type_to_register.__bases__[0]

		if base_class not in cls._registered_types:
			cls._registered_types[base_class] = {}

		type_name = type_to_register.get_name()
		required_data = type_to_register.get_required_component()

		if type_name in cls._registered_types:
			raise ValueError(f"Type <{type_name}> already in registered types")

		cls._registered_types[base_class][type_name] = type_to_register
		cls._generate_required_data(type_name, base_class, required_data)

	@classmethod
	def get_required_data(cls, type_name: str, base_class: type) -> dict[str, ...]:
		return cls._required_data[base_class][type_name]

	@classmethod
	def _check_pure_type(cls, base_class: type) -> bool:
		return base_class in cls._pure_registered_types

	@classmethod
	def _generate_required_data(cls, type_name: str, base_class: type, required_data: tuple[tuple[str, type], ...]):
		required_components = {}

		for required_tuple in required_data:
			required_component = required_tuple[0]
			component_type = required_tuple[1]

			if component_type is int:
				default_value = 0
			elif component_type is float:
				default_value = 0.0
			elif component_type is str:
				default_value = ""
			elif get_origin(component_type) is tuple:
				default_value = {}

				# When type is a tuple, give (name, tuple[tuple_type], (str, ...))
				tuple_type = component_type.__args__[0]  # NoQA
				is_pure_type = cls._check_pure_type(tuple_type)

				tuple_data = required_tuple[2]
				for name in tuple_data:
					if is_pure_type:
						default_value[name] = cls.get_required_data(tuple_type.get_name(), tuple_type)
					else:
						default_value[name] = cls.get_required_data(name, tuple_type)
			else:
				default_value = ""
				logging.warning(f"Unknown type <{component_type}> in REQUIRED_DATA for {type_name}")

			required_components[required_component] = default_value

		cls._required_data.setdefault(base_class, {})[type_name] = required_components

	@classmethod
	def get_type[B](cls, type_name: str, base_class: type[B]) -> type[B]:
		if base_class not in cls._registered_types:
			raise ValueError(f"Class type <{base_class}> not in registered types")

		if type_name not in cls._registered_types[base_class]:
			raise ValueError(f"Type <{type_name}> not in registered types")

		return cls._registered_types[base_class][type_name]
