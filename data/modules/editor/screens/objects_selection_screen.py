import pygame

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE
from data.modules.editor.screens.object_selection_screen import ObjectSelectionScreen
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.objects.chest import Chest
from data.modules.objects.cube import LargeGreenCube, LargeRedCube, LargeCube, SmallGreenCube, SmallRedCube, SmallCube
from data.modules.objects.lever import Lever
from data.modules.ui.element import Button, Frame
from data.modules.ui.screen import UIScreen


class ObjectsSelectionScreen:
	def __init__(self, editor_state: SharedTileState):
		self._editor_state: SharedTileState = editor_state

		self.screens: list[ObjectSelectionScreen] = [
			ObjectSelectionScreen(self._editor_state, [SmallCube, SmallRedCube, SmallGreenCube, LargeCube, LargeRedCube, LargeGreenCube, Lever, Chest], (16 * TILE_SCALE, 16 * TILE_SCALE), n_cols=3)
		]

		self.current_screen: ObjectSelectionScreen = self.screens[0]

		self.ui_screen: UIScreen = UIScreen()
		self.button_frame = self.ui_screen.add_frame(
			Frame((0, SCREEN_HEIGHT - 86), (SCREEN_WIDTH, 90)).
			add_element(Button((3, 3), "tile_set_button", self.switch_screen, 0))
		)

	def switch_screen(self, new_screen_id: int):
		"""
		Callback for button press
		:param new_screen_id: Screen index to switch to
		"""

		self.current_screen = self.screens[new_screen_id]
		self._editor_state.current_object_type = type(self.current_screen.objects[self.current_screen.selected_object_index])

	def get_selected(self):
		return type(self.current_screen.objects[self.current_screen.selected_object_index])

	def update(self, delta: float):
		if not self.ui_screen.on_ui():
			self.current_screen.update(delta)

		self.ui_screen.update(delta)

	def draw(self, display: pygame.Surface):
		self.current_screen.draw(display)

		self.ui_screen.draw(display)
