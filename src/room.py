from environment import Environment


class Room(Environment):
    def __init__(self, name, gridSize):
        Environment.__init__(self, name, gridSize)