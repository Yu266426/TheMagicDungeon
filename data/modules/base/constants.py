from enum import Enum

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 800

TILE_SIZE: float = SCREEN_WIDTH / 8
TILE_SCALE: float = TILE_SIZE / 16


class GameStates(Enum):
	LOADING = 1
	START = 2
	GAME = 3
	EDITOR = 4
	END = 5
