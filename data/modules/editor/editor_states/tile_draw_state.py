import enum

import pygame

from data.modules.base.constants import SCREEN_WIDTH, TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import get_tile_pos, draw_rect_outline
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.editor.tools.tile_tools import TileDrawTool
from data.modules.ui.text import Text


class TileTools(enum.Enum):
	DRAW = enum.auto()


class TileDrawState(EditorState):
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue, tile_selection_info: TileSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.tile_selection_info = tile_selection_info

		self.current_tool: TileTools = TileTools.DRAW
		self.tools: dict[TileTools, EditorTool] = {
			TileTools.DRAW: TileDrawTool(self._room, self._shared_state, self._action_queue)
		}

		self.tiled_mouse_pos = get_tile_pos(self._shared_state.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		self.layer_text = Text((SCREEN_WIDTH - 10, 7), "arial", 60, (200, 200, 200), text="1", use_sys=True)

	def update_draw_layer(self):
		# Change draw layer
		if InputManager.keys_down[pygame.K_1]:
			self.tile_selection_info.layer = 0
			self.layer_text.set_text("1")
		elif InputManager.keys_down[pygame.K_2]:
			self.tile_selection_info.layer = 1
			self.layer_text.set_text("2")
		elif InputManager.keys_down[pygame.K_3]:
			self.tile_selection_info.layer = 2
			self.layer_text.set_text("3")

	def update(self, delta: float):
		self._shared_state.show_global_ui = True

		self._shared_state.controlled_screen.update(delta)
		self.tiled_mouse_pos = get_tile_pos(self._shared_state.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		self.update_draw_layer()

		if not self._shared_state.on_global_ui:
			self.tools[self.current_tool].update(self.tiled_mouse_pos, self.tile_selection_info)

	def draw(self, screen: pygame.Surface):
		draw_rect_outline(screen, (255, 255, 0), -self._shared_state.controlled_screen.camera.target, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)
		self._room.draw(screen, self._shared_state.controlled_screen.camera, {})

		if not self._shared_state.on_global_ui:
			self.tools[self.current_tool].draw(screen, self._shared_state.controlled_screen.camera, self.tiled_mouse_pos, self.tile_selection_info)

		self.layer_text.draw(screen, "r")

	def next_state(self, mode_index: int):
		if mode_index == 0:
			if InputManager.keys_pressed[pygame.K_SPACE]:
				return EditorStates.TILE_SELECTION_STATE
			else:
				return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			return EditorStates.OBJECT_DRAW_STATE
