import pygame
from pygbase import InputManager, Camera

from data.modules.base.constants import TILE_SIZE
from data.modules.base.room import EditorRoom
from data.modules.base.utils import draw_rect_outline
from data.modules.editor.actions.editor_actions import EditorActionBatch, EditorActionQueue
from data.modules.editor.actions.object_actions import RemoveObjectAction, PlaceObjectAction
from data.modules.editor.editor_selection_info import ObjectSelectionInfo
from data.modules.editor.shared_editor_state import SharedEditorState
from data.modules.editor.tools.editor_tool import EditorTool


class ObjectDrawTool(EditorTool):
	def __init__(self, room: EditorRoom, shared_state: SharedEditorState, action_queue: EditorActionQueue):
		super().__init__(room, shared_state, action_queue)

		self.current_mouse_pos: tuple | None = None

		self.current_batch: EditorActionBatch | None = None

	def update(self, mouse_pos: tuple[int, int], selection_info: ObjectSelectionInfo):
		if InputManager.mouse_pressed[0]:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = mouse_pos[1] * TILE_SIZE

			if selection_info.current_object_type is not None and self._room.get_object((x_pos, y_pos - 1)) is None:
				action = PlaceObjectAction(self._room, selection_info.current_object_type((x_pos, y_pos)))
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
				self._action_queue.add_action(self.current_batch)
				self.current_batch = None

	def draw(self, screen: pygame.Surface, camera: Camera, mouse_pos: tuple, selection_info: ObjectSelectionInfo):
		draw_rect_outline(
			screen, (255, 255, 255),
			(mouse_pos[0] * TILE_SIZE - camera.pos.x, mouse_pos[1] * TILE_SIZE - camera.pos.y),
			(TILE_SIZE, TILE_SIZE),
			2
		)

		# Draw selected object if not deleting
		if not InputManager.mouse_pressed[2]:
			if selection_info.current_object_type is not None:
				x_pos = mouse_pos[0] * TILE_SIZE
				y_pos = mouse_pos[1] * TILE_SIZE

				selection_info.current_object_type((x_pos, y_pos)).draw(screen, camera, flag=pygame.BLEND_ADD)
