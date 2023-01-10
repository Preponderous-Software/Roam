# @author Daniel McCoy Stephenson
class Inventory:
    def __init__(self):
        self.contents = []
        self.size = 100
        self.selectedItemIndex = 0
        
    def getContents(self):
        return self.contents
    
    def getSize(self):
        return self.size
    
    def place(self, item):
        if len(self.contents) < self.size:
            self.contents.append(item)
        else:
            return -1
    
    def remove(self, item):            
        # if item is selected
        if self.selectedItemIndex != None and self.selectedItemIndex < len(self.contents):
            if self.contents[self.selectedItemIndex] == item:
                self.selectedItemIndex = 0
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

    def getSelectedItemIndex(self):
        return self.selectedItemIndex

    def setSelectedItemIndex(self, index):
        self.selectedItemIndex = index
            
    def getItemByIndex(self, index):
        if index < len(self.contents):
            return self.contents[index]
        else:
            return None
    
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
                self.selectedItemIndex = self.selectedItemIndex % 10
    
    def getFirstTenItems(self):
        if len(self.contents) > 10:
            return self.contents[:10]
        else:
            return self.contents
        
    def getLastTenItems(self):
        if len(self.contents) > 10:
            return self.contents[-10:]
        else:
            return self.contents