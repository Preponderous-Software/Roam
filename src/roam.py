from math import ceil, floor
import time
import pygame
from apple import Apple
from appleTree import AppleTree
from config import Config
from food import Food
from graphik import Graphik
from grass import Grass
from leaves import Leaves
from map import Map
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
        self.map = Map(self.config.gridSize)
        pygame.init()
        pygame.display.set_caption("Roam")
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load('src/icon.PNG'))
        self.graphik = Graphik(self.gameDisplay)
        self.currentRoom = self.map.getSpawnRoom()
        self.initializeLocationWidthAndHeight()
        self.player = Player()
        self.score = 0
        self.numApplesEaten = 0
        self.status = Status(self.graphik)
        self.status.set("entered the world", self.tick)
        self.numDeaths = 0
    
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
        print("Rooms Explored: " + str(len(self.map.getRooms())) + "/" + str((self.config.worldBorder + 1)*(self.config.worldBorder + 1)))
        print("Apples eaten: " + str(self.numApplesEaten))
        print("Items in inventory: " + str(len(self.player.getInventory().getContents())))
        print("Number of deaths: " + str(self.numDeaths))
        print("")
        print("Score: " + str(self.score))
        print("----------")    
    
    def quitApplication(self):
        self.printStats()
        pygame.quit()
        quit()

    def getLocationOfPlayer(self):
        return self.map.getLocation(self.player, self.currentRoom)

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
    
    def changeRooms(self):
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()

        if abs(x) > self.config.worldBorder or abs(y) > self.config.worldBorder:
            self.status.set("reached world border", self.tick)
            return

        playerLocation = self.getLocationOfPlayer()
        self.currentRoom.removeEntity(self.player)
        
        room = self.map.getRoom(x, y)
        if room == -1:
            x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocation()
            self.currentRoom = self.map.generateNewRoom(x, y)
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
    
    def movePlayer(self, direction):
        if direction == -1:
            return

        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.currentRoom.getGrid(), location)

        if newLocation == -1:
            # we're at a border
            self.changeRooms()
            return

        if self.map.locationContainsEntity(newLocation, AppleTree):
            # apple trees are solid
            return
        
        # search for food
        for entity in newLocation.getEntities():
            if isinstance(entity, Food):
                newLocation.removeEntity(entity)
                scoreIncrease = 1 * len(self.map.getRooms())
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

        playerLocation = self.getLocationOfPlayer()
        targetLocation = self.currentRoom.getGrid().getUp(playerLocation)
        if targetLocation == -1:
            self.status.set("no location above player", self.tick)
            return
        if self.map.locationContainsEntity(targetLocation, AppleTree):
            self.status.set("blocked by apple tree", self.tick)
            return

        toPlace = self.player.getInventory().getContents().pop()

        if toPlace == -1:
            return
            
        self.currentRoom.addEntityToLocation(toPlace, targetLocation)
        self.status.set("placed '" + toPlace.getName() + "'", self.tick)

    # @source https://stackoverflow.com/questions/63342477/how-to-take-screenshot-of-entire-display-pygame
    def captureScreen(self, name, pos, size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.gameDisplay, (0,0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk**

    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
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
        elif key == pygame.K_q:
            self.player.setPlacing(True)
        elif key == pygame.K_PRINTSCREEN:
            x, y = self.gameDisplay.get_size()
            self.captureScreen("test.png", (0,0), (x,y))

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
        elif key == pygame.K_q:
            self.player.setPlacing(False)
    
    # Draws the given environment in its entirety.
    def drawEnvironment(self, room: Room):
        for location in room.getGrid().getLocations():
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
    
    def respawnPlayer(self):
        self.currentRoom.removeEntity(self.player)
        self.map.getSpawnRoom().addEntity(self.player)
        self.currentRoom = self.map.getSpawnRoom()
        self.player.energy = self.player.maxEnergy
        self.player.getInventory().clear()
        self.status.set("respawned", self.tick)
    
    def displayInfo(self):
        x, y = self.gameDisplay.get_size()
        startingX = x/8
        startingY = y/8
        size = 30
        self.displayEnergy(startingX, startingY, size)
        
    def displayEnergy(self, startingX, startingY, size):
        self.graphik.drawText("Energy:", startingX, startingY - size/2, size, self.config.black)
        self.graphik.drawText(str(floor((self.player.getEnergy()))), startingX, startingY + size/2, size, self.config.black)
    
    def displayInventoryTopItem(self):
        x, y = self.gameDisplay.get_size()
        xpos = x - x/8
        ypos = y/10
        size = 15
        inventory = self.player.getInventory()
        if len(inventory.getContents()) == 0:
            return
        topItem = inventory.getContents()[-1]
        self.graphik.drawText("Next item: " + topItem.getName(), xpos, ypos, size, self.config.black)

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
            elif self.player.isPlacing():
                self.executePlaceAction()

            self.player.removeEnergy(0.05)
            if self.player.isDead():
                self.status.set("you died", self.tick)
                self.score = ceil(self.score * 0.9)
                self.numDeaths += 1

            self.gameDisplay.fill(self.currentRoom.getBackgroundColor())
            self.drawEnvironment(self.currentRoom)
            self.displayInfo()
            self.displayInventoryTopItem()
            self.status.checkForExpiration(self.tick)
            self.status.draw()
            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
            
            if self.player.isDead():
                time.sleep(3)
                self.respawnPlayer()
        
        self.quitApplication()

roam = Roam()
roam.run()