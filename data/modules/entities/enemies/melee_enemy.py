import pygame
import pygbase

from data.modules.entities.components.item_slot import ItemSlot
from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.items.energy_sword import EnergySword
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.melee_attack_state import MeleeAttackState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.level.level import Level


class MeleeEnemy(Enemy, animations=("idle", "run"), states=("wander", "stunned", "melee_attack")):
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

		self.offset = self.animations.get_current_image().get_image().get_height() / 2

		self.item_slot = ItemSlot(self.pos, (25, -42), entity_manager, False)
		self.item_slot.equip_item(EnergySword(entity_manager, level))

		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, self.entity_manager, self.animations, state_data["wander"]),
			"stunned": StunnedState(self.pos, self.movement, "wander", state_data["stunned"]),
			"attack": MeleeAttackState(self.pos, self.movement, self.entity_manager, self.item_slot, self.offset, state_data["melee_attack"])
		}, "wander")

		self.player_pos = entity_manager.get_entities_of_tag("player")[0].pos

	def removed(self):
		self.item_slot.removed()

	def damaged(self):
		self.state_manager.change_state("stunned")
		self.animations.reset_animation_on_switch = True
		self.animations.switch_state("idle")

	def update(self, delta: float):
		Enemy.update(self, delta)

		self.animations.update(delta)
		self.state_manager.update(delta)

		self.item_slot.update(self.player_pos)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, draw_pos="midbottom")
		self.item_slot.draw(surface, camera)

		pygbase.DebugDisplay.draw_rect(camera.world_to_screen_rect(self.collider.rect), "yellow")
