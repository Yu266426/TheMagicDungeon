import pygame
import pygbase

from data.modules.entities.components.line_collider import LineCollider
from data.modules.entities.entity import Entity


class SwordSwing(Entity):
	def __init__(self, pos, angle: float, length: float, damage: int, flip: int):
		super().__init__(pos)
		self.alive = True

		self.damage = damage

		self.starting_angle = angle
		self.max_angle = 100

		self.flip = flip
		self.swing_speed = 700

		self.collider = LineCollider(self.pos, angle, length).link_pos(pos)

	def is_alive(self):
		return self.alive

	def update(self, delta: float):
		self.collider.change_angle(self.flip * self.swing_speed * delta)

		if abs(self.collider.angle - self.starting_angle) > self.max_angle:
			self.alive = False

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.collider.draw(screen, camera)
