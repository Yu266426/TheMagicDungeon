import pygame

from data.modules.base.camera import Camera
from data.modules.base.resources import ResourceManager, ResourceTypes
from data.modules.graphics.animation import Animation


class GameObject:
	def __init__(self, pos: tuple, sprite_sheet_id: int, image_id: int, custom_hitbox: pygame.Rect | None = None):
		self.pos = pygame.Vector2(pos)
		self.image = ResourceManager.get_resource(ResourceTypes.SPRITE_SHEET, sprite_sheet_id).get_image(image_id)
		self.rect = self.image.get_rect(midbottom=self.pos)

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface, camera: Camera):
		display.blit(self.image, self.pos - camera.target)


class AnimatableObject(Animation):
	def __init__(self, pos: tuple, sprite_sheet_id: int, anim_start_index: int, length: int, looping: bool = True, custom_hitbox: pygame.Rect | None = None):
		super().__init__(pos, sprite_sheet_id, anim_start_index, length, looping)
		self.rect = self.images[0].get_rect(midbottom=self.pos).copy()

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def update(self, delta: float):  # Draw method in Animation
		pass
