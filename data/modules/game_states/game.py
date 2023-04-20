import pygame
from pygbase import InputManager, Camera, EventManager, Common
from pygbase.game_state import GameState

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.level import Level
from data.modules.entities.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.player import Player


class Game(GameState, name="game"):
	def __init__(self):
		super().__init__()
		self.entities = EntityManager()
		Common.set_value("entities", self.entities)

		self.level = Level(self.entities)

		self.camera = Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.player = Player((400, 400), self.level, self.camera)
		self.entities.add_entity(self.player)

		for _ in range(1000):
			self.entities.add_entity(Enemy((500, 400), self.level, self.entities))

	def update(self, delta: float):
		self.entities.update(delta)

		if InputManager.keys_down[pygame.K_SPACE]:
			self.level.generate_level()

		self.camera.lerp_to_target(self.player.collider.rect.center - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), delta * 5)

		if InputManager.keys_down[pygame.K_ESCAPE]:
			EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))

		self.level.draw(screen, self.camera)
