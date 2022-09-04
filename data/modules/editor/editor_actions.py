from data.modules.base.level import Room
from data.modules.objects.tile import Tile


class EditorAction:
	def execute(self):
		pass

	def undo(self):
		pass


class EditorActionBatch:
	def __init__(self):
		self.actions: list[EditorAction] = []

	def add_action(self, action: EditorAction):
		self.actions.append(action)

	def execute(self):
		for action in self.actions:
			action.execute()

	def undo(self):
		for action in self.actions[::-1]:
			action.undo()


class PlaceTileAction(EditorAction):
	def __init__(self, room: Room, level: int, row: int, col: int, tile: Tile):
		self._room = room

		self._level = level
		self._row = row
		self._col = col

		self._tile = tile

		self._prev_tile = None

	def execute(self):
		self._prev_tile = self._room.get_tile(self._level, (self._col, self._row))
		self._room.add_tile(self._level, (self._col, self._row), self._tile)

	def undo(self):
		self._room.remove_tile(self._level, (self._col, self._row))
		self._room.add_tile(self._level, (self._col, self._row), self._prev_tile)


class RemoveTileAction(EditorAction):
	def __init__(self, room: Room, level: int, row: int, col: int):
		self._room = room

		self._level = level
		self._row = row
		self._col = col

		self._prev_tile = None

	def execute(self):
		self._prev_tile = self._room.get_tile(self._level, (self._col, self._row))
		self._room.remove_tile(self._level, (self._col, self._row))

	def undo(self):
		self._room.add_tile(self._level, (self._col, self._row), self._prev_tile)