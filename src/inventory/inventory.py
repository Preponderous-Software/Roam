# @author Daniel McCoy Stephenson
class Inventory:
    def __init__(self):
        self.contents = []
        self.size = 100
        self.selectedItem = None
        
    def getContents(self):
        return self.contents
    
    def place(self, item):
        if len(self.contents) < self.size:
            self.contents.append(item)
            self.selectedItem = item
        else:
            return -1
    
    def remove(self, item):
        self.contents.remove(item)
    
    def clear(self):
        self.contents = []
    
    def getNumEntitiesByType(self, entityType):
        count = 0
        for entity in self.contents:
            if isinstance(entity, entityType):
                count += 1
        return count
    
    def cycleRight(self):
        if len(self.contents) == 0:
            return
        
        if self.selectedItem != None:
            index = self.contents.index(self.selectedItem)
            if index < len(self.contents) - 1:
                self.selectedItem = self.contents[index + 1]
            else:
                self.selectedItem = self.contents[0]
        else:
            self.selectedItem = self.contents[0]
    
    def cycleLeft(self):
        if len(self.contents) == 0:
            return
            
        if self.selectedItem != None:
            index = self.contents.index(self.selectedItem)
            if index > 0:
                self.selectedItem = self.contents[index - 1]
            else:
                self.selectedItem = self.contents[len(self.contents) - 1]
        else:
            self.selectedItem = self.contents[0]