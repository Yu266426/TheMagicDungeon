import pygbase

from data.modules.objects.game_object import GameObject


class RuneAltar(GameObject):
	def __init__(self, pos: tuple, pixel_pos: bool):
		self.inactive_image = pygbase.ResourceManager.get_resource("sprite_sheet", "rune_altar").get_image(0)
		self.transition_animation = pygbase.Animation("sprite_sheet", "rune_altar", 1, 2, looping=False)
		self.active_image = pygbase.ResourceManager.get_resource("sprite_sheet", "rune_altar").get_image(3)

		super().__init__("rune_altar", pos, pixel_pos, self.inactive_image)

	def update(self, delta: float):
		pass
