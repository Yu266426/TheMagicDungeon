from pygbase.ui.screen import ControlledScreen

from data.modules.base.constants import TILE_SIZE
from data.modules.base.room import EditorRoom


class SharedEditorState:
	def __init__(self, room: EditorRoom):
		# UI
		self.show_global_ui = True
		self.on_global_ui = False

		self.should_draw_tool = True

		# Room Screen
		self.controlled_screen = ControlledScreen(keep_in=(0, 0, room.n_cols * TILE_SIZE, room.n_rows * TILE_SIZE))
