import pygame

from data.modules.base.camera import Camera
from data.modules.base.inputs import InputManager
from data.modules.base.level import Level
from data.modules.entities.entity import Entity


class Player(Entity):
	def __init__(self, pos: tuple[int, int], image, level: Level):
		super().__init__(pos, image, hitbox=(80, 50))
		self.image.fill("red")

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

	def draw(self, display: pygame.Surface, camera: Camera):
		display.blit(self.image, self.image.get_rect(midbottom=self.pos).topleft - camera.target)
