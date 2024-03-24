import json
import os
import random
from collections import deque

import pygame
import pygbase
from pygbase import Camera

from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import ROOM_DIR, BATTLE_DIR
from data.modules.level.room import Room
from data.modules.base.utils import get_tile_pos, get_pixel_pos
from data.modules.entities.entity_manager import EntityManager


class Level:
	def __init__(self, entity_manager: EntityManager, room_size: int):
		self.entity_manager = entity_manager
		self.particle_manager: pygbase.ParticleManager = pygbase.Common.get_value("particle_manager")

		self.rooms: dict[int, dict[int, Room]] = {}
		self.connections = {}

		self.room_size = room_size

		self.prev_player_room_pos = None

	def cleanup(self):
		"""
		Removes objects from rooms
		"""

		for row in self.rooms.values():
			for room in row.values():
				room.remove_objects()

	def add_room(self, pos: tuple[int, int], room_name: str, connections: tuple[bool, bool, bool, bool], battle_name: str):
		if pos[1] not in self.rooms:
			self.rooms[pos[1]] = {}

		room = Room(room_name, self.entity_manager, battle_name, self, offset=(pos[0] * self.room_size * TILE_SIZE, pos[1] * self.room_size * TILE_SIZE), connections=connections)
		self.rooms[pos[1]][pos[0]] = room
		return room

	def get_room(self, pos: tuple[float, float]) -> Room | None:
		"""
		:param pos: Position in pixels
		:return: Room | None
		"""
		room_pos = get_tile_pos(pos, (self.room_size * TILE_SIZE, self.room_size * TILE_SIZE))

		if room_pos[1] in self.rooms and room_pos[0] in self.rooms[room_pos[1]]:
			return self.rooms[room_pos[1]][room_pos[0]]
		return None

	def get_tile(self, pos: pygame.Vector2 | tuple[float, float]):
		room = self.get_room(pos)
		if room is not None:
			return room.get_tile(1, get_tile_pos(pos, (TILE_SIZE, TILE_SIZE)))
		return None

	def update(self, player_pos):
		player_room_pos = get_tile_pos(player_pos, (self.room_size * TILE_SIZE, self.room_size * TILE_SIZE))

		if not self.prev_player_room_pos:
			self.prev_player_room_pos = player_room_pos

			self.get_room(player_pos).entered()
		elif self.prev_player_room_pos != player_room_pos:
			self.get_room(player_pos).entered()
			self.get_room(get_pixel_pos(self.prev_player_room_pos, (self.room_size * TILE_SIZE, self.room_size * TILE_SIZE))).exited()

			self.prev_player_room_pos = player_room_pos

		self.get_room(player_pos).update()

	def draw_tile(self, level: int, pos: tuple[int, int], display: pygame.Surface, camera: Camera):
		room = self.get_room((pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))

		if room is not None:
			room.draw_tile(level, pos[1], pos[0], display, camera, with_offset=True)

	def draw(self, display: pygame.Surface, camera: Camera):
		top_left = get_tile_pos(camera.pos, (TILE_SIZE, TILE_SIZE))
		bottom_right = get_tile_pos(camera.pos + pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), (TILE_SIZE, TILE_SIZE))
		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 2, bottom_right[1] + 2

		for level in range(0, 3):
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(level, (col, row), display, camera)

				if level == 1:
					entities = self.entity_manager.get_entities(row)
					for entity in entities:
						entity.draw(display, camera)


class LevelGenerator:
	def __init__(self, depth: int, entity_manager: EntityManager, room_size: int):
		self.depth: int = depth
		self.entity_manager = entity_manager
		self.room_size = room_size

	# TODO: Redo generation to be over multiple frames
	def generate_level(self):
		level = Level(self.entity_manager, self.room_size)

		# Reset level
		for row in level.rooms.values():
			for room in row.values():
				room.remove_objects()

		level.rooms.clear()
		level.connections.clear()

		def add_connection(start: tuple[int, int], end: tuple[int, int]):
			if start not in connections:
				connections[start] = []
			connections[start].append(end)

			if end not in connections:
				connections[end] = []
			connections[end].append(start)

		def get_connections(pos: tuple[int, int]):
			top, bottom, left, right = False, False, False, False
			for connection in connections[pos]:
				if connection[0] == pos[0] and connection[1] == pos[1] - 1:
					top = True
				elif connection[0] == pos[0] and connection[1] == pos[1] + 1:
					bottom = True
				elif connection[0] == pos[0] - 1 and connection[1] == pos[1]:
					left = True
				elif connection[0] == pos[0] + 1 and connection[1] == pos[1]:
					right = True
			return top, bottom, left, right

		# Directions for generation
		directions = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1)
		]

		# All the rooms available
		room_names = []
		for _, _, file_names in os.walk(ROOM_DIR):
			for file_name in file_names:
				name = file_name[:-5]  # Remove .json

				# Ensure only rooms of correct size
				with open(ROOM_DIR / file_name) as room_file:
					room_data = json.load(room_file)
					if room_data["rows"] != self.room_size or room_data["cols"] != self.room_size:
						continue

				# Ignore special rooms
				if name != "start":
					room_names.append(name)

		# Load available battles
		battle_names = []
		for _, _, file_names in os.walk(BATTLE_DIR):
			for file_name in file_names:
				name = file_name[:-5]  # Remove .json

				battle_names.append(name)

		# Room generation
		generated_rooms: set[tuple[int, int]] = set()
		connections: dict[tuple[int, int], list[tuple[int, int]]] = {}  # Start, list[end]
		end_rooms: list[tuple[int, int]] = []

		room_queue: deque[tuple[tuple[int, int], int]] = deque()  # Position, depth

		# Add start room
		generated_rooms.add((0, 0))

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

			if room_depth < self.depth:
				# Get available directions
				available_directions = []
				for direction in directions:
					new_pos = (room_pos[0] + direction[0], room_pos[1] + direction[1])
					if new_pos not in generated_rooms:
						available_directions.append(direction)

				# If direction available
				if len(available_directions) != 0:
					# Have a chance to spread, with the end trying to decrease the change the further the room
					if random.random() < 0.85 - room_depth * (1 / self.depth) * 0.5:
						# Find direction to spread
						direction = random.choice(available_directions)

						new_pos = room_pos[0] + direction[0], room_pos[1] + direction[1]
						if level.get_room((new_pos[0] * self.room_size * TILE_SIZE, new_pos[1] * self.room_size * TILE_SIZE)) is None:
							generated_rooms.add(new_pos)
							add_connection(room_pos, new_pos)
							room_queue.append((new_pos, room_depth + 1))

						room_queue.append(room_info)  # Current room still active, move to end of queue
					else:
						# This room is the final room in its branch
						end_rooms.append(room_pos)

		# Finalize generation
		# TODO: Add hallways when needed
		for room_pos in generated_rooms:
			room_name = random.choice(room_names) if room_pos != (0, 0) else "start"

			if room_name != "start":
				level.add_room(room_pos, room_name, get_connections(room_pos), random.choice(battle_names))
			else:
				level.add_room(room_pos, room_name, get_connections(room_pos), "")

		return level
