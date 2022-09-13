from data.modules.objects.game_object import AnimatableObject


class Lever(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 56, 7, looping=False)
