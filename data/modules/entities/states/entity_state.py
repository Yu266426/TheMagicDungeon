class EntityState:
	REQUIRED_DATA: tuple[tuple[str, type], ...] = ()

	def __init_subclass__(cls, **kwargs):
		# This is used by enemy loader to determine what information to give when creating enemy
		if "requires" in kwargs:
			requires = kwargs["requires"]
			if not isinstance(requires, tuple):
				raise TypeError("\"requires\" argument in EntityState subclass should by of type tuple[str, ...]")

			cls.REQUIRED_DATA = requires

	def on_enter(self):
		pass

	def update(self, delta: float):
		pass

	def next_state(self) -> str:
		return ""
