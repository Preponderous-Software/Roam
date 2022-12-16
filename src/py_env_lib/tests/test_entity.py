from unittest.mock import MagicMock
from src.entity import Entity

# test initializing entity
def test_initialization():
    entity = Entity("test")
    assert entity.id != None
    assert entity.name == "test"
    assert entity.creationDate != None
    assert entity.environmentID == -1
    assert entity.gridID == -1
    assert entity.locationID == -1

# test getters
def test_getters():
    entity = Entity("test")
    assert entity.getID() != None
    assert entity.getName() == "test"
    assert entity.getEnvironmentID() == -1
    assert entity.getCreationDate() != None
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

# test setters
def test_setters():
    entity = Entity("test")
    entity.setID(1)
    assert entity.getID() == 1
    entity.setName("test2")
    assert entity.getName() == "test2"
    entity.setEnvironmentID(2)
    assert entity.getEnvironmentID() == 2
    entity.setCreationDate("test3")
    assert entity.getCreationDate() == "test3"
    entity.setGridID(3)
    assert entity.getGridID() == 3
    entity.setLocationID(4)
    assert entity.getLocationID() == 4

# test printing info
def test_printInfo():
    entity = Entity("test")
    entity.printInfo = MagicMock()
    entity.printInfo()
    entity.printInfo.assert_called_once_with()