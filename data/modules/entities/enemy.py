import math

import pygame
import pygbase

from data.modules.entities.components.box_collider import BoxCollider
from data.modules.entities.components.health import Health
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.map.level import Level


class Enemy(Entity):
	def __init__(self, pos, level: Level, entity_manager: EntityManager):
		super().__init__(pos)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheet", "player_idle_animation", 0, 1), 8),
			("run", pygbase.Animation("sprite_sheet", "player_run_animation", 0, 2), 8)
		], "idle"
		)

		self.collider = BoxCollider((70, 50)).link_pos(self.pos)

		self.movement = Movement(3000, 10, level, self.collider)

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, 5, self.animations),
			"stunned": StunnedState(2, "wander", self.pos, self.movement)
		}, "wander")

		self.health = Health(10)
		self.damage_timer = pygbase.Timer(0.6, True, False)

		self.entity_manager = entity_manager

	def update(self, delta: float):
		self.animations.update(delta)

		self.damage_timer.tick(delta)

		self.state_manager.update(delta)

		if self.damage_timer.done():
			damage_entities = self.entity_manager.get_entities_of_tag("damage")
			for entity in damage_entities:
				if self.collider.collides_with(entity.collider):
					# print(entity)
					self.health.damage(entity.damage)

					dir_vec = entity.pos - self.pos
					if dir_vec.length() != 0:
						dir_vec.normalize_ip()

					self.movement.velocity -= dir_vec * 2000

					self.damage_timer.start()

					self.state_manager.change_state("stunned")
					self.animations.reset_animation_on_switch = True
					self.animations.switch_state("idle")
					break

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		if not self.damage_timer.done():
			if math.sin(pygame.time.get_ticks() / 25) > 0:
				self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
		else:
			self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")

	def is_alive(self):
		return self.health.is_alive()
