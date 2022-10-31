from enum import Enum


class EditorModes(Enum):
	TileEditing = 0
	TileSelecting = 1
	ObjectEditing = 2
	ObjectSelecting = 3


class SharedTileState:
	def __init__(self, sprite_sheet_name: str):
		# Tile mode
		self.level = 0

		self.sprite_sheet_name = sprite_sheet_name
		self.ids: dict[int, dict[int, int]] = {0: {0: 0}}

		self.selected_topleft = (0, 0)
		self.selected_bottomright = (0, 0)
