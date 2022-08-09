from environment import Environment


class Room(Environment):
    def __init__(self, name, gridSize, backgroundColor):
        Environment.__init__(self, name, gridSize)
        self.backgroundColor = backgroundColor
    
    def getBackgroundColor(self):
        return self.backgroundColor