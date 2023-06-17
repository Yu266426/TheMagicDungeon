import pygame
import pygbase

from data.modules.entities.attacks.fireball import Fireball
from data.modules.entities.attacks.sword_swing import SwordSwing
from data.modules.entities.items.item import Item
from data.modules.entities.entity_manager import EntityManager
from data.modules.map.level import Level


class EnergySword(Item):
	def __init__(self, entities: EntityManager, level: Level, particle_manager: pygbase.ParticleManager, lighting_manager: pygbase.LightingManager):
		super().__init__(100)

		self.animations = pygbase.AnimationManager([
			("active", pygbase.Animation("energy_sword", 0, 1), 1)
		], "active")

		self.starting_angle_offset = -60

		self.attack_angle = 0
		self.attack_flip = 1

		self.angle_offset = 0
		self.swinging_down = True

		self.attack_length = 80
		self.attack_damage = 5

		self.level = level
		self.entity_manager: EntityManager = entities
		self.particle_manager: pygbase.ParticleManager = particle_manager
		self.lighting_manager: pygbase.LightingManager = lighting_manager

		self.attack_cooldown = pygbase.Timer(0.5, True, False)

	def added_to_slot(self, pos: pygame.Vector2):
		super().added_to_slot(pos)

	def update(self, delta: float):
		self.animations.update(delta)
		self.attack_cooldown.tick(delta)

		if pygbase.InputManager.get_mouse_just_pressed(0) and self.attack_cooldown.done():
			self.entity_manager.add_entity(SwordSwing(self.pos, self.angle + (180 if self.flip_x else 0), self.attack_length, self.attack_damage, self.convert_flip()), tags=("damage",))
			# self.entity_manager.add_entity(Fireball(self.pos, self.angle, 800, 400, 30, 70, 10, self.level, self.entity_manager, self.particle_manager, self.lighting_manager))

			self.attack_cooldown.start()

			self.swinging_down = True
		if not self.attack_cooldown.done():
			if self.swinging_down:
				self.angle_offset += 800 * delta
				if self.angle_offset >= 70:
					self.angle_offset = 70
					self.swinging_down = False
			else:
				self.angle_offset -= 400 * delta
				if self.angle_offset <= 0:
					self.angle_offset = 0
		else:
			self.angle_offset = 0

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		draw_angle = self.angle + (self.starting_angle_offset - self.angle_offset) * self.convert_flip() + (180 if self.flip_x else 0)

		self.animations.draw_at_pos(
			screen,
			self.pos,
			camera,
			angle=draw_angle,
			pivot_point=(0, 30),
			draw_pos="midbottom"
		)
