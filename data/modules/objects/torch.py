import pygbase

from data.modules.objects.game_object import GameObject


class Torch(GameObject):
	def __init__(self, pos: tuple):
		super().__init__("torch", pos, pygbase.ResourceManager.get_resource())
