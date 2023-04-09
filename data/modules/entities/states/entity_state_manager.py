from data.modules.entities.states.entity_state import EntityState


class EntityStateManager:
	def __init__(self, states: dict[str, EntityState], current_state: str):
		self.current_state = current_state
		self.states = states

	def update(self, delta: float):
		next_state = self.states[self.current_state].next_state()
		if next_state != "":
			self.current_state = next_state

		self.states[self.current_state].update(delta)
