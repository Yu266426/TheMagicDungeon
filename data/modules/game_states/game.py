import pygame
import pygbase

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.entities.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.player import Player
from data.modules.map.level import Level


class Game(pygbase.GameState, name="game"):
	def __init__(self):
		super().__init__()
		self.entities = EntityManager()
		self.particle_manager = pygbase.ParticleManager()
		self.lighting_manager = pygbase.LightingManager(0.5)

		self.level = Level(self.entities)

		self.camera = pygbase.Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.player = Player((400, 400), self.camera, self.entities, self.level, self.particle_manager, self.lighting_manager)
		self.entities.add_entity(self.player)

		for _ in range(100):
			self.entities.add_entity(Enemy((500, 400), self.level, self.entities))

	def update(self, delta: float):
		self.entities.update(delta)
		self.particle_manager.update(delta)
		self.lighting_manager.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_SPACE):
			self.level.generate_level()

		self.camera.lerp_to_target(self.player.collider.rect.center - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), delta * 5)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))

		self.level.draw(screen, self.camera)
		self.lighting_manager.draw(screen, self.camera)

		self.particle_manager.draw(screen, self.camera)
