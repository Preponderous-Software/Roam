# @author Daniel McCoy Stephenson
from inventory.inventorySlot import InventorySlot


class Inventory:
    def __init__(self):
        self.inventorySlots = []
        self.size = 25
        for i in range(self.size):
            self.inventorySlots.append(InventorySlot())
        self.selectedInventorySlotIndex = 0
    
    def getInventorySlots(self):
        return self.inventorySlots
    
    def getNumInventorySlots(self):
        return len(self.inventorySlots)
    
    def placeIntoFirstAvailableInventorySlot(self, item):
        for inventorySlot in self.inventorySlots:
            if inventorySlot.getItem() == None:
                # set the item
                inventorySlot.setItem(item)
                inventorySlot.setAmount(1)
                return True
            elif inventorySlot.getItem().getName() == item.getName() and inventorySlot.getAmount() < inventorySlot.getMaxStackSize():
                # increment the amount
                inventorySlot.addAmount(1)
                return True
        return False
    
    def removeByItem(self, item):
        for inventorySlot in self.inventorySlots:
            if inventorySlot.getItem() == item:
                if inventorySlot.getAmount() > 1:
                    inventorySlot.subtractAmount(1)
                else:
                    inventorySlot.clear()
                return True
        return False
    
    def clear(self):
        for inventorySlot in self.inventorySlots:
            inventorySlot.clear()
            
    def getNumFreeInventorySlots(self):
        count = 0
        for inventorySlot in self.inventorySlots:
            if inventorySlot.getItem() == None:
                count += 1
        return count
    
    def getNumTakenInventorySlots(self):
        count = 0
        for inventorySlot in self.inventorySlots:
            if inventorySlot.getItem() != None:
                count += 1
        return count
    
    def getNumItemsByType(self, type):
        count = 0
        for inventorySlot in self.inventorySlots:
            item = inventorySlot.getItem()
            if isinstance(item, type):
                count += inventorySlot.getAmount()
        return count
    
    def getSelectedInventorySlotIndex(self):
        return self.selectedInventorySlotIndex
    
    def setSelectedInventorySlotIndex(self, index):
        self.selectedInventorySlotIndex = index
            
    def getItemByIndex(self, index):
        return self.inventorySlots[index].getItem()
    
    def getSelectedInventorySlot(self):
        return self.inventorySlots[self.selectedInventorySlotIndex]
    
    def removeSelectedItem(self):
        self.inventorySlots[self.selectedInventorySlotIndex].subtractAmount(1)
        
    def getFirstTenInventorySlots(self):
        if len(self.inventorySlots) > 10:
            return self.inventorySlots[:10]
        else:
            return self.inventorySlots
