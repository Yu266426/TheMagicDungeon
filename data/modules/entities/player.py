import pygame
import pygbase

from data.modules.entities.components.box_collider import BoxCollider
from data.modules.entities.components.interaction_controller import InteractionController
from data.modules.entities.components.item_slot import ItemSlot
from data.modules.entities.items.energy_sword import EnergySword
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.level import Level


class Player(Entity):
	def __init__(self, pos, camera: pygbase.Camera, entity_manager: EntityManager, level: Level):
		super().__init__(pos)

		self.current_state = "idle"

		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheet", "player_idle_animation", 0, 1), 8),
			("run", pygbase.Animation("sprite_sheet", "player_run_animation", 0, 2), 8)
		], "player_idle")

		self.collider = BoxCollider((70, 50)).link_pos(self.pos)

		self.input = pygame.Vector2()
		self.movement = Movement(5000, 10, level, self.collider)

		self.entity_manager = entity_manager

		self.item_slot = ItemSlot(self.pos, (25, -42), entity_manager, camera)
		self.item_slot.equip_item(EnergySword(entity_manager, level))

		self.camera = camera

		self.lighting_manager: pygbase.LightingManager = pygbase.Common.get_value("lighting_manager")
		self.light = pygbase.Light(self.pos, 0.2, 300, 10, 1.2).link_pos(self.pos)
		self.light2 = pygbase.Light(self.pos, 0.5, 500, 20, 1.2).link_pos(self.pos)

		self.interaction_controller = InteractionController(250, self)

	def added(self):
		self.lighting_manager.add_light(self.light)
		self.lighting_manager.add_light(self.light2)

	def removed(self):
		self.lighting_manager.remove_light(self.light)
		self.lighting_manager.remove_light(self.light2)

	def get_inputs(self):
		self.input.x = pygbase.InputManager.get_key_pressed(pygame.K_d) - pygbase.InputManager.get_key_pressed(pygame.K_a)
		self.input.y = pygbase.InputManager.get_key_pressed(pygame.K_s) - pygbase.InputManager.get_key_pressed(pygame.K_w)
		if self.input.length() != 0:
			self.input.normalize_ip()
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

	def update(self, delta: float):
		self.get_inputs()

		if pygbase.InputManager.get_key_just_pressed(pygame.K_SPACE):
			self.movement.add_force(self.input, 5000)

		self.movement.move_in_direction(self.pos, self.input, delta)

		self.animations.update(delta)

		self.item_slot.update(delta)

		self.interaction_controller.update(self.entity_manager)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
		self.item_slot.draw(surface, camera)
