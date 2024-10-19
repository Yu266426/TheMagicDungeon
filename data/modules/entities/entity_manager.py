from data.modules.base.constants import TILE_SIZE
from data.modules.base.utils import get_1d_tile_pos
from data.modules.entities.entity import Entity


class EntityManager:
	def __init__(self):
		self.entities: list[Entity] = []
		self.sorted_entities: dict[int, list[Entity]] = {}
		self.tagged_entities: dict[str, list[Entity]] = {}

		self.entities_to_remove = set()

	def clear_entities(self):
		for entity in self.entities:
			self.entities_to_remove.add(entity)

		self._remove_entities()

	def add_entity(self, entity: "Entity", tags: tuple[str, ...] | None = None):
		self.entities.append(entity)
		entity.added()

		if tags is not None:
			entity.entity_tags += tags

		for tag in entity.entity_tags:
			self.tagged_entities.setdefault(tag, []).append(entity)

	def add_entity_to_remove(self, entity):
		self.entities_to_remove.add(entity)

	def get_entities_of_tag(self, tag: str) -> list[Entity]:
		if tag in self.tagged_entities:
			return self.tagged_entities[tag]

		return []

	def get_entities(self, y_pos: int) -> list[Entity]:
		if y_pos in self.sorted_entities:
			return [entity for entity in self.sorted_entities[y_pos]]

		return []

	def _remove_entities(self):
		self.sorted_entities.clear()

		entities_to_remove = self.entities_to_remove.copy()
		self.entities_to_remove.clear()

		for entity in entities_to_remove:
			self.entities.remove(entity)
			entity.removed()

			for tag in entity.tags:
				self.tagged_entities[tag].remove(entity)

				if len(self.tagged_entities[tag]) == 0:
					del self.tagged_entities[tag]

	def update(self, delta: float):
		self._remove_entities()

		for entity in self.entities:
			if not entity.is_alive():
				self.add_entity_to_remove(entity)

		for entity in self.entities:
			if entity.active:
				entity.update(delta)

			y_pos = get_1d_tile_pos(entity.pos.y, TILE_SIZE)

			if y_pos not in self.sorted_entities:
				self.sorted_entities[y_pos] = []

			self.sorted_entities[y_pos].append(entity)

		for row, entities in self.sorted_entities.items():
			entities.sort(key=lambda e: e.pos.y * 7 + e.pos.x)
