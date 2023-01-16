from math import ceil
import random
from entity.apple import Apple
from entity.grass import Grass
from entity.leaves import Leaves
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from entity.rock import Rock
from entity.wood import Wood
from lib.pyenvlib.entity import Entity

from world.room import Room
from world.roomType import RoomType


class RoomFactory():
    def __init__(self, gridSize, graphik, tickCounter):
        self.gridSize = gridSize
        self.graphik = graphik
        self.tickCounter = tickCounter
    
    def createRoom(self, roomType, x, y):
        if roomType == RoomType.EMPTY:
            return self.createEmptyRoom((0, 0, 0), x, y)
        elif roomType == RoomType.GRASSLAND:
            return self.createGrassRoom(x, y)
        elif roomType == RoomType.FOREST:
            return self.createForestRoom(x, y)
        elif roomType == RoomType.JUNGLE:
            return self.createJungleRoom(x, y)
        elif roomType == RoomType.MOUNTAIN:
            return self.createMountainRoom(x, y)
    
    def createRandomRoom(self, x, y):
        # get random int
        number = random.randrange(0, 4)
        if number == 0:
            newRoom = self.createRoom(RoomType.GRASSLAND, x, y)
        elif number == 1:
            newRoom = self.createRoom(RoomType.FOREST, x, y)
        elif number == 2:
            newRoom = self.createRoom(RoomType.JUNGLE, x, y)
        elif number == 3:
            newRoom = self.createRoom(RoomType.MOUNTAIN, x, y)
        else:
            newRoom = self.createRoom(RoomType.EMPTY, x, y)
        return newRoom
        
    # create methods
    def createEmptyRoom(self, color, x, y):
        newRoom = Room(("(" + str(x) + ", " + str(y) + ")"), self.gridSize, color, x, y, self.graphik)
        return newRoom
    
    def createGrassRoom(self, x, y):
        newRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        newRoom = self.createEmptyRoom(newRoomColor, x, y)

        # generate grass
        self.spawnGrass(newRoom)

        # generate rocks
        self.spawnSomeRocks(newRoom)

        # generate chickens
        self.spawnChickens(newRoom)
        
        return newRoom

    def createForestRoom(self, x, y):
        newRoom = self.createGrassRoom(x, y)

        # generate food
        maxTrees = ceil(self.gridSize/3)
        for i in range(0, maxTrees):
            self.spawnTree(newRoom)

        # generate bears
        self.spawnBears(newRoom)
        return newRoom
    
    def createJungleRoom(self, x, y):
        newRoom = self.createGrassRoom(x, y)
        
        # generate leaves
        self.spawnLeaves(newRoom)

        # generate lots of food
        maxTrees = ceil(self.gridSize/3)
        for i in range(0, maxTrees*4):
            self.spawnTree(newRoom)
        return newRoom

    def createMountainRoom(self, x, y):
        newRoom = self.createEmptyRoom((random.randrange(100, 110), random.randrange(100, 110), random.randrange(100, 110)), x, y)
        
        # generate rocks
        self.fillWithRocks(newRoom)
        return newRoom

    # spawn methods
    def spawnGrass(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            if random.randrange(1, 101) > 5: # 95% chance
                room.addEntityToLocation(Grass(), location)
    
    def spawnSomeRocks(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            if random.randrange(1, 101) == 1: # 1% chance
                room.addEntityToLocation(Rock(), location)

    def fillWithRocks(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            room.addEntityToLocation(Rock(), location)

    def spawnTree(self, room: Room):
        wood = Wood()
        room.addEntity(wood)

        location = self.getLocationOfEntity(wood, room)

        locationsToSpawnApples = []
        locationsToSpawnApples.append(room.grid.getUp(location))
        locationsToSpawnApples.append(room.grid.getLeft(location))
        locationsToSpawnApples.append(room.grid.getDown(location))
        locationsToSpawnApples.append(room.grid.getRight(location))
        
        # spawn leaves and apples around the tree
        for appleSpawnLocation in locationsToSpawnApples:
            if appleSpawnLocation == -1 or self.locationContainsEntityType(appleSpawnLocation, Wood):
                continue
            room.addEntityToLocation(Leaves(), appleSpawnLocation)
            if random.randrange(0, 2) == 0:
                room.addEntityToLocation(Apple(), appleSpawnLocation)
    
    def spawnChickens(self, room: Room):
        for i in range(0, 5):
            if random.randrange(1, 101) > 75: # 25% chance
                newChicken = Chicken(self.tickCounter.getTick())
                room.addEntity(newChicken)
                room.addLivingEntity(newChicken)
    
    def spawnBears(self, room: Room):
        for i in range(0, 2):
            if random.randrange(1, 101) > 90: # 10% chance
                newBear = Bear(self.tickCounter.getTick())
                room.addEntity(newBear)
                room.addLivingEntity(newBear)
    
    def spawnLeaves(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            if random.randrange(1, 101) > 5: # 95% chance
                room.addEntityToLocation(Leaves(), location)
    
    # helper methods
    def getLocationOfEntity(self, entity: Entity, room: Room):
        locationID = entity.getLocationID()
        grid = room.getGrid()
        return grid.getLocation(locationID)

    def locationContainsEntityType(self, location, entityType):
        for entityId in location.getEntities():
            entity = location.getEntity(entityId)
            if isinstance(entity, entityType):
                return True
        return False