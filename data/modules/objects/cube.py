from data.modules.objects.game_object import AnimatableObject


class SmallCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 0, 3)


class SmallRedCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 7, 2)


class SmallGreenCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 14, 2)


class LargeCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 21, 3)


class LargeRedCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 28, 2)


class LargeGreenCube(AnimatableObject):
	def __init__(self, pos: tuple):
		super().__init__(pos, "small_animatable", 35, 2)
