import datetime
from math import ceil, floor, sqrt
import time
import pygame
from entity.apple import Apple
from config.config import Config
from entity.bear import Bear
from entity.chicken import Chicken
from entity.livingEntity import LivingEntity
from ui.energyBar import EnergyBar
from entity.food import Food
from lib.graphik.src.graphik import Graphik
from entity.grass import Grass
from lib.pyenvlib.grid import Grid
from entity.rock import Rock
from ui.selectedItemPreview import SelectedItemPreview
from entity.leaves import Leaves
from lib.pyenvlib.location import Location
from world.map import Map
from entity.player import Player
from ui.status import Status
from entity.wood import Wood

# @author Daniel McCoy Stephenson
# @since August 16th, 2022
class WorldScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status, tick: int):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.tick = tick
        self.running = True
        self.showInventory = False
    
    def initialize(self):
        self.map = Map(self.config.gridSize, self.graphik)
        self.currentRoom = self.map.getSpawnRoom()
        self.initializeLocationWidthAndHeight()
        self.player = Player()
        self.currentRoom.addEntity(self.player)
        self.status.set("entered the world", self.tick)
        self.score = 0
        self.numApplesEaten = 0
        self.numDeaths = 0
        self.energyBar = EnergyBar(self.graphik, self.player)
        self.selectedItemPreview = SelectedItemPreview(self.graphik, self.player.getInventory())

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
        elif direction == -1:
            return -1
    
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
        if self.player.isCrouching():
            return

        location = self.getLocationOfPlayer()
        newLocation = self.getLocationDirection(direction, self.currentRoom.getGrid(), location)

        if newLocation == -1:
            # we're at a border
            self.changeRooms()
            return

        if self.locationContainsSolidEntity(newLocation):
            return
        
        # if bear is in the new location, kill the player
        for entityId in list(newLocation.getEntities().keys()):
            entity = newLocation.getEntity(entityId)
            if isinstance(entity, Bear):
                self.player.kill()
                return
        
        if self.player.getEnergy() < self.player.getTargetEnergy() * 0.95:
            # search for food to eat
            for entityId in list(newLocation.getEntities().keys()):
                entity = newLocation.getEntity(entityId)
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
        itemTypes = [Wood, Leaves, Grass, Apple, Rock, Chicken]
        for itemType in itemTypes:
            if isinstance(entity, itemType):
                return True
        return False
    
    def getLocationAtMousePosition(self):
        x, y = pygame.mouse.get_pos()
        x = int(x / self.locationWidth)
        y = int(y / self.locationHeight)
        return self.currentRoom.getGrid().getLocationByCoordinates(x, y)
    
    def executeGatherAction(self):
        targetLocation = self.getLocationAtMousePosition()
    
        if targetLocation == -1:
            self.status.set("no location available", self.tick)
            return
        
        # if location too far away
        distanceLimit = self.config.playerInteractionDistanceLimit
        playerLocation = self.getLocationOfPlayer()
        if abs(targetLocation.getX() - playerLocation.getX()) > distanceLimit or abs(targetLocation.getY() - playerLocation.getY()) > distanceLimit:
            self.status.set("too far away", self.tick)
            return

        toRemove = -1
        reversedEntityIdList = list(reversed(targetLocation.getEntities()))
        for entityId in reversedEntityIdList:
            entity = targetLocation.getEntity(entityId)
            if self.canBePickedUp(entity):
                toRemove = entity
                break

        if toRemove == -1:
            return
            
        result = self.player.getInventory().place(toRemove)
        if result == -1:
            self.status.set("inventory full", self.tick)
            return
        self.currentRoom.removeEntity(toRemove)
        if isinstance(toRemove, LivingEntity):
            self.currentRoom.removeLivingEntity(toRemove)
        self.status.set("picked up '" + entity.getName() + "' (" + str(self.player.getInventory().getNumEntitiesByType(type(entity))) + ")", self.tick)
        self.player.removeEnergy(self.config.playerInteractionEnergyCost)
        self.player.setTickLastGathered(self.tick)
    
    def getLocationInFrontOfPlayer(self):
        lastDirectionPlayerWasFacing = self.player.getLastDirection()
        directionPlayerIsFacing = self.player.getDirection()
        direction = lastDirectionPlayerWasFacing
        if direction == -1:
            # player was standing still
            direction = directionPlayerIsFacing
        playerLocation = self.getLocationOfPlayer()
        return self.getLocationDirection(direction, self.currentRoom.grid, playerLocation)
    
    def locationContainsSolidEntity(self, location):
        for entityId in list(location.getEntities().keys()):
            entity = location.getEntity(entityId)
            if entity.isSolid():
                return True
        return False
    
    def executePlaceAction(self):
        if self.player.getInventory().getNumEntities() == 0:
            self.status.set("no items", self.tick)
            return

        targetLocation = self.getLocationAtMousePosition()
        if targetLocation == -1:
            self.status.set("no location available", self.tick)
            return
        if targetLocation == -2:
            self.status.set("can't place while moving", self.tick)
            return
        if self.locationContainsSolidEntity(targetLocation):
            self.status.set("location blocked", self.tick)
            return
        
        # if location too far away
        distanceLimit = self.config.playerInteractionDistanceLimit
        playerLocation = self.getLocationOfPlayer()
        if abs(targetLocation.getX() - playerLocation.getX()) > distanceLimit or abs(targetLocation.getY() - playerLocation.getY()) > distanceLimit:
            self.status.set("too far away", self.tick)
            return
        
        # if living entity is in the location, don't place
        for entityId in list(targetLocation.getEntities().keys()):
            entity = targetLocation.getEntity(entityId)
            if isinstance(entity, LivingEntity):
                self.status.set("blocked by " + entity.getName(), self.tick)
                return

        self.player.removeEnergy(self.config.playerInteractionEnergyCost)

        toPlace = self.player.getInventory().getSelectedItem()
        if toPlace == None:
            self.status.set("no item selected", self.tick)
            return
        self.player.getInventory().removeSelectedItem()

        if toPlace == -1:
            return
            
        self.currentRoom.addEntityToLocation(toPlace, targetLocation)
        if isinstance(toPlace, LivingEntity):
            self.currentRoom.addLivingEntity(toPlace)
        self.status.set("placed '" + toPlace.getName() + "'", self.tick)
        self.player.setTickLastPlaced(self.tick)
    
    def cyclePlayerInventoryRight(self):
        # if inventory empty return
        if len(self.player.getInventory().getContents()) == 0:
            self.status.set("inventory empty", self.tick)
            return
            
        self.player.cycleInventoryRight()
        selectedItem = self.player.getInventory().getSelectedItem()
        if selectedItem == None:
            self.status.set("no item selected", self.tick)
        else:
            self.status.set("selected item: " + selectedItem.getName(), self.tick)
    
    def cyclePlayerInventoryLeft(self):
        # if inventory empty return
        if len(self.player.getInventory().getContents()) == 0:
            self.status.set("inventory empty", self.tick)
            return

        self.player.cycleInventoryLeft()
        selectedItem = self.player.getInventory().getSelectedItem()
        if selectedItem == None:
            self.status.set("no item selected", self.tick)
        else:
            self.status.set("selected item: " + selectedItem.getName(), self.tick)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            return "options"
        elif key == pygame.K_w or key == pygame.K_UP:
            self.player.setDirection(0)
            if self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
                self.movePlayer(self.player.direction)
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.player.setDirection(1)
            if self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
                self.movePlayer(self.player.direction)
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.player.setDirection(2)
            if self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
                self.movePlayer(self.player.direction)
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.player.setDirection(3)
            if self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
                self.movePlayer(self.player.direction)
        elif key == pygame.K_e:
            self.cyclePlayerInventoryRight()
        elif key == pygame.K_q:
            self.cyclePlayerInventoryLeft()
        elif key == pygame.K_PRINTSCREEN:
            x, y = self.graphik.getGameDisplay().get_size()
            self.captureScreen("screenshot-" + str(datetime.datetime.now()).replace(" ", "-").replace(":", ".") +".png", (0,0), (x,y))
            self.status.set("screenshot saved", self.tick)
        elif key == pygame.K_LSHIFT:
            self.player.setSpeed(self.player.getSpeed()*self.config.runSpeedFactor)
        elif key == pygame.K_LCTRL:
            self.player.setCrouching(True)
        elif key == pygame.K_i:
            self.showInventory = not self.showInventory

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
        elif key == pygame.K_LCTRL:
            self.player.setCrouching(False)

    # @source https://stackoverflow.com/questions/63342477/how-to-take-screenshot-of-entire-display-pygame
    def captureScreen(self, name, pos, size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.graphik.getGameDisplay(), (0,0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk**
    
    def respawnPlayer(self):
        # drop all items and clear inventory
        playerLocationId = self.player.getLocationID()
        playerLocation = self.currentRoom.getGrid().getLocation(playerLocationId)
        for item in self.player.getInventory().getContents():
            self.currentRoom.addEntityToLocation(item, playerLocation)
            if isinstance(item, LivingEntity):
                self.currentRoom.addLivingEntity(item)
        self.player.getInventory().clear()

        self.currentRoom.removeEntity(self.player)
        self.map.getSpawnRoom().addEntity(self.player)
        self.currentRoom = self.map.getSpawnRoom()
        self.player.energy = self.player.targetEnergy
        self.status.set("respawned", self.tick)
        pygame.display.set_caption(("Roam " + str(self.currentRoom.getName())))
    
    def checkPlayerMovementCooldown(self, tickToCheck):
        ticksPerSecond = self.config.ticksPerSecond
        return tickToCheck + ticksPerSecond/self.player.getSpeed() < self.tick
    
    def eatFoodInInventory(self):
        for item in self.player.getInventory().getContents():
            if isinstance(item, Food):
                self.player.addEnergy(item.getEnergy())
                self.player.getInventory().remove(item)
                self.status.set("ate " + item.getName() + " from inventory", self.tick)
                return
    
    def handlePlayerActions(self):
        if self.player.isMoving() and self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
            self.movePlayer(self.player.direction)

        if self.player.isGathering() and self.checkPlayerMovementCooldown(self.player.getTickLastGathered()):
            self.executeGatherAction()
        elif self.player.isPlacing() and self.checkPlayerMovementCooldown(self.player.getTickLastPlaced()):
            self.executePlaceAction()
        
        if self.player.needsEnergy() and self.config.autoEatFoodInInventory:
            self.eatFoodInInventory()
    
    def removeEnergyAndCheckForDeath(self):
        self.player.removeEnergy(self.config.energyDepletionRate)
        if self.player.getEnergy() < self.player.getTargetEnergy() * 0.10:
            self.status.set("low on energy!", self.tick)
        if self.player.isDead():
            self.status.set("you died", self.tick)
            self.score = ceil(self.score * 0.9)
            self.numDeaths += 1
    
    def drawPlayerInventory(self):
        # draw inventory background that is 50% size of screen and centered
        backgroundX = self.graphik.getGameDisplay().get_width()/4
        backgroundY = self.graphik.getGameDisplay().get_height()/4
        backgroundWidth = self.graphik.getGameDisplay().get_width()/2
        backgroundHeight = self.graphik.getGameDisplay().get_height()/2
        self.graphik.drawRectangle(backgroundX, backgroundY, backgroundWidth, backgroundHeight, (0,0,0))
            
        # draw contents inside inventory background
        itemsPerRow = 10
        row = 0
        column = 0
        margin = 5
        for item in self.player.getInventory().getContents():
            itemX = backgroundX + column*backgroundWidth/itemsPerRow + margin
            itemY = backgroundY + row*backgroundHeight/itemsPerRow + margin
            itemWidth = backgroundWidth/itemsPerRow - 2*margin
            itemHeight = backgroundHeight/itemsPerRow - 2*margin
            
            image = item.getImage()
            scaledImage = pygame.transform.scale(image, (itemWidth, itemHeight))
            self.graphik.gameDisplay.blit(scaledImage, (itemX, itemY))
            
            column += 1
            if column == itemsPerRow:
                column = 0
                row += 1
        
        # draw '(press I to close)' text below inventory
        self.graphik.drawText("(press I to close)", backgroundX, backgroundY + backgroundHeight + 20, 20, (255,255,255))

    def draw(self):
        self.graphik.getGameDisplay().fill(self.currentRoom.getBackgroundColor())
        self.currentRoom.draw(self.locationWidth, self.locationHeight)
        self.status.draw()
        self.energyBar.draw()
        self.selectedItemPreview.draw()

        # draw room coordinates in top left corner
        coordinatesText = "(" + str(self.currentRoom.getX()) + ", " + str(self.currentRoom.getY()) + ")"
        self.graphik.drawText(coordinatesText, 30, 20, 20, (255,255,255))
        
        if self.showInventory:
            self.drawPlayerInventory()

    def handleMouseDownEvent(self):
        if pygame.mouse.get_pressed()[0]: # left click
            self.player.setGathering(True)
        elif pygame.mouse.get_pressed()[2]: # right click
            self.player.setPlacing(True)

    def handleMouseUpEvent(self):
        if not pygame.mouse.get_pressed()[0]:
            self.player.setGathering(False)
        if not pygame.mouse.get_pressed()[2]:
            self.player.setPlacing(False)

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleMouseDownEvent()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handleMouseUpEvent()
            
            # move living entities
            self.currentRoom.moveLivingEntities()

            self.handlePlayerActions()
            self.removeEnergyAndCheckForDeath()
            self.status.checkForExpiration(self.tick)
            self.draw()
            
            pygame.display.update()

            time.sleep(self.config.tickSpeed)
            self.tick += 1
            
            if self.player.isDead():
                time.sleep(3)
                self.respawnPlayer()
        
        self.printStats()
        return