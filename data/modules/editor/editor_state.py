from enum import Enum

from data.modules.editor.editor_actions import EditorAction, EditorActionBatch


class EditorModes(Enum):
	TileEditing = 0
	TileSelecting = 1
	ObjectEditing = 2
	ObjectSelecting = 3


class EditorState:
	def __init__(self, sprite_sheet_id: int):
		self.mode = EditorModes.TileEditing

		self.level = 0

		self.sprite_sheet_id = sprite_sheet_id
		self.ids: dict[int, dict[int, int]] = {0: {0: 0}}

		self.selected_topleft = (0, 0)
		self.selected_bottomright = (0, 0)

		self.action_index = -1
		self.editor_actions: list[EditorAction | EditorActionBatch] = []
		self.max_action_length = 20

	def add_action(self, action: EditorAction | EditorActionBatch):
		if self.action_index != len(self.editor_actions) - 1:
			for index in range(len(self.editor_actions) - self.action_index - 1):
				self.editor_actions.pop()

		self.editor_actions.append(action)
		self.action_index += 1

		if self.max_action_length < len(self.editor_actions):
			self.editor_actions.pop(0)
			self.action_index -= 1

	def undo_action(self):
		if 0 <= self.action_index:
			self.editor_actions[self.action_index].undo()
			self.action_index -= 1

	def redo_action(self):
		if self.action_index < len(self.editor_actions) - 1:
			self.action_index += 1
			self.editor_actions[self.action_index].execute()
