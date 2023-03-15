import pygame
from pygbase import ResourceManager
from pygbase import Camera
from pygbase.graphics.animation import Animation


class GameObject:
	def __init__(self, pos: tuple, sprite_sheet_id: int, image_id: int, custom_hitbox: pygame.Rect | None = None):
		self.pos = pygame.Vector2(pos)
		self.image = ResourceManager.get_resource(2, sprite_sheet_id).get_image(image_id)
		self.rect = self.image.get_rect(midbottom=self.pos)

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface, camera: Camera, flag=0):
		display.blit(self.image, self.pos - camera.target, special_flags=flag)


class AnimatableObject(Animation):
	def __init__(self, pos: tuple, sprite_sheet_name: str, anim_start_index: int, anim_length: int, looping: bool = True, custom_hitbox: pygame.Rect | None = None):
		super().__init__(sprite_sheet_name, anim_start_index, anim_length, looping)
		self.pos = pygame.Vector2(pos)
		self.rect = self.images[0].get_image().get_rect(midbottom=self.pos).copy()

		if custom_hitbox is None:
			self.hitbox = self.rect.copy()
		else:
			self.hitbox: pygame.Rect = custom_hitbox
			self.hitbox.midbottom = self.pos

	def update(self, delta: float):  # Draw method in Animation
		pass

	def draw(self, display: pygame.Surface, camera: Camera, flag=0):
		self.draw_at_pos(display, self.pos, camera, flag)
