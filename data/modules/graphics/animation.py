import pygame

from data.modules.base.camera import Camera
from data.modules.base.resources import ResourceManager, ResourceTypes


class Animation:
	def __init__(self, pos: tuple, sprite_sheet_id: int, anim_start_index: int, length: int, looping=True):
		self.pos = pygame.Vector2(pos)

		self.sprite_sheet_id = sprite_sheet_id
		self.anim_start_index = anim_start_index
		self.length = length

		self.looping = looping

		self.frame = 0.0
		self.images: list[pygame.Surface] = []

		self._load_animation()

	def _load_animation(self):
		for index in range(self.anim_start_index, self.anim_start_index + self.length + 1):
			self.images.append(ResourceManager.get_resource(ResourceTypes.SPRITE_SHEET, self.sprite_sheet_id).get_image(index))

	def change_frame(self, amount: float):
		self.frame += amount

		if self.frame >= self.length:
			if self.looping:
				self.frame = 0
			else:
				self.frame = self.length - 0.01
		if self.frame < 0:
			if self.looping:
				self.frame = self.length - 0.01
			else:
				self.frame = 0

	def draw(self, display: pygame.Surface, camera: Camera):
		display.blit(self.images[int(self.frame)], self.pos - camera.target)
