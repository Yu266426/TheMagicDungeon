import pygbase

from data.modules.entities.components.circle_collider import CircleCollider
from data.modules.entities.entity import Entity


class Explosion(Entity):
	def __init__(self, pos, radius: float, damage: float, particle_manager: pygbase.ParticleManager):
		super().__init__(pos)
		self.alive = True

		self.collider = CircleCollider(self.pos, radius)
		self.damage = damage

		self.particle_manager = particle_manager
		self.explosion_particles = particle_manager.add_spawner(pygbase.CircleSpawner(self.pos, 0.05, 40, radius, True, "fire", particle_manager))

		self.timer = pygbase.Timer(0.3, False, False)

	def is_alive(self):
		return self.alive

	def update(self, delta: float):
		self.timer.tick(delta)

		if self.alive and self.timer.done():
			self.alive = False
			self.particle_manager.remove_spawner(self.explosion_particles)
