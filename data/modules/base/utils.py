import pygame


def get_tile_pos(pos: tuple | pygame.Vector2, tile_size: tuple[int | float, int | float]):
	return int(pos[0] // tile_size[0]), int(pos[1] // tile_size[1])


def get_1d_pos(pos: int | float, tile_size: int | float):
	return int(pos // tile_size)


def generate_3d_list(levels: int, n_rows: int, n_cols: int, fill_data=None):
	data = []

	for _ in range(levels):
		rows = []
		for __ in range(n_rows):
			col = []
			for ___ in range(n_cols):
				col.append(fill_data)
			rows.append(col)

		data.append(rows)

	return data


def generate_2d_list(n_rows: int, n_cols: int, fill: bool = False):
	data = []
	for _ in range(n_rows):
		col = []
		if fill:
			for __ in range(n_cols):
				col.append(None)
		data.append(col)
	return data


def abs_tuple(tup1: tuple[int, int], tup2: tuple[int, int]):
	new_tup1 = min(tup1[0], tup2[0]), min(tup1[1], tup2[1])
	new_tup2 = max(tup1[0], tup2[0]), max(tup1[1], tup2[1])

	return new_tup1, new_tup2


def draw_rect_outline(display: pygame.Surface, colour, pos: tuple[int | float, int | float] | pygame.Vector2, size: tuple[int | float, int | float] | pygame.Vector2, width: int):
	pygame.draw.rect(
		display, colour,
		(pos, size),
		width=width
	)
