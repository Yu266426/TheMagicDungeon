import pygame
from pygbase import Camera, Common, InputManager
from pygbase.graphics.animation import AnimationManager, Animation

from data.modules.entities.attacks.sword_swing import SwordSwing
from data.modules.entities.components.items.item import Item
from data.modules.entities.components.line_collider import LineCollider
from data.modules.entities.entity_manager import EntityManager


class EnergySword(Item):
	def __init__(self):
		super().__init__(100)

		self.animations = AnimationManager([
			("drawn", Animation("energy_sword", 0, 1), 1)
		], "drawn")

		self.angle = -30

		self.entity_manager: EntityManager = Common.get_value("entities")

	def added_to_slot(self, pos: pygame.Vector2):
		super().added_to_slot(pos)

	def update(self, delta: float):
		self.animations.update(delta)

		if InputManager.mouse_pressed[0]:
			self.entity_manager.add_entity(SwordSwing(self.pos, self.angle, 40, 5), tags=["damage"])

	def draw(self, screen: pygame.Surface, camera: Camera):
		self.animations.draw_at_pos(screen, self.pos, camera, angle=self.angle, draw_pos="midbottom")
