import pygame
import pygbase

from data.modules.entities.components.boxcollider import BoxCollider
from data.modules.entities.components.health import Health
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.wander_state import WanderState
from data.modules.map.level import Level


class Enemy(Entity):
	def __init__(self, pos, level: Level, entity_manager: EntityManager):
		super().__init__(pos)

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("player_idle_animation", 0, 1), 8)
		], "idle"
		)

		self.collider = BoxCollider((70, 50)).link_pos(self.pos)

		self.movement = Movement(3000, 10, level, self.collider)

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, 5)
		}, "wander")

		self.health = Health(10)
		self.damage_timer = pygbase.Timer(0.2, False, False)

		self.entity_manager = entity_manager

	def update(self, delta: float):
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
					break

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")

	def is_alive(self):
		return self.health.is_alive()
