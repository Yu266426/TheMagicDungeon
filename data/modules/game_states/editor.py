import pygame
from pygbase import InputManager, EventManager
from pygbase.game_state import GameState
from pygbase.ui.element import TextSelectionMenu, Frame
from pygbase.ui.screen import UIScreen

from data.modules.base.room import EditorRoom
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo, ObjectSelectionInfo
from data.modules.editor.editor_states.editor_state import EditorState, EditorStates
from data.modules.editor.editor_states.object_draw_state import ObjectDrawState
from data.modules.editor.editor_states.object_selection_state import ObjectSelectionState
from data.modules.editor.editor_states.tile_draw_state import TileDrawState
from data.modules.editor.editor_states.tile_selection_state import TileSelectionState
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.objects.cube import SmallCube
from data.modules.objects.game_object import AnimatableObject


class Editor(GameState):
	def __init__(self):
		super().__init__(4)

		self.room = EditorRoom("test", n_rows=10, n_cols=10)

		self.shared_state = SharedEditorState(self.room)
		self.action_queue = EditorActionQueue()

		self.tile_selection_info = TileSelectionInfo("tiles")
		self.object_selection_info = ObjectSelectionInfo(SmallCube)

		self.current_state: EditorStates = EditorStates.TILE_DRAW_STATE
		self.states: dict[EditorStates, EditorState] = {
			EditorStates.TILE_DRAW_STATE: TileDrawState(self.room, self.shared_state, self.action_queue, self.tile_selection_info),
			EditorStates.TILE_SELECTION_STATE: TileSelectionState(self.room, self.shared_state, self.action_queue, self.tile_selection_info),
			EditorStates.OBJECT_DRAW_STATE: ObjectDrawState(self.room, self.shared_state, self.action_queue, self.object_selection_info),
			EditorStates.OBJECT_SELECTION_STATE: ObjectSelectionState(self.room, self.shared_state, self.action_queue, self.object_selection_info)
		}

		self.mode_selector = TextSelectionMenu((0, 0), (260, 60), [
			"Tile",
			"Object"
		])

		self.ui = UIScreen()
		self.selector_frame = self.ui.add_frame(Frame((10, 10), (260, 60)))
		self.selector_frame.add_element(self.mode_selector)

	def reset_object_animations(self):
		for game_object in self.room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.frame = 0

	def update(self, delta: float):
		if self.shared_state.show_global_ui:
			self.ui.update(delta)
			self.shared_state.on_global_ui = self.ui.on_ui()

		self.current_state = self.states[self.current_state].next_state(self.mode_selector.index)

		self.states[self.current_state].update(delta)

		if InputManager.keys_down[pygame.K_z]:
			if InputManager.mods & pygame.KMOD_LCTRL and not InputManager.mods & pygame.KMOD_SHIFT:
				self.action_queue.undo_action()
			if InputManager.mods & pygame.KMOD_LCTRL and InputManager.mods & pygame.KMOD_SHIFT:
				self.action_queue.redo_action()

		# Animate objects
		for game_object in self.room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.change_frame(delta * 2)

		# Save
		if InputManager.mods & pygame.KMOD_LCTRL:
			if InputManager.keys_down[pygame.K_s]:
				self.room.save()

		if InputManager.keys_pressed[pygame.K_ESCAPE]:
			EventManager.run_handlers(0, pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.states[self.current_state].draw(screen)

		if self.shared_state.show_global_ui:
			self.ui.draw(screen)

	def next_state(self) -> GameState:
		return self
