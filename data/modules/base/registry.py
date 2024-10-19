import logging

from data.modules.entities.enemies.melee_enemy import MeleeEnemy
from data.modules.entities.states.melee_attack_state import MeleeAttackState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.objects.altars import RuneAltar
from data.modules.objects.torch import Torch


class Registry:
	_registered_types: dict[type, dict[str, type]] = {}

	@classmethod
	def register(cls):
		logging.info("Registering objects")

		cls.register_type("torch", Torch)
		cls.register_type("rune_altar", RuneAltar)

		logging.info("Registering enemies")

		cls.register_type("melee", MeleeEnemy)

		logging.info("Registering entity states")

		cls.register_type("wander", WanderState)
		cls.register_type("stunned", StunnedState)
		cls.register_type("melee_attack", MeleeAttackState)

	@classmethod
	def register_type(cls, type_name: str, type_to_register: type):
		base_class = type_to_register.__bases__[0]

		if base_class not in cls._registered_types:
			cls._registered_types[base_class] = {}

		if type_name in cls._registered_types:
			raise ValueError(f"Type <{type_name}> already in registered types")

		cls._registered_types[base_class][type_name] = type_to_register

	@classmethod
	def get_type[T](cls, type_name: str, base_class: type[T]) -> T:
		if type_name not in cls._registered_types:
			raise ValueError(f"Type <{type_name}> not in registered types")

		return cls._registered_types[base_class][type_name]
