import math
from typing import Optional

import pygame
import pygbase


class LineCollider:
	def __init__(self, start_pos: pygame.Vector2, angle: float, length: float):
		self.start_pos = start_pos
		self.angle = angle
		self.length = length

		self.line = pygame.Vector2(self.length, 0).rotate(self.angle)

	@property
	def end_pos(self):
		return self.start_pos + self.line

	def get_range(self) -> tuple[tuple[float, float], tuple[float, float]]:
		quadrant = math.floor((self.angle % 360) / 90) + 1

		end_pos = self.end_pos

		if quadrant == 1:
			x_range = self.start_pos.x, end_pos.x
			y_range = self.start_pos.y, end_pos.y
		elif quadrant == 2:
			x_range = end_pos.x, self.start_pos.x
			y_range = self.start_pos.y, end_pos.y
		elif quadrant == 3:
			x_range = end_pos.x, self.start_pos.x
			y_range = end_pos.y, self.start_pos.y
		else:  # Quadrant 4
			x_range = self.start_pos.x, end_pos.x
			y_range = end_pos.y, self.start_pos.y

		return x_range, y_range

	def get_slope(self) -> float:
		if self.line.x != 0:
			return self.line.y / self.line.x
		return float("inf")

	def get_y_intercept(self, slope: float) -> float:
		return self.start_pos.y - slope * self.start_pos.x

	def line_collide(self, line: "LineCollider") -> Optional[tuple[float, float]]:
		my_slope = self.get_slope()
		my_y_intercept = self.get_y_intercept(my_slope)

		line_slope = line.get_slope()
		line_y_intercept = line.get_y_intercept(line_slope)

		# Make sure lines aren't parallel
		if abs(my_slope - line_slope) < 0.00001:
			return None

		# Find intersection
		intersect_x = (line_y_intercept - my_y_intercept) / (my_slope - line_slope)
		intersect_y = my_slope * intersect_x + my_y_intercept

		# Make sure intersection is within line segments
		x_range, y_range = self.get_range()

		if intersect_x < x_range[0] or x_range[1] < intersect_x:
			return None
		elif intersect_y < y_range[0] or y_range[1] < intersect_y:
			return None

		return intersect_x, intersect_y

	def collides_with(self, collider):
		from data.modules.entities.components.hitbox import Hitbox

		if isinstance(collider, Hitbox):
			pass
		elif isinstance(collider, LineCollider):
			return self.line_collide(collider) is not None

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.line(screen, "yellow", camera.world_to_screen(self.start_pos), camera.world_to_screen(self.start_pos + self.line))
