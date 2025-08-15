# @author Daniel McCoy Stephenson
class InventorySlot:
    def __init__(self):
        self.contents = []

    def getContents(self):
        return self.contents

    def setContents(self, contents):
        self.contents = contents

    def getNumItems(self):
        return len(self.contents)

    def add(self, item):
        self.contents.append(item)

    def remove(self, item):
        self.contents.remove(item)

    def pop(self):
        return self.contents.pop(0)

    def clear(self):
        self.contents = []

    def isEmpty(self):
        return len(self.contents) == 0

    def getMaxStackSize(self):
        return 20
