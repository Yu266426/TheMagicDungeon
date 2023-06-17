import logging

import pygbase

from data.modules.base.constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.game_states.main_menu import MainMenu
from data.modules.objects.game_object import ObjectLoader

if __name__ == '__main__':
	# profiler = cProfile.Profile()
	# profiler.enable()

	pygbase.init((SCREEN_WIDTH, SCREEN_HEIGHT), logging_level=logging.INFO)

	pygbase.add_image_resource("image", 1, str(IMAGE_DIR))
	pygbase.add_sprite_sheet_resource("sprite_sheet", 2, str(SPRITE_SHEET_DIR), default_scale=TILE_SCALE)

	pygbase.add_particle_setting(
		"fire",
		[(255, 40, 30), (255, 90, 0), (255, 154, 0)],
		(5, 11),
		(6, 10),
		(0, 2),
		(0, 0),
		False
	)

	app = pygbase.App(MainMenu, run_on_load_complete=(ObjectLoader.init,))
	app.run()

	pygbase.quit()

# profiler.disable()
# profiler.dump_stats("stats.prof")
