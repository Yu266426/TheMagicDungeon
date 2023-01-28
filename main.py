import pygame

from data.modules.engine.app import App
import data.modules.engine as engine
from data.modules.game_states.main_menu import MainMenu

if __name__ == '__main__':
	pygame.init()

	engine.init()

	app = App(MainMenu)
	app.run()

	pygame.quit()
