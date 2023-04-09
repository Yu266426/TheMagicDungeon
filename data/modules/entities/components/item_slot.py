from typing import Optional

import pygame
from pygbase import Camera, Common

from data.modules.entities.components.items.item import Item


class ItemSlot:
	def __init__(self, pos: pygame.Vector2, offset: tuple):
		self.pos = pos
		self.offset = pygame.Vector2(offset)
		self.offset_pos = self.pos + self.offset

		self.item: Optional[Item] = None

		self.entity_manager = Common.get_value("entities")

		self.flip_x = False

	def equip_item(self, item: Item, tags: Optional[list[str]] = None):
		self.item = item
		self.item.added_to_slot(self.offset_pos)

		self.entity_manager.add_entity(self.item, tags)

	def update(self, delta: float):
		if not self.flip_x:
			self.offset_pos.update(self.pos + self.offset)
		else:
			self.offset_pos.update((self.pos.x - self.offset.x, self.pos.y + self.offset.y))

		if self.item is not None:
			self.item.update(delta)

			if not self.item.check_durability():
				self.entity_manager.remove_entity(self.item)
				self.item = None

	def draw(self, screen: pygame.Surface, camera: Camera):
		if self.item is not None:
			self.item.draw(screen, camera)
