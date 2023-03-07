import pygbase
from pygbase.app import App

from data.modules.base.constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.files import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.game_states.main_menu import MainMenu

if __name__ == '__main__':
	pygbase.init((SCREEN_WIDTH, SCREEN_HEIGHT))

	pygbase.add_image_resource("image", 1, str(IMAGE_DIR))
	pygbase.add_sprite_sheet_resource("sprite_sheet", 2, TILE_SCALE, str(SPRITE_SHEET_DIR))

	app = App(MainMenu)
	app.run()

	pygbase.quit()
