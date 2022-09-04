import pygame

from data.modules.base.game import Game
from data.modules.base.resources import ResourceManager

if __name__ == '__main__':
	pygame.init()

	ResourceManager.init_load()

	while Game.is_running:
		Game.handle_events()
		Game.update()
		Game.draw()
