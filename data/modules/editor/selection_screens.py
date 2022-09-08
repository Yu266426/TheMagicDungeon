import pygame

from data.modules.base.constants import SCREEN_HEIGHT, TILE_SCALE, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.base.resources import ResourceManager, ResourceTypes
from data.modules.base.utils import abs_tuple, get_tile_pos
from data.modules.editor.editor_state import EditorState
from data.modules.graphics.sprite_sheet import SpriteSheet
from data.modules.objects.chest import Chest
from data.modules.objects.cube import SmallCube, SmallRedCube, SmallGreenCube, LargeCube, LargeRedCube, LargeGreenCube
from data.modules.objects.lever import Lever
from data.modules.objects.game_object import GameObject, AnimatableObject
from data.modules.ui.element import Frame, Button
from data.modules.ui.screen import UIScreen, ControlledScreen


class TileSelectionScreen:
	def __init__(self, editor_state: EditorState, sheet_ids: list[int]):
		self.editor_state: EditorState = editor_state

		self.screens: list[SpriteSheetScreen] = []
		for sheet_id in sheet_ids:
			self.screens.append(SpriteSheetScreen(self.editor_state, sheet_id))

		self.current_screen: SpriteSheetScreen = self.screens[0]

		self.ui_screen: UIScreen = UIScreen()
		self.button_frame = self.ui_screen.add_frame(Frame((0, SCREEN_HEIGHT - 86), (SCREEN_WIDTH, 90)))

		if len(sheet_ids) > 0:
			self.button_frame.add_element(Button((3, 3), 0, self.switch_screen, 0))

			for loop in range(1, len(sheet_ids)):
				self.button_frame.add_element(Button((3, 0), 0, self.switch_screen, loop), align_with_previous=(False, True), add_on_to_previous=(True, False))

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

	def update_state(self):
		selected_topleft, selected_bottomright = abs_tuple(self.selected_topleft, self.selected_bottomright)

		self.selected_topleft = selected_topleft
		self.selected_bottomright = selected_bottomright

		self.editor_state.selected_topleft = self.selected_topleft
		self.editor_state.selected_bottomright = self.selected_bottomright

		self.editor_state.ids = self.get_ids()

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (self.sprite_sheet.tile_width, self.sprite_sheet.tile_height))

	def update(self, delta: float):
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
			self.update_state()

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


class ObjectsSelectionScreen:
	def __init__(self, editor_state: EditorState):
		self._editor_state: EditorState = editor_state

		self.screens: list[ObjectSelectionScreen] = [
			ObjectSelectionScreen(self._editor_state, [SmallCube, SmallRedCube, SmallGreenCube, LargeCube, LargeRedCube, LargeGreenCube, Lever, Chest], (16 * TILE_SCALE, 16 * TILE_SCALE), n_cols=3)
		]

		self.current_screen: ObjectSelectionScreen = self.screens[0]

		self.ui_screen: UIScreen = UIScreen()
		self.button_frame = self.ui_screen.add_frame(
			Frame((0, SCREEN_HEIGHT - 86), (SCREEN_WIDTH, 90)).
			add_element(Button((3, 3), 0, self.switch_screen, 0))
		)

	def switch_screen(self, new_screen_id: int):
		"""
		Callback for button press
		:param new_screen_id: Screen index to switch to
		:return: None
		"""

		self.current_screen = self.screens[new_screen_id]
		self._editor_state.current_object_type = type(self.current_screen.objects[self.current_screen.selected_object_index])

	def get_selected(self):
		return type(self.current_screen.objects[self.current_screen.selected_object_index])

	def update(self, delta: float):
		if not self.ui_screen.on_ui():
			self.current_screen.update(delta)

		self.ui_screen.update(delta)

	def draw(self, display: pygame.Surface):
		self.current_screen.draw(display)

		self.ui_screen.draw(display)


class ObjectSelectionScreen(ControlledScreen):
	def __init__(self, editor_state: EditorState, object_types: list, object_size: tuple, n_cols=1):
		super().__init__()

		self._editor_state = editor_state

		self.object_size = object_size
		self.n_cols = n_cols
		self.n_rows = len(object_types) // n_cols + 1

		self.selected_object_index = 0
		self.objects: list[GameObject | AnimatableObject] = []
		for index, object_type in enumerate(object_types):
			x = index % n_cols
			y = index // n_cols
			self.objects.append(object_type((x * object_size[0], y * object_size[1])))

		self._tiled_mouse_pos = (0, 0)

	def _get_mouse_pos(self):
		self._tiled_mouse_pos = get_tile_pos(self._world_mouse_pos, (self.object_size[0], self.object_size[1]))

	def update(self, delta: float):
		self._mouse_update()
		self._get_mouse_pos()

		if InputManager.mouse_down[0]:
			if (0 <= self._tiled_mouse_pos[0] < self.n_cols and
					0 <= self._tiled_mouse_pos[1] < self.n_rows):
				index = self._tiled_mouse_pos[1] * self.n_cols + self._tiled_mouse_pos[0]
				if index < len(self.objects):
					self.selected_object_index = index
					self._editor_state.current_object_type = type(self.objects[self.selected_object_index])

		# Animate objects
		for game_object in self.objects:
			if issubclass(type(game_object), AnimatableObject):
				game_object.change_frame(delta * 2)

		self._mouse_control()
		self._keyboard_control(delta)

	def draw(self, display: pygame.Surface):
		for game_object in self.objects:
			game_object.draw(display, self._camera)

		pygame.draw.rect(
			display, (255, 255, 255),
			pygame.Rect(
				(self.selected_object_index % self.n_cols) * self.object_size[0] - self._camera.target.x,
				(self.selected_object_index // self.n_cols) * self.object_size[1] - self._camera.target.y,
				self.object_size[0], self.object_size[1]
			),
			width=2
		)
