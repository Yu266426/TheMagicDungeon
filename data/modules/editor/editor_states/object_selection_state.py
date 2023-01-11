import pygame

from data.modules.base.constants import TILE_SCALE
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import ObjectSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.screens.object_selection_screen import ObjectSelectionScreen
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.objects.chest import Chest
from data.modules.objects.cube import SmallCube, SmallRedCube, SmallGreenCube, LargeCube, LargeRedCube, LargeGreenCube
from data.modules.objects.lever import Lever


class ObjectSelectionState(EditorState):
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue, object_selection_info: ObjectSelectionInfo):
		super().__init__(room, shared_state, action_queue)

		self.object_selection_info = object_selection_info

		self.object_screen_index = 0
		self.object_screens: list[ObjectSelectionScreen] = [
			ObjectSelectionScreen(self.object_selection_info, [SmallCube, SmallRedCube, SmallGreenCube, LargeCube, LargeRedCube, LargeGreenCube, Lever, Chest], (16 * TILE_SCALE, 16 * TILE_SCALE), n_cols=3)
		]

	def update(self, delta: float):
		self._shared_state.show_global_ui = False

		self.object_screens[self.object_screen_index].update(delta)

	def draw(self, screen: pygame.Surface):
		self.object_screens[self.object_screen_index].draw(screen)

	def next_state(self, mode_index: int):
		if mode_index == 0:
			return EditorStates.TILE_DRAW_STATE
		elif mode_index == 1:
			if InputManager.keys_pressed[pygame.K_SPACE]:
				return EditorStates.OBJECT_SELECTION_STATE
			else:
				return EditorStates.OBJECT_DRAW_STATE
