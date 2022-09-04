import pygame

from data.modules.base.camera import Camera
from data.modules.base.resources import ResourceManager, ResourceTypes


class Tile:
	def __init__(self, sprite_sheet_id: int, image_index: int, pos: tuple | pygame.Vector2):
		self.sprite_sheet_id = sprite_sheet_id
		self.image_index = image_index

		self.image: pygame.Surface = ResourceManager.get_resource(ResourceTypes.SPRITE_SHEET, sprite_sheet_id).get_image(image_index)
		self.rect: pygame.Rect = self.image.get_rect(bottomleft=pos)

	def draw(self, display: pygame.Surface, camera: Camera, flag: int = 0):
		display.blit(self.image, (self.rect.topleft - camera.target, self.rect.size), special_flags=flag)