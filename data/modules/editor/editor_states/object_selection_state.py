import pygame
import pygbase

from data.modules.base.constants import TILE_SCALE, SCREEN_HEIGHT
from data.modules.level.room import EditorRoom
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import ObjectSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.screens.object_selection_screen import ObjectSelectionScreen
from data.modules.editor.shared_editor_state import SharedEditorState


class ObjectSelectionState(EditorState):
	def __init__(self, room: EditorRoom, shared_state: SharedEditorState, action_queue: EditorActionQueue, object_selection_info: ObjectSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.object_selection_info: ObjectSelectionInfo = object_selection_info

		self.object_screen_index: int = 0
		self.object_screens: list[ObjectSelectionScreen] = [
			ObjectSelectionScreen(self.object_selection_info, ["small_cube", "small_red_cube", "small_green_cube", "large_cube", "large_red_cube", "large_green_cube", "lever", "chest", "torch"], (16 * TILE_SCALE, 16 * TILE_SCALE), n_cols=6),
			ObjectSelectionScreen(self.object_selection_info, ["rune_altar"], (32 * TILE_SCALE, 48 * TILE_SCALE), n_cols=5),
		]

		self.ui = pygbase.UIManager()
		self.button_frame = self.ui.add_frame(pygbase.Frame((pygbase.UIValue(0, False), pygbase.UIValue(SCREEN_HEIGHT - 90)), (pygbase.UIValue(1, False), pygbase.UIValue(90)), bg_colour=(20, 20, 20, 150)))

		self.button_frame.add_element(pygbase.Button(
			(pygbase.UIValue(10), pygbase.UIValue(10)),
			(pygbase.UIValue(0), pygbase.UIValue(70)),
			"image",
			"tile_set_button",
			self.button_frame,
			self.switch_screen,
			callback_args=(0,)
		))
		for loop in range(1, len(self.object_screens)):
			self.button_frame.add_element(pygbase.Button((pygbase.UIValue(10), pygbase.UIValue(10)), (pygbase.UIValue(0), pygbase.UIValue(70)), "image", "tile_set_button", self.button_frame, self.switch_screen, callback_args=(loop,)), align_with_previous=(False, True), add_on_to_previous=(True, False))

	def switch_screen(self, new_index: int):
		self.object_screen_index = new_index

		self.object_selection_info.set_object(self.object_screens[self.object_screen_index].objects[self.object_screens[self.object_screen_index].selected_object_index])

	def update(self, delta: float):
		self._shared_state.show_global_ui = False

		self.ui.update(delta)

		if self._shared_state.should_draw_tool and not self.ui.on_ui():
			self.object_screens[self.object_screen_index].update(delta)

	def draw(self, screen: pygame.Surface):
		self.object_screens[self.object_screen_index].draw(screen)

		self.ui.draw(screen)

	def next_state(self, mode_index: int):
		if mode_index == 0:
			return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			if pygbase.InputManager.get_key_pressed(pygame.K_SPACE):
				return EditorStates.OBJECT_SELECTION_STATE
			else:
				return EditorStates.OBJECT_DRAW_STATE
