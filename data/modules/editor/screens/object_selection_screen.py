import pygame

from data.modules.base.inputs import InputManager
from data.modules.base.utils import draw_rect_outline, get_tile_pos
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.objects.game_object import AnimatableObject, GameObject
from data.modules.ui.screen import ControlledScreen


class ObjectSelectionScreen(ControlledScreen):
	def __init__(self, editor_state: SharedTileState, object_types: list, object_size: tuple, n_cols=1):
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
			if 0 <= self._tiled_mouse_pos[0] < self.n_cols and 0 <= self._tiled_mouse_pos[1] < self.n_rows:
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

		draw_rect_outline(
			display, (255, 255, 255),
			((self.selected_object_index % self.n_cols) * self.object_size[0] - self._camera.target.x, (self.selected_object_index // self.n_cols) * self.object_size[1] - self._camera.target.y),
			self.object_size,
			2
		)