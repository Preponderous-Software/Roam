from math import ceil
import random
from entity.apple import Apple
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from lib.graphik.src.graphik import Graphik
from entity.rock import Rock
from entity.wood import Wood
from lib.pyenvlib.entity import Entity
from entity.grass import Grass
from entity.leaves import Leaves
from world.roomFactory import RoomFactory
from world.tickCounter import TickCounter
from world.room import Room


# @author Daniel McCoy Stephenson
# @since August 15th, 2022
class Map:
    def __init__(self, gridSize, graphik: Graphik, tickCounter: TickCounter):
        self.rooms = []
        self.gridSize = gridSize
        self.graphik = graphik
        self.tickCounter = tickCounter
        self.roomFactory = RoomFactory(self.gridSize, self.graphik, self.tickCounter)
        self.spawnRoom = self.generateNewRoom(0, 0)
    
    def getRooms(self):
        return self.rooms
    
    def getRoom(self, x, y):
        for room in self.getRooms():
            if room.getX() == x and room.getY() == y:
                return room
        return -1
    
    def getSpawnRoom(self):
        return self.spawnRoom

    def getLocationOfEntity(self, entity: Entity, room: Room):
        locationID = entity.getLocationID()
        grid = room.getGrid()
        return grid.getLocation(locationID)

    def generateNewRoom(self, x, y):
        newRoom = self.roomFactory.createRandomRoom(x, y)
        self.rooms.append(newRoom)
        return newRoom