import json
import os
import random

import pygame
import pygbase

from data.modules.base.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import ROOM_DIR
from data.modules.base.utils import get_tile_pos, generate_3d_list
from data.modules.entities.entity_manager import EntityManager
from data.modules.objects.game_object import GameObject
from data.modules.objects.object_loader import ObjectLoader
from data.modules.objects.tile import Tile


class Room:
	def __init__(self, name: str, entity_manager: EntityManager, particle_manager: pygbase.ParticleManager, n_rows: int = 10, n_cols: int = 10, offset: tuple = (0, 0), connections=(False, False, False, False), random_floor=True):
		self.n_rows = n_rows
		self.n_cols = n_cols

		self.offset = int(offset[0]), int(offset[1])
		self.tile_offset = get_tile_pos(self.offset, (TILE_SIZE, TILE_SIZE))

		# layer[back, player, front]
		self.tiles: list[list[list[Tile | None]]] = []
		self.objects: list[GameObject] = []

		# New room
		self.save_path = ROOM_DIR / f"{name}.json"
		if not os.path.isfile(self.save_path):
			print("Creating new room")

			self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)
		else:
			self.load(entity_manager, particle_manager)

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)

	def generate_walls(self, connections, gap_radius: int = 1):
		"""
		Generates walls with gaps

		:param connections: Up, Down, Left, Right
		:param gap_radius: Size of gap
		"""

		wall_sheet = pygbase.ResourceManager.get_resource("sprite_sheet", "walls")

		if self.n_cols % 2 == 0:
			x_mid_point = self.n_cols // 2 - 1

			# Top and bottom
			for col in range(self.n_cols):
				if connections[0]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius + 1:
						self.tiles[1][0][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][0][col] = None
				else:
					self.tiles[1][0][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1]))

				if connections[1]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius + 1:
						self.tiles[1][self.n_rows - 1][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][self.n_rows - 1][col] = None
				else:
					self.tiles[1][self.n_rows - 1][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1]))
		else:
			x_mid_point = self.n_cols // 2

			# Top and bottom
			for col in range(self.n_cols):
				if connections[0]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius:
						self.tiles[1][0][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][0][col] = None
				else:
					self.tiles[1][0][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], TILE_SIZE + self.offset[1]))

				if connections[1]:
					if col < x_mid_point - gap_radius or col > x_mid_point + gap_radius:
						self.tiles[1][self.n_rows - 1][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][self.n_rows - 1][col] = None
				else:
					self.tiles[1][self.n_rows - 1][col] = Tile("walls", random.randrange(0, wall_sheet.length), (col * TILE_SIZE + self.offset[0], self.n_rows * TILE_SIZE + self.offset[1]))

		if self.n_rows % 2 == 0:
			y_mid_point = self.n_rows // 2 - 1

			# Left and Right
			for row in range(self.n_rows):
				if connections[2]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius + 1:
						self.tiles[1][row][0] = Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][row][0] = None
				else:
					self.tiles[1][row][0] = Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))

				if connections[3]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius + 1:
						self.tiles[1][row][self.n_cols - 1] = Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][row][self.n_cols - 1] = None
				else:
					self.tiles[1][row][self.n_cols - 1] = Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))
		else:
			y_mid_point = self.n_rows // 2

			# Left and Right
			for row in range(self.n_rows):
				if connections[2]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius:
						self.tiles[1][row][0] = Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][row][0] = None
				else:
					self.tiles[1][row][0] = Tile("walls", random.randrange(0, wall_sheet.length), (self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))

				if connections[3]:
					if row < y_mid_point - gap_radius or row > y_mid_point + gap_radius:
						self.tiles[1][row][self.n_cols - 1] = Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))
					else:
						self.tiles[1][row][self.n_cols - 1] = None
				else:
					self.tiles[1][row][self.n_cols - 1] = Tile("walls", random.randrange(0, wall_sheet.length), ((self.n_cols - 1) * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))

	def generate_floor(self):
		tiles_sheet = pygbase.ResourceManager.get_resource("sprite_sheet", "tiles")
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self.tiles[0][row][col] = Tile(
					"tiles",
					random.randrange(0, tiles_sheet.length),
					(col * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])
				)

	def load(self, entity_manager: EntityManager, particle_manager: pygbase.ParticleManager):
		with open(self.save_path) as file:
			room_data: dict = json.load(file)

		self.n_rows = room_data["rows"]
		self.n_cols = room_data["cols"]

		self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

		for level, tiles in enumerate(room_data["tiles"]):
			for tile in tiles:
				row = tile["pos"][0]
				col = tile["pos"][1]
				self.tiles[level][row][col] = Tile(tile["image_info"][0], tile["image_info"][1], (col * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1]))

		for game_object in room_data["objects"]:
			object_name = game_object["name"]
			pos = game_object["pos"]

			entity_manager.add_entity(ObjectLoader.create_object(object_name, (pos[0] * TILE_SIZE + self.offset[0], pos[1] * TILE_SIZE + self.offset[1]), {"entity_manager": entity_manager, "particle_manager": particle_manager}), ("object",))

	def save(self):
		data = {
			"rows": self.n_rows,
			"cols": self.n_cols,
			"tiles": [[], [], []],
			"objects": []
		}

		for level, level_data in enumerate(self.tiles):
			for row, row_data in enumerate(level_data):
				for col, tile in enumerate(row_data):
					if tile is not None:
						tile_data = {
							"pos": [row, col],
							"image_info": [tile.sprite_sheet_name, tile.image_index],
						}
						data["tiles"][level].append(tile_data)

		for game_object in self.objects:
			data["objects"].append({
				"name": game_object.name,
				"pos": [int(game_object.pos.x / TILE_SIZE), int(game_object.pos.y / TILE_SIZE)]
			})

		with open(self.save_path, "w") as file:
			file.write(json.dumps(data))

		print("Level saved")

	def check_bounds(self, pos: tuple[int, int]):
		return 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows

	def get_tile(self, layer: int, pos: tuple[int, int]) -> Tile:
		pos = pos[0] - self.tile_offset[0], pos[1] - self.tile_offset[1]

		if self.check_bounds(pos):
			return self.tiles[layer][pos[1]][pos[0]]

	def add_tile(self, layer: int, pos: tuple[int, int], tile: Tile):
		if self.check_bounds(pos):
			self.tiles[layer][pos[1]][pos[0]] = tile

	def remove_tile(self, layer: int, pos: tuple[int, int]):
		if self.check_bounds(pos):
			self.tiles[layer][pos[1]][pos[0]] = None

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
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject):
		if game_object is not None:
			game_object.removed()
			self.objects.remove(game_object)

	def draw_tile(self, layer: int, row: int, col: int, display: pygame.Surface, camera: pygbase.Camera, with_offset: bool = False):
		if with_offset:
			col -= self.tile_offset[0]
			row -= self.tile_offset[1]

		if self.check_bounds((col, row)):
			if self.tiles[layer][row][col] is not None:
				self.tiles[layer][row][col].draw(display, camera)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera, entities: dict[int, dict]):
		top_left: tuple[int, int] = get_tile_pos((camera.pos.x - self.offset[0], camera.pos.y - self.offset[1]), (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.pos.x + SCREEN_WIDTH - self.offset[0], camera.pos.y + SCREEN_HEIGHT - self.offset[1]), (TILE_SIZE, TILE_SIZE))

		y_offset = int(self.offset[1] // TILE_SIZE)

		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 1, bottom_right[1] + 2

		for layer in range(len(self.tiles)):
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(layer, row, col, screen, camera)

				if layer == 1:
					if row + y_offset in entities:
						for entity in entities[row + y_offset].values():
							entity.draw(screen, camera)

		for game_object in self.objects:
			game_object.draw(screen, camera)


class EditorRoom:
	def __init__(self, name: str, particle_manager: pygbase.ParticleManager, n_rows: int = 10, n_cols: int = 10):
		self.n_rows = n_rows
		self.n_cols = n_cols

		# layer[back, player, front]
		self.tiles: list[list[list[Tile | None]]] = []
		self.objects: list[GameObject] = []

		# New room
		self.save_path = os.path.join(ROOM_DIR, f"{name}.json")
		if not os.path.isfile(self.save_path):
			print("Creating new editor room")
			self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)
		else:
			self.load(particle_manager)

	def load(self, particle_manager: pygbase.ParticleManager):
		with open(self.save_path) as file:
			room_data: dict = json.load(file)

		self.n_rows = room_data["rows"]
		self.n_cols = room_data["cols"]

		self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

		for level, tiles in enumerate(room_data["tiles"]):
			for tile in tiles:
				row = tile["pos"][0]
				col = tile["pos"][1]
				self.tiles[level][row][col] = Tile(tile["image_info"][0], tile["image_info"][1], (col * TILE_SIZE, (row + 1) * TILE_SIZE))

		for game_object in room_data["objects"]:
			object_type = game_object["name"]
			pos = game_object["pos"]
			self.objects.append(ObjectLoader.create_object(object_type, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE), {"particle_manager": particle_manager}))

	def save(self):
		data = {
			"rows": self.n_rows,
			"cols": self.n_cols,
			"tiles": [[], [], []],
			"objects": []
		}

		for level, level_data in enumerate(self.tiles):
			for row, row_data in enumerate(level_data):
				for col, tile in enumerate(row_data):
					if tile is not None:
						tile_data = {
							"pos": [row, col],
							"image_info": [tile.sprite_sheet_name, tile.image_index],
						}
						data["tiles"][level].append(tile_data)

		for game_object in self.objects:
			data["objects"].append({
				"name": game_object.name,
				"pos": [int(game_object.pos.x / TILE_SIZE), int(game_object.pos.y / TILE_SIZE)]
			})

		with open(self.save_path, "w") as file:
			file.write(json.dumps(data))

		print("Level saved")

	def check_bounds(self, pos: tuple[int, int]):
		return 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows

	def get_tile(self, layer: int, pos: tuple[int, int]) -> Tile:
		if self.check_bounds(pos):
			return self.tiles[layer][pos[1]][pos[0]]

	def add_tile(self, layer: int, pos: tuple[int, int], tile: Tile):
		if self.check_bounds(pos):
			self.tiles[layer][pos[1]][pos[0]] = tile

	def remove_tile(self, layer: int, pos: tuple[int, int]):
		if self.check_bounds(pos):
			self.tiles[layer][pos[1]][pos[0]] = None

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
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject):
		if game_object is not None:
			game_object.removed()
			self.objects.remove(game_object)

	def draw_tile(self, layer: int, row: int, col: int, display: pygame.Surface, camera: pygbase.Camera):
		if self.check_bounds((col, row)):
			if self.tiles[layer][row][col] is not None:
				self.tiles[layer][row][col].draw(display, camera)

	def draw(self, screen: pygame.Surface, camera: pygbase.Camera, entities: dict[int, dict]):
		top_left: tuple[int, int] = get_tile_pos(camera.pos, (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.pos.x + SCREEN_WIDTH, camera.pos.y + SCREEN_HEIGHT), (TILE_SIZE, TILE_SIZE))

		top_left = top_left[0], top_left[1]
		bottom_right = bottom_right[0] + 1, bottom_right[1] + 2

		for layer in range(len(self.tiles)):
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(layer, row, col, screen, camera)

				if layer == 1:
					if row in entities:
						for entity in entities[row].values():
							entity.draw(screen, camera)

		for game_object in self.objects:
			game_object.draw(screen, camera)

	def draw_room_to_surface(self, surface: pygame.Surface):
		surface_size = surface.get_size()

		room_surface = pygame.Surface((self.n_cols * TILE_SIZE, self.n_rows * TILE_SIZE), flags=pygame.SRCALPHA)
		temp_camera = pygbase.Camera()

		for layer in range(len(self.tiles)):
			for row in range(self.n_rows):
				for col in range(self.n_cols):
					self.draw_tile(layer, row, col, room_surface, temp_camera)

		pygame.transform.scale(room_surface, surface_size, surface)
