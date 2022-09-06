import json
import os

import pygame

from data.modules.base.camera import Camera
from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from data.modules.base.files import LEVEL_DIR
from data.modules.base.utils import get_tile_pos, generate_level_list
from data.modules.objects.game_object import GameObject, AnimatableObject
from data.modules.objects.objects import object_types
from data.modules.objects.tile import Tile


class Room:
	def __init__(self, name: str, n_rows: int = 10, n_cols: int = 10, pos: tuple = (0, 0)):
		self.n_rows = n_rows
		self.n_cols = n_cols

		self.pos = pos

		# level[back, same, front]
		self.tiles: list[list[list[Tile | None]]] = []
		self.objects: list[GameObject | AnimatableObject] = []

		# New level
		self.save_path = os.path.join(LEVEL_DIR, f"{name}.json")
		if not os.path.isfile(self.save_path):
			self.tiles = generate_level_list(3, self.n_rows, self.n_cols)

		else:
			self.load()

	def load(self):
		with open(self.save_path) as file:
			room_data: dict = json.load(file)

		self.n_rows = room_data["rows"]
		self.n_cols = room_data["cols"]

		self.tiles = generate_level_list(3, self.n_rows, self.n_cols)

		for level, tiles in enumerate(room_data["tiles"]):
			for tile in tiles:
				row = tile["pos"][0]
				col = tile["pos"][1]
				self.tiles[level][row][col] = Tile(tile["image_info"][0], tile["image_info"][1], ((col + self.pos[0]) * TILE_SIZE, ((row + self.pos[1]) + 1) * TILE_SIZE))

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
							"image_info": [tile.sprite_sheet_id, tile.image_index],
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

	def get_tile(self, level: int, pos: tuple[int, int]):
		pos = pos[0] - self.pos[0], pos[1] - self.pos[1]

		if 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows:
			return self.tiles[level][pos[1]][pos[0]]

	def add_tile(self, level: int, pos: tuple[int, int], tile: Tile):
		pos = pos[0] - self.pos[0], pos[1] - self.pos[1]

		if 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows:
			self.tiles[level][pos[1]][pos[0]] = tile

	def remove_tile(self, level: int, pos: tuple[int, int]):
		pos = pos[0] - self.pos[0], pos[1] - self.pos[1]

		if 0 <= pos[0] < self.n_cols and 0 <= pos[1] < self.n_rows:
			self.tiles[level][pos[1]][pos[0]] = None

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

	def draw_tile(self, level: int, row: int, col: int, display: pygame.Surface, camera: Camera):
		if 0 <= row < self.n_cols and 0 <= col < self.n_rows:
			if self.tiles[level][row][col] is not None:
				self.tiles[level][row][col].draw(display, camera)

	def draw(self, display: pygame.Surface, camera: Camera):
		top_left: tuple[int, int] = get_tile_pos((camera.target.x, camera.target.y), (TILE_SIZE, TILE_SIZE))
		bottom_right: tuple[int, int] = get_tile_pos((camera.target.x + SCREEN_WIDTH, camera.target.y + SCREEN_HEIGHT), (TILE_SIZE, TILE_SIZE))

		top_left = top_left[0] - self.pos[0], top_left[1] - self.pos[1]
		bottom_right = bottom_right[0] - self.pos[0] + 1, bottom_right[1] - self.pos[1] + 2

		for level in range(len(self.tiles)):
			for row in range(top_left[1], bottom_right[1]):
				for col in range(top_left[0], bottom_right[0]):
					self.draw_tile(level, row, col, display, camera)

		for game_object in self.objects:
			game_object.draw(display, camera)
