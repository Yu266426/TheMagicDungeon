import json
import os
import random

import pygame
from pygbase import ResourceManager, SCREEN_WIDTH, SCREEN_HEIGHT
from pygbase.camera import Camera

from data.modules.base.constants import TILE_SIZE
from data.modules.base.files import LEVEL_DIR
from data.modules.base.utils import get_tile_pos, generate_3d_list
from data.modules.objects.game_object import GameObject, AnimatableObject
from data.modules.objects.objects import object_types
from data.modules.objects.tile import Tile


class Room:
	def __init__(self, name: str, n_rows: int = 10, n_cols: int = 10, offset: tuple = (0, 0), connections=(False, False, False, False), random_floor=True):
		self.n_rows = n_rows
		self.n_cols = n_cols

		self.offset = int(offset[0]), int(offset[1])
		self.tile_offset = get_tile_pos(self.offset, (TILE_SIZE, TILE_SIZE))

		# layer[back, player, front]
		self.tiles: list[list[list[Tile | None]]] = []
		self.objects: list[GameObject | AnimatableObject] = []

		# New room
		self.save_path = os.path.join(LEVEL_DIR, f"{name}.json")
		if not os.path.isfile(self.save_path):
			print("Creating new room")

			self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)
		else:
			self.load()

			if random_floor:
				self.generate_floor()
			self.generate_walls(connections)

	def generate_walls(self, connections, gap_radius: int = 1):
		"""
		Generates walls with gaps

		:param connections: Up, Down, Left, Right
		:param gap_radius: Size of gap
		"""

		wall_sheet = ResourceManager.get_resource(2, "walls")

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
		tiles_sheet = ResourceManager.get_resource(2, "tiles")
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self.tiles[0][row][col] = Tile(
					"tiles",
					random.randrange(0, tiles_sheet.length),
					(col * TILE_SIZE + self.offset[0], (row + 1) * TILE_SIZE + self.offset[1])
				)

	def load(self):
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
			object_type = game_object["type"]
			pos = game_object["pos"]
			self.objects.append(object_types[object_type]((pos[0] + self.offset[0], pos[1] + self.offset[1])))

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
				"type": type(game_object).__name__,
				"pos": [int(game_object.pos.x), int(game_object.pos.y)]
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

	def add_object(self, game_object: GameObject | AnimatableObject):
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject | AnimatableObject):
		if game_object is not None:
			self.objects.remove(game_object)

	def draw_tile(self, layer: int, row: int, col: int, display: pygame.Surface, camera: Camera, with_offset: bool = False):
		if with_offset:
			col -= int(self.offset[0] / TILE_SIZE)
			row -= int(self.offset[1] / TILE_SIZE)

		if self.check_bounds((col, row)):
			if self.tiles[layer][row][col] is not None:
				self.tiles[layer][row][col].draw(display, camera)

	def draw(self, screen: pygame.Surface, camera: Camera, entities: dict[int, dict]):
		top_left: tuple[int, int] = get_tile_pos((camera.target.x - self.offset[0], camera.target.y - self.offset[1]), (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.target.x + SCREEN_WIDTH - self.offset[0], camera.target.y + SCREEN_HEIGHT - self.offset[1]), (TILE_SIZE, TILE_SIZE))

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
	def __init__(self, name: str, n_rows: int = 10, n_cols: int = 10):
		self.n_rows = n_rows
		self.n_cols = n_cols

		# layer[back, player, front]
		self.tiles: list[list[list[Tile | None]]] = []
		self.objects: list[GameObject | AnimatableObject] = []

		# New room
		self.save_path = os.path.join(LEVEL_DIR, f"{name}.json")
		if not os.path.isfile(self.save_path):
			print("Creating new room")
			self.tiles = generate_3d_list(3, self.n_rows, self.n_cols)
		else:
			self.load()

	def load(self):
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
			object_type = game_object["type"]
			pos = game_object["pos"]
			self.objects.append(object_types[object_type](pos))

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
				"type": type(game_object).__name__,
				"pos": [int(game_object.pos.x), int(game_object.pos.y)]
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

	def add_object(self, game_object: GameObject | AnimatableObject):
		self.objects.append(game_object)

	def remove_object(self, game_object: GameObject | AnimatableObject):
		if game_object is not None:
			self.objects.remove(game_object)

	def draw_tile(self, layer: int, row: int, col: int, display: pygame.Surface, camera: Camera):
		if self.check_bounds((col, row)):
			if self.tiles[layer][row][col] is not None:
				self.tiles[layer][row][col].draw(display, camera)

	def draw(self, screen: pygame.Surface, camera: Camera, entities: dict[int, dict]):
		top_left: tuple[int, int] = get_tile_pos(camera.target, (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.target.x + SCREEN_WIDTH, camera.target.y + SCREEN_HEIGHT), (TILE_SIZE, TILE_SIZE))

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
