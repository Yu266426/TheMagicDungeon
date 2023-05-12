import pygame
import pygbase

from data.modules.base.room import EditorRoom
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.screens.sprite_sheet_screen import SpriteSheetScreen
from data.modules.editor.shared_editor_state import SharedEditorState


class TileSelectionState(EditorState):
	def __init__(self, room: EditorRoom, shared_state: SharedEditorState, action_queue: EditorActionQueue, tile_selection_info: TileSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.tile_selection_info = tile_selection_info

		self.sprite_sheet_index = 0
		self.sprite_sheets: list[SpriteSheetScreen] = [
			SpriteSheetScreen(self.tile_selection_info, "tiles"),
			SpriteSheetScreen(self.tile_selection_info, "walls")
		]

		self.ui = pygbase.UIManager()
		self.button_frame = self.ui.add_frame(pygbase.Frame((0, 0.9), (1, 0.1)))

		self.button_frame.add_element(pygbase.Button((0.01, 0.02), (0, 0.9), pygbase.Common.get_resource_type("image"), "tile_set_button", self.button_frame, self.switch_screen, callback_args=(0,)))
		for loop in range(1, len(self.sprite_sheets)):
			self.button_frame.add_element(pygbase.Button((0.01, 0), (0, 0.9), pygbase.Common.get_resource_type("image"), "tile_set_button", self.button_frame, self.switch_screen, callback_args=(loop,)), align_with_previous=(False, True), add_on_to_previous=(True, False))

	def switch_screen(self, new_index: int):
		self.sprite_sheet_index = new_index

		self.tile_selection_info.sprite_sheet_name = self.sprite_sheets[self.sprite_sheet_index].sprite_sheet_name
		self.tile_selection_info.selected_topleft = self.sprite_sheets[self.sprite_sheet_index].selected_topleft
		self.tile_selection_info.selected_bottomright = self.sprite_sheets[self.sprite_sheet_index].selected_bottomright

		self.tile_selection_info.ids = self.sprite_sheets[self.sprite_sheet_index].get_ids()

	def update(self, delta: float):
		self._shared_state.show_global_ui = False

		self.ui.update(delta)

		if self._shared_state.should_draw_tool and not self.ui.on_ui():
			self.sprite_sheets[self.sprite_sheet_index].update(delta)

	def draw(self, screen: pygame.Surface):
		self.sprite_sheets[self.sprite_sheet_index].draw(screen)

		self.ui.draw(screen)

	def next_state(self, mode_index: int):
		if mode_index == 0:
			if pygbase.InputManager.keys_pressed[pygame.K_SPACE]:
				return EditorStates.TILE_SELECTION_STATE
			else:
				self.sprite_sheets[self.sprite_sheet_index].update_state()
				return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			return EditorStates.OBJECT_DRAW_STATE
