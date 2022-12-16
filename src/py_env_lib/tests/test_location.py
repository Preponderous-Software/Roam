from unittest.mock import MagicMock
from src.location import Location
from src.entity import Entity

# test initializing location
def test_initialization():
    location = Location(0, 0)
    assert location.id != None
    assert location.x == 0
    assert location.y == 0

# test getters
def test_getters():
    location = Location(0, 0)
    assert location.getID() != None
    assert location.getX() == 0
    assert location.getY() == 0

# test getting number of entities
def test_getNumEntities():
    location = Location(0, 0)
    assert location.getNumEntities() == 0

# test adding entity
def test_addEntity():
    Location.isEntityPresent = MagicMock(return_value=False)
    Entity.setLocationID = MagicMock()

    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert location.getNumEntities() == 1

    # test that isEntityPresent was called
    Location.isEntityPresent.assert_called_once_with(entity)

    # test that setLocationID was called
    Entity.setLocationID.assert_called_once_with(location.getID())

# test removing entity
def test_removeEntity():
    Location.isEntityPresent = MagicMock(return_value=False)
    Entity.setLocationID = MagicMock()

    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    
    Location.isEntityPresent = MagicMock(return_value=True)
    location.removeEntity(entity)
    assert location.getNumEntities() == 0

    # test that isEntityPresent was called
    Location.isEntityPresent.assert_called_once_with(entity)

    # test that setLocationID was called
    Entity.setLocationID.assert_called()

# test checking if entity is present
def test_isEntityPresent():
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert location.isEntityPresent(entity) == True
    
# test getting entities
def test_getEntities():
    Location.isEntityPresent = MagicMock(return_value=False)
    Entity.setLocationID = MagicMock()
    
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert location.getEntities() == [entity]