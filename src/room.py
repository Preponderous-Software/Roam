from re import X
from environment import Environment


class Room(Environment):
    def __init__(self, name, gridSize, backgroundColor, x, y):
        Environment.__init__(self, name, gridSize)
        self.backgroundColor = backgroundColor
        self.x = x
        self.y = y
    
    def getBackgroundColor(self):
        return self.backgroundColor
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y