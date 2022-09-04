import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.inputs import InputManager
from data.modules.ui.element import Frame


class ControlledScreen:
	def __init__(self, pos: tuple[int | float, int | float] = (0, 0), keep_in: tuple | None = None):
		self._camera: Camera = Camera(pos)
		self._prev_target: pygame.Vector2 = self._camera.target.copy()

		self._mouse_pos: pygame.Vector2 = pygame.Vector2(pygame.mouse.get_pos())
		self._prev_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self._world_mouse_pos: pygame.Vector2 = self._mouse_pos.copy()

		self.keep_in = keep_in

	def _handle_bounds(self):
		if self.keep_in is not None:
			if self.keep_in[2] - self.keep_in[0] < SCREEN_WIDTH:
				if self.keep_in[0] < self._camera.target.x:
					self._camera.target.x = self.keep_in[0]
				if self._camera.target.x + SCREEN_WIDTH < self.keep_in[2]:
					self._camera.target.x = self.keep_in[2] - SCREEN_WIDTH
			else:
				if self._camera.target.x < self.keep_in[0] - 20:
					self._camera.target.x = self.keep_in[0] - 20
				if self.keep_in[2] < self._camera.target.x + SCREEN_WIDTH + 20:
					self._camera.target.x = self.keep_in[2] - SCREEN_WIDTH + 20

			if self.keep_in[3] - self.keep_in[1] < SCREEN_HEIGHT:
				if self.keep_in[1] < self._camera.target.y:
					self._camera.target.y = self.keep_in[1]
				if self._camera.target.y + SCREEN_HEIGHT < self.keep_in[3]:
					self._camera.target.y = self.keep_in[3] - SCREEN_HEIGHT
			else:
				if self._camera.target.y < self.keep_in[1] - 20:
					self._camera.target.y = self.keep_in[1] - 20
				if self.keep_in[3] < self._camera.target.y + SCREEN_HEIGHT + 20:
					self._camera.target.y = self.keep_in[3] - SCREEN_HEIGHT + 20

	def _mouse_update(self):
		self._mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

		self._world_mouse_pos = self._camera.screen_to_world(self._mouse_pos)

	def _mouse_control(self, mouse_button: int = 1):
		if InputManager.mouse_down[mouse_button]:
			self._prev_mouse_pos = self._mouse_pos.copy()
			self._prev_target = self._camera.target.copy()
		if InputManager.mouse_pressed[mouse_button]:
			self._camera.set_target(self._prev_target + (self._prev_mouse_pos - self._mouse_pos))

		self._handle_bounds()

	def _keyboard_control(self, delta: float, speed: float = 600):
		if InputManager.mods == 0:
			x_input = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
			y_input = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]

			self._camera.set_target(self._camera.target + pygame.Vector2(x_input, y_input) * speed * delta)

		self._handle_bounds()


class UIScreen:
	def __init__(self):
		self._frames: list[Frame] = []

	def add_frame(self, frame: Frame):
		self._frames.append(frame)
		return frame

	def on_ui(self) -> bool:
		for frame in self._frames:
			if frame.rect.collidepoint(*pygame.mouse.get_pos()):
				return True

		return False

	def update(self, delta: float):
		for frame in self._frames:
			frame.update(delta)

	def draw(self, display: pygame.Surface):
		for frame in self._frames:
			frame.draw(display)
