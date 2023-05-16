import pygame
from pygbase import InputManager, Camera, AnimationManager, Animation

from data.modules.map.level import Level
from data.modules.entities.components.hitbox import Hitbox
from data.modules.entities.components.item_slot import ItemSlot
from data.modules.entities.components.items.energy_sword import EnergySword
from data.modules.entities.components.movement import Movement
from data.modules.entities.entity import Entity


class Player(Entity):
	def __init__(self, pos, level: Level, camera: Camera):
		super().__init__(pos)

		self.current_state = "idle"

		self.animations = AnimationManager([
			("idle", Animation("player_idle_animation", 0, 1), 8),
			("run", Animation("player_run_animation", 0, 2), 8)
		], "player_idle")

		self.collider = Hitbox((70, 50)).link_pos(self.pos)

		self.input = pygame.Vector2()
		self.movement = Movement(400, level, self.collider)

		self.item_slot = ItemSlot(self.pos, (32, -36))
		self.item_slot.equip_item(EnergySword())

		self.camera = camera

	def get_inputs(self):
		self.input.x = InputManager.keys_pressed[pygame.K_d] - InputManager.keys_pressed[pygame.K_a]
		self.input.y = InputManager.keys_pressed[pygame.K_s] - InputManager.keys_pressed[pygame.K_w]
		if self.input.length() != 0:
			self.input.normalize_ip()
			self.animations.switch_state("run")
		else:
			self.animations.switch_state("idle")

		if InputManager.mods & pygame.KMOD_SHIFT:
			self.input *= 0.4

	def update(self, delta: float):
		self.get_inputs()

		self.movement.move_in_direction(self.pos, self.input, delta)

		self.animations.update(delta)

		mouse_pos = self.camera.screen_to_world(pygame.mouse.get_pos())
		if mouse_pos.x < self.pos.x:
			self.item_slot.flip_x = True
		else:
			self.item_slot.flip_x = False

		self.item_slot.update(delta)

	def draw(self, screen: pygame.Surface, camera: Camera):
		self.animations.draw_at_pos(screen, self.pos, camera, draw_pos="midbottom")
		self.item_slot.draw(screen, camera)
