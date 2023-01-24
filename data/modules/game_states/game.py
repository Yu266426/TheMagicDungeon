import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.inputs import InputManager
from data.modules.base.level import Level
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.player import Player
from data.modules.game_states.game_state import GameState, GameStateIds


class Game(GameState):
	def __init__(self):
		super().__init__(GameStateIds.GAME)

		self.entities = EntityManager()

		self.level = Level(self.entities)

		self.camera = Camera(pos=(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))

		self.player = Player((400, 400), pygame.Surface((80, 80)), self.level)
		self.entities.add_entity(self.player)

	def next_state(self) -> GameState:
		return self

	def update(self, delta: float):
		self.entities.update(delta)

		if InputManager.keys_down[pygame.K_SPACE]:
			self.level = Level(self.entities)
			self.player.level = self.level

		self.camera.lerp_to_target(self.player.hitbox.center - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), delta * 5)

	def draw(self, screen: pygame.Surface):
		screen.fill((0, 0, 0))

		self.level.draw(screen, self.camera)
