import pygame
import pygbase

from data.modules.entities.attacks.explosion import Explosion
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.map.level import Level


class Fireball(Entity):
	def __init__(self, pos, direction: float, speed: float, projectile_range: float, radius: float, explosion_radius: float, damage: float, level: Level, entity_manager: EntityManager, particle_manager: pygbase.ParticleManager):
		super().__init__(pos)
		self.alive = True

		self.movement = pygame.Vector2(speed, 0).rotate(-direction)
		self.radius = radius

		self.distance = 0
		self.projectile_range = projectile_range

		self.explosion_radius = explosion_radius
		self.damage = damage

		self.level = level
		self.entity_manager = entity_manager
		self.particle_manager = particle_manager
		self.fire_particles = self.particle_manager.add_spawner(pygbase.CircleSpawner(self.pos, 0.05, 50, self.radius, True, "fire", particle_manager).link_pos(self.pos))

	def is_alive(self):
		return self.alive

	def update(self, delta: float):
		next_move = self.movement * delta

		self.pos += next_move
		self.distance += next_move.length()

		if self.alive and (self.distance > self.projectile_range or self.level.get_tile(self.pos) is not None):
			self.alive = False

			self.particle_manager.remove_spawner(self.fire_particles)

			self.entity_manager.add_entity(Explosion(self.pos, self.explosion_radius, self.damage, self.particle_manager), tags=("damage",))
