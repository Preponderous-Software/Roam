from math import ceil
import random
from apple import Apple
from appleTree import AppleTree
from entity import Entity
from grass import Grass
from leaves import Leaves
from room import Room


# @author Daniel McCoy Stephenson
# @since August 15th, 2022
class Map:
    def __init__(self, gridSize):
        self.rooms = []
        self.gridSize = gridSize
        self.spawnRoom = self.generateSpawnRoom()
    
    def getRooms(self):
        return self.rooms
    
    def getRoom(self, x, y):
        for room in self.getRooms():
            if room.getX() == x and room.getY() == y:
                return room
        return -1
    
    def getSpawnRoom(self):
        return self.spawnRoom

    def getLocation(self, entity: Entity, room: Room):
        locationID = entity.getLocationID()
        grid = room.getGrid()
        return grid.getLocation(locationID)

    def generateSpawnRoom(self):
        spawnRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        spawnRoom = Room("Spawn", self.gridSize, spawnRoomColor, 0, 0)
        self.spawnGrass(spawnRoom)
        self.rooms.append(spawnRoom)
        return spawnRoom

    def generateNewRoom(self, x, y):
        newRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        newRoom = Room(("Room (" + str(x) + ", " + str(y) + ")"), self.gridSize, newRoomColor, x, y)

        # generate grass
        self.spawnGrass(newRoom)

        # generate food
        for i in range(0, random.randrange(0, ceil(self.gridSize/2))):
            self.spawnAppleTree(newRoom)

        self.rooms.append(newRoom)
        return newRoom

    def spawnGrass(self, room: Room):
        for location in room.getGrid().getLocations():
            if random.randrange(1, 101) > 5: # 95% chance
                room.addEntityToLocation(Grass(), location)

    def spawnAppleTree(self, room: Room):
        # spawn tree
        appleTree = AppleTree()
        room.addEntity(appleTree)

        location = self.getLocation(appleTree, room)

        locationsToSpawnApples = []
        locationsToSpawnApples.append(room.grid.getUp(location))
        locationsToSpawnApples.append(room.grid.getLeft(location))
        locationsToSpawnApples.append(room.grid.getDown(location))
        locationsToSpawnApples.append(room.grid.getRight(location))
        
        # spawn leaves and apples around the tree
        for appleSpawnLocation in locationsToSpawnApples:
            if appleSpawnLocation == -1 or self.locationContainsEntity(appleSpawnLocation, AppleTree):
                continue
            room.addEntityToLocation(Leaves(), appleSpawnLocation)
            if random.randrange(0, 2) == 0:
                room.addEntityToLocation(Apple(), appleSpawnLocation)

    def locationContainsEntity(self, location, entityType):
        for entity in location.getEntities():
            if isinstance(entity, entityType):
                return True
        return False