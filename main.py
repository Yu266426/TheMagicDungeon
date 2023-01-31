import pygame

import pygbase
from pygbase import ResourceType
from pygbase.app import App
from pygbase.graphics.sprite_sheet import SpriteSheet

from data.modules.base.constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.files import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.game_states.main_menu import MainMenu

if __name__ == '__main__':
	pygame.init()

	pygbase.init((SCREEN_WIDTH, SCREEN_HEIGHT))


	def load_image(data: dict, resource_path: str):
		scale = data["scale"]

		image = pygame.image.load(resource_path).convert_alpha()
		image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
		return image


	pygbase.add_resource_type(1, ResourceType(
		"image", IMAGE_DIR,
		{"scale": 1},
		None,
		load_image
	))

	pygbase.add_resource_type(2, ResourceType(
		"sprite_sheet", SPRITE_SHEET_DIR,
		{
			"rows": 0,
			"columns": 0,
			"tile_width": 0,
			"tile_height": 0,
			"scale": -1
		},
		lambda data: data["scale"] != -1,
		lambda data, resource_path: SpriteSheet(data, resource_path, TILE_SCALE)
	))

	app = App(MainMenu)
	app.run()

	pygame.quit()
