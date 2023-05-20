import pygame
import pygbase

from data.modules.entities.components.movement import Movement
from data.modules.entities.states.entity_state import EntityState


class StunnedState(EntityState):
	def __init__(self, stunned_time: float, after_state: str, pos: pygame.Vector2, movement: Movement):
		self.timer = pygbase.Timer(stunned_time, True, False)

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
		else:
			return ""
