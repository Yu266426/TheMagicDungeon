from data.modules.base.constants import TILE_SIZE
from data.modules.base.utils import get_1d_pos


class EntityManager:
	def __init__(self):
		from data.modules.entities.entity import Entity
		self.entities: list[Entity] = []
		self.sorted_entities: dict[int, list] = {}

	def add_entity(self, entity):
		self.entities.append(entity)

	def update(self, delta: float):
		self.sorted_entities.clear()

		for entity in self.entities:
			entity.update(delta)

			y_pos = get_1d_pos(entity.pos.y, TILE_SIZE)

			if y_pos not in self.sorted_entities:
				self.sorted_entities[y_pos] = []

			self.sorted_entities[y_pos].append(entity)

	def get_entities(self, y_pos: int):
		entities = []
		if y_pos in self.sorted_entities:
			for entity in self.sorted_entities[y_pos]:
				entities.append(entity)

		return entities
