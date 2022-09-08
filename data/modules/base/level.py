import os
import random
from collections import deque

import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import TILE_SIZE
from data.modules.base.files import LEVEL_DIR
from data.modules.base.room import Room


class Level:
	def __init__(self):
		self.rooms: dict[int, dict[int, Room]] = {}
		self.connections: dict[tuple[int, int], list[tuple[int, int]]] = {}

		self.room_size = 30
		self.generate_level()

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
		start_room = self.add_room((0, 0), (0, 0), "test")

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
					# Have a chance to spread
					if random.random() < 0.7:
						room_queue.append(room_info)

						# Spread in all directions
						direction = random.choice(available_directions)

						new_pos = room_pos[0] + direction[0], room_pos[1] + direction[1]
						if self.get_room(new_pos) is None:
							new_room = self.add_room(new_pos, direction, random.choice(room_names))

							self.add_connection(room_pos, new_pos)

							room_queue.append((new_room, new_pos, room_depth + 1))
					else:
						end_rooms.append(room)

	def add_connection(self, start: tuple[int, int], end: tuple[int, int]):
		if start not in self.connections:
			self.connections[start] = []
		self.connections[start].append(end)

	def add_room(self, pos: tuple[int, int], direction: tuple[int, int], room_name: str):
		if pos[0] not in self.rooms:
			self.rooms[pos[0]] = {}

		room = Room(room_name, offset=(pos[0] + self.room_size * direction[0], pos[1] + self.room_size + direction[1]))
		self.rooms[pos[0]][pos[1]] = room
		return room

	def get_room(self, pos: tuple[int, int]):
		if pos[0] in self.rooms and pos[1] in self.rooms[pos[0]]:
			return self.rooms[pos[0]][pos[1]]
		return None

	def draw(self, display: pygame.Surface, camera: Camera):
		for row, row_info in self.rooms.items():
			for col, col_info in row_info.items():
				pygame.draw.rect(display, "white", pygame.Rect(row * 100 - camera.target.x, col * 100 - camera.target.y, 80, 80))

		pygame.draw.rect(display, "yellow", pygame.Rect(*-camera.target, 80, 80))

		for start, ends in self.connections.items():
			for end in ends:
				pygame.draw.line(
					display, "green", (start[0] * 100 - camera.target.x + 40, start[1] * 100 - camera.target.y + 40),
					(end[0] * 100 - camera.target.x + 40, end[1] * 100 - camera.target.y + 40),
					width=5
				)
