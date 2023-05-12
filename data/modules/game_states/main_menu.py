import pygame
from pygbase import InputManager, EventManager, Common, GameState
from pygbase import Frame, Button, ImageElement
from pygbase import UIManager


class MainMenu(GameState, name="main_menu"):
	def __init__(self):
		super().__init__()

		self.ui = UIManager()

		self.title_frame = self.ui.add_frame(Frame((0.2, 0.1), (0.6, 0.3)))
		self.title_frame.add_element(ImageElement((0, 0), (1, 0), Common.get_resource_type("image"), "main_title", self.title_frame))

		self.button_frame = self.ui.add_frame(Frame((0.25, 0.4), (0.5, 0.6)))

		from data.modules.game_states.game import Game
		self.button_frame.add_element(Button((0, 0), (1, 0), Common.get_resource_type("image"), "button", self.button_frame, self.set_next_state_type, callback_args=(Game, ()), text="Start"))

		from data.modules.game_states.editor import Editor
		self.button_frame.add_element(Button((0, 0.02), (1, 0), Common.get_resource_type("image"), "button", self.button_frame, self.set_next_state_type, callback_args=(Editor, ()), text="Editor"), add_on_to_previous=(False, True))

		self.button_frame.add_element(Button((0, 0.02), (1, 0), Common.get_resource_type("image"), "button", self.button_frame, EventManager.post_event, callback_args=(pygame.QUIT,), text="Quit"), add_on_to_previous=(False, True))

	def update(self, delta: float):
		self.ui.update(delta)

		if InputManager.keys_pressed[pygame.K_ESCAPE]:
			EventManager.run_handlers("all", pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)
