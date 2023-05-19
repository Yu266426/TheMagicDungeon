import math
from typing import Optional, TYPE_CHECKING

import pygame
import pygbase

if TYPE_CHECKING:
	from data.modules.entities.components.hitbox import Hitbox


class LineCollider:
	def __init__(self, start_pos: pygame.Vector2 | tuple[float, float], angle: float, length: float):
		self.start_pos: pygame.Vector2 = pygame.Vector2(start_pos)
		self.angle: float = angle
		self.length: float = length

		self.line = pygame.Vector2(0, -self.length).rotate(self.angle)

	def link_pos(self, pos: pygame.Vector2) -> "LineCollider":
		self.start_pos = pos
		return self

	def set_angle(self, new_angle: float):
		self.angle = new_angle
		self.line = pygame.Vector2(0, -self.length).rotate(self.angle)

	def change_angle(self, amount: float):
		self.angle += amount
		self.line = pygame.Vector2(0, -self.length).rotate(self.angle)

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

	# def get_slope(self) -> float:
	# 	if self.line.x != 0:
	# 		return self.line.y / self.line.x
	# 	return float("inf")
	#
	# def get_y_intercept(self, slope: float) -> float:
	# 	return self.start_pos.y - slope * self.start_pos.x
	#
	# def line_collide(self, line: "LineCollider") -> Optional[tuple[float, float]]:
	# 	my_slope = self.get_slope()
	# 	my_y_intercept = self.get_y_intercept(my_slope)
	#
	# 	line_slope = line.get_slope()
	# 	line_y_intercept = line.get_y_intercept(line_slope)
	#
	# 	# Make sure lines aren't parallel
	# 	if abs(my_slope - line_slope) < 0.00001:
	# 		return None
	#
	# 	# Find intersection
	# 	intersect_x = (line_y_intercept - my_y_intercept) / (my_slope - line_slope)
	# 	intersect_y = my_slope * intersect_x + my_y_intercept
	#
	# 	# Make sure intersection is within line segments
	# 	x_range, y_range = self.get_range()
	#
	# 	if intersect_x < x_range[0] or x_range[1] < intersect_x:
	# 		return None
	# 	elif intersect_y < y_range[0] or y_range[1] < intersect_y:
	# 		return None
	#
	# 	return intersect_x, intersect_y

	def line_collide(self, line) -> bool:
		other_start = line.start_pos
		other_end = line.end_pos

		# Cross Product Method (ChatGPT, make more clear in future)
		dir_1 = (other_end.x - other_start.x) * (self.start_pos.y - other_start.y) - (other_end.y - other_start.y) * (self.start_pos.x - other_start.x)
		dir_2 = (other_end.x - other_start.x) * (self.end_pos.y - other_start.y) - (other_end.y - other_start.y) * (self.end_pos.x - other_start.x)
		dir_3 = (self.end_pos.x - self.start_pos.x) * (other_start.y - self.start_pos.y) - (self.end_pos.y - self.start_pos.y) * (other_start.x - self.start_pos.x)
		dir_4 = (self.end_pos.x - self.start_pos.x) * (other_end.y - self.start_pos.y) - (self.end_pos.y - self.start_pos.y) * (other_end.x - self.start_pos.x)

		return (dir_1 > 0 > dir_2 or dir_1 < 0 < dir_2) and (dir_3 > 0 > dir_4 or dir_3 < 0 < dir_4)

	def collides_with(self, collider):
		from data.modules.entities.components.hitbox import Hitbox

		if isinstance(collider, Hitbox):
			if collider.rect.collidepoint(*self.start_pos):
				return True
			if collider.rect.collidepoint(*self.end_pos):
				return True

			for line in collider.get_edge_lines():
				if self.line_collide(line):
					return True
			return False
		elif isinstance(collider, LineCollider):
			return self.line_collide(collider)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera):
		pygame.draw.line(screen, "yellow", camera.world_to_screen(self.start_pos), camera.world_to_screen(self.start_pos + self.line), width=4)
