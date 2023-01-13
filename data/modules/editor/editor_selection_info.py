from typing import Optional, Union, Type

from data.modules.objects.game_object import GameObject, AnimatableObject


class TileSelectionInfo:
	def __init__(self, sprite_sheet_name: str):
		# Draw Layer
		self.layer = 0

		# Selection Info
		self.sprite_sheet_name = sprite_sheet_name
		self.ids: dict[int, dict[int, int]] = {0: {0: 0}}

		self.selected_topleft = (0, 0)
		self.selected_bottomright = (0, 0)


class ObjectSelectionInfo:
	def __init__(self, starting_object: Union[Type[GameObject], Type[AnimatableObject]]):
		self.current_object_type: Optional[Type] = starting_object
