import pygame.typing

import pygbase
from data.modules.base.constants import PIXEL_SCALE
from data.modules.base.registry.registrable import Registrable
from data.modules.base.utils import to_scaled_sequence


class ModelPart:
	pass


class ImageModelPart(ModelPart, Registrable):
	@staticmethod
	def get_name() -> str:
		return "static"

	@staticmethod
	def get_required_component() -> tuple[tuple[str, type | str] | tuple[str, type, tuple[str, ...]], ...]:
		return ("type", "static"), ("image", str), ("offset", "point"), ("pivot", "point"), ("parent", str), ("layer", int)

	def __init__(self, parent_pos: pygame.Vector2, data: dict):
		self._image: pygbase.Image = pygbase.Resources.get_resource("images", data["image"])

		self.offset = pygame.Vector2(data["offset"])
		self._pivot = to_scaled_sequence(data["pivot"])

		self.layer = data["layer"]

		self._parent_pos = parent_pos  # Reference to parent pos
		self.pos = pygame.Vector2(self._parent_pos + self.offset)

		# TODO: decide how to handle these
		self.angle = 0.0
		self.flipped = False

		self.part_offset = pygame.Vector2()

	def update(self):
		self.pos.update(self._parent_pos + self.offset * PIXEL_SCALE)

	def draw(self, surface: pygame.Surface, camera: pygbase.Camera):
		self._image.draw(surface, camera.world_to_screen(self._parent_pos + (self.offset + self.part_offset) * PIXEL_SCALE), self.angle, pivot_point=self._pivot, flip=(self.flipped, False), draw_pos="center")
