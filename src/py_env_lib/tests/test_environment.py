from unittest.mock import MagicMock
from src.environment import Environment
from src.grid import Grid
from src.entity import Entity
from src.location import Location

# test initializing environment
def test_initialization():
    environment = Environment("test", 10)
    assert environment.id != None
    assert environment.name == "test"
    assert environment.grid != None
    assert environment.creationDate != None

# test getters
def test_getters():
    environment = Environment("test", 10)
    assert environment.getID() != None
    assert environment.getName() == "test"
    assert environment.getGrid() != None
    assert environment.getCreationDate() != None

# test setters
def test_setters():
    environment = Environment("test", 10)
    environment.setID(1)
    assert environment.getID() == 1
    environment.setName("test2")
    assert environment.getName() == "test2"
    environment.setGrid(Grid(10, 10))
    assert environment.getGrid() != None