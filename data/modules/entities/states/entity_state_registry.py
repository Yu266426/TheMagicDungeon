import logging

from data.modules.entities.states.entity_state import EntityState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState


class EntityStateRegistry:
	_registered_states: dict[str, type[EntityState]] = {}

	@classmethod
	def register_state(cls, state_name: str, state: type[EntityState]):
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

def register_entity_states():
	logging.info("Registering entity states")

	EntityStateRegistry.register_state("wander", WanderState)
	EntityStateRegistry.register_state("stunned", StunnedState)
