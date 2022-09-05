from data.modules.objects.object import AnimatableObject


class SmallCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 0, 3)
