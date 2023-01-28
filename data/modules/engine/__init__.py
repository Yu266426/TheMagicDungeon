from .events import EventManager
from .inputs import InputManager


def init():
	EventManager.init()
	InputManager.register_handlers()
