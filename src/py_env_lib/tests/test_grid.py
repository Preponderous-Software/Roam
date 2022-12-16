from unittest.mock import MagicMock
from src.grid import Grid
from src.location import Location
from src.entity import Entity

# test initializing grid
def test_initialization():    
    grid = Grid(10, 10)
    assert grid.id != None
    assert grid.columns == 10
    assert grid.rows == 10
    assert grid.locations != None
    assert grid.getSize() == 100

# test getters
def test_getters():    
    grid = Grid(10, 10)
    assert grid.getID() != None
    assert grid.getColumns() == 10
    assert grid.getRows() == 10
    assert grid.getLocations() != None
    assert grid.getSize() == 100

# test setters
def test_setters():
    grid = Grid(10, 10)
    grid.setID(1)
    assert grid.getID() == 1
    grid.setColumns(5)
    assert grid.getColumns() == 5
    grid.setRows(5)
    assert grid.getRows() == 5
    grid.setLocations([])
    assert grid.getLocations() == []
    
# def adding an entity to a specific location
def test_adding_an_entity_to_a_specific_location():
    grid = Grid(10, 10)
    entity = Entity("test")
    location = Location(1, 1)
    grid.addLocation(location)
    grid.addEntityToLocation(entity, location)
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1
    assert location.getEntities()[0] == entity