import math
from xml.sax import parse

import pygame

from data.modules.base.registry.registrable import Registrable
from data.modules.entities.models.character_model import CharacterModel


class HumanoidModel(CharacterModel, Registrable):
	@staticmethod
	def get_name() -> str:
		return "humanoid"

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type | str] | tuple[str, type, tuple[str, ...]], ...]:
		return ("parts", tuple[str], ("body", "leg")),

	def __init__(self, pos: pygame.Vector2, data: dict):
		# TODO: So many pitfalls here, revise to be safer (although deepcopy is too slow).
		#  Maybe make a data transform class that handles this for me

		# Modify data from model to fit humanoid
		data_copy = data.copy()

		parts = data["parts"].copy()

		# Base right leg on "leg"
		parts["right_leg"] = parts["leg"].copy()
		# Mirror for left leg
		parts["left_leg"] = parts["leg"].copy()
		parts["left_leg"]["offset"] = (-parts["leg"]["offset"][0], parts["leg"]["offset"][1])

		del parts["leg"]

		data_copy["parts"] = parts

		super().__init__(pos, data_copy)

		self.body_part = self.parts["body"]
		self.right_leg = self.parts["right_leg"]
		self.left_leg = self.parts["left_leg"]

		self.height_offset = self.body_part.offset.y

		self.flipped = False

		self.state = "idle"
		self.state_switch_time = pygame.time.get_ticks()

		self.right_leg_down = False
		self.left_leg_down = False

		self.max_leg_angle = 30

	def switch_state(self, new_state: str):
		if new_state != self.state:
			self.state = new_state
			self.state_switch_time = pygame.time.get_ticks()

	@staticmethod
	def _lerp(start, end, delta: float, lerp_speed: int = 8):
		return pygame.math.lerp(start, end, delta * lerp_speed)

	@staticmethod
	def _move_lerp(start, end, delta: float, speed: int = 20):
		offset = (end - start)

		if offset != 0:
			offset /= offset

		return start + offset * min(speed * delta, abs(end - start))

	def _idle_animate(self, delta: float):
		self.body_part.offset.y = self._lerp(self.body_part.offset.y, self.height_offset, delta * 8)
		self.body_part.part_offset.y = (math.sin((pygame.time.get_ticks() - self.state_switch_time) / 120)) * 0.02

		self.left_leg.angle = self._lerp(self.left_leg.angle, 0, delta, lerp_speed=20)
		self.right_leg.angle = self._lerp(self.right_leg.angle, 0, delta, lerp_speed=20)

	def _run_animate(self, delta: float):
		self.body_part.part_offset.y = self._lerp(self.body_part.part_offset.y, 0, delta * 8)
		self.body_part.offset.y = self.height_offset - (math.sin((pygame.time.get_ticks() - self.state_switch_time) / 100)) * 0.08

		angle_sign = -1 if self.flipped else 1

		# TODO: Fix animation
		# Right leg animation
		if self.right_leg_down:
			to_angle = -self.max_leg_angle * angle_sign

			self.right_leg.angle = self._move_lerp(self.right_leg.angle, to_angle, delta, speed=50)

			if abs(self.right_leg.angle - to_angle) < 0.5:
				self.right_leg_down = False
		else:
			to_angle = self.max_leg_angle * angle_sign

			self.right_leg.angle = self._move_lerp(self.right_leg.angle, to_angle, delta, speed=20)

			if abs(self.right_leg.angle - to_angle) < 0.5:
				self.right_leg_down = True

		self.left_leg.angle = (math.sin((pygame.time.get_ticks() - self.state_switch_time) / 100)) * 30

	# self.right_leg.angle = -(math.sin((pygame.time.get_ticks() - self.state_switch_time) / 100)) * 30

	def update(self, delta: float):
		if self.state == "idle":
			self._idle_animate(delta)
		elif self.state == "run":
			self._run_animate(delta)

		if self.flipped != self.body_part.flipped:
			self.body_part.flipped = self.flipped

			self.state_switch_time = pygame.time.get_ticks()

			if self.flipped:
				self.right_leg_down = True
				self.left_leg_down = False
			else:
				self.right_leg_down = False
				self.left_leg_down = True

		CharacterModel.update(self, delta)
