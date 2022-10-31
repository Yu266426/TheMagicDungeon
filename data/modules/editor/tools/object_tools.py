import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import draw_rect_outline
from data.modules.editor.actions.editor_actions import EditorActionBatch
from data.modules.editor.actions.object_actions import RemoveObjectAction, PlaceObjectAction
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.editor.tools.editor_tool import EditorTool


class ObjectDrawTool(EditorTool):
	def __init__(self, room: Room, editor_state: SharedTileState):
		super().__init__(room, editor_state)

		self.current_mouse_pos: tuple | None = None

		self.current_batch: EditorActionBatch | None = None

	def update(self, mouse_pos: tuple[int, int]):
		if InputManager.mouse_pressed[0]:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = mouse_pos[1] * TILE_SIZE

			if self._room.get_object((x_pos, y_pos - 1)) is None:
				action = PlaceObjectAction(self._room, self._editor_state.current_object_type((x_pos, y_pos)))
				action.execute()

				if self.current_batch is None:
					self.current_batch = EditorActionBatch()

				self.current_batch.add_action(action)

		if InputManager.mouse_pressed[2]:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = (mouse_pos[1] - 1) * TILE_SIZE

			if self._room.get_object((x_pos, y_pos)) is not None:
				action = RemoveObjectAction(self._room, self._room.get_object((x_pos, y_pos)))
				action.execute()

				if self.current_batch is None:
					self.current_batch = EditorActionBatch()

				self.current_batch.add_action(action)

		if InputManager.mouse_up[0] or InputManager.mouse_up[2]:
			if self.current_batch is not None:
				self._editor_state.add_action(self.current_batch)
				self.current_batch = None

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		draw_rect_outline(
			display, (255, 255, 255),
			(mouse_pos[0] * TILE_SIZE - camera.target.x, mouse_pos[1] * TILE_SIZE - camera.target.y),
			(TILE_SIZE, TILE_SIZE),
			2
		)

		# Draw selected object
		if self._editor_state.current_object_type is not None:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = mouse_pos[1] * TILE_SIZE

			self._editor_state.current_object_type((x_pos, y_pos)).draw(display, camera, flag=pygame.BLEND_ADD)
