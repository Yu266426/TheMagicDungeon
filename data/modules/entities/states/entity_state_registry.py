import logging

from data.modules.entities.states.entity_state import EntityState
from data.modules.entities.states.melee_attack_state import MeleeAttackState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState


class EntityStateRegistry:
	_registered_states: dict[str, type[EntityState]] = {}

	@classmethod
	def register_states(cls):
		logging.info("Registering entity states")

		cls._register_state("wander", WanderState)
		cls._register_state("stunned", StunnedState)
		cls._register_state("melee_attack", MeleeAttackState)

	@classmethod
	def _register_state(cls, state_name: str, state: type[EntityState]):
		if not issubclass(state, EntityState):
			raise TypeError(f"Provided type <{state} not subclass of <GameObject>")

		if state_name in cls._registered_states:
			raise ValueError(f"State <{state_name}> already in registered states")

		cls._registered_states[state_name] = state

	@classmethod
	def get_state_type(cls, state_name: str) -> type[EntityState]:
		if state_name not in cls._registered_states:
			raise ValueError(f"State <{state_name}> not in registered states")

		return cls._registered_states[state_name]
