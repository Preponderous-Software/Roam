class InventorySlot:
    def __init__(self):
        self.item = None
    
    def getItem(self):
        return self.item

    def setItem(self, item):
        self.item = item