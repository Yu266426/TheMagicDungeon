class TileSelectionInfo:
	def __init__(self, sprite_sheet_name: str):
		# Tile mode
		self.layer = 0

		self.sprite_sheet_name = sprite_sheet_name
		self.ids: dict[int, dict[int, int]] = {0: {0: 0}}

		self.selected_topleft = (0, 0)
		self.selected_bottomright = (0, 0)
