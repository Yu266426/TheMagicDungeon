import enum
from abc import abstractmethod

import pygame

from data.modules.level.room import EditorRoom
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.shared_editor_state import SharedEditorState


class EditorStates(enum.Enum):
	TILE_DRAW_STATE = enum.auto()
	TILE_SELECTION_STATE = enum.auto()
	OBJECT_DRAW_STATE = enum.auto()
	OBJECT_SELECTION_STATE = enum.auto()


class EditorState:
	def __init__(self, room: EditorRoom, shared_state: SharedEditorState, action_queue: EditorActionQueue):
		self._room = room
		self._action_queue = action_queue
		self._shared_state = shared_state

	@abstractmethod
	def update(self, delta: float):
		pass

	@abstractmethod
	def draw(self, screen: pygame.Surface):
		pass

	@abstractmethod
	def next_state(self, mode_index: int):
		pass
