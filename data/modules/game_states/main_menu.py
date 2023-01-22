import pygame

from data.modules.game_states.game_state import GameState
from data.modules.ui.element import Frame, Button
from data.modules.ui.screen import UIScreen


class MainMenu(GameState):
	def __init__(self):
		self.ui = UIScreen()

		self.next_game_state = ""

		self.button_frame = Frame((200, 200), (400, 400))
		self.ui.add_frame(self.button_frame)

		self.button_frame.add_element(Button((0, 0), "main_menu_button", self.set_next_state, "game", text="Start"))
		self.button_frame.add_element(Button((0, 30), "main_menu_button", self.set_next_state, "editor", text="Editor"), add_on_to_previous=(False, True))

	def set_next_state(self, next_state):
		self.next_game_state = next_state

	def next_state(self):
		if self.next_game_state == "":
			return self
		elif self.next_game_state == "game":
			from data.modules.game_states.game import Game
			return Game()
		elif self.next_game_state == "editor":
			from data.modules.game_states.editor import Editor
			return Editor()

	def update(self, delta: float):
		self.ui.update(delta)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)
