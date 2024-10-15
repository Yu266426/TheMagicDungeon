import pathlib

CURRENT_DIR = pathlib.Path.cwd()
DATA_DIR = CURRENT_DIR / "data"

ASSET_DIR = DATA_DIR / "assets"
IMAGE_DIR = ASSET_DIR / "images"
SPRITE_SHEET_DIR = ASSET_DIR / "sprite_sheets"

GAME_DATA_DIR = DATA_DIR / "game_data"

ROOM_DIR = GAME_DATA_DIR / "rooms"
OBJECT_DIR = GAME_DATA_DIR / "objects"
ENEMY_DIR = GAME_DATA_DIR / "enemies"

BATTLE_DIR = GAME_DATA_DIR / "battles"
