class Inventory:
    def __init__(self):
        self.contents = []
    
    def getContents(self):
        return self.contents
    
    def place(self, item):
        self.contents.append(item)
    
    def remove(self, item):
        self.contents.remove(item)
