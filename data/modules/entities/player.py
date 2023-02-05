import pygame
from pygbase import InputManager, Camera
from pygbase.graphics.animation import Animation

from data.modules.base.level import Level
from data.modules.entities.entity import Entity


class Player(Entity):
	def __init__(self, pos: tuple[int, int], level: Level):
		super().__init__(pos, None, hitbox=(80, 50))
		self.walk_animation = Animation("player_run_animation", 0, 2)

		self.input = pygame.Vector2()

		self.level = level

	def get_inputs(self):
		self.input.x = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.input.y = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]
		if self.input.length() != 0:
			self.input.normalize_ip()

		if InputManager.mods & pygame.KMOD_SHIFT:
			self.input *= 0.4

	def update(self, delta: float):
		self.get_inputs()

		self.move(self.input * 500 * delta, self.level)

		self.walk_animation.change_frame(10 * delta)

	def draw(self, display: pygame.Surface, camera: Camera):
		self.walk_animation.draw_at_pos(display, self.pos, camera, draw_pos="midbottom")
