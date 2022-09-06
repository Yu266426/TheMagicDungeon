from data.modules.objects.game_object import AnimatableObject


class Chest(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 63, 6, looping=False)
