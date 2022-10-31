import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.editor.screens.sprite_sheet_screen import SpriteSheetScreen
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.ui.element import Frame, Button
from data.modules.ui.screen import UIScreen


class TileSelectionScreen:
	def __init__(self, shared_tile_state: SharedTileState, sheet_names: list[str]):
		self.shared_tile_state: SharedTileState = shared_tile_state

		self.screens: list[SpriteSheetScreen] = []
		for sheet_name in sheet_names:
			self.screens.append(SpriteSheetScreen(self.shared_tile_state, sheet_name))

		self.current_screen: SpriteSheetScreen = self.screens[0]

		self.ui_screen: UIScreen = UIScreen()
		self.button_frame = self.ui_screen.add_frame(Frame((0, SCREEN_HEIGHT - 86), (SCREEN_WIDTH, 90)))

		if len(sheet_names) > 0:
			self.button_frame.add_element(Button((3, 3), "tile_set_button", self.switch_screen, 0))

			for loop in range(1, len(sheet_names)):
				self.button_frame.add_element(Button((3, 0), "tile_set_button", self.switch_screen, loop), align_with_previous=(False, True), add_on_to_previous=(True, False))

	def switch_screen(self, new_screen_id: int):
		"""
		Callback for button press
		"""

		self.current_screen = self.screens[new_screen_id]
		# if isinstance(self.screens[new_screen_id], SpriteSheetScreen):
		self.shared_tile_state.sprite_sheet_name = self.current_screen.sprite_sheet_name
		self.shared_tile_state.selected_topleft = self.current_screen.selected_topleft
		self.shared_tile_state.selected_bottomright = self.current_screen.selected_bottomright

		self.shared_tile_state.ids = self.current_screen.get_ids()

	def update(self, delta: float):
		if not self.ui_screen.on_ui():
			self.current_screen.update(delta)

		self.ui_screen.update(delta)

	def draw(self, display: pygame.Surface):
		self.current_screen.draw(display)

		self.ui_screen.draw(display)
