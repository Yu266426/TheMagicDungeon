import pygame

from data.modules.base.constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import get_tile_pos
from data.modules.editor.editor_state import EditorState, EditorModes
from data.modules.editor.editor_tool import EditorTool, TileDrawTool, ObjectDrawTool
from data.modules.editor.selection_screens import TileSelectionScreen, ObjectsSelectionScreen
from data.modules.objects.game_object import AnimatableObject
from data.modules.ui.element import Frame, Button, TextSelector
from data.modules.ui.screen import ControlledScreen, UIScreen
from data.modules.ui.text import Text


class Editor:
	def __init__(self):
		self._room = Room("test", n_rows=20, n_cols=20)

		self._editor_state = EditorState(4)

		self._editing_screen = EditingScreen(self._room, self._editor_state)
		self._selection_screen = TileSelectionScreen(self._editor_state, [4, 7])
		self._object_selection_screen = ObjectsSelectionScreen(self._editor_state)

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

		self.button_frame = self._ui_screen.add_frame(Frame((10, SCREEN_HEIGHT - 80), (SCREEN_WIDTH - 20, 70)))
		self.button_frame.add_element(Button((0, 0), 0, self.reset_object_animations, size=(None, 70)))

	def reset_object_animations(self):
		for game_object in self._room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.frame = 0

	def update(self, delta: float):
		self._ui_screen.update(delta)

		# Mode switcher
		if self.prev_selection_index != self.mode_selection.index:  # Only runs once
			if self.mode_selection.index == 0:  # Switch to Tile mode
				self._editor_state.mode = EditorModes.TileEditing

				# Ensure correct tool
				if self._editing_screen.tool is self._editing_screen.object_draw_tool:
					self._editing_screen.tool = self._editing_screen.tile_draw_tool

			elif self.mode_selection.index == 1:  # Switch to Object mode
				self._editor_state.mode = EditorModes.ObjectEditing

				# Ensure correct tool
				if self._editing_screen.tool is self._editing_screen.tile_draw_tool:
					self._editing_screen.tool = self._editing_screen.object_draw_tool

				# Setup state
				self._editor_state.current_object_type = self._object_selection_screen.get_selected()

			self.prev_selection_index = self.mode_selection.index

		# Hide mode switcher
		# If drawing
		if InputManager.mouse_pressed[0] or InputManager.mouse_pressed[2]:
			if not self._ui_screen.on_ui():
				self.selector_frame.active = False
				self.button_frame.active = False
		else:
			self.selector_frame.active = True
			self.button_frame.active = True

			# If in selection mode
			if self._editor_state.mode == EditorModes.TileSelecting or self._editor_state.mode == EditorModes.ObjectSelecting:
				self.selector_frame.active = False
				self.button_frame.active = False
			else:
				self.selector_frame.active = True
				self.button_frame.active = True

		# Update screens
		if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
			self._editing_screen.update(delta, self._ui_screen.on_ui())
		if self._editor_state.mode == EditorModes.TileSelecting:
			self._selection_screen.update(delta)
		elif self._editor_state.mode == EditorModes.ObjectSelecting:
			self._object_selection_screen.update(delta)

		# Switch to selection screen
		if InputManager.keys_down[pygame.K_SPACE]:
			if self._editor_state.mode == EditorModes.TileEditing:
				self._editor_state.mode = EditorModes.TileSelecting

			if self._editor_state.mode == EditorModes.ObjectEditing:
				self._editor_state.mode = EditorModes.ObjectSelecting

		if InputManager.keys_up[pygame.K_SPACE]:
			if self._editor_state.mode == EditorModes.TileSelecting:
				self._editor_state.mode = EditorModes.TileEditing

				self._selection_screen.current_screen.update_state()  # Ensure selection is consistent

			if self._editor_state.mode == EditorModes.ObjectSelecting:
				self._editor_state.mode = EditorModes.ObjectEditing

		# Save
		if InputManager.mods == pygame.KMOD_LCTRL and InputManager.keys_down[pygame.K_s]:
			self._room.save()

		# Animate objects
		for game_object in self._room.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.change_frame(delta * 2)

		if InputManager.keys_down[pygame.K_0]:
			self.reset_object_animations()

	def draw(self, display: pygame.Surface):
		display.fill((30, 30, 30))

		if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
			self._editing_screen.draw(display)

		elif self._editor_state.mode == EditorModes.TileSelecting:
			self._selection_screen.draw(display)

		elif self._editor_state.mode == EditorModes.ObjectSelecting:
			self._object_selection_screen.draw(display)

		self._ui_screen.draw(display)


class EditingScreen(ControlledScreen):
	def __init__(self, room: Room, editor_state: EditorState):
		super().__init__(keep_in=(0, 0, room.n_cols * TILE_SIZE, room.n_rows * TILE_SIZE))
		self._room = room
		self._editor_state = editor_state

		self._tiled_mouse_pos = (0, 0)

		# Editor tools
		self.tile_draw_tool = TileDrawTool(self._room, self._editor_state)
		self.object_draw_tool = ObjectDrawTool(self._room, self._editor_state)
		self.tool: EditorTool = self.tile_draw_tool

		# UI
		self._layer_text = Text((SCREEN_WIDTH - 10, 7), "arial", 60, (200, 200, 200), text="1", use_sys=True)

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (TILE_SIZE, TILE_SIZE))
		self._tiled_mouse_pos = self._tiled_mouse_pos[0], self._tiled_mouse_pos[1]

	def update(self, delta: float, on_ui: bool):
		self._mouse_update()
		self._get_mouse_pos()

		# Tool
		if not on_ui:
			self.tool.update(self._tiled_mouse_pos)

		if InputManager.keys_down[pygame.K_z]:
			if InputManager.mods == pygame.KMOD_LCTRL:
				self._editor_state.undo_action()
			if InputManager.mods == pygame.KMOD_LCTRL + pygame.KMOD_LSHIFT:
				self._editor_state.redo_action()

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

		self._keyboard_control(delta)
		self._mouse_control()

	def draw(self, display: pygame.Surface):
		# Room outline
		pygame.draw.rect(
			display, (255, 255, 0),
			pygame.Rect(
				*-self._camera.target,
				self._room.n_cols * TILE_SIZE, self._room.n_rows * TILE_SIZE
			), width=2
		)

		self._room.draw(display, self._camera)
		self.tool.draw(display, self._camera, self._tiled_mouse_pos)
		self._layer_text.draw(display, draw_from="r")
