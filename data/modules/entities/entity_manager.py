from data.modules.base.constants import TILE_SIZE
from data.modules.base.utils import get_1d_pos


class EntityManager:
	def __init__(self):
		from data.modules.entities.entity import Entity
		self.entities: list[Entity] = []
		self.sorted_entities: dict[int, list[Entity]] = {}
		self.tagged_entities: dict[str, list[Entity]] = {}

	def add_entity(self, entity, tags: list[str] = None):
		entity_tags = [] if tags is None else tags

		self.entities.append(entity)

		for tag in entity_tags:
			if tag not in self.tagged_entities:
				self.tagged_entities[tag] = []

			self.tagged_entities[tag].append(entity)

	def get_entities_of_tag(self, tag: str):
		if tag in self.tagged_entities:
			return self.tagged_entities[tag]
		else:
			return []

	def update(self, delta: float):
		self.sorted_entities.clear()

		for entity in self.entities:
			if not entity.is_alive():
				self.entities.remove(entity)

		for tag, entities in self.tagged_entities.items():
			for entity in entities:
				if not entity.is_alive():
					entities.remove(entity)

		for entity in self.entities:
			entity.update(delta)
			if not entity.is_alive():
				self.entities.remove(entity)
				continue

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
