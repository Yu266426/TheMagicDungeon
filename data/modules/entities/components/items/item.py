import pygame
from pygbase import Camera

from data.modules.entities.entity import Entity


class Item(Entity):
	def __init__(self, durability: int):
		super().__init__((0, 0))

		self.durability: int = durability
		self.flip_x: bool = False  # Updated by ItemSlot

	def added_to_slot(self, pos: pygame.Vector2):
		self.pos = pos

	def check_durability(self):
		if self.durability != -1:
			return self.durability > 0
		else:
			return True

	def reduce_durability(self, amount):
		if self.durability != -1:
			self.durability -= amount
			if self.durability < 0:
				self.durability = 0

	def update(self, delta: float):
		pass

	def draw(self, screen: pygame.Surface, camera: Camera):
		pass
