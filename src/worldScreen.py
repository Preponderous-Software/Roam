import datetime
from math import ceil
import time
import pygame
from apple import Apple
from config import Config
from energyBar import EnergyBar
from food import Food
from graphik import Graphik
from grass import Grass
from grid import Grid
from selectedItemPreview import SelectedItemPreview
from leaves import Leaves
from location import Location
from map import Map
from player import Player
from status import Status
from wood import Wood

# @author Daniel McCoy Stephenson
# @since August 16th, 2022
class WorldScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status, tick: int):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.tick = tick
        self.map = Map(self.config.gridSize, self.graphik)
        self.currentRoom = self.map.getSpawnRoom()
        self.initializeLocationWidthAndHeight()
        self.player = Player()
        self.currentRoom.addEntity(self.player)
        self.status.set("entered the world", self.tick)
        self.score = 0
        self.numApplesEaten = 0
        self.numDeaths = 0
        self.running = True
        self.energyBar = EnergyBar(self.graphik, self.player)
        self.selectedItemPreview = SelectedItemPreview(graphik, self.player.getInventory())

    def initializeLocationWidthAndHeight(self):
        x, y = self.graphik.getGameDisplay().get_size()
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

    def getLocationOfPlayer(self):
        return self.map.getLocation(self.player, self.currentRoom)

    def getLocationDirection(self, direction: int, grid: Grid, location: Location):
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
        pygame.display.set_caption(("Roam " + str(self.currentRoom.getName())))
        
    def movePlayer(self, direction: int):
        if direction == -1:
            return

        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.currentRoom.getGrid(), location)

        if newLocation == -1:
            # we're at a border
            self.changeRooms()
            return

        if self.map.locationContainsEntity(newLocation, Wood):
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
        self.player.setTickLastMoved(self.tick)
    
    def canBePickedUp(self, entity):
        itemTypes = [Wood, Leaves, Grass, Apple]
        for itemType in itemTypes:
            if isinstance(entity, itemType):
                return True
        return False
    
    def executeGatherAction(self):
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
        self.player.removeEnergy(self.config.playerInteractionEnergyCost)
    
    def executePlaceAction(self):
        if len(self.player.getInventory().getContents()) == 0:
            self.status.set("no items", self.tick)
            return

        playerLocation = self.getLocationOfPlayer()
        targetLocation = self.currentRoom.getGrid().getUp(playerLocation)
        if targetLocation == -1:
            self.status.set("no location above player", self.tick)
            return
        if self.map.locationContainsEntity(targetLocation, Wood):
            self.status.set("blocked by wood", self.tick)
            return

        toPlace = self.player.getInventory().getContents().pop() 

        if toPlace == -1:
            return
            
        self.currentRoom.addEntityToLocation(toPlace, targetLocation)
        self.status.set("placed '" + toPlace.getName() + "'", self.tick)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            return "options"
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
            self.player.setGathering(True)
        elif key == pygame.K_q:
            self.player.setPlacing(True)
        elif key == pygame.K_PRINTSCREEN:
            x, y = self.graphik.getGameDisplay().get_size()
            self.captureScreen("screenshot-" + str(datetime.datetime.now()).replace(" ", "-").replace(":", ".") +".png", (0,0), (x,y))
            self.status.set("screenshot saved", self.tick)
        elif key == pygame.K_LSHIFT:
            self.player.setSpeed(self.player.getSpeed()*self.config.runSpeedFactor)

    def handleKeyUpEvent(self, key):
        if (key == pygame.K_w or key == pygame.K_UP) and self.player.getDirection() == 0:
            self.player.setDirection(-1)
        elif (key == pygame.K_a or key == pygame.K_LEFT) and self.player.getDirection() == 1:
            self.player.setDirection(-1)
        elif (key == pygame.K_s or key == pygame.K_DOWN) and self.player.getDirection() == 2:
            self.player.setDirection(-1)
        elif (key == pygame.K_d or key == pygame.K_RIGHT) and self.player.getDirection() == 3:
            self.player.setDirection(-1)
        elif key == pygame.K_e:
            self.player.setGathering(False)
        elif key == pygame.K_q:
            self.player.setPlacing(False)
        elif key == pygame.K_LSHIFT:
            self.player.setSpeed(self.player.getSpeed()/self.config.runSpeedFactor)

    # @source https://stackoverflow.com/questions/63342477/how-to-take-screenshot-of-entire-display-pygame
    def captureScreen(self, name, pos, size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.graphik.getGameDisplay(), (0,0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk**
    
    def respawnPlayer(self):
        self.currentRoom.removeEntity(self.player)
        self.map.getSpawnRoom().addEntity(self.player)
        self.currentRoom = self.map.getSpawnRoom()
        self.player.energy = self.player.maxEnergy
        self.player.getInventory().clear()
        self.status.set("respawned", self.tick)
        pygame.display.set_caption(("Roam " + str(self.currentRoom.getName())))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.printStats()
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    result = self.handleKeyDownEvent(event.key)
                    if result == "options":
                        return "options"
                elif event.type == pygame.KEYUP:
                    self.handleKeyUpEvent(event.key)
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()
                elif event.type == pygame.VIDEORESIZE:
                    self.initializeLocationWidthAndHeight()

            if self.player.getTickLastMoved() + 30/self.player.getSpeed() < self.tick:
                self.movePlayer(self.player.direction)

            if self.player.isGathering():
                self.executeGatherAction()
            elif self.player.isPlacing():
                self.executePlaceAction()

            # remove energy and check for death
            self.player.removeEnergy(self.config.energyDepletionRate)
            if self.player.getEnergy() < self.player.getMaxEnergy() * 0.10:
                self.status.set("low on energy!", self.tick)
            if self.player.isDead():
                self.status.set("you died", self.tick)
                self.score = ceil(self.score * 0.9)
                self.numDeaths += 1
            
            self.status.checkForExpiration(self.tick)

            # draw
            self.graphik.getGameDisplay().fill(self.currentRoom.getBackgroundColor())
            self.currentRoom.draw(self.locationWidth, self.locationHeight)
            self.status.draw()
            self.energyBar.draw()
            self.selectedItemPreview.draw()

            # update
            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
            
            if self.player.isDead():
                time.sleep(3)
                self.respawnPlayer()
        
        self.printStats()
        return