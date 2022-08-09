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
        self.environment = Room("Environment #1", self.config.gridSize)
        self.initializeLocationWidthAndHeight()
        self.player = Player()
    
    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()
        
    def quitApplication(self):
        pygame.quit()
        quit()
    
    def getLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
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
    
    def movePlayer(self, direction):
        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.environment.getGrid(), location)

        if newLocation == -1:
            # we're at a border
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
    
    # Draws the environment in its entirety.
    def drawEnvironment(self):
        for location in self.environment.getGrid().getLocations():
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
            color = self.config.white
            if location.getNumEntities() > 0:
                topEntity = location.getEntities()[-1]
                return topEntity.getColor()
        return color
                
    def run(self):
        self.environment.addEntity(self.player)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()

            self.gameDisplay.fill(self.config.white)
            self.drawEnvironment()
            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
        
        self.quitApplication()

untitledExplorationGame = UntitledExplorationGame()
untitledExplorationGame.run()