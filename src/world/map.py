from math import ceil
import os
import random
from entity.apple import Apple
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from lib.graphik.src.graphik import Graphik
from entity.stone import Stone
from entity.oakWood import OakWood
from lib.pyenvlib.entity import Entity
from entity.grass import Grass
from entity.leaves import Leaves
from world.roomFactory import RoomFactory
from world.roomJsonReaderWriter import RoomJsonReaderWriter
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
        
        # load in spawn room from file if it exists
        roomJsonReaderWriter = RoomJsonReaderWriter(self.gridSize, self.graphik, self.tickCounter)
        path = "data/rooms/room_0_0.json"
        if (os.path.exists(path)):
            print("Loading spawn room from file")
            self.spawnRoom = roomJsonReaderWriter.loadRoom(path)
        else:
            print("Generating new spawn room")
            self.spawnRoom = self.generateNewRoom(0, 0)
        self.rooms.append(self.spawnRoom)
    
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
        # 50% chance to generate last room type
        newRoom = None
        if random.randrange(1, 101) > 50:
            newRoom = self.roomFactory.createRoom(self.roomFactory.lastRoomTypeCreated, x, y)
        else:
            newRoom = self.roomFactory.createRandomRoom(x, y)
        self.rooms.append(newRoom)

        # save room to file
        roomJsonReaderWriter = RoomJsonReaderWriter(self.gridSize, self.graphik, self.tickCounter)
        path = "data/rooms/room_" + str(x) + "_" + str(y) + ".json"
        roomJsonReaderWriter.saveRoom(newRoom, path)

        return newRoom
    
    def addRoom(self, room):
        self.rooms.append(room)