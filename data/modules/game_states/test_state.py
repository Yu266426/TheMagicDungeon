import pygame
import pygbase

from data.modules.entities.components.hitbox import Hitbox
from data.modules.entities.components.line_collider import LineCollider


class TestState(pygbase.GameState, name="testing"):
	def __init__(self):
		super().__init__()

		self.box = Hitbox((200, 200), (200, 300))
		self.box_lines = self.box.get_edge_lines()

		self.line = LineCollider((30, 30), 100, 1000)

	def update(self, delta: float):
		if pygbase.InputManager.get_key_pressed(pygame.K_a):
			self.line.set_angle(self.line.angle - 10 * delta)
		if pygbase.InputManager.get_key_pressed(pygame.K_d):
			self.line.set_angle(self.line.angle + 10 * delta)

		# print(self.line.collides_with(self.box_lines[0]))
		print(self.box.collides_with(self.line), self.line.collides_with(self.box))

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))

		pygame.draw.rect(screen, "white", self.box.rect)
		self.line.draw(screen, pygbase.Camera())

		pygame.draw.line(screen, "green", self.box_lines[0].start_pos, self.box_lines[0].end_pos, width=5)
