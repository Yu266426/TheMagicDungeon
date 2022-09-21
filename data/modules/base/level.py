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
		self.connections = {}

		self.room_size = 7
		self.connections = self.generate_level(3)

	# TODO: Redo generation to be over multiple frames
	def generate_level(self, depth=3):
		def add_connection(start: tuple[int, int], end: tuple[int, int]):
			if start not in connections:
				connections[start] = []

			connections[start].append(end)

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
		generated_rooms: set[tuple[int, int]] = set()
		connections: dict[tuple[int, int], list[tuple[int, int]]] = {}  # Start, list[end]
		end_rooms: list[tuple[int, int]] = []

		room_queue: deque[tuple[tuple[int, int], int]] = deque()  # Position, depth

		# Start in all directions
		for direction in directions:
			generated_rooms.add(direction)
			room_queue.append((direction, 1))
			add_connection((0, 0), direction)

		while len(room_queue) > 0:
			# Get room info, and move to end of queue
			room_info = room_queue.popleft()
			room_pos = room_info[0]
			room_depth = room_info[1]

			if room_depth < depth:
				# Get available directions
				available_directions = []
				for direction in directions:
					new_pos = (room_pos[0] + direction[0], room_pos[1] + direction[1])
					if new_pos not in generated_rooms:
						available_directions.append(direction)

				# If direction available
				if len(available_directions) != 0:
					# Have a chance to spread, with the end trying to decrease the change the further the room
					if random.random() < 0.85 - room_depth * 0.03:
						# Find direction to spread
						direction = random.choice(available_directions)

						new_pos = room_pos[0] + direction[0], room_pos[1] + direction[1]
						if self.get_room(new_pos) is None:
							generated_rooms.add(new_pos)
							add_connection(room_pos, new_pos)
							room_queue.append((new_pos, room_depth + 1))

						room_queue.append(room_info)  # Current room still active, move to end of queue
					else:
						# This room is the final room in its branch
						end_rooms.append(room_pos)

		# Finalize generation
		# Start room
		self.add_room((0, 0), "test")

		# TODO: Finish
		for room_pos in generated_rooms:
			self.add_room(room_pos, random.choice(room_names))

		return connections

	def add_room(self, pos: tuple[int, int], room_name: str):
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

		# Generation Map
		for row, row_data in self.rooms.items():
			for col, room in row_data.items():
				pygame.draw.rect(display, "white", pygame.Rect(col * 100 - camera.target.x, row * 100 - camera.target.y, 80, 80))

		pygame.draw.rect(display, "yellow", pygame.Rect(*-camera.target, 80, 80))

		for start, ends in self.connections.items():
			for end in ends:
				pygame.draw.line(
					display, "green", (start[0] * 100 - camera.target.x + 40, start[1] * 100 - camera.target.y + 40),
					(end[0] * 100 - camera.target.x + 40, end[1] * 100 - camera.target.y + 40),
					width=5
				)
