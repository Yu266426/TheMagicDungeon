import json
import logging
import os
import random
from collections import deque

import pygame
import pygbase
from pygbase import Camera

from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import ROOM_DIR, BATTLE_DIR
from data.modules.base.utils import get_tile_pos
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.room import Room, Hallway
from data.modules.objects.tile import Tile


class Level:
	def __init__(self, entity_manager: EntityManager, room_separation: int, wall_gap_radius: int):
		self.entity_manager = entity_manager
		self.particle_manager: pygbase.ParticleManager = pygbase.Common.get_value("particle_manager")

		# TODO: Rework to separate tiles from rooms
		# A game room is responsible for its location, loading the tiles, and special tiles
		# The level is responsible for feeding collision data, rendering tiles, etc.

		# layer[0: Ground, 1: Player | Walls, 2: Above]
		self.tiles: dict[int, dict[tuple[int, int], Tile]] = {}

		self.rooms: dict[tuple[int, int], Room] = {}
		self.connections = {}

		self.room_separation = room_separation
		self.wall_gap_radius = wall_gap_radius

		self.prev_player_room_pos = None

	def cleanup(self):
		"""
		Removes objects from rooms
		"""

		for room in self.rooms.values():
			room.remove_objects()

	def check_is_tile(self, layer: int, pos: tuple[int, int]) -> bool:
		return layer in self.tiles and pos in self.tiles[layer]

	def add_tile(self, layer: int, tile_pos: tuple[int, int], tile: Tile):
		assert tile is not None
		# logging.debug(f"Adding tile at {layer}, {tile_pos} with position {tile.rect}")
		self.tiles.setdefault(layer, {})[tile_pos] = tile

	def remove_tile(self, layer: int, tile_pos: tuple[int, int]):
		if self.check_is_tile(layer, tile_pos):
			del self.tiles[layer][tile_pos]

			if len(self.tiles[layer].values()) == 0:
				del self.tiles[layer]

	def get_tile(self, pos: pygame.Vector2 | tuple[float, float], layer: int = 1) -> Tile | None:
		tile_pos = get_tile_pos(pos, (TILE_SIZE, TILE_SIZE))

		if not self.check_is_tile(layer, tile_pos):
			return None

		return self.tiles[layer][tile_pos]

	def get_tile_at_tile_pos(self, tile_pos: tuple[int, int], layer: int = 1) -> Tile | None:
		if not self.check_is_tile(layer, tile_pos):
			return None

		return self.tiles[layer][tile_pos]

	def add_room(self, room_pos: tuple[int, int], room_name: str, battle_name: str = ""):
		room = Room(room_name, self.entity_manager, battle_name, self, offset=(room_pos[0] * self.room_separation * TILE_SIZE, room_pos[1] * self.room_separation * TILE_SIZE))
		self.rooms[room_pos] = room
		room.populate_tiles()
		return room

	def add_room_ex(self, room_pos: tuple[int, int], room_name: str, connections: tuple[bool, bool, bool, bool], battle_name: str, room_data: dict):
		offset = (self.room_separation - room_data["cols"]) // 2, (self.room_separation - room_data["rows"]) // 2

		room = Room(room_name, self.entity_manager, battle_name, self, offset=(room_pos[0] * self.room_separation * TILE_SIZE + offset[0] * TILE_SIZE, room_pos[1] * self.room_separation * TILE_SIZE + offset[1] * TILE_SIZE), connections=connections)
		self.rooms[room_pos] = room
		room.populate_tiles()
		return room

	def add_hallway(self, room_pos: tuple[int, int], connected_room_pos: tuple[int, int], room_data: dict, connected_room_data: dict):
		room_size = room_data["cols"], room_data["rows"]
		connected_room_size = connected_room_data["cols"], connected_room_data["rows"]

		# Horizontal connection
		if room_pos[1] == connected_room_pos[1]:
			center_x = int((room_pos[0] + 0.5) + self.room_separation)
			center_y = int((room_pos[1] + 0.5) + self.room_separation)

			# Left
			if connected_room_pos[0] < room_pos[0]:
				room_left_x = center_x - room_size[0] // 2

			# Right
			if room_pos[0] < connected_room_pos[0]:
				room_left_x = center_x + room_size[0] // 2

	def get_room(self, pos: tuple[float, float] | pygame.Vector2) -> Room | None:
		"""
		:param pos: Position in pixels
		:return: Room | None
		"""
		room_pos = get_tile_pos(pos, (self.room_separation * TILE_SIZE, self.room_separation * TILE_SIZE))

		return self.rooms.get(room_pos)

	def get_room_from_room_pos(self, room_pos: tuple[int, int]) -> Room | None:
		return self.rooms.get(room_pos)

	def update(self, delta: float, player_pos: pygame.Vector2):
		player_room_pos = get_tile_pos(player_pos, (self.room_separation * TILE_SIZE, self.room_separation * TILE_SIZE))
		current_room = self.get_room_from_room_pos(player_room_pos)

		player_room_tile_pos = get_tile_pos(player_pos, (TILE_SIZE, TILE_SIZE))
		player_room_tile_pos = player_room_tile_pos[0] - current_room.tile_offset[0], player_room_tile_pos[1] - current_room.tile_offset[1]

		# print(player_room_tile_pos, current_room.n_cols, current_room.n_rows)

		if not self.prev_player_room_pos and 1 <= player_room_tile_pos[0] < current_room.n_cols and 1 <= player_room_tile_pos[1] < current_room.n_rows - 1:
			self.prev_player_room_pos = player_room_pos

			current_room.entered()
		elif self.prev_player_room_pos != player_room_pos and 1 <= player_room_tile_pos[0] < current_room.n_cols - 1 and 1 <= player_room_tile_pos[1] < current_room.n_rows - 1:
			current_room.entered()
			self.get_room_from_room_pos(self.prev_player_room_pos).exited()

			self.prev_player_room_pos = player_room_pos

		self.get_room(player_pos).update(delta)

	def draw_tile(self, layer: int, tile_pos: tuple[int, int], surface: pygame.Surface, camera: Camera):
		# room = self.get_room((pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
		#
		# if room is not None:
		# 	room.draw_tile(level, pos, display, camera, with_offset=True)
		tile = self.get_tile_at_tile_pos(tile_pos, layer)
		if tile is not None:
			tile.draw(surface, camera)

	def draw(self, surface: pygame.Surface, camera: Camera):
		top_left = get_tile_pos(camera.pos, (TILE_SIZE, TILE_SIZE))
		bottom_right = get_tile_pos(camera.pos + pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), (TILE_SIZE, TILE_SIZE))
		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 2, bottom_right[1] + 2

		for layer in range(0, 3):
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(layer, (col, row), surface, camera)

				if layer == 1:
					entities = self.entity_manager.get_entities(row)
					for entity in entities:
						entity.draw(surface, camera)


class LevelGenerator:
	def __init__(self, depth: int, entity_manager: EntityManager, room_separation: int, wall_gap_radius: int):
		self.depth: int = depth
		self.entity_manager = entity_manager
		self.room_separation = room_separation
		self.wall_gap_radius = wall_gap_radius

	# TODO: Redo generation to be over multiple frames
	def generate_level(self):
		level = Level(self.entity_manager, self.room_separation, self.wall_gap_radius)

		# Reset level
		# TODO: Why?
		for room in level.rooms.values():
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
			for _connection in connections[pos]:
				if _connection[0] == pos[0] and _connection[1] == pos[1] - 1:
					top = True
				elif _connection[0] == pos[0] and _connection[1] == pos[1] + 1:
					bottom = True
				elif _connection[0] == pos[0] - 1 and _connection[1] == pos[1]:
					left = True
				elif _connection[0] == pos[0] + 1 and _connection[1] == pos[1]:
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
		rooms: dict[str, dict] = {}
		room_names = []

		for _, _, file_names in os.walk(ROOM_DIR):
			for file_name in file_names:
				name = file_name[:-5]  # Remove .json

				# Ensure only rooms of correct size
				with open(ROOM_DIR / file_name) as room_file:
					room_data = json.load(room_file)
					if room_data["rows"] > self.room_separation or room_data["cols"] > self.room_separation:
						continue

					rooms[name] = room_data

				# Ignore special rooms
				if name not in ("lobby", "start", "start2", "room1"):
					room_names.append(name)

		# Load available battles
		battle_names = []
		for _, _, file_names in os.walk(BATTLE_DIR):
			for file_name in file_names:
				name = file_name[:-5]  # Remove .json

				battle_names.append(name)

		# Room generation
		rooms_to_generate: set[tuple[int, int]] = set()
		connections: dict[tuple[int, int], list[tuple[int, int]]] = {}  # Start, list[end]
		end_rooms: list[tuple[int, int]] = []

		room_queue: deque[tuple[tuple[int, int], int]] = deque()  # Position, depth

		# Add start room
		rooms_to_generate.add((0, 0))

		# Start in all directions
		for direction in directions:
			rooms_to_generate.add(direction)
			room_queue.append((direction, 1))
			add_connection((0, 0), direction)

		while len(room_queue) > 0:
			# Get room info, and move to end of queue
			room_info = room_queue.popleft()
			room_pos = room_info[0]
			room_depth = room_info[1]

			if room_depth > self.depth:
				continue

			# Get available directions
			available_directions = []
			for direction in directions:
				new_pos = (room_pos[0] + direction[0], room_pos[1] + direction[1])
				if new_pos not in rooms_to_generate:
					available_directions.append(direction)

			# If direction not available, continue
			if len(available_directions) == 0:
				continue

			# Have a chance to spread, with the end trying to decrease the change the further the room
			if random.random() < 0.85 - room_depth * (1 / self.depth) * 0.5:
				# Find direction to spread
				direction = random.choice(available_directions)
				new_pos = room_pos[0] + direction[0], room_pos[1] + direction[1]

				rooms_to_generate.add(new_pos)
				add_connection(room_pos, new_pos)
				room_queue.append((new_pos, room_depth + 1))

				room_queue.append(room_info)  # Current room still active, move to end of queue
			else:
				# This room is the final room in its branch
				end_rooms.append(room_pos)

		# Finalize generation
		# TODO: Add hallways when needed
		generated_rooms: dict[tuple[int, int], str] = {}
		rooms_added = set()
		for room_pos in rooms_to_generate:
			room_name = random.choice(room_names) if room_pos != (0, 0) else "start2"

			room_connections = get_connections(room_pos)

			if room_name != "start2":
				if room_pos not in rooms_added:
					rooms_added.add(room_pos)
				else:
					logging.warning("Duplicate")
				level.add_room_ex(room_pos, room_name, room_connections, random.choice(battle_names), rooms[room_name])
			else:
				if room_pos not in rooms_added:
					rooms_added.add(room_pos)
				else:
					logging.warning("Duplicate")

				level.add_room_ex(room_pos, room_name, room_connections, "", rooms[room_name])

			generated_rooms[room_pos] = room_name

		for room_pos, room_name in generated_rooms.items():
			for connection in connections:
				level.add_hallway(room_pos, connection, rooms[room_name], rooms[generated_rooms[connection]])

		return level
