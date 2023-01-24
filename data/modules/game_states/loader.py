import pygame

from data.modules.base.resources import ResourceManager
from data.modules.game_states.game_state import GameState, GameStateIds


class Loading(GameState):
	def __init__(self):
		super().__init__(GameStateIds.LOADING)

		ResourceManager.init_load()

		self.should_switch = False

	def next_state(self) -> GameState:
		if self.should_switch:
			from data.modules.game_states.main_menu import MainMenu

			return MainMenu()
		return self

	def update(self, delta: float):
		self.should_switch = ResourceManager.load_update()

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))
