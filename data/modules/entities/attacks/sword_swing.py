import pygame
import pygbase

from data.modules.entities.components.line_collider import LineCollider
from data.modules.entities.entity import Entity


class SwordSwing(Entity):
	def __init__(self, pos, angle: float, length: float, damage: int):
		super().__init__(pos)

		self.damage = damage

		self.collider = LineCollider(self.pos, angle, length)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.collider.draw(screen, camera)
