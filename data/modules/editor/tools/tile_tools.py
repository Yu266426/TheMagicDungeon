import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.base.room import Room
from data.modules.base.utils import draw_rect_outline
from data.modules.editor.actions.editor_actions import EditorActionBatch, EditorActionQueue
from data.modules.editor.actions.tile_actions import RemoveTileAction, PlaceTileAction
from data.modules.editor.shared_editor_state import SharedTileState
from data.modules.editor.tools.editor_tool import EditorTool
from data.modules.objects.tile import Tile


class TileDrawTool(EditorTool):
	def __init__(self, room: Room, editor_state: SharedTileState, action_queue: EditorActionQueue):
		super().__init__(room, editor_state, action_queue)

		self.current_place_tile: tuple[int, int] | None = None
		self.current_erase_tile: tuple[int, int] | None = None

		self.current_batch: EditorActionBatch | None = None

	def draw_tiles(self, mouse_pos: tuple[int, int]):
		for row, row_data in self._editor_state.ids.items():
			for col, image_id in row_data.items():
				tile_x = mouse_pos[0] + col - self._editor_state.selected_topleft[0]
				tile_y = mouse_pos[1] + row - self._editor_state.selected_topleft[1]

				if self.current_place_tile != mouse_pos:
					action = PlaceTileAction(self._room, self._editor_state.level, tile_y, tile_x, Tile(
						self._editor_state.sprite_sheet_name,
						image_id,
						(tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
					))
					action.execute()

					if self.current_batch is None:
						self.current_batch = EditorActionBatch()

					self.current_batch.add_action(action)

		self.current_place_tile = mouse_pos

	def erase_tiles(self, mouse_pos: tuple[int, int]):
		for row in range(self._editor_state.selected_bottomright[1] - self._editor_state.selected_topleft[1] + 1):
			for col in range(self._editor_state.selected_bottomright[0] - self._editor_state.selected_topleft[0] + 1):
				tile_x = mouse_pos[0] + col
				tile_y = mouse_pos[1] + row

				if self.current_erase_tile != mouse_pos:
					action = RemoveTileAction(self._room, self._editor_state.level, tile_y, tile_x)
					action.execute()

					if self.current_batch is None:
						self.current_batch = EditorActionBatch()

					self.current_batch.add_action(action)

		self.current_erase_tile = mouse_pos

	def update(self, mouse_pos: tuple[int, int]):
		# Draw
		if InputManager.mouse_pressed[0]:
			self.draw_tiles(mouse_pos)

		# Erase
		elif InputManager.mouse_pressed[2]:
			self.erase_tiles(mouse_pos)

		if InputManager.mouse_up[0] or InputManager.mouse_up[2]:
			if self.current_batch is not None:
				self._action_queue.add_action(self.current_batch)
				self.current_batch = None

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		# Tile outline rect
		draw_rect_outline(
			display, (255, 255, 255),
			(mouse_pos[0] * TILE_SIZE - camera.target.x, mouse_pos[1] * TILE_SIZE - camera.target.y),
			(TILE_SIZE * (self._editor_state.selected_bottomright[0] - self._editor_state.selected_topleft[0] + 1), TILE_SIZE * (self._editor_state.selected_bottomright[1] - self._editor_state.selected_topleft[1] + 1)),
			2
		)

		# If not deleting tiles, draw ghost tile
		if not InputManager.mouse_pressed[2]:
			for row, row_data in self._editor_state.ids.items():
				for col, image_id in row_data.items():
					tile_x = mouse_pos[0] + col - self._editor_state.selected_topleft[0]
					tile_y = mouse_pos[1] + row - self._editor_state.selected_topleft[1]

					Tile(
						self._editor_state.sprite_sheet_name,
						image_id,
						(tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
					).draw(display, camera, flag=pygame.BLEND_ADD)
