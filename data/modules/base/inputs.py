import pygame.mouse


class InputManager:
	# Mouse
	mouse_down: list[bool, bool, bool] = [False, False, False]
	mouse_up: list[bool, bool, bool] = [False, False, False]
	mouse_pressed: tuple[bool, bool, bool] = (False, False, False)

	# Keyboard
	keys_down = [False] * 512
	keys_pressed = [False] * 512
	keys_up = [False] * 512

	mods = 0

	@classmethod
	def reset(cls):
		cls.mouse_down[:] = [False, False, False]
		cls.mouse_up[:] = [False, False, False]
		cls.mouse_pressed = pygame.mouse.get_pressed(3)

		cls.keys_down[:] = [False] * 512
		cls.keys_up[:] = [False] * 512
		cls.keys_pressed = pygame.key.get_pressed()

		cls.mods = pygame.key.get_mods()
