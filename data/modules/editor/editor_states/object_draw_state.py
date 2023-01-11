import enum

import pygame

from data.modules.base.constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import draw_rect_outline, get_tile_pos
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import ObjectSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.editor.tools.object_tools import ObjectDrawTool
from data.modules.objects.game_object import AnimatableObject
from data.modules.ui.element import Frame, Button
from data.modules.ui.screen import UIScreen


class ObjectTools(enum.Enum):
	DRAW = enum.auto()


class ObjectDrawState(EditorState):
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue, object_selection_info: ObjectSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.object_selection_info = object_selection_info

		self.current_tool: ObjectTools = ObjectTools.DRAW
		self.tools: dict[ObjectTools, EditorTool] = {
			ObjectTools.DRAW: ObjectDrawTool(self._room, self._shared_state, self._action_queue)
		}

		self.tiled_mouse_pos = get_tile_pos(self._shared_state.controlled_screen.world_mouse_pos, (TILE_SIZE, TILE_SIZE))

		self.ui = UIScreen()
		self.button_frame = self.ui.add_frame(Frame((0, SCREEN_HEIGHT - 90), (SCREEN_WIDTH, 90), bg_colour=(20, 20, 20, 150)))
		self.button_frame.add_element(Button((10, 10), "reload", self.reset_object_animations, size=(None, 70)))

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
		draw_rect_outline(screen, (255, 255, 0), -self._shared_state.controlled_screen.camera.target, (self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE), 2)
		self._room.draw(screen, self._shared_state.controlled_screen.camera, {})

		if not self._shared_state.on_global_ui and not self.ui.on_ui():
			self.tools[self.current_tool].draw(screen, self._shared_state.controlled_screen.camera, self.tiled_mouse_pos, self.object_selection_info)

		self.ui.draw(screen)

	def next_state(self, mode_index: int):
		if mode_index == 0:
			return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			if InputManager.keys_pressed[pygame.K_SPACE]:
				return EditorStates.OBJECT_SELECTION_STATE
			else:
				return EditorStates.OBJECT_DRAW_STATE