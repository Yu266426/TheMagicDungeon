import os
from typing import Optional

import pygame
import pygbase

from data.modules.base.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data.modules.base.paths import ROOM_DIR
from data.modules.game_states.editor import Editor
from data.modules.map.room import EditorRoom


class EditorRoomSelection(pygbase.GameState, name="editor_room_select"):
	def __init__(self):
		super().__init__()

		self.ui = pygbase.UIManager()
		self.rooms_frame = self.ui.add_frame(pygbase.VerticalScrollingFrame(
			(pygbase.UIValue(0.02, False), pygbase.UIValue(0.02, False)),
			(pygbase.UIValue(0.48, False), pygbase.UIValue(0.80, False)),
			5,
			bg_colour=(50, 50, 50, 100)
		))

		self.rooms = os.listdir(ROOM_DIR)

		# Generate Room Buttons
		if len(self.rooms) > 0:
			# First one
			self.rooms_frame.add_element(pygbase.Button(
				(pygbase.UIValue(0), pygbase.UIValue(0)),
				(pygbase.UIValue(1, False), pygbase.UIValue(0)),
				"image", "button",
				self.rooms_frame,
				self.select_room,
				callback_args=(0, self.rooms[0][:-5]),
				text=self.rooms[0][:-5]
			))

			# Rest of the rooms
			for index, room in enumerate(self.rooms[1:]):
				room_name = room[:-5]

				self.rooms_frame.add_element(pygbase.Button(
					(pygbase.UIValue(0), pygbase.UIValue(10)),
					(pygbase.UIValue(1, False), pygbase.UIValue(0)),
					"image", "button",
					self.rooms_frame,
					self.select_room,
					callback_args=(index + 1, room_name),
					text=room_name
				), align_with_previous=(True, False), add_on_to_previous=(False, True))

		self.selected_room: Optional[EditorRoom] = None
		self.selected_room_image = pygame.Surface((SCREEN_WIDTH * 0.46, SCREEN_HEIGHT * 0.46), flags=pygame.SRCALPHA)
		self.selected_room_image.fill((20, 20, 20))

		self.particle_manager = pygbase.ParticleManager()

		# Buttons
		from data.modules.game_states.main_menu import MainMenu
		self.ui.add_element(pygbase.Button(
			(pygbase.UIValue(0.02, False), pygbase.UIValue(0.84, False)),
			(pygbase.UIValue(0), pygbase.UIValue(0.14, False)),
			"image", "home_button",
			self.ui.base_container,
			self.set_next_state_type,
			callback_args=(MainMenu, ())
		))

		self.ui.add_element(pygbase.Button(
			(pygbase.UIValue(0.02, False), pygbase.UIValue(0.84, False)),
			(pygbase.UIValue(0.32, False), pygbase.UIValue(0.14, False)),
			"image", "button",
			self.ui.base_container,
			self.edit_button_callback,
			text="Edit"
		), add_on_to_previous=(True, False))

		# Room Info
		self.info_frame = self.ui.add_frame(pygbase.Frame(
			(pygbase.UIValue(0.52, False), pygbase.UIValue(0.50, False)),
			(pygbase.UIValue(0.46, False), pygbase.UIValue(0.48, False)),
			bg_colour=(50, 50, 50, 100)
		))

		self.room_name_text = self.info_frame.add_element(pygbase.TextElement(
			(pygbase.UIValue(0.04, False), pygbase.UIValue(0.04, False)),
			"arial black", pygbase.UIValue(35),
			"white",
			"Name: N/A",
			self.info_frame
		))

		self.size_text = self.info_frame.add_element(pygbase.TextElement(
			(pygbase.UIValue(0.04, False), pygbase.UIValue(0.04, False)),
			"arial black", pygbase.UIValue(35),
			"white",
			"Size: N/A",
			self.info_frame
		), add_on_to_previous=(False, True))

	def select_room(self, index, room_name):
		self.selected_room = EditorRoom(room_name, self.particle_manager)
		self.selected_room.draw_room_to_surface(self.selected_room_image)

		self.room_name_text.set_text(f"Name: {room_name}")
		self.size_text.set_text(f"Size: ({self.selected_room.n_cols} , {self.selected_room.n_rows})")

	def edit_button_callback(self):
		if self.selected_room is not None:
			self.set_next_state(Editor(self.selected_room, self.particle_manager))

	def update(self, delta: float):
		self.ui.update(delta)

		if pygbase.InputManager.get_key_just_pressed(pygame.K_ESCAPE):
			pygbase.EventManager.post_event(pygame.QUIT)

	def draw(self, screen: pygame.Surface):
		screen.fill((30, 30, 30))
		self.ui.draw(screen)

		screen.blit(self.selected_room_image, (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * 0.02))
