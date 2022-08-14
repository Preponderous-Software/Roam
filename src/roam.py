from math import ceil, floor
import random
import time
import pygame
from apple import Apple
from appleTree import AppleTree
from config import Config
from entity import Entity
from environment import Environment
from food import Food
from graphik import Graphik
from grass import Grass
from leaves import Leaves
from player import Player
from room import Room
from status import Status


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Roam:
    def __init__(self):
        self.config = Config()
        self.running = True
        self.tick = 0
        pygame.init()
        pygame.display.set_caption("Roam")
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load('src/icon.PNG'))
        self.graphik = Graphik(self.gameDisplay)
        self.generateSpawnRoom()
        self.initializeLocationWidthAndHeight()
        self.player = Player()
        self.rooms = []
        self.rooms.append(self.currentRoom)
        self.score = 0
        self.numApplesEaten = 0
        self.status = Status(self.graphik)
        self.status.set("entered the world", self.tick)
    
    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.currentRoom.getGrid().getRows()
        self.locationHeight = y/self.currentRoom.getGrid().getColumns()

    def printStats(self):
        print("=== Stats ===")
        print("Rooms Explored: ", len(self.rooms))
        print("Apples eaten: ", self.numApplesEaten)
        print("Items in inventory: ", len(self.player.getInventory().getContents()))
        print("")
        print("Score: ", self.score)
        print("----------")    
    
    def quitApplication(self):
        self.printStats()
        pygame.quit()
        quit()
    
    def getLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.currentRoom.getGrid()
        return grid.getLocation(locationID)

    def getLocationOfPlayer(self):
        return self.getLocation(self.player)

    def getLocationDirection(self, direction, grid, location):
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getLeft(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getRight(location)
    
    def getCoordinatesForNewRoomBasedOnPlayerLocation(self):
        location = self.getLocationOfPlayer()
        x = self.currentRoom.getX()
        y = self.currentRoom.getY()
        if location.getX() == self.config.gridSize - 1:
            # we are on the right side of this room
            x += 1
        elif location.getX() == 0:
            # we are on the left side of this room
            x -= 1
        elif location.getY() == self.config.gridSize - 1:
            # we are at the bottom of this room
            y += 1
        elif location.getY() == 0:
            # we are at the top of this room
            y -= 1
        return x, y
    
    def spawnAppleTree(self, room: Environment):
        # spawn tree
        appleTree = AppleTree()
        room.addEntity(appleTree)

        location = self.getLocation(appleTree)

        locationsToSpawnApples = []
        locationsToSpawnApples.append(self.currentRoom.grid.getUp(location))
        locationsToSpawnApples.append(self.currentRoom.grid.getLeft(location))
        locationsToSpawnApples.append(self.currentRoom.grid.getDown(location))
        locationsToSpawnApples.append(self.currentRoom.grid.getRight(location))
        
        # spawn leaves and apples around the tree
        for appleSpawnLocation in locationsToSpawnApples:
            if appleSpawnLocation == -1 or self.locationContainsEntity(appleSpawnLocation, AppleTree):
                continue
            room.addEntityToLocation(Leaves(), appleSpawnLocation)
            if random.randrange(0, 2) == 0:
                room.addEntityToLocation(Apple(), appleSpawnLocation)
    
    def spawnGrass(self, room: Room):
        for location in room.getGrid().getLocations():
            room.addEntityToLocation(Grass(), location)
    
    def generateSpawnRoom(self):
        spawnRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        self.currentRoom = Room("Spawn", self.config.gridSize, spawnRoomColor, 0, 0)
        self.spawnGrass(self.currentRoom)
        
    def generateNewRoom(self):
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()
        newRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        newRoom = Room(("Room (" + str(x) + ", " + str(y) + ")"), self.config.gridSize, newRoomColor, x, y)
        
        self.currentRoom = newRoom

        # generate grass
        self.spawnGrass(self.currentRoom)

        # generate food
        for i in range(0, random.randrange(0, ceil(self.config.gridSize/2))):
            self.spawnAppleTree(newRoom)

        self.rooms.append(newRoom)
        if self.config.debug:
            print("A new room was generated with the coordinates ", x, y)
    
    def getRoom(self, x, y):
        for room in self.rooms:
            if room.getX() == x and room.getY() == y:
                return room
        return -1
    
    def changeRooms(self):
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()

        if abs(x) > self.config.worldBorder or abs(y) > self.config.worldBorder:
            # reached world border
            return

        playerLocation = self.getLocationOfPlayer()
        self.currentRoom.removeEntity(self.player)
        
        room = self.getRoom(x, y)
        if room == -1:
            self.generateNewRoom()
            self.status.set("new area discovered", self.tick)
        else:
            self.currentRoom = room

        targetX = playerLocation.getX()
        targetY = playerLocation.getY()

        min = 0
        max = self.config.gridSize - 1
        if playerLocation.getY() == min:
            targetY = max
        elif playerLocation.getY() == max:
            targetY = min
        
        if playerLocation.getX() == min:
            targetX = max
        elif playerLocation.getX() == max:
            targetX = min

        targetLocation = self.currentRoom.getGrid().getLocationByCoordinates(targetX, targetY)
        self.currentRoom.addEntityToLocation(self.player, targetLocation)
        self.initializeLocationWidthAndHeight()
        pygame.display.set_caption(("Roam - " + str(self.currentRoom.getName())))
    
    def locationContainsEntity(self, location, entityType):
        for entity in location.getEntities():
            if isinstance(entity, entityType):
                return True
        return False
    
    def movePlayer(self, direction):
        if direction == -1:
            return

        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.currentRoom.getGrid(), location)

        if newLocation == -1:
            # we're at a border
            self.changeRooms()
            return

        if self.locationContainsEntity(newLocation, AppleTree):
            # apple trees are solid
            return
        
        # search for food
        for entity in newLocation.getEntities():
            if isinstance(entity, Food):
                newLocation.removeEntity(entity)
                scoreIncrease = 1 * len(self.rooms)
                self.score += scoreIncrease
                self.player.addEnergy(entity.getEnergy())
                
                if isinstance(entity, Apple):
                    self.numApplesEaten += 1
                    self.status.set("ate '" + entity.getName() + "'", self.tick)

        # move player
        location.removeEntity(self.player)
        newLocation.addEntity(self.player)
    
        # decrease energy
        self.player.removeEnergy(self.config.playerMovementEnergyCost)
    
    def canBePickedUp(self, entity):
        itemTypes = [AppleTree, Leaves, Grass, Apple]
        for itemType in itemTypes:
            if isinstance(entity, itemType):
                return True
        return False
    
    def executeInteractAction(self):
        playerLocation = self.getLocationOfPlayer()

        toCheck = []
        toCheck.append(playerLocation)
        toCheck.append(self.currentRoom.getGrid().getUp(playerLocation))
        toCheck.append(self.currentRoom.getGrid().getLeft(playerLocation))
        toCheck.append(self.currentRoom.getGrid().getDown(playerLocation))
        toCheck.append(self.currentRoom.getGrid().getRight(playerLocation))
    
        toRemove = -1
        for location in toCheck:
            if location == -1:
                continue
            reversedEntityList = list(reversed(location.getEntities()))
            for entity in reversedEntityList:
                if self.canBePickedUp(entity):
                    toRemove = entity
                    break
            if toRemove != -1:
                break
        
        if toRemove == -1:
            return
            
        self.currentRoom.removeEntity(toRemove)
        self.player.getInventory().place(toRemove)
        self.status.set("picked up '" + entity.getName() + "'", self.tick)
    
    def executePlaceAction(self):
        if len(self.player.getInventory().getContents()) == 0:
            self.status.set("no items", self.tick)
            return

        toPlace = self.player.getInventory().getContents().pop()

        if toPlace == -1:
            return

        playerLocation = self.getLocationOfPlayer()
        self.currentRoom.addEntityToLocation(toPlace, playerLocation)
        self.status.set("placed '" + toPlace.getName() + "'", self.tick)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_q:
            self.quitApplication()
        elif key == pygame.K_F11:
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            self.initializeGameDisplay()
        elif key == pygame.K_l:
            if self.config.limitTickSpeed:
                self.config.limitTickSpeed = False
            else:
                self.config.limitTickSpeed = True
        elif key == pygame.K_w or key == pygame.K_UP:
            self.player.setDirection(0)
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.player.setDirection(1)
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.player.setDirection(2)
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.player.setDirection(3)
        elif key == pygame.K_e:
            self.player.setInteracting(True)
        elif key == pygame.K_p:
            self.executePlaceAction()

    def handleKeyUpEvent(self, key):
        if key == pygame.K_w or key == pygame.K_UP and self.player.getDirection() == 0:
            self.player.setDirection(-1)
        elif key == pygame.K_a or key == pygame.K_LEFT and self.player.getDirection() == 1:
            self.player.setDirection(-1)
        elif key == pygame.K_s or key == pygame.K_DOWN and self.player.getDirection() == 2:
            self.player.setDirection(-1)
        elif key == pygame.K_d or key == pygame.K_RIGHT and self.player.getDirection() == 3:
            self.player.setDirection(-1)
        elif key == pygame.K_e:
            self.player.setInteracting(False)
    
    # Draws the given environment in its entirety.
    def drawEnvironment(self, environment):
        for location in environment.getGrid().getLocations():
            self.drawLocation(location, location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight)

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)

    # Returns the color that a location should be displayed as.
    def getColorOfLocation(self, location):
        if location == -1:
            color = self.config.white
        else:
            color = self.currentRoom.getBackgroundColor()
            if location.getNumEntities() > 0:
                topEntity = location.getEntities()[-1]
                return topEntity.getColor()
        return color
    
    def checkForPlayerDeath(self):
        # check for player death
        if self.player.getEnergy() <= 0:
            time.sleep(1)
            self.quitApplication()
    
    def displayInfo(self):
        x, y = self.gameDisplay.get_size()
        startingX = x/8
        startingY = y/8
        size = 30
        self.displayEnergy(startingX, startingY, size)
        startingX *= size/10
        self.displayScore(startingX, startingY, size)
        
    def displayEnergy(self, startingX, startingY, size):
        self.graphik.drawText("Energy:", startingX, startingY - size/2, size, self.config.black)
        self.graphik.drawText(str(floor((self.player.getEnergy()))), startingX, startingY + size/2, size, self.config.black)
    
    def displayScore(self, startingX, startingY, size):
        self.graphik.drawText("Score:", startingX, startingY - size/2, size, self.config.black)
        self.graphik.drawText(str(self.score), startingX, startingY + size/2, size, self.config.black)

    def run(self):
        self.currentRoom.addEntity(self.player)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
                elif event.type == pygame.KEYUP:
                    self.handleKeyUpEvent(event.key)
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()

            self.movePlayer(self.player.direction)
            if self.player.isInteracting():
                self.executeInteractAction()
            self.player.removeEnergy(0.05)
            self.gameDisplay.fill(self.currentRoom.getBackgroundColor())
            self.drawEnvironment(self.currentRoom)
            self.displayInfo()
            self.status.checkForExpiration(self.tick)
            self.status.draw()
            pygame.display.update()

            self.checkForPlayerDeath()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
        
        self.quitApplication()

roam = Roam()
roam.run()