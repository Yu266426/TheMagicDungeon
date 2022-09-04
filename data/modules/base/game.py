import pygame.display

from data.modules.base.constants import SCREEN_HEIGHT, SCREEN_WIDTH, GameStates
from data.modules.editor.editor import Editor
from data.modules.base.inputs import InputManager
from data.modules.base.resources import ResourceManager


class Game:
	is_running: bool = True

	window: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock: pygame.time.Clock = pygame.time.Clock()

	game_state = GameStates.LOADING

	editor = None

	@classmethod
	def change_state(cls, new_state: GameStates, *args):
		if new_state == GameStates.EDITOR:
			if cls.editor is None:
				cls.editor = Editor()

			cls.game_state = new_state

	@classmethod
	def handle_events(cls):
		InputManager.reset()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				cls.is_running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					cls.is_running = False

				if event.key <= 512:
					InputManager.keys_down[event.key] = True

			elif event.type == pygame.KEYUP:
				if event.key <= 512:
					InputManager.keys_up[event.key] = True

			elif event.type == pygame.MOUSEBUTTONDOWN:
				button = event.button
				if button <= 2:
					InputManager.mouse_down[event.button - 1] = True

			elif event.type == pygame.MOUSEBUTTONUP:
				button = event.button
				if button <= 2:
					InputManager.mouse_up[event.button - 1] = True

	@classmethod
	def update(cls):
		cls.clock.tick()
		delta = cls.clock.get_time() / 1000

		pygame.display.set_caption(f"{round(cls.clock.get_fps())}")

		if cls.game_state == GameStates.LOADING:
			if ResourceManager.load_update():
				cls.change_state(GameStates.EDITOR)

		elif cls.game_state == GameStates.EDITOR:
			cls.editor.update(delta)

	@classmethod
	def draw(cls):
		if cls.game_state == GameStates.LOADING:
			cls.window.fill((0, 0, 0))

		elif cls.game_state == GameStates.EDITOR:
			cls.editor.draw(cls.window)

		pygame.display.update()
