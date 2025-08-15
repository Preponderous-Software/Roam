from src.entity.grass import Grass
from src.inventory import inventory


def createInventory():
    return inventory.Inventory()


def createGrassEntity():
    return Grass()


def test_initialization():
    inventoryInstance = createInventory()
    assert inventoryInstance.getNumInventorySlots() == 25
    assert inventoryInstance.getNumFreeInventorySlots() == 25
    assert inventoryInstance.getNumTakenInventorySlots() == 0


def test_placeIntoFirstAvailableInventorySlot():
    inventoryInstance = createInventory()
    item = createGrassEntity()
    inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    assert inventoryInstance.getNumFreeInventorySlots() == 24
    assert inventoryInstance.getNumTakenInventorySlots() == 1
    assert inventoryInstance.getNumItems() == 1
    assert inventoryInstance.getInventorySlots()[0].getContents() == [item]


def test_removeByItem():
    inventoryInstance = createInventory()
    item = createGrassEntity()
    inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    inventoryInstance.removeByItem(item)
    assert inventoryInstance.getNumFreeInventorySlots() == 25
    assert inventoryInstance.getNumTakenInventorySlots() == 0
    assert inventoryInstance.getNumItems() == 0
    assert inventoryInstance.getInventorySlots()[0].getContents() == []


def test_clear():
    inventoryInstance = createInventory()
    item = createGrassEntity()
    inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    inventoryInstance.clear()
    assert inventoryInstance.getNumFreeInventorySlots() == 25
    assert inventoryInstance.getNumTakenInventorySlots() == 0
    assert inventoryInstance.getNumItems() == 0
    assert inventoryInstance.getInventorySlots()[0].getContents() == []


def test_getNumFreeInventorySlots():
    inventoryInstance = createInventory()
    for i in range(5 * 20):
        item = createGrassEntity()
        inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    assert inventoryInstance.getNumFreeInventorySlots() == 20
    assert inventoryInstance.getNumTakenInventorySlots() == 5


def test_getNumTakenInventorySlots():
    inventoryInstance = createInventory()
    for i in range(5 * 20):
        item = createGrassEntity()
        inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    assert inventoryInstance.getNumTakenInventorySlots() == 5
    assert inventoryInstance.getNumFreeInventorySlots() == 20


def test_getNumItems():
    inventoryInstance = createInventory()
    for i in range(5):
        item = createGrassEntity()
        inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    assert inventoryInstance.getNumItems() == 5


def test_getNumItemsByType():
    inventoryInstance = createInventory()
    for i in range(5):
        item = createGrassEntity()
        inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    assert inventoryInstance.getNumItemsByType(Grass) == 5


def test_getSelectedInventorySlotIndex():
    inventoryInstance = createInventory()
    assert inventoryInstance.getSelectedInventorySlotIndex() == 0


def test_setSelectedInventorySlotIndex():
    inventoryInstance = createInventory()
    inventoryInstance.setSelectedInventorySlotIndex(5)
    assert inventoryInstance.getSelectedInventorySlotIndex() == 5


def test_getSelectedInventorySlot():
    inventoryInstance = createInventory()
    assert (
        inventoryInstance.getSelectedInventorySlot()
        == inventoryInstance.getInventorySlots()[0]
    )


def removeSelectedItem():
    inventoryInstance = createInventory()
    item = createGrassEntity()
    inventoryInstance.placeIntoFirstAvailableInventorySlot(item)
    inventoryInstance.removeSelectedItem()
    assert inventoryInstance.getNumFreeInventorySlots() == 25
    assert inventoryInstance.getNumTakenInventorySlots() == 0
    assert inventoryInstance.getNumItems() == 0
    assert inventoryInstance.getInventorySlots()[0].getContents() == []


def test_getFirstTenInventorySlots():
    inventoryInstance = createInventory()
    assert (
        inventoryInstance.getFirstTenInventorySlots()
        == inventoryInstance.getInventorySlots()[:10]
    )
