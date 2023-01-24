import pygame

from data.modules.base.app import App
from data.modules.base.events import EventManager
from data.modules.base.inputs import InputManager

if __name__ == '__main__':
	pygame.init()

	EventManager.init()
	InputManager.register_handlers()

	app = App()
	app.run()

	pygame.quit()
