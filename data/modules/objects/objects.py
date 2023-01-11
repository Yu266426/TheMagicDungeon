from data.modules.objects.chest import Chest
from data.modules.objects.cube import SmallCube, SmallGreenCube, SmallRedCube, LargeCube, LargeGreenCube, LargeRedCube
from data.modules.objects.lever import Lever

object_types: dict = {}


def add_object_type(name: str, object_type):
	global object_types

	object_types[name] = object_type


add_object_type("SmallCube", SmallCube)
add_object_type("SmallGreenCube", SmallGreenCube)
add_object_type("SmallRedCube", SmallRedCube)
add_object_type("LargeCube", LargeCube)
add_object_type("LargeGreenCube", LargeGreenCube)
add_object_type("LargeRedCube", LargeRedCube)
add_object_type("Lever", Lever)
add_object_type("Chest", Chest)
