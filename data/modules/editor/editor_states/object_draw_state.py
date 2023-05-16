import enum

import pygame
import pygbase

from data.modules.base.constants import TILE_SIZE
from data.modules.map.room import EditorRoom
from data.modules.base.utils import draw_rect_outline, get_tile_pos
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import ObjectSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.editor.tools.object_tools.object_tools import ObjectDrawTool
from data.modules.objects.game_object import AnimatableObject


class ObjectTools(enum.Enum):
	DRAW = enum.auto()


class ObjectDrawState(EditorState):
	def __init__(self, room: EditorRoom, shared_state: SharedEditorState, action_queue: EditorActionQueue, object_selection_info: ObjectSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.object_selection_info = object_selection_info

		self.current_tool: ObjectTools = ObjectTools.DRAW
		self.tools: dict[ObjectTools, EditorTool] = {
			ObjectTools.DRAW: ObjectDrawTool(self._room, self._shared_state, self._action_queue)
		}

		self.tiled_mouse_pos = get_tile_pos(self._shared_state.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		self.ui = pygbase.UIManager()
		self.button_frame = self.ui.add_frame(pygbase.Frame((0, 0.9), (1, 0.1), bg_colour=(20, 20, 20, 150)))
		self.button_frame.add_element(pygbase.Button((0.01, 0.05), (0, 0.9), pygbase.Common.get_resource_type("image"), "reload", self.button_frame, self.reset_object_animations))

	def reset_object_animations(self):
		for game_object in self._room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.frame = 0

	def update(self, delta: float):
		self._shared_state.show_global_ui = True
		self.ui.update(delta)

		self._shared_state.controlled_screen.update(delta)
		self.tiled_mouse_pos = get_tile_pos(self._shared_state.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		if not self._shared_state.on_global_ui and not self.ui.on_ui():
			self.tools[self.current_tool].update(self.tiled_mouse_pos, self.object_selection_info)

	def draw(self, screen: pygame.Surface):
		draw_rect_outline(screen, (255, 255, 0), -self._shared_state.controlled_screen.camera.pos, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)
		self._room.draw(screen, self._shared_state.controlled_screen.camera, {})

		if not self._shared_state.on_global_ui and self._shared_state.should_draw_tool and not self.ui.on_ui():
			self.tools[self.current_tool].draw(screen, self._shared_state.controlled_screen.camera, self.tiled_mouse_pos, self.object_selection_info)

		self.ui.draw(screen)

	def next_state(self, mode_index: int):
		if mode_index == 0:
			return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			if pygbase.InputManager.keys_pressed[pygame.K_SPACE]:
				return EditorStates.OBJECT_SELECTION_STATE
			else:
				return EditorStates.OBJECT_DRAW_STATE
