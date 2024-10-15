import pygame
import pygbase

from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.level.level import Level


class BasicEnemy(Enemy, animations=("idle", "run"), states=("wander", "stunned")):
	def __init__(
			self,
			pos: pygame.typing.Point,
			level: Level,
			entity_manager: EntityManager,
			collider_size: tuple[int, int],
			health: int,
			animation_data: dict[str, tuple[str, int, int, int]],
			state_data: dict[str, dict[str, ...]]
	):
		super().__init__(pos, level, entity_manager, collider_size, health, animation_data, state_data)

		idle_animation_data = animation_data["idle"]
		run_animation_data = animation_data["run"]

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheet", *idle_animation_data[:3]), idle_animation_data[3]),
			("run", pygbase.Animation("sprite_sheet", *run_animation_data[:3]), run_animation_data[3])
		], "idle")

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, state_data["wander"]["range"], self.animations),
			"stunned": StunnedState(state_data["stunned"]["time"], "wander", self.pos, self.movement)
		}, "wander")

	def damaged(self):
		self.state_manager.change_state("stunned")
		self.animations.reset_animation_on_switch = True
		self.animations.switch_state("idle")

	def update(self, delta: float):
		Enemy.update(self, delta)

		self.animations.update(delta)
		self.state_manager.update(delta)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")

		pygbase.DebugDisplay.draw_rect(camera.world_to_screen_rect(self.collider.rect), "yellow")
