import cProfile
import logging

import pygame
import pygbase

from data.modules.base.constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.game_states.main_menu import MainMenu

if __name__ == '__main__':
	# profiler = cProfile.Profile()
	# profiler.enable()

	pygbase.init((SCREEN_WIDTH, SCREEN_HEIGHT), logging_level=logging.INFO)

	pygbase.add_image_resource("image", 1, str(IMAGE_DIR))
	pygbase.add_sprite_sheet_resource("sprite_sheet", 2, str(SPRITE_SHEET_DIR), default_scale=TILE_SCALE)

	app = pygbase.App(MainMenu)
	app.run()

	pygbase.quit()

# profiler.disable()
# profiler.dump_stats("stats.prof")
