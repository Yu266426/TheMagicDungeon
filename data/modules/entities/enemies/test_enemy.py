import pygame
import pygbase

from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.level.level import Level


class TestEnemy(Enemy):
	def __init__(self, pos: tuple | pygame.Vector2, level: Level, entity_manager: EntityManager):
		super().__init__(pos, level, entity_manager, (70, 50), 10)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheet", "player_idle_animation", 0, 1), 8),
			("run", pygbase.Animation("sprite_sheet", "player_run_animation", 0, 2), 8)
		], "idle"
		)

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, 5, self.animations),
			"stunned": StunnedState(2, "wander", self.pos, self.movement)
		}, "wander")

	def damaged(self):
		self.state_manager.change_state("stunned")
		self.animations.reset_animation_on_switch = True
		self.animations.switch_state("idle")

	def update(self, delta: float):
		super().update(delta)

		self.animations.update(delta)
		self.state_manager.update(delta)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")

		pygame.draw.rect(surface, "yellow", camera.world_to_screen_rect(self.collider.rect), width=1)
