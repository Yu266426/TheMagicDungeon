from abc import ABC, abstractmethod


class Registrable(ABC):
	@staticmethod
	@abstractmethod
	def get_name() -> str:
		pass

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type] | tuple[str, type, tuple[str, ...]], ...]:
		return ()

	@staticmethod
	def get_is_pure():
		return False
