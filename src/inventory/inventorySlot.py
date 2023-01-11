class InventorySlot:
    def __init__(self):
        self.item = None
        self.amount = 0
    
    def getItem(self):
        return self.item

    def setItem(self, item):
        self.item = item
    
    def clear(self):
        self.item = None
        self.amount = 0
    
    def setAmount(self, amount):
        self.amount = amount
    
    def getAmount(self):
        return self.amount

    def addAmount(self, amount):
        self.amount += amount
    
    def subtractAmount(self, amount):
        self.amount -= amount
        if self.amount == 0:
            self.clear()
    
    def getMaxStackSize(self):
        return 20