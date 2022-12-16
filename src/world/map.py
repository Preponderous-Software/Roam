from math import ceil
import random
from entity.apple import Apple
from graphik.src.graphik import Graphik
from entity.rock import Rock
from entity.wood import Wood
from py_env_lib.src.entity import Entity
from entity.grass import Grass
from entity.leaves import Leaves
from world.room import Room


# @author Daniel McCoy Stephenson
# @since August 15th, 2022
class Map:
    def __init__(self, gridSize, graphik: Graphik):
        self.rooms = []
        self.gridSize = gridSize
        self.graphik = graphik
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

    def getLocation(self, entity: Entity, room: Room):
        locationID = entity.getLocationID()
        grid = room.getGrid()
        return grid.getLocation(locationID)

    def generateNewRoom(self, x, y):
        newRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        newRoom = Room(("(" + str(x) + ", " + str(y) + ")"), self.gridSize, newRoomColor, x, y, self.graphik)

        # generate grass
        self.spawnGrass(newRoom)

        # generate food
        maxTrees = ceil(self.gridSize/3)
        for i in range(0, maxTrees):
            self.spawnTree(newRoom)

        # generate rocks
        self.spawnRocks(newRoom)

        self.rooms.append(newRoom)
        return newRoom

    def spawnGrass(self, room: Room):
        for location in room.getGrid().getLocations():
            if random.randrange(1, 101) > 5: # 95% chance
                room.addEntityToLocation(Grass(), location)
    
    def spawnRocks(self, room: Room):
        for location in room.getGrid().getLocations():
            if random.randrange(1, 101) == 1: # 1% chance
                room.addEntityToLocation(Rock(), location)

    def spawnTree(self, room: Room):
        wood = Wood()
        room.addEntity(wood)

        location = self.getLocation(wood, room)

        locationsToSpawnApples = []
        locationsToSpawnApples.append(room.grid.getUp(location))
        locationsToSpawnApples.append(room.grid.getLeft(location))
        locationsToSpawnApples.append(room.grid.getDown(location))
        locationsToSpawnApples.append(room.grid.getRight(location))
        
        # spawn leaves and apples around the tree
        for appleSpawnLocation in locationsToSpawnApples:
            if appleSpawnLocation == -1 or self.locationContainsEntity(appleSpawnLocation, Wood):
                continue
            room.addEntityToLocation(Leaves(), appleSpawnLocation)
            if random.randrange(0, 2) == 0:
                room.addEntityToLocation(Apple(), appleSpawnLocation)

    def locationContainsEntity(self, location, entityType):
        for entity in location.getEntities():
            if isinstance(entity, entityType):
                return True
        return False