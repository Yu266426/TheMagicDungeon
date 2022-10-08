from data.modules.base.constants import TILE_SIZE
from data.modules.base.utils import get_1d_pos, generate_2d_list


class EntityManager:
	def __init__(self):
		from data.modules.entities.entity import Entity
		self.entities: list[Entity] = []
		self.sorted_entities: dict[int, dict[int, list]] = {}

	def add_entity(self, entity):
		self.entities.append(entity)

	def update(self, delta: float):
		self.sorted_entities.clear()

		for entity in self.entities:
			entity.update(delta)

			x_pos = get_1d_pos(entity.pos.x, TILE_SIZE)
			y_pos = get_1d_pos(entity.pos.y, TILE_SIZE)

			if y_pos not in self.sorted_entities:
				self.sorted_entities[y_pos] = {}
			if x_pos not in self.sorted_entities[y_pos]:
				self.sorted_entities[y_pos][x_pos] = []

			self.sorted_entities[y_pos][x_pos].append(entity)

	def get_entities(self, x_pos: int, y_pos: int, size: tuple[int, int] = (1, 1)):
		entities = {}
		for y in range(y_pos, y_pos + size[1]):
			if y in self.sorted_entities:

				for x in range(x_pos, x_pos + size[0]):
					if x in self.sorted_entities[y]:

						for entity in self.sorted_entities[y][x]:
							if y not in entities:
								entities[y] = {}
							entities[y][x] = entity

		return entities
