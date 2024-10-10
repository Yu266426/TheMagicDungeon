import random

import pygame
import pygbase

from data.modules.objects.game_object import GameObject


class Torch(GameObject):
	def __init__(self, pos: tuple, pixel_pos: bool):
		super().__init__("torch", pos, pixel_pos, pygbase.ResourceManager.get_resource("sprite_sheet", "objects").get_image(1))

		self.particle_manager: pygbase.ParticleManager = pygbase.Common.get_value("particle_manager")
		self.fire = pygbase.CircleSpawner(self.pos + pygame.Vector2(0, -92), 0.05, 3, 20, True, "fire", self.particle_manager)

		self.lighting_manager: pygbase.LightingManager = pygbase.Common.get_value("lighting_manager")
		self.light = pygbase.Light(self.pos + pygame.Vector2(0, -92), 0.3, 50, 5, random.uniform(1.7, 2.3), tint=(255, 225, 53))

	def added(self):
		self.particle_manager.add_spawner(self.fire)
		self.lighting_manager.add_light(self.light)

	def removed(self):
		self.particle_manager.remove_spawner(self.fire)
		self.lighting_manager.remove_light(self.light)
