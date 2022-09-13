import pygame

from data.modules.base.resources import ResourceManager
from data.modules.game_states.game_state import GameState


class Loading(GameState):
	def __init__(self):
		ResourceManager.init_load()

		self.should_switch = False

	def next_state(self):
		if self.should_switch:
			from data.modules.game_states.game import Game
			return Game()
		return self

	def update(self, delta: float):
		self.should_switch = ResourceManager.load_update()

	def draw(self, display: pygame.Surface):
		display.fill((0, 0, 0))
