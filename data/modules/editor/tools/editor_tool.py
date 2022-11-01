import pygame

from data.modules.base.camera import Camera
from data.modules.base.room import Room
from data.modules.editor.actions.editor_actions import EditorActionQueue
from data.modules.editor.shared_editor_state import SharedTileState


class EditorTool:
	def __init__(self, room: Room, editor_state: SharedTileState, action_queue: EditorActionQueue):
		self._room = room
		self._editor_state = editor_state
		self._action_queue = action_queue

	def update(self, mouse_pos: tuple[int, int]):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		pass
