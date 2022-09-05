import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE
from data.modules.base.inputs import InputManager
from data.modules.base.level import Room
from data.modules.editor.editor_actions import PlaceTileAction, RemoveTileAction, EditorActionBatch, PlaceObjectAction, RemoveObjectAction
from data.modules.editor.editor_state import EditorState
from data.modules.objects.tile import Tile


class EditorTool:
	def __init__(self, room: Room, editor_state: EditorState):
		self._room = room
		self._editor_state = editor_state

	def update(self, mouse_pos: tuple[int, int]):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		pass


class TileDrawTool(EditorTool):
	def __init__(self, room: Room, editor_state: EditorState):
		super().__init__(room, editor_state)

		self.current_place_tile: tuple[int, int] | None = None
		self.current_erase_tile: tuple[int, int] | None = None

		self.current_batch: EditorActionBatch | None = None

	def update(self, mouse_pos: tuple[int, int]):
		# Draw
		if InputManager.mouse_pressed[0]:
			for row, row_data in self._editor_state.ids.items():
				for col, image_id in row_data.items():
					tile_x = mouse_pos[0] + col - self._editor_state.selected_topleft[0]
					tile_y = mouse_pos[1] + row - self._editor_state.selected_topleft[1]

					if self.current_place_tile != mouse_pos:
						action = PlaceTileAction(self._room, self._editor_state.level, tile_y, tile_x, Tile(
							self._editor_state.sprite_sheet_id,
							image_id,
							(tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
						))
						action.execute()

						if self.current_batch is None:
							self.current_batch = EditorActionBatch()

						self.current_batch.add_action(action)

			self.current_place_tile = mouse_pos

		# Erase
		elif InputManager.mouse_pressed[2]:
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

		if InputManager.mouse_up[0] or InputManager.mouse_up[2]:
			if self.current_batch is not None:
				self._editor_state.add_action(self.current_batch)
				self.current_batch = None

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		# Tile outline rect
		pygame.draw.rect(
			display, (255, 255, 255),
			pygame.Rect(
				mouse_pos[0] * TILE_SIZE - camera.target.x,
				mouse_pos[1] * TILE_SIZE - camera.target.y,
				TILE_SIZE * (self._editor_state.selected_bottomright[0] - self._editor_state.selected_topleft[0] + 1),
				TILE_SIZE * (self._editor_state.selected_bottomright[1] - self._editor_state.selected_topleft[1] + 1)
			), width=2
		)

		# If not deleting tiles, draw ghost tile
		if not InputManager.mouse_pressed[2]:
			for row, row_data in self._editor_state.ids.items():
				for col, image_id in row_data.items():
					tile_x = mouse_pos[0] + col - self._editor_state.selected_topleft[0]
					tile_y = mouse_pos[1] + row - self._editor_state.selected_topleft[1]

					Tile(
						self._editor_state.sprite_sheet_id,
						image_id,
						(tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
					).draw(display, camera, flag=pygame.BLEND_ADD)


class ObjectDrawTool(EditorTool):
	def __init__(self, room: Room, editor_state: EditorState):
		super().__init__(room, editor_state)

		self.current_mouse_pos: tuple | None = None

	def update(self, mouse_pos: tuple[int, int]):
		if InputManager.mouse_pressed[0]:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = mouse_pos[1] * TILE_SIZE

			if self._room.get_object((x_pos, y_pos - 1)) is None:
				action = PlaceObjectAction(self._room, self._editor_state.current_object_type((x_pos, y_pos)))
				action.execute()

				self._editor_state.add_action(action)

		if InputManager.mouse_pressed[2]:
			x_pos = mouse_pos[0] * TILE_SIZE
			y_pos = (mouse_pos[1] - 1) * TILE_SIZE

			if self._room.get_object((x_pos, y_pos)) is not None:
				action = RemoveObjectAction(self._room, self._room.get_object((x_pos, y_pos)))
				action.execute()

				self._editor_state.add_action(action)

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		pygame.draw.rect(
			display, (255, 255, 255),
			pygame.Rect(
				mouse_pos[0] * TILE_SIZE - camera.target.x,
				mouse_pos[1] * TILE_SIZE - camera.target.y,
				TILE_SIZE,
				TILE_SIZE
			), width=2
		)
