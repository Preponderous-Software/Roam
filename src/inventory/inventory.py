# @author Daniel McCoy Stephenson
class Inventory:
    def __init__(self):
        self.contents = []
        self.size = 100
        self.selectedItemIndex = None
        
    def getContents(self):
        return self.contents
    
    def getSize(self):
        return self.size
    
    def place(self, item):
        if len(self.contents) < self.size:
            self.contents.append(item)
            self.selectedItemIndex = self.contents.index(item)
        else:
            return -1
    
    def remove(self, item):            
        # if item is selected
        if self.selectedItemIndex != None and self.selectedItemIndex < len(self.contents):
            if self.contents[self.selectedItemIndex] == item:
                self.selectedItemIndex = None
        self.contents.remove(item)
    
    def clear(self):
        self.contents = []
    
    def getNumEntities(self):
        return len(self.contents)
    
    def getNumEntitiesByType(self, entityType):
        count = 0
        for entity in self.contents:
            if isinstance(entity, entityType):
                count += 1
        return count
    
    def cycleRight(self):
        if len(self.contents) == 0:
            return
        
        if self.selectedItemIndex != None:
            index = self.selectedItemIndex
            if index < len(self.contents) - 1:
                self.selectedItemIndex = index + 1
            else:
                self.selectedItemIndex = 0
        else:
            self.selectedItemIndex = 0
    
    def cycleLeft(self):
        if len(self.contents) == 0:
            return
        
        if self.selectedItemIndex != None:
            index = self.selectedItemIndex
            if index > 0:
                self.selectedItemIndex = index - 1
            else:
                self.selectedItemIndex = len(self.contents) - 1
        else:
            self.selectedItemIndex = 0
    
    def getSelectedItem(self):
        if self.selectedItemIndex == None:
            return None
        else:
            if self.selectedItemIndex > len(self.contents) - 1:
                self.selectedItemIndex = None
                return None
            
            return self.contents[self.selectedItemIndex]
    
    def removeSelectedItem(self):
        if self.selectedItemIndex != None:
            self.contents.pop(self.selectedItemIndex)
            if len(self.contents) == 0:
                self.selectedItemIndex = None
            else:
                self.selectedItemIndex = 0