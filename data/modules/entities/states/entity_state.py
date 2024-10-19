class EntityState:
	def on_enter(self):
		pass

	def update(self, delta: float):
		pass

	def next_state(self) -> str:
		return ""
