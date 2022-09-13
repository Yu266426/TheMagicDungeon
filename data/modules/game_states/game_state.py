from abc import abstractmethod

import pygame


class GameState:
	@abstractmethod
	def next_state(self):
		pass

	@abstractmethod
	def update(self, delta: float):
		pass

	@abstractmethod
	def draw(self, display: pygame.Surface):
		pass
