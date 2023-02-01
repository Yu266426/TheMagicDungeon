import pygame
from pygbase import InputManager, EventManager
from pygbase.game_state import GameState
from pygbase.ui.element import Frame, Image, Button
from pygbase.ui.screen import UIScreen


class MainMenu(GameState):
	def __init__(self):
		super().__init__(2)

		self.ui = UIScreen()

		self.title_frame = self.ui.add_frame(Frame((150, 50), (500, 200)))
		self.title_frame.add_element(Image((0, 0), "main_title"))

		self.go_to_state = ""

		self.button_frame = self.ui.add_frame(Frame((220, 300), (360, 400)))
		self.ui.add_frame(self.button_frame)

		self.button_frame.add_element(Button((0, 0), "button", self.set_next_state, "game", text="Start"))
		self.button_frame.add_element(Button((0, 30), "button", self.set_next_state, "editor", text="Editor"), add_on_to_previous=(False, True))

	def set_next_state(self, next_state):
		self.go_to_state = next_state

	def next_state(self) -> GameState:
		if self.go_to_state == "":
			return self
		elif self.go_to_state == "game":
			from data.modules.game_states.game import Game
			return Game()
		elif self.go_to_state == "editor":
			from data.modules.game_states.editor import Editor
			return Editor()

	def update(self, delta: float):
		self.ui.update(delta)

		if InputManager.keys_pressed[pygame.K_ESCAPE]:
			EventManager.run_handlers(0, pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)
