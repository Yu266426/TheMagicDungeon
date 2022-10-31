import pygame

from data.modules.editor.screens.tile_selection_screen import TileSelectionScreen
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.editor.states.editor_state import EditorState


class TileDrawState(EditorState):
	def __init__(self):
		self.shared_tile_state: SharedTileState = SharedTileState("tiles")

		self.selection_screen = TileSelectionScreen(self.shared_tile_state, ["tiles", "walls"])

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface):
		pass
