import pygame

from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.screens.sprite_sheet_screen import SpriteSheetScreen
from data.modules.editor.shared_editor_state import SharedEditorState


class TileSelectionState(EditorState):
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue, tile_selection_info: TileSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.tile_selection_info = tile_selection_info

		self.sprite_sheet_index = 0
		self.sprite_sheets: list[SpriteSheetScreen] = [
			SpriteSheetScreen(self.tile_selection_info, "tiles"),
			SpriteSheetScreen(self.tile_selection_info, "walls")
		]

	def update(self, delta: float):
		self.sprite_sheets[self.sprite_sheet_index].update(delta)

	def draw(self, screen: pygame.Surface):
		self.sprite_sheets[self.sprite_sheet_index].draw(screen)

	def next_state(self):
		if InputManager.keys_pressed[pygame.K_SPACE]:
			return EditorStates.TILE_SELECTION_STATE
		else:
			return EditorStates.TILE_DRAW_STATE
