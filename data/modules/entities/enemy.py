import pygame
from pygbase import AnimationManager, Camera
from pygbase.graphics.animation import Animation

from data.modules.base.level import Level
from data.modules.entities.components.health import Health
from data.modules.entities.components.hitbox import Hitbox
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.wander_state import WanderState


class Enemy(Entity):
	def __init__(self, pos, level: Level, entity_manager: EntityManager):
		super().__init__(pos)

		self.animations = AnimationManager([
			("idle", Animation("player_idle_animation", 0, 1), 8)
		], "idle"
		)

		self.hitbox = Hitbox((70, 50)).link_pos(self.pos)

		self.movement = Movement(300, level, self.hitbox)

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, 5)
		}, "wander")

		self.health = Health(10)

		self.entity_manager = entity_manager

	def update(self, delta: float):
		self.state_manager.update(delta)

		damage_entities = self.entity_manager.get_entities_of_tag("damage")
		for entity in damage_entities:
			if self.hitbox.rect.colliderect(entity.hitbox.rect):
				self.health.damage(entity.damage)

	def draw(self, screen: pygame.Surface, camera: Camera):
		self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
		self.state_manager.draw(screen, camera)

	def is_alive(self):
		return self.health.is_alive()
