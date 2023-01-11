from abc import abstractmethod

import pygame

from data.modules.base.camera import Camera
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.editor_selection_info import TileSelectionInfo, ObjectSelectionInfo
from data.modules.editor.shared_editor_state import SharedEditorState


class EditorTool:
	def __init__(self, room: Room, shared_state: SharedEditorState, action_queue: EditorActionQueue):
		self._room = room
		self._shared_state = shared_state
		self._action_queue = action_queue

	@abstractmethod
	def update(self, mouse_pos: tuple[int, int], selection_info: TileSelectionInfo | ObjectSelectionInfo):
		pass

	@abstractmethod
	def draw(self, screen: pygame.Surface, camera: Camera, mouse_pos: tuple, selection_info: TileSelectionInfo | ObjectSelectionInfo):
		pass
