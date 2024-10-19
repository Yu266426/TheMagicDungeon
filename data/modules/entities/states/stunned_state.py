import pygame
import pygbase

from data.modules.base.registrable import Registrable
from data.modules.entities.components.movement import Movement
from data.modules.entities.states.entity_state import EntityState


class StunnedState(EntityState, Registrable):
	@staticmethod
	def get_name() -> str:
		return "stunned"

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type] | tuple[str, type, tuple[str, ...]], ...]:
		return ("time", int),

	def __init__(self, pos: pygame.Vector2, movement: Movement, after_state: str, data: dict[str, ...]):
		self.timer = pygbase.Timer(data["time"], False, False)

		self.after_state = after_state

		self.pos = pos
		self.movement = movement

	def on_enter(self):
		self.timer.start()

	def update(self, delta: float):
		self.timer.tick(delta)

		self.movement.move_in_direction(self.pos, pygame.Vector2(), delta)

	def next_state(self) -> str:
		if self.timer.done():
			return self.after_state

		return ""
