import pygame

import data.modules.engine as engine
from data.modules.base.files import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.engine import ResourceType
from data.modules.engine.app import App
from data.modules.engine.graphics.sprite_sheet import SpriteSheet
from data.modules.game_states.main_menu import MainMenu

if __name__ == '__main__':
	pygame.init()

	engine.init()


	def load_image(data: dict, resource_path: str):
		scale = data["scale"]

		image = pygame.image.load(resource_path).convert_alpha()
		image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
		return image


	engine.add_resource_type(1, ResourceType(
		"image", IMAGE_DIR,
		{"scale": 1},
		None,
		load_image
	))

	engine.add_resource_type(2, ResourceType(
		"sprite_sheet", SPRITE_SHEET_DIR,
		{
			"rows": 0,
			"columns": 0,
			"tile_width": 0,
			"tile_height": 0,
			"scale": -1
		},
		lambda data: data["scale"] != -1,
		lambda data, resource_path: SpriteSheet(data, resource_path)
	))

	app = App(MainMenu)
	app.run()

	pygame.quit()
