import random
import time
import pygame
from config import Config
from entity import Entity
from graphik import Graphik
from player import Player
from room import Room


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class UntitledExplorationGame:
    def __init__(self):
        self.config = Config()
        self.running = True
        self.tick = 0
        pygame.init()
        pygame.display.set_caption("Untitled Exploration Game")
        self.initializeGameDisplay()
        self.graphik = Graphik(self.gameDisplay)
        self.redRoom = Room("Red Room", self.config.gridSize, (200, 0, 0), 0, 0)
        self.currentRoom = self.redRoom
        self.initializeLocationWidthAndHeight()
        self.player = Player()
        self.rooms = []
        self.rooms.append(self.redRoom)
    
    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.currentRoom.getGrid().getRows()
        self.locationHeight = y/self.currentRoom.getGrid().getColumns()
        
    def quitApplication(self):
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
        
    def generateNewRoom(self):
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()
        newRoom = Room("New Room", self.config.gridSize, (random.randrange(50, 200), random.randrange(50, 200), random.randrange(50, 200)), x, y)
        self.rooms.append(newRoom)
        print("A new room was generated with the coordinates ", x, y)
    
    def getRoom(self, x, y):
        for room in self.rooms:
            if room.getX() == x and room.getY() == y:
                return room
        return -1
    
    def changeRooms(self):
        self.currentRoom.removeEntity(self.player)
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()
        room = self.getRoom(x, y)
        if room == -1:
            self.generateNewRoom()
            self.currentRoom = self.rooms[-1]
        else:
            self.currentRoom = room
        
        self.currentRoom.addEntity(self.player)
        self.initializeLocationWidthAndHeight()
    
    def movePlayer(self, direction):
        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.currentRoom.getGrid(), location)

        if newLocation == -1:
            # we're at a border
            self.changeRooms()
            return

        location.removeEntity(self.player)
        newLocation.addEntity(self.player)
    
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
            self.movePlayer(0)
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.movePlayer(1)
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.movePlayer(2)
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.movePlayer(3)
    
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
                
    def run(self):
        self.currentRoom.addEntity(self.player)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()

            self.gameDisplay.fill(self.currentRoom.getBackgroundColor())
            self.drawEnvironment(self.currentRoom)
            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
        
        self.quitApplication()

untitledExplorationGame = UntitledExplorationGame()
untitledExplorationGame.run()