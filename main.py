import pygame

from data.modules.base.app import App

if __name__ == '__main__':
	pygame.init()

	app = App()
	app.run()

	pygame.quit()
