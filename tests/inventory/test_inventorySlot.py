from src.inventory import inventorySlot
from src.entity.grass import Grass


def createInventorySlot():
    return inventorySlot.InventorySlot()


def createItem():
    return Grass()


def test_initialization():
    inventorySlotInstance = createInventorySlot()
    assert inventorySlotInstance.getContents() == []
    assert inventorySlotInstance.getNumItems() == 0
    assert inventorySlotInstance.isEmpty() == True
    assert inventorySlotInstance.getMaxStackSize() == 20


def test_add():
    inventorySlotInstance = createInventorySlot()
    itemToAdd = createItem()
    inventorySlotInstance.add(itemToAdd)
    assert inventorySlotInstance.getContents() == [itemToAdd]
    assert inventorySlotInstance.getNumItems() == 1
    assert inventorySlotInstance.isEmpty() == False


def test_remove():
    inventorySlotInstance = createInventorySlot()
    itemToRemove = createItem()
    inventorySlotInstance.add(itemToRemove)
    inventorySlotInstance.remove(itemToRemove)
    assert inventorySlotInstance.getContents() == []
    assert inventorySlotInstance.getNumItems() == 0
    assert inventorySlotInstance.isEmpty() == True


def test_pop():
    inventorySlotInstance = createInventorySlot()
    itemToPop = createItem()
    inventorySlotInstance.add(itemToPop)
    assert inventorySlotInstance.pop() == itemToPop
    assert inventorySlotInstance.getContents() == []
    assert inventorySlotInstance.getNumItems() == 0
    assert inventorySlotInstance.isEmpty() == True


def test_clear():
    inventorySlotInstance = createInventorySlot()
    item = createItem()
    inventorySlotInstance.add(item)
    inventorySlotInstance.clear()
    assert inventorySlotInstance.getContents() == []
    assert inventorySlotInstance.getNumItems() == 0
    assert inventorySlotInstance.isEmpty() == True


def test_setContents():
    inventorySlotInstance = createInventorySlot()
    item1 = createItem()
    item2 = createItem()
    inventorySlotInstance.setContents([item1, item2])
    assert inventorySlotInstance.getContents() == [item1, item2]
    assert inventorySlotInstance.getNumItems() == 2
    assert inventorySlotInstance.isEmpty() == False


def test_getMaxStackSize():
    inventorySlotInstance = createInventorySlot()
    assert inventorySlotInstance.getMaxStackSize() == 20
