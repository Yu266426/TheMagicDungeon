import pygame
import pygbase

from data.modules.base.constants import TILE_SCALE
from data.modules.objects.game_object import GameObject


class Torch(GameObject):
	def __init__(self, pos: tuple, additional_args: dict):
		super().__init__("torch", pos, pygbase.ResourceManager.get_resource("sprite_sheet", "objects").get_image(1))

		if "particle_manager" in additional_args:
			self.particle_manager: pygbase.ParticleManager = additional_args["particle_manager"]
			self.fire = self.particle_manager.add_spawner(pygbase.CircleSpawner(self.pos + pygame.Vector2(8 * TILE_SCALE, 12), 0.05, 3, 20, True, "fire", self.particle_manager))
		else:
			self.particle_manager = None
			self.fire = None

	def removed(self):
		if self.particle_manager is not None:
			self.particle_manager.remove_spawner(self.fire)
