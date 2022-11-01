from abc import abstractmethod

import pygame


class EditorState:
	@abstractmethod
	def update(self, delta: float):
		pass

	@abstractmethod
	def draw(self, display: pygame.Surface):
		pass

	@abstractmethod
	def next_state(self):
		pass
