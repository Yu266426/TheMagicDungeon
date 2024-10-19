from data.modules.base.registrable import Registrable


class AnimationData(Registrable):
	@staticmethod
	def get_name() -> str:
		return "animation"

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type] | tuple[str, type, tuple[str, ...]], ...]:
		return ("sprite_sheet", str), ("start_index", int), ("length", int), ("speed", int)

	@staticmethod
	def get_is_pure():
		return True

	def __init__(self):
		pass
