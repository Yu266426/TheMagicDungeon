import logging

import pygame
import pygbase

from data.modules.base.constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import IMAGE_DIR, SPRITE_SHEET_DIR
from data.modules.base.registry.registry import Registry
from data.modules.entities.enemies.enemy_loader import EnemyLoader
from data.modules.entities.enemies.melee_enemy import MeleeEnemy
from data.modules.entities.items.energy_sword import EnergySword
from data.modules.entities.models.humanoid_model import HumanoidModel
from data.modules.entities.models.model_loader import ModelLoader
from data.modules.entities.models.model_part import ImageModelPart
from data.modules.entities.states.melee_attack_state import MeleeAttackState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.game_states.main_menu import MainMenu
from data.modules.objects.altars import RuneAltar
from data.modules.objects.object_loader import ObjectLoader
from data.modules.objects.torch import Torch


def register_types():
	logging.info("Registering objects")
	Registry.register_type(Torch)
	Registry.register_type(RuneAltar)

	logging.info("Registering entity states")
	Registry.register_type(WanderState)
	Registry.register_type(StunnedState)
	Registry.register_type(MeleeAttackState)

	logging.info("Registering items")
	Registry.register_type(EnergySword)

	logging.info("Registering model parts")
	Registry.register_type(ImageModelPart)

	logging.info("Registering models")
	Registry.register_type(HumanoidModel)

	logging.info("Registering enemies")
	Registry.register_type(MeleeEnemy)

	logging.debug("Done registering")


def toggle_debug(event: pygame.Event):
	if event.key == pygame.K_F3:
		pygbase.DebugDisplay.toggle_fps()
	elif event.key == pygame.K_F4:
		pygbase.DebugDisplay.toggle()


if __name__ == '__main__':
	# profiler = cProfile.Profile()
	# profiler.enable()

	pygbase.init((SCREEN_WIDTH, SCREEN_HEIGHT), logging_level=logging.DEBUG, rotate_resolution=2, light_radius_interval=3, shadow_ratio=1.6)
	# pygbase.DebugDisplay.show()
	pygbase.EventManager.add_handler("all", pygame.KEYDOWN, toggle_debug)

	pygbase.EventManager.create_custom_event("start_game")

	pygbase.add_image_resource("images", 1, str(IMAGE_DIR), default_scale=TILE_SCALE)
	pygbase.add_sprite_sheet_resource("sprite_sheets", 2, str(SPRITE_SHEET_DIR), default_scale=TILE_SCALE)

	pygbase.Common.set_value("particle_manager", pygbase.ParticleManager())
	pygbase.Common.set_value("lighting_manager", pygbase.LightingManager(0.3, 0.4))
	pygbase.Common.set_value("dialogue_manager", pygbase.DialogueManager(15, 0.05))

	pygbase.add_particle_setting(
		"fire",
		[(255, 40, 30), (255, 90, 0), (255, 154, 0)],
		(5, 11),
		(6, 10),
		(0, 2),
		(0, -100),
		False,
		((0, 0), (0, 0))
	)

	pygbase.add_particle_setting(
		"rune_altar",
		[(143, 186, 255), (102, 237, 255), (82, 154, 255)],
		(5, 11),
		(6, 10),
		(0, 2),
		(0, -100),
		False,
		((0, 0), (0, 0))
	)

	# Run app
	app = pygbase.App(
		MainMenu,
		# Game,,
		"Catacombs of Time",
		flags=pygame.SCALED,
		run_on_load_complete=(
			Registry.init,
			register_types,
			ObjectLoader.init,
			ModelLoader.init,
			EnemyLoader.init
		)
	)
	app.run()

	pygbase.quit()

# profiler.disable()
# profiler.dump_stats("stats.prof")
