import math

import pygame
import pygbase

from data.modules.entities.attacks.fireball import Fireball
from data.modules.entities.components.box_collider import BoxCollider
from data.modules.entities.components.health import Health
from data.modules.entities.components.interaction_controller import InteractionController
from data.modules.entities.components.item_slot import ItemSlot
from data.modules.entities.items.energy_sword import EnergySword
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.level import Level


class Player(Entity, tags=("player",)):
	def __init__(self, pos, camera: pygbase.Camera, entity_manager: EntityManager, level: Level):
		super().__init__(pos)
		self.entity_manager = entity_manager
		self.level = level

		self.current_state = "idle"

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheet", "player_idle_animation", 0, 1), 8),
			("run", pygbase.Animation("sprite_sheet", "player_run_animation", 0, 2), 8)
		], "player_idle")

		self.collider = BoxCollider((70, 50)).link_pos(self.pos)

		self.input = pygame.Vector2()
		self.movement = Movement(5000, 10, level, self.collider)

		self.camera = camera

		self.lighting_manager: pygbase.LightingManager = pygbase.Common.get_value("lighting_manager")
		self.light = pygbase.Light(self.pos, 0.2, 300, 10, 1.2).link_pos(self.pos)
		self.light2 = pygbase.Light(self.pos, 0.5, 500, 20, 1.2).link_pos(self.pos)

		self.interaction_controller = InteractionController(250, self)

		self.health = Health(10000)
		self.damage_timer = pygbase.Timer(0.6, True, False)

		self.item_slot = ItemSlot(self.pos, (25, -42), entity_manager, True)
		self.item_slot.equip_item(EnergySword(entity_manager, level))

	def added(self):
		self.lighting_manager.add_light(self.light)
		self.lighting_manager.add_light(self.light2)

	def removed(self):
		self.lighting_manager.remove_light(self.light)
		self.lighting_manager.remove_light(self.light2)

	def damaged(self):
		pass

	def get_inputs(self):
		self.input.x = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.input.y = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		if self.input.length() != 0:
			self.input.normalize_ip()
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

	def check_damaged(self):
		if self.damage_timer.done():
			damage_entities = self.entity_manager.get_entities_of_tag("damage")
			for entity in damage_entities:
				if "from_player" in entity.entity_tags:
					continue

				# TODO: Is NoQA really the answer?
				if self.collider.collides_with(entity.collider):  # NoQA
					# print(entity)
					self.health.damage(entity.damage)  # NoQA

					dir_vec = entity.pos - self.pos
					if dir_vec.length() != 0:
						dir_vec.normalize_ip()

					self.movement.velocity -= dir_vec * 2000

					self.damage_timer.start()

					self.damaged()
					break

		self.visible = self.damage_timer.done() or not math.sin(pygame.time.get_ticks() / 25) > 0

	def update(self, delta: float):
		self.damage_timer.tick(delta)

		self.get_inputs()

		# Debug
		if pygbase.InputManager.get_key_just_pressed(pygame.K_SPACE):
			self.movement.add_force(self.input, 5000)
		if pygbase.InputManager.get_mouse_just_pressed(2):
			mouse_world_pos = self.camera.screen_to_world(pygame.mouse.get_pos())
			angle = pygbase.utils.get_angle_to(self.pos - (0, 30), mouse_world_pos)
			self.entity_manager.add_entity(Fireball(
				self.pos - (0, 30),
				angle,
				800,
				min(400, self.pos.distance_to(mouse_world_pos)),
				30,
				70,
				10,
				self.level,
				self.entity_manager
			), tags=("from_player",))
		# Debug end

		self.movement.move_in_direction(self.pos, self.input, delta)

		self.animations.update(delta)

		if pygbase.InputManager.get_mouse_just_pressed(0):
			self.item_slot.use_item()

		self.item_slot.update(self.camera.screen_to_world(pygame.mouse.get_pos()))

		self.interaction_controller.update(self.entity_manager)

		self.check_damaged()

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
		self.item_slot.draw(surface, camera)

	def is_alive(self):
		return self.health.is_alive()
