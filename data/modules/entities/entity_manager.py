from data.modules.base.constants import TILE_SIZE
from data.modules.base.utils import get_1d_tile_pos


class EntityManager:
	def __init__(self):
		from data.modules.entities.entity import Entity
		self.entities: list[Entity] = []
		self.entity_tags: dict[Entity, set[str]] = {}
		self.sorted_entities: dict[int, list[Entity]] = {}
		self.tagged_entities: dict[str, list[Entity]] = {}

		self.entities_to_remove = set()

	def add_entity(self, entity, tags: tuple[str] = None):
		entity_tags = () if tags is None else tags

		self.entities.append(entity)
		self.entity_tags[entity] = set()

		for tag in entity_tags:
			self.entity_tags[entity].add(tag)

		for tag in entity_tags:
			if tag not in self.tagged_entities:
				self.tagged_entities[tag] = []

			self.tagged_entities[tag].append(entity)

	def add_entity_to_remove(self, entity):
		self.entities_to_remove.add(entity)

	def get_entities_of_tag(self, tag: str):
		if tag in self.tagged_entities:
			return self.tagged_entities[tag]
		else:
			return []

	def get_entities(self, y_pos: int):
		entities = []
		if y_pos in self.sorted_entities:
			for entity in self.sorted_entities[y_pos]:
				entities.append(entity)

		return entities

	def remove_entities(self):
		self.sorted_entities.clear()

		for entity in self.entities_to_remove:
			self.entities.remove(entity)

			for tag in self.entity_tags[entity]:
				self.tagged_entities[tag].remove(entity)

		self.entities_to_remove.clear()

	def update(self, delta: float):
		self.remove_entities()

		for entity in self.entities:
			if not entity.is_alive():
				self.add_entity_to_remove(entity)

		for entity in self.entities:
			entity.update(delta)

			y_pos = get_1d_tile_pos(entity.pos.y, TILE_SIZE)

			if y_pos not in self.sorted_entities:
				self.sorted_entities[y_pos] = []

			self.sorted_entities[y_pos].append(entity)

		for row, entities in self.sorted_entities.items():
			entities.sort(key=lambda e: e.pos.y * 7 + e.pos.x)
