import pygame
import pygbase

from data.modules.base.registry.animation_data import AnimationData
from data.modules.base.registry.registrable import Registrable
from data.modules.base.utils import to_scaled_sequence, to_scaled
from data.modules.entities.components.item_slot import ItemSlot
from data.modules.entities.enemies.enemy import Enemy
from data.modules.entities.entity_manager import EntityManager
from data.modules.entities.states.entity_state import EntityState
from data.modules.entities.states.entity_state_manager import EntityStateManager
from data.modules.entities.states.melee_attack_state import MeleeAttackState
from data.modules.entities.states.stunned_state import StunnedState
from data.modules.entities.states.wander_state import WanderState
from data.modules.level.level import Level


class MeleeEnemy(Enemy, Registrable):
	@staticmethod
	def get_name() -> str:
		return "melee"

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type | str] | tuple[str, type, tuple[str, ...]], ...]:
		return (
			("animations", tuple[AnimationData], ("idle", "run")),
			("states", tuple[EntityState], ("wander", "stunned", "melee_attack")),
			("weapon", str)
		)

	def __init__(
			self,
			pos: pygame.typing.Point,
			level: Level,
			entity_manager: EntityManager,
			collider_size: tuple[int, int],
			health: int,
			data: dict[str, ...]
	):
		Enemy.__init__(self, pos, level, entity_manager, collider_size, health, data)

		idle_animation_data = data["animations"]["idle"]
		run_animation_data = data["animations"]["run"]

		self.flip_x = False
		self.animations = pygbase.AnimationManager([
			("idle", pygbase.Animation("sprite_sheets", *idle_animation_data[:3]), idle_animation_data[3]),
			("run", pygbase.Animation("sprite_sheets", *run_animation_data[:3]), run_animation_data[3])
		], "idle")

		self.offset = self.animations.get_current_image().get_image().get_height() / 2

		self.item_slot = ItemSlot(self.pos, (4, -6.72), entity_manager, False)
		self.item_slot.equip_item(data["weapon"])

		state_data = data["states"]
		self.state_manager = EntityStateManager({
			"wander": WanderState(self.pos, self.movement, level, self.entity_manager, self.animations, state_data["wander"]),
			"stunned": StunnedState(self.pos, self.movement, "wander", state_data["stunned"]),
			"attack": MeleeAttackState(self.pos, self.movement, self.entity_manager, self.item_slot, self.offset, state_data["melee_attack"])
		}, "wander")

		self.player_pos = entity_manager.get_entities_of_tag("player")[0].pos

		self.lighting_manager: pygbase.LightingManager = pygbase.Common.get_value("lighting_manager")
		self.shadow = pygbase.Shadow(self.pos, to_scaled(3.5)).link_pos(self.pos)

	def added(self):
		self.lighting_manager.add_shadow(self.shadow)

	def removed(self):
		self.item_slot.removed()
		self.lighting_manager.remove_shadow(self.shadow)

	def damaged(self):
		self.state_manager.change_state("stunned")
		self.animations.reset_animation_on_switch = True
		self.animations.switch_state("idle")

	def update(self, delta: float):
		Enemy.update(self, delta)

		self.animations.update(delta)
		self.state_manager.update(delta)

		self.flip_x = self.player_pos.x < self.pos.x
		self.item_slot.flip_x = self.flip_x

		self.item_slot.update(self.player_pos)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self.animations.draw_at_pos(surface, self.pos, camera, flip=(self.flip_x, False), draw_pos="midbottom")
		self.item_slot.draw(surface, camera)

		pygbase.Debug.draw_rect(camera.world_to_screen_rect(self.collider.rect), "yellow")
