import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.inputs import InputManager
from data.modules.base.level import Level


class GameScene:
	def __init__(self):
		self.level = Level()

		self.camera = Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

	def update(self, delta: float):
		x_input = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		y_input = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]

		self.camera.set_target(self.camera.target + pygame.Vector2(x_input, y_input) * 600 * delta)

	def draw(self, display: pygame.Surface):
		display.fill("black")

		self.level.draw(display, self.camera)
