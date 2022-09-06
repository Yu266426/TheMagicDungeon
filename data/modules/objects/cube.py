from data.modules.objects.game_object import AnimatableObject


class SmallCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 0, 3)


class SmallRedCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 7, 2)


class SmallGreenCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 14, 2)


class LargeCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 21, 3)


class LargeRedCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 28, 2)


class LargeGreenCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, 2, 35, 2)
