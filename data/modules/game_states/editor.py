import pygame

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.screens.editing_screen import EditingScreen
from data.modules.editor.screens.objects_selection_screen import ObjectsSelectionScreen
from data.modules.editor.screens.tile_selection_screen import TileSelectionScreen
from data.modules.editor.shared_editor_state import EditorModes
from data.modules.editor.states.tile_draw_state import TileDrawState
from data.modules.game_states.game_state import GameState
from data.modules.objects.game_object import AnimatableObject
from data.modules.ui.element import Frame, Button, TextSelector
from data.modules.ui.screen import UIScreen


class Editor(GameState):
	def __init__(self):
		self.room = Room("room2", n_rows=10, n_cols=10)
		# self._room = Room("test2", n_rows=20, n_cols=20, random_floor=False)

		self.action_queue = EditorActionQueue()

		self.tile_draw_state = TileDrawState(self.room, self.action_queue)

		# self._editing_screen = EditingScreen(self._room, )
		# self._selection_screen = TileSelectionScreen(["tiles", "walls"])
		# self._object_selection_screen = ObjectsSelectionScreen(self._editor_state)

		# Mode switcher
		self.prev_selection_index = 0
		self.mode_selection = TextSelector((0, 0), (260, 60), [
			"Tile",
			"Object"
		])

		self._ui_screen = UIScreen()
		self.selector_frame = self._ui_screen.add_frame(Frame((10, 10), (260, 60)))
		self.selector_frame.add_element(
			self.mode_selection
		)

		self.button_panel = self._ui_screen.add_frame(Frame((10, SCREEN_HEIGHT - 80), (SCREEN_WIDTH - 20, 70)))
		self.button_panel.add_element(Button((0, 0), "reload", self.reset_object_animations, size=(None, 70)))

	def reset_object_animations(self):
		for game_object in self.room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.frame = 0

	def update(self, delta: float):
		self._ui_screen.update(delta)

		self.tile_draw_state.update(delta)

		# # Mode switcher
		# if self.prev_selection_index != self.mode_selection.index:  # Only runs once
		# 	if self.mode_selection.index == 0:  # Switch to Tile mode
		# 		self._editor_state.mode = EditorModes.TileEditing
		#
		# 		# Ensure correct tool
		# 		if self._editing_screen.tool is self._editing_screen.object_draw_tool:
		# 			self._editing_screen.tool = self._editing_screen.tile_draw_tool
		#
		# 	elif self.mode_selection.index == 1:  # Switch to Object mode
		# 		self._editor_state.mode = EditorModes.ObjectEditing
		#
		# 		# Ensure correct tool
		# 		if self._editing_screen.tool is self._editing_screen.tile_draw_tool:
		# 			self._editing_screen.tool = self._editing_screen.object_draw_tool
		#
		# 		# Setup state
		# 		self._editor_state.current_object_type = self._object_selection_screen.get_selected()
		#
		# 	self.prev_selection_index = self.mode_selection.index

		# Hide mode switcher
		# If drawing
		# if InputManager.mouse_pressed[0] or InputManager.mouse_pressed[2]:
		# 	if not self._ui_screen.on_ui():
		# 		self.selector_frame.active = False
		# 		self.button_panel.active = False
		# else:
		# 	self.selector_frame.active = True
		# 	self.button_panel.active = True
		#
		# 	# If in selection mode
		# 	if self._editor_state.mode == EditorModes.TileSelecting or self._editor_state.mode == EditorModes.ObjectSelecting:
		# 		self.selector_frame.active = False
		# 		self.button_panel.active = False
		# 	else:
		# 		self.selector_frame.active = True
		# 		self.button_panel.active = True
		#
		# # Update screens
		# if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
		# 	self._editing_screen.update(delta, self._ui_screen.on_ui())
		# if self._editor_state.mode == EditorModes.TileSelecting:
		# 	self._selection_screen.update(delta)
		# elif self._editor_state.mode == EditorModes.ObjectSelecting:
		# 	self._object_selection_screen.update(delta)
		#
		# # Switch to selection screen
		# if InputManager.keys_down[pygame.K_SPACE]:
		# 	if self._editor_state.mode == EditorModes.TileEditing:
		# 		self._editor_state.mode = EditorModes.TileSelecting
		#
		# 	if self._editor_state.mode == EditorModes.ObjectEditing:
		# 		self._editor_state.mode = EditorModes.ObjectSelecting
		#
		# if InputManager.keys_up[pygame.K_SPACE]:
		# 	if self._editor_state.mode == EditorModes.TileSelecting:
		# 		self._editor_state.mode = EditorModes.TileEditing
		#
		# 		self._selection_screen.current_screen.update_state()  # Ensure selection is consistent
		#
		# 	if self._editor_state.mode == EditorModes.ObjectSelecting:
		# 		self._editor_state.mode = EditorModes.ObjectEditing

		# Save
		if InputManager.mods & pygame.KMOD_LCTRL:
			if InputManager.keys_down[pygame.K_s]:
				self.room.save()

		# Animate objects
		for game_object in self.room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.change_frame(delta * 2)

		if InputManager.keys_down[pygame.K_0]:
			self.reset_object_animations()

	def draw(self, display: pygame.Surface):
		display.fill((30, 30, 30))

		self.tile_draw_state.draw(display)

		# if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
		# 	self._editing_screen.draw(display)
		#
		# elif self._editor_state.mode == EditorModes.TileSelecting:
		# 	self._selection_screen.draw(display)
		#
		# elif self._editor_state.mode == EditorModes.ObjectSelecting:
		# 	self._object_selection_screen.draw(display)

		self._ui_screen.draw(display)

	def next_state(self):
		return self
