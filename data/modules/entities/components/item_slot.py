from typing import Optional

import pygame
import pygbase
from pygbase.utils import get_angle_to

from data.modules.entities.items.item import Item
from data.modules.entities.entity_manager import EntityManager


class ItemSlot:
	def __init__(self, pos: pygame.Vector2, offset: tuple, entities: EntityManager, camera: pygbase.Camera):
		self.pos = pos
		self.offset = pygame.Vector2(offset)
		self.offset_pos = self.pos + self.offset

		self.flip_x = False

		self.item: Optional[Item] = None

		self.entity_manager = entities
		self.camera = camera

	def equip_item(self, item: Item, tags: Optional[tuple[str]] = None):
		self.item = item
		self.item.added_to_slot(self.offset_pos)

		self.entity_manager.add_entity(self.item, tags)

	def update(self, delta: float):
		mouse_pos = self.camera.screen_to_world(pygame.mouse.get_pos())
		if mouse_pos.x < self.pos.x:
			self.flip_x = True
			self.offset_pos.update(self.pos.x - self.offset.x, self.pos.y + self.offset.y)
		else:
			self.flip_x = False
			self.offset_pos.update(self.pos + self.offset)

		if self.item is not None:
			self.item.angle = get_angle_to(self.camera.world_to_screen(self.offset_pos), pygame.mouse.get_pos()) % 360
			self.item.flip_x = self.flip_x

			if not self.item.check_durability():
				self.entity_manager.add_entity_to_remove(self.item)
				self.item = None

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		if self.item is not None:
			self.item.draw(screen, camera)
