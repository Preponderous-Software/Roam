from environment import Environment


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
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