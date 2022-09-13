import os
import random
from collections import deque

import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.base.files import LEVEL_DIR
from data.modules.base.room import Room
from data.modules.base.utils import get_tile_pos


class Level:
	def __init__(self):
		self.rooms: dict[int, dict[int, Room]] = {}
		self.connections: dict[tuple[int, int], list[tuple[int, int]]] = {}

		self.room_size = 7
		self.generate_level(5)

	def generate_level(self, depth=3):
		# Directions for generation
		directions = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1)
		]

		# All the rooms available
		room_names = []
		for _, _, file_names in os.walk(LEVEL_DIR):
			for file_name in file_names:
				room_names.append(file_name[:-5])

		# Room generation
		room_queue: deque[tuple[Room, tuple[int, int], int]] = deque()
		self.add_room((0, 0), (0, 0), "test")  # Start Room

		# Start in all directions
		for direction in directions:
			new_room = self.add_room(direction, direction, random.choice(room_names))
			room_queue.append((new_room, direction, 1))
			self.add_connection((0, 0), direction)

		end_rooms = []

		while len(room_queue) > 0:
			# Get room info, and move to end of queue
			room_info = room_queue.popleft()
			room = room_info[0]
			room_pos = room_info[1]
			room_depth = room_info[2]

			if room_depth < depth:
				# Get available directions
				available_directions = []
				for direction in directions:
					if self.get_room((room_pos[0] + direction[0], room_pos[1] + direction[1])) is None:
						available_directions.append(direction)

				# If direction available
				if len(available_directions) != 0:
					# Have a chance to spread, with the end trying to decrease the change the further the room
					if random.random() < 0.85 - room_depth * 0.03:
						# Find direction to spread
						direction = random.choice(available_directions)

						new_pos = room_pos[0] + direction[0], room_pos[1] + direction[1]
						if self.get_room(new_pos) is None:
							new_room = self.add_room(new_pos, direction, random.choice(room_names))
							self.add_connection(room_pos, new_pos)
							room_queue.append((new_room, new_pos, room_depth + 1))

						room_queue.append(room_info)  # Current room still active, move to end of queue
					else:
						# This room is the final room in its branch
						end_rooms.append(room)

	def add_connection(self, start: tuple[int, int], end: tuple[int, int]):
		if start not in self.connections:
			self.connections[start] = []
		self.connections[start].append(end)

	def add_room(self, pos: tuple[int, int], direction: tuple[int, int], room_name: str):
		if pos[1] not in self.rooms:
			self.rooms[pos[1]] = {}

		room = Room(room_name, offset=(pos[0] * self.room_size * TILE_SIZE, pos[1] * self.room_size * TILE_SIZE))
		self.rooms[pos[1]][pos[0]] = room
		return room

	def get_room(self, pos: tuple[int, int]):
		if pos[1] in self.rooms and pos[0] in self.rooms[pos[1]]:
			return self.rooms[pos[1]][pos[0]]
		return None

	def draw(self, display: pygame.Surface, camera: Camera):
		top_left = get_tile_pos(camera.target, (self.room_size * TILE_SIZE, self.room_size * TILE_SIZE))
		bottom_right = get_tile_pos(camera.target + pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), (self.room_size * TILE_SIZE, self.room_size * TILE_SIZE))

		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 2, bottom_right[1] + 2

		for row in range(top_left[1], bottom_right[1]):
			for col in range(top_left[0], bottom_right[0]):
				if row in self.rooms and col in self.rooms[row]:
					self.rooms[row][col].draw(display, camera)

# for row, row_info in self.rooms.items():
# 	for col, col_info in row_info.items():
# 		pygame.draw.rect(display, "white", pygame.Rect(row * 100 - camera.target.x, col * 100 - camera.target.y, 80, 80))
#
# pygame.draw.rect(display, "yellow", pygame.Rect(*-camera.target, 80, 80))
#
# for start, ends in self.connections.items():
# 	for end in ends:
# 		pygame.draw.line(
# 			display, "green", (start[0] * 100 - camera.target.x + 40, start[1] * 100 - camera.target.y + 40),
# 			(end[0] * 100 - camera.target.x + 40, end[1] * 100 - camera.target.y + 40),
# 			width=5
# 		)
