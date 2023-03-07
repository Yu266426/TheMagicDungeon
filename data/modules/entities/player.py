import pygame
from pygbase import InputManager, Camera, AnimationManager, Animation

from data.modules.base.level import Level
from data.modules.entities.entity import Entity


class Player(Entity):
	def __init__(self, pos: tuple[int, int], level: Level):
		super().__init__(pos, None, hitbox=(70, 50))

		self.current_state = "idle"

		self.animations = AnimationManager([
			("idle", Animation("player_idle_animation", 0, 1), 8),
			("run", Animation("player_run_animation", 0, 2), 8)
		], "player_idle")

		self.input = pygame.Vector2()

		self.level = level

	def get_inputs(self):
		self.input.x = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.input.y = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]
		if self.input.length() != 0:
			self.input.normalize_ip()
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

		if InputManager.mods & pygame.KMOD_SHIFT:
			self.input *= 0.4

	def update(self, delta: float):
		self.get_inputs()

		self.move(self.input * 500 * delta, self.level)

		self.animations.update(delta)

	def draw(self, display: pygame.Surface, camera: Camera):
		self.animations.draw_at_pos(display, self.pos, camera, draw_pos="midbottom")
