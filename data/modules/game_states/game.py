import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.inputs import InputManager
from data.modules.base.level import Level
from data.modules.game_states.game_state import GameState


class Game(GameState):
	def __init__(self):
		self.level = Level()

		self.camera = Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.x_input = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.y_input = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]

	def next_state(self):
		return self

	def update(self, delta: float):
		self.x_input = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.y_input = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]

		self.camera.set_target(self.camera.target + pygame.Vector2(self.x_input, self.y_input) * 600 * delta)

		if InputManager.keys_down[pygame.K_SPACE]:
			self.level = Level()

	def draw(self, display: pygame.Surface):
		display.fill("black")

		self.level.draw(display, self.camera)
