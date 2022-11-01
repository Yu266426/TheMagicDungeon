import pygame

from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import get_tile_pos, draw_rect_outline
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.editor.tools.object_tools import ObjectDrawTool
from data.modules.editor.tools.tile_tools import TileDrawTool
from data.modules.ui.screen import ControlledScreen
from data.modules.ui.text import Text


class EditingScreen(ControlledScreen):
	def __init__(self, room: Room, editor_state: SharedTileState):
		super().__init__(keep_in=(0, 0, room.n_cols * TILE_SIZE, room.n_rows * TILE_SIZE))
		self._room = room
		self._editor_state = editor_state

		self._tiled_mouse_pos = (0, 0)

		# Editor tools
		self.tile_draw_tool = TileDrawTool(self._room, self._editor_state)
		self.object_draw_tool = ObjectDrawTool(self._room, self._editor_state)
		self.tool: EditorTool = self.tile_draw_tool

		# UI
		self.on_ui = False

		self._layer_text = Text((SCREEN_WIDTH - 10, 7), "arial", 60, (200, 200, 200), text="1", use_sys=True)

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (TILE_SIZE, TILE_SIZE))
		self._tiled_mouse_pos = self._tiled_mouse_pos[0], self._tiled_mouse_pos[1]

	def update_draw_level(self):
		# Change draw level
		if InputManager.keys_down[pygame.K_1]:
			self._editor_state.level = 0
			self._layer_text.set_text("1")
		elif InputManager.keys_down[pygame.K_2]:
			self._editor_state.level = 1
			self._layer_text.set_text("2")
		elif InputManager.keys_down[pygame.K_3]:
			self._editor_state.level = 2
			self._layer_text.set_text("3")

	def update(self, delta: float, on_ui: bool):
		self._mouse_update()
		self._get_mouse_pos()
		self.on_ui = on_ui

		# Tool
		if not on_ui:
			self.tool.update(self._tiled_mouse_pos)

		if InputManager.keys_down[pygame.K_z]:
			if InputManager.mods & pygame.KMOD_LCTRL and not InputManager.mods & pygame.KMOD_SHIFT:
				self._editor_state.undo_action()
			if InputManager.mods & pygame.KMOD_LCTRL and InputManager.mods & pygame.KMOD_SHIFT:
				self._editor_state.redo_action()

		self.update_draw_level()

		self._keyboard_control(delta)
		self._mouse_control()

	def draw(self, display: pygame.Surface):
		# Room outline
		draw_rect_outline(display, (255, 255, 0), -self._camera.target, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)

		self._room.draw(display, self._camera, {})

		if not self.on_ui:
			self.tool.draw(display, self._camera, self._tiled_mouse_pos)

		self._layer_text.draw(display, draw_from="r")
