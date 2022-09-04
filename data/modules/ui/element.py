import pygame

from data.modules.base.inputs import InputManager
from data.modules.base.resources import ResourceManager, ResourceTypes
from data.modules.ui.text import Text


class UIElement:
	def __init__(self, pos: tuple, size: tuple):
		self.pos = pos
		self.size = size

		self.rect = pygame.Rect(pos, size) if pos[1] is not None else None

	def update(self, delta: float):
		pass

	def draw(self, display: pygame.Surface):
		pass


class Frame(UIElement):
	def __init__(self, pos: tuple, size: tuple, bg_colour=None):
		super().__init__(pos, size)

		self.bg = None
		if bg_colour is not None:
			self.bg = pygame.Surface(self.size).convert_alpha()
			self.bg.fill(bg_colour)

		self.elements: list[UIElement] = []

	def add_element(self, element: UIElement, align_with_previous: tuple = (False, False), add_on_to_previous: tuple = (False, False)) -> "Frame":
		# Align
		if align_with_previous[0]:
			element.pos = self.elements[-1].pos[0], element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		if align_with_previous[1]:
			element.pos = element.pos[0], self.elements[-1].pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		# Add on
		if add_on_to_previous[0]:
			element.pos = self.elements[-1].pos[0] + self.elements[-1].size[0] + element.pos[0], element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		if add_on_to_previous[1]:
			element.pos = element.pos[0], self.elements[-1].pos[1] + self.elements[-1].size[1] + element.pos[1]
			element.rect = pygame.Rect(element.pos, element.size)

		# If element does not go out of frame, add it to the frame
		if 0 <= element.pos[0] and element.pos[0] + element.size[0] <= self.size[0]:
			if 0 <= element.pos[1] and element.pos[1] + element.size[1] <= self.size[1]:
				# Offset the rect to frame space
				element.rect.x += self.rect.x
				element.rect.y += self.rect.y

				if isinstance(element, Frame):
					for f_element in element.elements:
						f_element.rect.x += element.rect.x
						f_element.rect.y += element.rect.y

				self.elements.append(element)
		else:
			print(f"WARNING: Element of type: `{type(element).__name__}` too large to fit in frame.")

		return self

	def update(self, delta: float):
		for element in self.elements:
			element.update(delta)

	def draw(self, display: pygame.Surface):
		if self.bg is not None:
			display.blit(self.bg, self.rect)

		for element in self.elements:
			element.draw(display)


class Button(UIElement):
	def __init__(self, pos: tuple, image_id: int, callback, *callback_args, size: tuple | None = None, center: str = "l"):
		self.image: pygame.Surface = ResourceManager.get_resource(ResourceTypes.IMAGE, image_id)

		if size is not None:
			if size[0] is None:
				self.image = pygame.transform.scale(self.image, (self.image.get_width() * size[1] / self.image.get_height(), size[1]))
			elif size[1] is None:
				self.image = pygame.transform.scale(self.image, (size[0], self.image.get_height() * size[0] / self.image.get_width()))
			else:
				self.image = pygame.transform.scale(self.image, size)

		if center == "l":
			super().__init__(pos, (self.image.get_width(), self.image.get_height()))
		elif center == "r":
			super().__init__((pos[0] - self.image.get_width(), pos[1]), (self.image.get_width(), self.image.get_height()))
		else:
			raise ValueError(f"center: `{center}` on {self.__class__.__name__} is not valid")

		self.callback = callback
		self.callback_args = callback_args

		self.mouse_on = False
		self.highlight = pygame.Surface(self.image.get_size()).convert_alpha()
		self.highlight.fill((255, 255, 255, 40))

	def update(self, delta: float):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.mouse_on = True

			if InputManager.mouse_down[0]:
				if self.callback is not None:
					self.callback(*self.callback_args)
		else:
			self.mouse_on = False

	def draw(self, display: pygame.Surface):
		display.blit(self.image, self.rect)

		if self.mouse_on:
			display.blit(self.highlight, self.rect)


class TextElement(UIElement):
	def __init__(self, pos: tuple, height: int | float, font_name: str, colour, text: str, centered=False, use_sys=True):
		super().__init__(pos, (0, height))

		self.text = Text(pos, font_name, height * 1.25, colour, text, use_sys=use_sys)

		self.centered = centered

	def set_text(self, new_text: str):
		self.text.set_text(new_text)
		self.text.render_text()

	def draw(self, display: pygame.Surface):
		render_surface = pygame.Surface(self.text.rendered_text[1].size).convert_alpha()
		render_surface.fill((0, 0, 0, 0))
		self.text.draw(render_surface, pos_based=False)
		self.rect.width = render_surface.get_width()

		offset = 0
		if self.centered:
			offset = self.rect.width / 2
		display.blit(render_surface, (self.rect.x - offset, self.rect.y))


class TextSelector(Frame):
	def __init__(self, pos: tuple, size: tuple, options: list):
		super().__init__(pos, size, bg_colour=(0, 0, 0, 150))

		self.options = options

		self.index = 0
		self.current_option = self.options[self.index]

		self.add_element(Button((0, 0), 0, self.change_option, -1, size=(None, self.rect.height)))
		self.add_element(Button((self.rect.width, 0), 0, self.change_option, 1, size=(None, self.rect.height), center="r"))

		self.text = TextElement((self.rect.width / 2, self.rect.height * 0.3 / 2), self.rect.height * 0.7, "arial", (255, 255, 255), self.current_option, centered=True)
		self.add_element(self.text)

	def change_option(self, direction):
		self.index += direction

		if self.index < 0:
			self.index = len(self.options) - 1
		elif len(self.options) <= self.index:
			self.index = 0

		self.current_option = self.options[self.index]

		self.text.set_text(self.current_option)
