import enum

import pygame

from data.modules.base.constants import SCREEN_WIDTH, TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import get_tile_pos, draw_rect_outline
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.editor.tools.tile_tools import TileDrawTool
from data.modules.ui.screen import ControlledScreen
from data.modules.ui.text import Text


class TileTools(enum.Enum):
	DRAW = enum.auto()


class TileDrawState(EditorState):
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue, tile_selection_info: TileSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.tile_selection_info = tile_selection_info

		self.controlled_screen = ControlledScreen(keep_in=(0, 0, room.n_cols * TILE_SIZE, room.n_rows * TILE_SIZE))

		self.current_tool: TileTools = TileTools.DRAW
		self.tools: dict[TileTools, EditorTool] = {
			TileTools.DRAW: TileDrawTool(self._room, self._shared_state, self._action_queue)
		}

		self.tiled_mouse_pos = get_tile_pos(self.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

	def update(self, delta: float):
		self.controlled_screen.update(delta)
		self.tiled_mouse_pos = get_tile_pos(self.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		if not self._shared_state.on_global_ui:
			self.tools[self.current_tool].update(self.tiled_mouse_pos, self.tile_selection_info)

	def draw(self, screen: pygame.Surface):
		draw_rect_outline(screen, (255, 255, 0), -self.controlled_screen.camera.target, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)
		self._room.draw(screen, self.controlled_screen.camera, {})

		if not self._shared_state.on_global_ui:
			self.tools[self.current_tool].draw(screen, self.controlled_screen.camera, self.tiled_mouse_pos, self.tile_selection_info)

	def next_state(self):
		if InputManager.keys_pressed[pygame.K_SPACE]:
			return EditorStates.TILE_SELECTION_STATE
		else:
			return EditorStates.TILE_DRAW_STATE

# class TileDrawState(ControlledScreen):
# 	def __init__(self, room: Room, action_queue: EditorActionQueue):
# 		super().__init__(keep_in=(0, 0, room.n_cols * TILE_SIZE, room.n_rows * TILE_SIZE))
# 		self._room: Room = room
# 		self._action_queue: EditorActionQueue = action_queue
#
# 		self.shared_tile_state: SharedTileState = SharedTileState("tiles")
#
# 		self.selection_screen = TileSelectionScreen(self.shared_tile_state, ["tiles", "walls"])
#
# 		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (TILE_SIZE, TILE_SIZE))
#
# 		# Tools
# 		self.tile_draw_tool = TileDrawTool(self._room, self.shared_tile_state, self._action_queue)
#
# 		# UI
# 		self._layer_text = Text((SCREEN_WIDTH - 10, 7), "arial", 60, (200, 200, 200), text="1", use_sys=True)
#
# 	def _get_mouse_pos(self):
# 		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (TILE_SIZE, TILE_SIZE))
# 		self._tiled_mouse_pos = self._tiled_mouse_pos[0], self._tiled_mouse_pos[1]
#
# 	def update_draw_level(self):
# 		# Change draw level
# 		if InputManager.keys_down[pygame.K_1]:
# 			self.shared_tile_state.level = 0
# 			self._layer_text.set_text("1")
# 		elif InputManager.keys_down[pygame.K_2]:
# 			self.shared_tile_state.level = 1
# 			self._layer_text.set_text("2")
# 		elif InputManager.keys_down[pygame.K_3]:
# 			self.shared_tile_state.level = 2
# 			self._layer_text.set_text("3")
#
# 	def update(self, delta: float, on_ui: bool):
# 		self._mouse_update()
# 		self._get_mouse_pos()
#
# 		if not on_ui:
# 			self.tile_draw_tool.update(self._tiled_mouse_pos)
#
# 		self.update_draw_level()
#
# 		self._keyboard_control(delta)
# 		self._mouse_control()
#
# 	def draw(self, display: pygame.Surface, on_ui: bool):
# 		# Room outline
# 		draw_rect_outline(display, (255, 255, 0), -self._camera.target, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)
#
# 		self._room.draw(display, self._camera, {})
#
# 		if not on_ui:
# 			self.tile_draw_tool.draw(display, self._camera, self._tiled_mouse_pos)
#
# 		self._layer_text.draw(display, draw_from="r")
#
# 	def next_state(self):
# 		return None
