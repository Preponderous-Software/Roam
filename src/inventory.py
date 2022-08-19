class Inventory:
    def __init__(self):
        self.contents = []
        self.size = 100
        
    def getContents(self):
        return self.contents
    
    def place(self, item):
        if len(self.contents) < self.size:
            self.contents.append(item)
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