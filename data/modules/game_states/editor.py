import enum

import pygame

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo
from data.modules.editor.editor_states.tile_selection_state import TileSelectionState
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.editor_states.tile_draw_state import TileDrawState
from data.modules.game_states.game_state import GameState
from data.modules.objects.game_object import AnimatableObject
from data.modules.ui.element import Frame, Button, TextSelector
from data.modules.ui.screen import UIScreen


class Editor(GameState):
	def __init__(self):
		self.room = Room("test", n_rows=10, n_cols=10)

		self.shared_state = SharedEditorState()
		self.action_queue = EditorActionQueue()

		self.tile_selection_info = TileSelectionInfo("tiles")

		self.current_state: EditorStates = EditorStates.TILE_DRAW_STATE
		self.states: dict[EditorStates, EditorState] = {
			EditorStates.TILE_DRAW_STATE: TileDrawState(self.room, self.shared_state, self.action_queue, self.tile_selection_info),
			EditorStates.TILE_SELECTION_STATE: TileSelectionState(self.room, self.shared_state, self.action_queue, self.tile_selection_info)
		}

	# self.room = Room("room2", n_rows=10, n_cols=10)
	# # self._room = Room("test2", n_rows=20, n_cols=20, random_floor=False)
	#
	# self.action_queue = EditorActionQueue()
	#
	# self.tile_draw_state = TileDrawState(self.room, self.action_queue)
	#
	# # self._editing_screen = EditingScreen(self._room, )
	# # self._selection_screen = TileSelectionScreen(["tiles", "walls"])
	# # self._object_selection_screen = ObjectsSelectionScreen(self._editor_state)
	#
	# # Mode switcher
	# self.prev_selection_index = 0
	# self.mode_selection = TextSelector((0, 0), (260, 60), [
	# 	"Tile",
	# 	"Object"
	# ])
	#
	# self._ui_screen = UIScreen()
	# self.selector_frame = self._ui_screen.add_frame(Frame((10, 10), (260, 60)))
	# self.selector_frame.add_element(
	# 	self.mode_selection
	# )
	#
	# self.button_panel = self._ui_screen.add_frame(Frame((10, SCREEN_HEIGHT - 80), (SCREEN_WIDTH - 20, 70)))
	# self.button_panel.add_element(Button((0, 0), "reload", self.reset_object_animations, size=(None, 70)))

	def reset_object_animations(self):
		for game_object in self.room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.frame = 0

	def update(self, delta: float):
		self.current_state = self.states[self.current_state].next_state()

		self.states[self.current_state].update(delta)

		if InputManager.keys_down[pygame.K_z]:
			if InputManager.mods & pygame.KMOD_LCTRL and not InputManager.mods & pygame.KMOD_SHIFT:
				self.action_queue.undo_action()
			if InputManager.mods & pygame.KMOD_LCTRL and InputManager.mods & pygame.KMOD_SHIFT:
				self.action_queue.redo_action()

	# self._ui_screen.update(delta)
	#
	# self.tile_draw_state.update(delta, self._ui_screen.on_ui())
	#
	# # Save
	# if InputManager.mods & pygame.KMOD_LCTRL:
	# 	if InputManager.keys_down[pygame.K_s]:
	# 		self.room.save()
	#
	# # Animate objects
	# for game_object in self.room.objects:
	# 	if issubclass(type(game_object), AnimatableObject):
	# 		game_object.change_frame(delta * 2)
	#
	# if InputManager.keys_down[pygame.K_0]:
	# 	self.reset_object_animations()

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.states[self.current_state].draw(screen)

	# display.fill((30, 30, 30))
	#
	# self.tile_draw_state.draw(display, self._ui_screen.on_ui())
	#
	# if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
	# 	self._editing_screen.draw(display)
	#
	# elif self._editor_state.mode == EditorModes.TileSelecting:
	# 	self._selection_screen.draw(display)
	#
	# elif self._editor_state.mode == EditorModes.ObjectSelecting:
	# 	self._object_selection_screen.draw(display)
	#
	# self._ui_screen.draw(display)

	def next_state(self):
		return self
