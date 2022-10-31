import pygame

from data.modules.base.camera import Camera
from data.modules.base.room import Room
from data.modules.editor.shared_editor_state import SharedTileState


class EditorTool:
	def __init__(self, room: Room, editor_state: SharedTileState):
		self._room = room
		self._editor_state = editor_state

	def update(self, mouse_pos: tuple[int, int]):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, mouse_pos: tuple):
		pass
