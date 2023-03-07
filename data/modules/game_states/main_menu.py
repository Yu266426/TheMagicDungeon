import pygame
from pygbase import InputManager, EventManager, Common
from pygbase.game_state import GameState
from pygbase.ui.element import Frame, Image, Button
from pygbase.ui.screen import UIScreen


class MainMenu(GameState):
	def __init__(self):
		super().__init__(2)

		self.ui = UIScreen()

		self.title_frame = self.ui.add_frame(Frame((150, 50), (500, 200)))
		self.title_frame.add_element(Image((0, 0), Common.get_value("image_res"), "main_title"))

		self.button_frame = self.ui.add_frame(Frame((220, 300), (360, 600)))

		from data.modules.game_states.game import Game
		self.button_frame.add_element(Button((0, 0), Common.get_value("image_res"), "button", self.set_next_state, Game, text="Start"))

		from data.modules.game_states.editor import Editor
		self.button_frame.add_element(Button((0, 30), Common.get_value("image_res"), "button", self.set_next_state, Editor, text="Editor"), add_on_to_previous=(False, True))

		self.button_frame.add_element(Button((0, 30), Common.get_value("image_res"), "button", EventManager.post_event, pygame.QUIT, text="Quit"), add_on_to_previous=(False, True))

	def update(self, delta: float):
		self.ui.update(delta)

		if InputManager.keys_pressed[pygame.K_ESCAPE]:
			EventManager.run_handlers(0, pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)
