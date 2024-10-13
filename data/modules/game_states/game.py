import pygame
import pygbase
import pygbase.ui.text

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from data.modules.base.utils import get_tile_pos
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.player import Player
from data.modules.level.level import Level, LevelGenerator


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()
		self.entity_manager = EntityManager()
		self.particle_manager: pygbase.ParticleManager = pygbase.Common.get_value("particle_manager")
		self.lighting_manager: pygbase.LightingManager = pygbase.Common.get_value("lighting_manager")

		room_separation = 21
		self.level: Level = LevelGenerator(100, self.entity_manager, room_separation, 1).generate_level()

		self.camera = pygbase.Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.player = Player(((room_separation / 2 - 0.5) * TILE_SIZE, room_separation / 2 * TILE_SIZE), self.camera, self.entity_manager, self.level)
		self.entity_manager.add_entity(self.player)

		self.camera.set_pos(self.player.pos + (-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.pos_text = pygbase.ui.text.Text((0, 0), "arial", 20, "yellow", "test", use_sys=True)

	def enter(self):
		self.particle_manager.clear()

	def exit(self):
		self.level.cleanup()
		self.entity_manager.clear_entities()

	def update(self, delta: float):
		self.entity_manager.update(delta)
		self.particle_manager.update(delta)
		self.lighting_manager.update(delta)

		self.camera.lerp_to_target(
			self.player.collider.rect.center
			- pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
			, delta * 8
		)

		self.level.update(delta, self.player.pos)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			# from data.modules.game_states.main_menu import MainMenu
			# self.set_next_state(MainMenu())

			pygbase.EventManager.post_event(pygame.QUIT)

		mouse_tile_pos = get_tile_pos(self.camera.screen_to_world(pygame.mouse.get_pos()), (TILE_SIZE, TILE_SIZE))
		self.pos_text.set_text(f"{mouse_tile_pos[0]},{mouse_tile_pos[1]}")
		self.pos_text.pos = pygame.Vector2(pygame.mouse.get_pos()) + (20, 0)
		self.pos_text.reposition()

	def draw(self, surface: pygame.Surface):
		surface.fill((0, 0, 0))

		self.level.draw(surface, self.camera)
		self.lighting_manager.draw(surface, self.camera)

		self.particle_manager.draw(surface, self.camera)

		self.pos_text.draw(surface)
