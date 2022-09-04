import pygame

from data.modules.base.constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.level import Room
from data.modules.base.resources import ResourceManager, ResourceTypes
from data.modules.base.utils import get_tile_pos, abs_tuple
from data.modules.editor.editor_state import EditorState, EditorModes
from data.modules.editor.editor_tool import EditorTool, TileDrawTool
from data.modules.graphics.sprite_sheet import SpriteSheet
from data.modules.ui.element import Frame, Button, TextSelector
from data.modules.ui.screen import ControlledScreen, UIScreen
from data.modules.ui.text import Text


class Editor:
	def __init__(self):
		self._room = Room("test2", n_rows=20, n_cols=20)

		self._editor_state = EditorState(4)

		self._editing_screen = EditingScreen(self._room, self._editor_state)
		self._selection_screen = SelectionScreen(self._editor_state)

	def update(self, delta: float):
		if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
			self._editing_screen.update(delta)

		elif self._editor_state.mode == EditorModes.TileSelecting:
			self._selection_screen.update(delta)

		# Switch to selection screen
		if InputManager.keys_down[pygame.K_SPACE]:
			if self._editor_state.mode == EditorModes.TileEditing:
				self._editor_state.mode = EditorModes.TileSelecting

		if InputManager.keys_up[pygame.K_SPACE]:
			if self._editor_state.mode == EditorModes.TileSelecting:
				self._editor_state.mode = EditorModes.TileEditing

		# Save
		if InputManager.mods == pygame.KMOD_LCTRL and InputManager.keys_down[pygame.K_s]:
			self._room.save()

	def draw(self, display: pygame.Surface):
		display.fill((30, 30, 30))

		if self._editor_state.mode == EditorModes.TileEditing or self._editor_state.mode == EditorModes.ObjectEditing:
			self._editing_screen.draw(display)

		elif self._editor_state.mode == EditorModes.TileSelecting:
			self._selection_screen.draw(display)


class EditingScreen(ControlledScreen):
	def __init__(self, room: Room, editor_state: EditorState):
		super().__init__()

		self._room = room
		self._editor_state = editor_state

		self._layer_text = Text((SCREEN_WIDTH - 10, 7), "arial", 60, (200, 200, 200), text="1", use_sys=True)

		self._tiled_mouse_pos = (0, 0)

		self._tool: EditorTool = TileDrawTool(self._room, self._editor_state)

		self._ui_screen = UIScreen()
		frame = self._ui_screen.add_frame(Frame((20, 20), (260, 80)))

		self.mode_selection = TextSelector((0, 0), (260, 60), [
			"Tile",
			"Object"
		])

		frame.add_element(
			self.mode_selection
		)

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (TILE_SIZE, TILE_SIZE))
		self._tiled_mouse_pos = self._tiled_mouse_pos[0], self._tiled_mouse_pos[1]

	def update(self, delta: float):
		self._mouse_update()
		self._get_mouse_pos()

		self._ui_screen.update(delta)

		# Mode switcher
		if self.mode_selection.index == 0:
			self._editor_state.mode = EditorModes.TileEditing
		if self.mode_selection.index == 1:
			self._editor_state.mode = EditorModes.ObjectEditing

		# Tool
		if not self._ui_screen.on_ui():
			self._tool.update(self._tiled_mouse_pos)

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
		self._tool.draw(display, self._camera, self._tiled_mouse_pos)
		self._layer_text.draw(display, draw_from="r")
		self._ui_screen.draw(display)


class SelectionScreen:
	def __init__(self, editor_state: EditorState):
		self.editor_state = editor_state

		self.screens = (
			SpriteSheetScreen(self.editor_state, 4),
			SpriteSheetScreen(self.editor_state, 7),
		)

		self.current_screen = self.screens[0]

		self.ui_screen: UIScreen = UIScreen()
		self.button_frame = self.ui_screen.add_frame(
			Frame((0, SCREEN_HEIGHT - 86), (SCREEN_WIDTH, 90))
			.add_element(Button((3, 3), 0, self.switch_screen, 0))
			.add_element(Button((3, 0), 0, self.switch_screen, 1), align_with_previous=(False, True), add_on_to_previous=(True, False))
		)

	def switch_screen(self, new_screen_id: int):
		"""
		Callback for button press
		:param new_screen_id: Screen index to switch to
		:return: None
		"""

		self.current_screen = self.screens[new_screen_id]
		if isinstance(self.screens[new_screen_id], SpriteSheetScreen):
			self.editor_state.sprite_sheet_id = self.current_screen.sprite_sheet_id
			self.editor_state.selected_topleft = self.current_screen.selected_topleft
			self.editor_state.selected_bottomright = self.current_screen.selected_bottomright

			self.editor_state.ids = self.current_screen.get_ids()

	def update(self, delta: float):
		if not self.ui_screen.on_ui():
			self.current_screen.update(delta)

		self.ui_screen.update(delta)

	def draw(self, display: pygame.Surface):
		self.current_screen.draw(display)

		self.ui_screen.draw(display)


class SpriteSheetScreen(ControlledScreen):
	"""
	Generic screen for selecting images from sprite_sheet
	"""

	def __init__(self, editor_state: EditorState, sprite_sheet_id: int):

		self.editor_state = editor_state

		self.sprite_sheet_id: int = sprite_sheet_id
		self.sprite_sheet: SpriteSheet = ResourceManager.get_resource(ResourceTypes.SPRITE_SHEET, sprite_sheet_id)

		super().__init__(keep_in=(0, 0, *self.sprite_sheet.image.get_size()))

		self.selected_topleft = (0, 0)
		self.selected_bottomright = (0, 0)

		self._tiled_mouse_pos = (0, 0)

	def get_ids(self) -> dict[int, dict[int, int]]:
		ids = {}

		for row in range(self.selected_topleft[1], self.selected_bottomright[1] + 1):
			for col in range(self.selected_topleft[0], self.selected_bottomright[0] + 1):
				if row not in ids:
					ids[row] = {}

				ids[row][col] = row * self.sprite_sheet.n_cols + col

		return ids

	def _update_state(self):
		self.editor_state.selected_topleft = self.selected_topleft
		self.editor_state.selected_bottomright = self.selected_bottomright

		self.editor_state.ids = self.get_ids()

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (self.sprite_sheet.tile_width, self.sprite_sheet.tile_height))

	def update(self, delta):
		self._mouse_update()
		self._get_mouse_pos()

		if InputManager.mouse_down[0]:
			if (0 <= self._tiled_mouse_pos[0] < self.sprite_sheet.n_cols and
					0 <= self._tiled_mouse_pos[1] < self.sprite_sheet.n_rows):
				self.selected_topleft = self._tiled_mouse_pos
				self.selected_bottomright = self._tiled_mouse_pos

		if InputManager.mouse_pressed[0]:
			if (0 <= self._tiled_mouse_pos[0] < self.sprite_sheet.n_cols and
					0 <= self._tiled_mouse_pos[1] < self.sprite_sheet.n_rows):
				self.selected_bottomright = self._tiled_mouse_pos

		if InputManager.mouse_up[0]:
			selected_topleft, selected_bottomright = abs_tuple(self.selected_topleft, self.selected_bottomright)

			self.selected_topleft = selected_topleft
			self.selected_bottomright = selected_bottomright

			self._update_state()

		self._keyboard_control(delta)
		self._mouse_control()

	def draw(self, display: pygame.Surface):
		self.sprite_sheet.draw_sheet(display, self._camera)

		selected_topleft, selected_bottomright = abs_tuple(self.selected_topleft, self.selected_bottomright)

		pygame.draw.rect(
			display, (255, 255, 255),
			pygame.Rect(
				selected_topleft[0] * self.sprite_sheet.tile_width - self._camera.target.x,
				selected_topleft[1] * self.sprite_sheet.tile_height - self._camera.target.y,
				self.sprite_sheet.tile_width * (selected_bottomright[0] - selected_topleft[0] + 1),
				self.sprite_sheet.tile_height * (selected_bottomright[1] - selected_topleft[1] + 1)
			), width=2
		)
