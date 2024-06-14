import json
import logging
import os
import random
from typing import TYPE_CHECKING

import pygame
import pygbase

from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import ROOM_DIR
from data.modules.base.utils import get_tile_pos
from data.modules.entities.entity_manager import EntityManager
from data.modules.level.battle import Battle
from data.modules.objects.game_object import GameObject
from data.modules.objects.object_loader import ObjectLoader
from data.modules.objects.tile import Tile

if TYPE_CHECKING:
	from data.modules.level.level import Level


class BaseRoom:
	def __init__(self, name: str, n_rows: int, n_cols: int, offset: tuple = (0, 0)):
		self.name = name

		self.n_rows = n_rows
		self.n_cols = n_cols

		self.offset = int(offset[0]), int(offset[1])
		self.tile_offset = get_tile_pos(self.offset, (TILE_SIZE, TILE_SIZE))

		# layer[back, player, front]
		# self.tiles: list[list[list[Tile | None]]] = []
		self.tiles: dict[int, dict[tuple[int, int], Tile]] = {}
		self.objects: list[GameObject] = []

	def check_bounds(self, pos: tuple[int, int]) -> bool:
		return 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows

	def check_is_tile(self, layer: int, pos: tuple[int, int]) -> bool:
		return layer in self.tiles and pos in self.tiles[layer]

	def get_tile(self, layer: int, pos: tuple[int, int], with_offset: bool = True) -> Tile | None:
		if with_offset:
			pos = pos[0] - self.tile_offset[0], pos[1] - self.tile_offset[1]

		if self.check_is_tile(layer, pos):
			return self.tiles[layer][pos]

		return None

	def add_tile(self, layer: int, pos: tuple[int, int], tile: Tile):
		assert tile is not None

		if self.check_bounds(pos):
			self.tiles.setdefault(layer, {})[pos] = tile

	def remove_tile(self, layer: int, pos: tuple[int, int]):
		if self.check_is_tile(layer, pos):
			del self.tiles[layer][pos]

			if len(self.tiles[layer].values()) == 0:
				del self.tiles[layer]

	def get_object(self, pos: tuple, with_hitbox: bool = False):
		if not with_hitbox:
			for game_object in self.objects:
				if game_object.rect.collidepoint(pos[0], pos[1]):
					return game_object
		else:
			for game_object in self.objects:
				if game_object.hitbox.collidepoint(pos[0], pos[1]):
					return game_object

		return None

	def add_object(self, game_object: GameObject):
		game_object.added()
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject):
		if game_object is not None:
			game_object.removed()
			self.objects.remove(game_object)

	def remove_objects(self):
		for game_object in self.objects:
			game_object.removed()

		self.objects.clear()

	def draw_tile(self, layer: int, pos: tuple[int, int], display: pygame.Surface, camera: pygbase.Camera, with_offset: bool = False):
		if with_offset:
			pos = pos[0] - self.tile_offset[0], pos[1] - self.tile_offset[1]

		# print(pos, self.check_is_tile(layer, pos), self.get_tile(layer, pos))
		if self.check_is_tile(layer, pos):
			self.get_tile(layer, pos, with_offset=False).draw(display, camera)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera, entities: dict[int, dict]):
		top_left: tuple[int, int] = get_tile_pos((camera.pos.x - self.offset[0], camera.pos.y - self.offset[1]), (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.pos.x + SCREEN_WIDTH - self.offset[0], camera.pos.y + SCREEN_HEIGHT - self.offset[1]), (TILE_SIZE, TILE_SIZE))

		y_offset = int(self.offset[1] // TILE_SIZE)

		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 1, bottom_right[1] + 2

		for layer in self.tiles.keys():
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(layer, (col, row), screen, camera)

				if layer == 1:
					if row + y_offset in entities:
						for entity in entities[row + y_offset].values():
							entity.draw(screen, camera)

		for game_object in self.objects:
			game_object.draw(screen, camera)


class Room(BaseRoom):
	def __init__(self, name: str, entity_manager: EntityManager, battle_name: str, level: "Level", n_rows: int = 10, n_cols: int = 10, offset: tuple = (0, 0), connections=(False, False, False, False), random_floor=True):
		super().__init__(name, n_rows, n_cols, offset)

		self.battle_in_progress = False
		self.battle = Battle(battle_name, level, self, entity_manager) if battle_name != "" else None

		self.hallway_connection_tiles: list[tuple[int, int]] = []

		# New room
		self.save_path = ROOM_DIR / f"{name}.json"
		if not os.path.isfile(self.save_path):
			logging.debug("Creating new room")

			# self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)
		else:
			self.load(entity_manager)

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)

	def generate_walls(self, connections, gap_radius: int = 1):
		"""
		Generates walls with gaps

		:param connections: Up, Down, Left, Right
		:param gap_radius: Radius of gap
		"""

		wall_sheet = pygbase.ResourceManager.get_resource("sprite_sheet", "walls")

		# Slightly different midpoints for odd vs even sized rooms
		if self.n_cols % 2 == 0:
			x_mid_point = self.n_cols // 2 - 1

			# Top and bottom
			for col in range(self.n_cols):
				if connections[0]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius + 1:
						self.add_tile(1, (col, 0), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (col, 0))
						self.hallway_connection_tiles.append((col, 0))
				else:
					self.add_tile(1, (col, 0), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1])))

				if connections[1]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius + 1:
						self.add_tile(1, (col, self.n_rows - 1), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (col, self.n_rows - 1))
						self.hallway_connection_tiles.append((col, self.n_rows - 1))
				else:
					self.add_tile(1, (col, self.n_rows - 1), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1])))
		else:
			x_mid_point = self.n_cols // 2

			# Top and bottom
			for col in range(self.n_cols):
				if connections[0]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius:
						self.add_tile(1, (col, 0), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (col, 0))
						self.hallway_connection_tiles.append((col, 0))
				else:
					self.add_tile(1, (col, 0), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1])))

				if connections[1]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius:
						self.add_tile(1, (col, self.n_rows - 1), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (col, self.n_rows - 1))
						self.hallway_connection_tiles.append((col, self.n_rows - 1))

				else:
					self.add_tile(1, (col, self.n_rows - 1), Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1])))

		if self.n_rows % 2 == 0:
			y_mid_point = self.n_rows // 2 - 1

			# Left and Right
			for row in range(self.n_rows):
				if connections[2]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius + 1:
						self.add_tile(1, (0, row), Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (0, row))
						self.hallway_connection_tiles.append((0, row))
				else:
					self.add_tile(1, (0, row), Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))

				if connections[3]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius + 1:
						self.add_tile(1, (self.n_cols - 1, row), Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (self.n_cols - 1, row))
						self.hallway_connection_tiles.append((self.n_cols - 1, row))
				else:
					self.add_tile(1, (self.n_cols - 1, row), Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))
		else:
			y_mid_point = self.n_rows // 2

			# Left and Right
			for row in range(self.n_rows):
				if connections[2]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius:
						self.add_tile(1, (0, row), Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (0, row))
						self.hallway_connection_tiles.append((0, row))
				else:
					self.add_tile(1, (0, row), Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))

				if connections[3]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius:
						self.add_tile(1, (self.n_cols - 1, row), Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))
					else:
						self.remove_tile(1, (self.n_cols - 1, row))
						self.hallway_connection_tiles.append((self.n_cols - 1, row))
				else:
					self.add_tile(1, (self.n_cols - 1, row), Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))

	def generate_floor(self):
		tiles_sheet = pygbase.ResourceManager.get_resource("sprite_sheet", "tiles")
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self.add_tile(0, (col, row), Tile(
					"tiles",
					random.randrange(0, tiles_sheet.length),
					(col * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])
				))

	def load(self, entity_manager: EntityManager):
		with open(self.save_path) as file:
			room_data: dict = json.load(file)

		self.n_rows = room_data["rows"]
		self.n_cols = room_data["cols"]

		# self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

		for level, tiles in enumerate(room_data["tiles"]):
			for tile in tiles:
				row = tile["pos"][0]
				col = tile["pos"][1]
				self.add_tile(level, (col, row), Tile(tile["image_info"][0], tile["image_info"][1], (col * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])))

		for object_data in room_data["objects"]:
			object_name = object_data["name"]
			pos = object_data["pos"]

			game_object, tags = ObjectLoader.create_object(object_name, (pos[0] + self.tile_offset[0], pos[1] + self.tile_offset[1]))
			game_object.added()

			entity_manager.add_entity(game_object, ("object",) + tags)
			self.objects.append(game_object)

	def is_valid_spawn(self, tile_pos: tuple[int, int]):
		return (
				1 not in self.tiles or
				tile_pos not in self.tiles[1]
		)

	def generate_spawn_pos(self):
		for _ in range(10):
			row = random.randrange(0, self.n_rows)
			col = random.randrange(0, self.n_cols)

			if self.is_valid_spawn((col, row)):
				# Find location close to middle of tile
				return (col + 0.5) * TILE_SIZE + self.offset[0], (row + 0.8) * TILE_SIZE + self.offset[1]

	def activate_walls(self):
		wall_sheet = pygbase.ResourceManager.get_resource("sprite_sheet", "walls")

		for tile_pos in self.hallway_connection_tiles:
			self.add_tile(1, tile_pos, Tile("walls", random.randrange(0, wall_sheet.length), (tile_pos[0] * TILE_SIZE + self.offset[0], (tile_pos[1] + 1) * TILE_SIZE + self.offset[1])))

	def deactivate_walls(self):
		for tile_pos in self.hallway_connection_tiles:
			self.remove_tile(1, tile_pos)

	def entered(self):
		"""
		Run when player enters more than 1 tile into the room (outer tiles are walls)
		"""

		if self.battle:
			if not self.battle.completed:
				self.battle_in_progress = True

				self.activate_walls()

	def exited(self):
		pass

	def update(self, delta: float):
		for game_object in self.objects:
			game_object.update(delta)

		if self.battle_in_progress:
			battle_done = self.battle.update()

			if battle_done:
				self.battle_in_progress = False
				self.deactivate_walls()


class EditorRoom(BaseRoom):
	def __init__(self, name: str, n_rows: int = 10, n_cols: int = 10):
		super().__init__(name, n_rows, n_cols)

		# New room
		self.save_path = os.path.join(ROOM_DIR, f"{name}.json")
		if not os.path.isfile(self.save_path):
			logging.debug("Creating new editor room")
		# self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)
		else:
			self.load()

	def load(self):
		with open(self.save_path) as file:
			room_data: dict = json.load(file)

		self.n_rows = room_data["rows"]
		self.n_cols = room_data["cols"]

		# self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

		for level, tiles in enumerate(room_data["tiles"]):
			for tile in tiles:
				row = tile["pos"][0]
				col = tile["pos"][1]
				self.add_tile(level, (col, row), Tile(tile["image_info"][0], tile["image_info"][1], (col * TILE_SIZE, (row + 1) * TILE_SIZE)))

		for game_object in room_data["objects"]:
			object_type = game_object["name"]
			pos = game_object["pos"]

			game_object, tags = ObjectLoader.create_object(object_type, pos)
			game_object.added()

			self.objects.append(game_object)

	def save(self):
		data = {
			"rows": self.n_rows,
			"cols": self.n_cols,
			"tiles": [[], [], []],
			"objects": []
		}

		for level, level_data in self.tiles.items():
			for pos, tile in level_data.items():
				tile_data = {
					"pos": pos,
					"image_info": [tile.sprite_sheet_name, tile.image_index],
				}
				data["tiles"][level].append(tile_data)

		for game_object in self.objects:
			data["objects"].append({
				"name": game_object.name,
				"pos": game_object.tile_pos
			})

		with open(self.save_path, "w") as file:
			file.write(json.dumps(data))

		logging.info("Level Saved")

	def draw_room_to_surface(self, surface: pygame.Surface):
		surface_size = surface.get_size()

		room_surface = pygame.Surface((self.n_cols * TILE_SIZE, self.n_rows * TILE_SIZE), flags=pygame.SRCALPHA)
		temp_camera = pygbase.Camera()

		for layer in range(len(self.tiles)):
			for row in range(self.n_rows):
				for col in range(self.n_cols):
					self.draw_tile(layer, (col, row), room_surface, temp_camera)

		for game_object in self.objects:
			game_object.draw(room_surface, temp_camera)

		pygame.transform.scale(room_surface, surface_size, surface)
