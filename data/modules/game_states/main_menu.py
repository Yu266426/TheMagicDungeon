import pygame

import pygbase


class MainMenu(pygbase.GameState, name="main_menu"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()

		self.title_frame = self.ui.add_frame(pygbase.Frame(
			(pygbase.UIValue(0.2, False), pygbase.UIValue(0.1, False)),
			(pygbase.UIValue(0.6, False), pygbase.UIValue(0.3, False))
		))
		self.title_frame.add_element(pygbase.ImageElement(
			(pygbase.UIValue(0, False), pygbase.UIValue(0, False)),
			(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
			"image",
			"main_title",
			self.title_frame
		))

		self.button_frame = self.ui.add_frame(pygbase.Frame((pygbase.UIValue(0.25, False), pygbase.UIValue(0.4, False)), (pygbase.UIValue(0.5, False), pygbase.UIValue(0.6, False))))

		from data.modules.game_states.game import Game
		from data.modules.game_states.test_state import TestState
		from data.modules.game_states.lobby import Lobby
		self.button_frame.add_element(pygbase.Button(
			(pygbase.UIValue(0, False), pygbase.UIValue(0, False)),
			(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
			"image",
			"button",
			self.button_frame,
			self.set_next_state_type,
			callback_args=(Lobby, ()),
			text="Start"
		))

		from data.modules.game_states.editor_room_selection import EditorRoomSelection
		self.button_frame.add_element(pygbase.Button(
			(pygbase.UIValue(0, False), pygbase.UIValue(0.02, False)),
			(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
			"image",
			"button",
			self.button_frame,
			self.set_next_state_type,
			callback_args=(EditorRoomSelection, ()),
			text="Editor"
		), add_on_to_previous=(False, True))

		self.button_frame.add_element(pygbase.Button(
			(pygbase.UIValue(0, False), pygbase.UIValue(0.02, False)),
			(pygbase.UIValue(1, False), pygbase.UIValue(0, False)),
			"image",
			"button",
			self.button_frame,
			pygbase.EventManager.post_event,
			callback_args=(pygame.QUIT,),
			text="Quit"
		), add_on_to_previous=(False, True))

	def update(self, delta: float):
		self.ui.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.run_handlers("all", pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)
