import pygame.display

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.inputs import InputManager
from data.modules.game_states.loader import Loading


class App:
	def __init__(self):
		pygame.init()

		self.is_running: bool = True
		self.target_fps = 60

		self.flags = pygame.SCALED | pygame.FULLSCREEN
		self.window: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.game_state = Loading()

	def handle_events(self):
		InputManager.reset()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.is_running = False

				if event.key <= 512:
					InputManager.keys_down[event.key] = True

			elif event.type == pygame.KEYUP:
				if event.key <= 512:
					InputManager.keys_up[event.key] = True

			elif event.type == pygame.MOUSEBUTTONDOWN:
				button = event.button - 1
				if button <= 2:
					InputManager.mouse_down[button] = True

			elif event.type == pygame.MOUSEBUTTONUP:
				button = event.button - 1
				if button <= 2:
					InputManager.mouse_up[button] = True

	def update(self):
		self.clock.tick()
		pygame.display.set_caption(f"{round(self.clock.get_fps())}")

		self.game_state.update(self.clock.get_time() / 1000)

	def draw(self):
		self.game_state.draw(self.window)

		pygame.display.flip()

	def switch_state(self):
		self.game_state = self.game_state.next_state()
