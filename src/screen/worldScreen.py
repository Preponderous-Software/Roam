import datetime
import json
from math import ceil
import os
import time
from uuid import UUID
import jsonschema
import pygame
from entity.apple import Apple
from config.config import Config
from entity.banana import Banana
from entity.coalOre import CoalOre
from entity.ironOre import IronOre
from entity.jungleWood import JungleWood
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from entity.living.livingEntity import LivingEntity
from screen.screenType import ScreenType
from stats.stats import Stats
from ui.energyBar import EnergyBar
from entity.food import Food
from lib.graphik.src.graphik import Graphik
from entity.grass import Grass
from lib.pyenvlib.grid import Grid
from entity.stone import Stone
from entity.leaves import Leaves
from lib.pyenvlib.location import Location
from world.roomFactory import RoomFactory
from world.roomJsonReaderWriter import RoomJsonReaderWriter
from world.tickCounter import TickCounter
from world.map import Map
from player.player import Player
from ui.status import Status
from entity.oakWood import OakWood

# @author Daniel McCoy Stephenson
# @since August 16th, 2022
class WorldScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status, tickCounter: TickCounter, stats: Stats, player: Player):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.tickCounter = tickCounter
        self.stats = stats
        self.player = player
        self.running = True
        self.showInventory = False
        self.nextScreen = ScreenType.OPTIONS_SCREEN
        self.changeScreen = False
        self.roomJsonReaderWriter = RoomJsonReaderWriter(self.config.gridSize, self.graphik, self.tickCounter)
    
    def initialize(self):
        self.map = Map(self.config.gridSize, self.graphik, self.tickCounter)
        self.currentRoom = self.map.getSpawnRoom()
        self.initializeLocationWidthAndHeight()
        
        # load player location if possible
        if (os.path.exists("data/playerLocation.json")):
            self.loadPlayerLocationFromFile()
        else:
            self.currentRoom.addEntity(self.player)
            self.stats.incrementRoomsExplored()
        
        # load player attributes if possible
        if (os.path.exists("data/playerAttributes.json")):
            self.loadPlayerAttributesFromFile()
        
        # load stats if possible
        if (os.path.exists("data/stats.json")):
            self.stats.load()
        
        # load tick if possible
        if (os.path.exists("data/tick.json")):
            self.tickCounter.load()
            
        self.status.set("entered the world")
        self.energyBar = EnergyBar(self.graphik, self.player)

    def initializeLocationWidthAndHeight(self):
        x, y = self.graphik.getGameDisplay().get_size()
        self.locationWidth = x/self.currentRoom.getGrid().getRows()
        self.locationHeight = y/self.currentRoom.getGrid().getColumns()

    def printStatsToConsole(self):
        print("=== Stats ===")
        print("Rooms Explored: " + str(self.stats.getRoomsExplored()))
        print("Apples eaten: " + str(self.stats.getFoodEaten()))
        print("Number of deaths: " + str(self.stats.getNumberOfDeaths()))
        print("")
        print("Score: " + str(self.stats.getScore()))
        print("----------")    

    def getLocationOfPlayer(self):
        return self.map.getLocationOfEntity(self.player, self.currentRoom)

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
    
    def getCoordinatesForNewRoomBasedOnPlayerLocationAndDirection(self):
        location = self.getLocationOfPlayer()
        x = self.currentRoom.getX()
        y = self.currentRoom.getY()

        if self.ifCorner(location):
            direction = self.player.getDirection()
            # if top left corner
            if location.getX() == 0 and location.getY() == 0:
                # if facing up
                if direction == 0:
                    y -= 1
                # if facing left
                elif direction == 1:
                    x -= 1
            # if top right corner
            elif location.getX() == self.config.gridSize - 1 and location.getY() == 0:
                # if facing up
                if direction == 0:
                    y -= 1
                # if facing right
                elif direction == 3:
                    x += 1
            # if bottom left corner
            elif location.getX() == 0 and location.getY() == self.config.gridSize - 1:
                # if facing down
                if direction == 2:
                    y += 1
                # if facing left
                elif direction == 1:
                    x -= 1
            # if bottom right corner
            elif location.getX() == self.config.gridSize - 1 and location.getY() == self.config.gridSize - 1:
                # if facing down
                if direction == 2:
                    y += 1
                # if facing right
                elif direction == 3:
                    x += 1
        else:
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
    
    def ifCorner(self, location: Location):
        return (location.getX() == 0 and location.getY() == 0) or (location.getX() == self.config.gridSize - 1 and location.getY() == 0) or (location.getX() == 0 and location.getY() == self.config.gridSize - 1) or (location.getX() == self.config.gridSize - 1 and location.getY() == self.config.gridSize - 1)
    
    def saveCurrentRoomToFile(self):
        currentRoomPath = "data/rooms/room_" + str(self.currentRoom.getX()) + "_" + str(self.currentRoom.getY()) + ".json"
        self.roomJsonReaderWriter.saveRoom(self.currentRoom, currentRoomPath)
    
    def changeRooms(self):
        x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocationAndDirection()

        if self.config.worldBorder != 0 and (abs(x) > self.config.worldBorder or abs(y) > self.config.worldBorder):
            self.status.set("reached world border")
            return

        playerLocation = self.getLocationOfPlayer()
        self.currentRoom.removeEntity(self.player)

        self.saveCurrentRoomToFile()
        
        room = self.map.getRoom(x, y)
        if room == -1:
            # attempt to load room if file exists, otherwise generate new room
            nextRoomPath = "data/rooms/room_" + str(x) + "_" + str(y) + ".json"
            if os.path.exists(nextRoomPath):
                roomJsonReaderWriter = RoomJsonReaderWriter(self.config.gridSize, self.graphik, self.tickCounter)
                room = roomJsonReaderWriter.loadRoom(nextRoomPath)
                self.map.addRoom(room)
                self.currentRoom = room
                self.status.set("area loaded")
            else:
                x, y = self.getCoordinatesForNewRoomBasedOnPlayerLocationAndDirection()
                self.currentRoom = self.map.generateNewRoom(x, y)
                self.status.set("new area discovered")
                self.stats.incrementRoomsExplored()
        else:
            self.currentRoom = room

        targetX = playerLocation.getX()
        targetY = playerLocation.getY()

        min = 0
        max = self.config.gridSize - 1
        
        # if in corner
        if self.ifCorner(playerLocation):
            playerDirection = self.player.getDirection()
            # if top left corner
            if playerLocation.getX() == 0 and playerLocation.getY() == 0:
                # if facing up
                if playerDirection == 0:
                    targetY = max
                # if facing left
                elif playerDirection == 1:
                    targetX = max
            # if top right corner
            elif playerLocation.getX() == max and playerLocation.getY() == 0:
                # if facing up
                if playerDirection == 0:
                    targetY = max
                # if facing right
                elif playerDirection == 3:
                    targetX = min
            # if bottom left corner
            elif playerLocation.getX() == 0 and playerLocation.getY() == max:
                # if facing down
                if playerDirection == 2:
                    targetY = min
                # if facing left
                elif playerDirection == 1:
                    targetX = max
            # if bottom right corner
            elif playerLocation.getX() == max and playerLocation.getY() == max:
                # if facing down
                if playerDirection == 2:
                    targetY = min
                # if facing right
                elif playerDirection == 3:
                    targetX = min
        else:
            # handle border
            if playerLocation.getX() == 0:
                targetX = max
            elif playerLocation.getX() == max:
                targetX = min
            elif playerLocation.getY() == 0:
                targetY = max
            elif playerLocation.getY() == max:
                targetY = min

        targetLocation = self.currentRoom.getGrid().getLocationByCoordinates(targetX, targetY)
        self.currentRoom.addEntityToLocation(self.player, targetLocation)
        self.initializeLocationWidthAndHeight()
        
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
        
        if self.player.needsEnergy():
            # search for food to eat
            for entityId in list(newLocation.getEntities().keys()):
                entity = newLocation.getEntity(entityId)
                if self.player.canEat(entity):
                    newLocation.removeEntity(entity)
                    self.player.addEnergy(entity.getEnergy())
                    
                    self.stats.incrementFoodEaten()
    
                    self.status.set("ate '" + entity.getName() + "'")
                    
                    self.stats.incrementScore()

        # move player
        location.removeEntity(self.player)
        newLocation.addEntity(self.player)
    
        # decrease energy
        self.player.removeEnergy(self.config.playerMovementEnergyCost)
        self.player.setTickLastMoved(self.tickCounter.getTick())
    
    def canBePickedUp(self, entity):
        itemTypes = [OakWood, JungleWood, Leaves, Grass, Apple, Stone, CoalOre, IronOre, Chicken, Bear, Banana]
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
            self.status.set("no location available")
            return
        
        # if location too far away
        distanceLimit = self.config.playerInteractionDistanceLimit
        playerLocation = self.getLocationOfPlayer()
        if abs(targetLocation.getX() - playerLocation.getX()) > distanceLimit or abs(targetLocation.getY() - playerLocation.getY()) > distanceLimit:
            self.status.set("too far away")
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
            
        result = self.player.getInventory().placeIntoFirstAvailableInventorySlot(toRemove)
        if result == False:
            self.status.set("no available inventory slots")
            return
        self.currentRoom.removeEntity(toRemove)
        if isinstance(toRemove, LivingEntity):
            self.currentRoom.removeLivingEntity(toRemove)
        self.status.set("picked up '" + entity.getName() + "'")
        self.player.removeEnergy(self.config.playerInteractionEnergyCost)
        self.player.setTickLastGathered(self.tickCounter.getTick())
    
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
        if self.player.getInventory().getNumTakenInventorySlots() == 0:
            self.status.set("no items")
            return

        targetLocation = self.getLocationAtMousePosition()
        if targetLocation == -1:
            self.status.set("no location available")
            return
        if targetLocation == -2:
            self.status.set("can't place while moving")
            return
        if self.locationContainsSolidEntity(targetLocation):
            self.status.set("location blocked")
            return
        
        # if location too far away
        distanceLimit = self.config.playerInteractionDistanceLimit
        playerLocation = self.getLocationOfPlayer()
        if abs(targetLocation.getX() - playerLocation.getX()) > distanceLimit or abs(targetLocation.getY() - playerLocation.getY()) > distanceLimit:
            self.status.set("too far away")
            return
        
        # if living entity is in the location, don't place
        for entityId in list(targetLocation.getEntities().keys()):
            entity = targetLocation.getEntity(entityId)
            if isinstance(entity, LivingEntity):
                self.status.set("blocked by " + entity.getName())
                return

        self.player.removeEnergy(self.config.playerInteractionEnergyCost)

        inventorySlot = self.player.getInventory().getSelectedInventorySlot()
        if inventorySlot.isEmpty():
            self.status.set("no item selected")
            return
        toPlace =  self.player.getInventory().removeSelectedItem()

        if toPlace == -1:
            return
            
        self.currentRoom.addEntityToLocation(toPlace, targetLocation)
        if isinstance(toPlace, LivingEntity):
            self.currentRoom.addLivingEntity(toPlace)
        self.status.set("placed '" + toPlace.getName() + "'")
        self.player.setTickLastPlaced(self.tickCounter.getTick())
    
    def changeSelectedInventorySlot(self, index):
        self.player.getInventory().setSelectedInventorySlotIndex(index)
        inventorySlot = self.player.getInventory().getSelectedInventorySlot()
        if inventorySlot.isEmpty():
            self.status.set("no item selected")
            return
        item = inventorySlot.getContents()[0]
        self.status.set("selected '" + item.getName() + "'")

    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            self.nextScreen = ScreenType.OPTIONS_SCREEN
            self.changeScreen = True
        elif key == pygame.K_w or key == pygame.K_UP:
            self.player.setDirection(0)
            self.player
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
        elif key == pygame.K_PRINTSCREEN:
            x, y = self.graphik.getGameDisplay().get_size()
            self.captureScreen("screenshot-" + str(datetime.datetime.now()).replace(" ", "-").replace(":", ".") +".png", (0,0), (x,y))
            self.status.set("screenshot saved")
        elif key == pygame.K_LSHIFT:
            self.player.setMovementSpeed(self.player.getMovementSpeed()*self.config.runSpeedFactor)
        elif key == pygame.K_LCTRL:
            self.player.setCrouching(True)
        elif key == pygame.K_i:
            self.switchToInventoryScreen()
            if self.player.isGathering():
                self.player.setGathering(False)
            if self.player.isPlacing():
                self.player.setPlacing(False)
        elif key == pygame.K_1:
            self.changeSelectedInventorySlot(0)
        elif key == pygame.K_2:
            self.changeSelectedInventorySlot(1)
        elif key == pygame.K_3:
            self.changeSelectedInventorySlot(2)
        elif key == pygame.K_4:
            self.changeSelectedInventorySlot(3)
        elif key == pygame.K_5:
            self.changeSelectedInventorySlot(4)
        elif key == pygame.K_6:
            self.changeSelectedInventorySlot(5)
        elif key == pygame.K_7:
            self.changeSelectedInventorySlot(6)
        elif key == pygame.K_8:
            self.changeSelectedInventorySlot(7)
        elif key == pygame.K_9:
            self.changeSelectedInventorySlot(8)
        elif key == pygame.K_0:
            self.changeSelectedInventorySlot(9)

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
            self.player.setMovementSpeed(self.player.getMovementSpeed()/self.config.runSpeedFactor)
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
        for inventorySlot in self.player.getInventory().getInventorySlots():
            if inventorySlot.isEmpty():
                continue
            for item in inventorySlot.getContents():
                self.currentRoom.addEntityToLocation(item, playerLocation)
                if isinstance(item, LivingEntity):
                    self.currentRoom.addLivingEntity(item)
        self.player.getInventory().clear()

        self.currentRoom.removeEntity(self.player)
        self.map.getSpawnRoom().addEntity(self.player)
        
        self.saveCurrentRoomToFile()
        
        self.currentRoom = self.map.getSpawnRoom()
        self.player.energy = self.player.targetEnergy
        self.status.set("respawned")
        self.player.setTickCreated(self.tickCounter.getTick())
    
    def checkPlayerMovementCooldown(self, tickToCheck):
        ticksPerSecond = self.config.ticksPerSecond
        return tickToCheck + ticksPerSecond/self.player.getMovementSpeed() < self.tickCounter.getTick()
    
    def checkPlayerGatherCooldown(self, tickToCheck):
        ticksPerSecond = self.config.ticksPerSecond
        return tickToCheck + ticksPerSecond/self.player.getGatherSpeed() < self.tickCounter.getTick()
    
    def checkPlayerPlaceCooldown(self, tickToCheck):
        ticksPerSecond = self.config.ticksPerSecond
        return tickToCheck + ticksPerSecond/self.player.getPlaceSpeed() < self.tickCounter.getTick()
    
    def eatFoodInInventory(self):
        for itemSlot in self.player.getInventory().getInventorySlots():
            if itemSlot.isEmpty():
                continue
            item = itemSlot.getContents()[0]
            if self.player.canEat(item):
                self.player.addEnergy(item.getEnergy())
                self.player.getInventory().removeByItem(item)
                self.stats.incrementFoodEaten()
                
                self.status.set("ate " + item.getName() + " from inventory")
                
                self.stats.incrementScore()
                return
    
    def handlePlayerActions(self):
        if self.player.isMoving() and self.checkPlayerMovementCooldown(self.player.getTickLastMoved()):
            self.movePlayer(self.player.direction)

        if self.player.isGathering() and self.checkPlayerGatherCooldown(self.player.getTickLastGathered()):
            self.executeGatherAction()
        elif self.player.isPlacing() and self.checkPlayerPlaceCooldown(self.player.getTickLastPlaced()):
            self.executePlaceAction()
        
        if self.player.needsEnergy() and self.config.autoEatFoodInInventory:
            self.eatFoodInInventory()
    
    def removeEnergyAndCheckForDeath(self):
        self.player.removeEnergy(self.config.energyDepletionRate)
        if self.player.getEnergy() < self.player.getTargetEnergy() * 0.10:
            self.status.set("low on energy!")
        if self.player.isDead():
            self.status.set("you died")
            self.stats.setScore(ceil(self.stats.getScore() * 0.9))
            self.stats.incrementNumberOfDeaths()
    
    def switchToInventoryScreen(self):
        self.nextScreen = ScreenType.INVENTORY_SCREEN
        self.changeScreen = True

    def draw(self):
        self.graphik.getGameDisplay().fill(self.currentRoom.getBackgroundColor())
        self.currentRoom.draw(self.locationWidth, self.locationHeight)
        self.status.draw()
        self.energyBar.draw()

        # draw room coordinates in top left corner
        coordinatesText = "(" + str(self.currentRoom.getX()) + ", " + str(self.currentRoom.getY() * -1) + ")"
        self.graphik.drawText(coordinatesText, 30, 20, 20, (255,255,255))
          
        itemPreviewXPos = self.graphik.getGameDisplay().get_width()/2 - 50*5 - 50/2
        itemPreviewYPos = self.graphik.getGameDisplay().get_height() - 50*3
        itemPreviewWidth = 50
        itemPreviewHeight = 50
        
        barXPos = itemPreviewXPos - 5
        barYPos = itemPreviewYPos - 5
        barWidth = itemPreviewWidth*11 + 5
        barHeight = itemPreviewHeight + 10
        
        # draw rectangle slightly bigger than item images
        self.graphik.drawRectangle(barXPos, barYPos, barWidth, barHeight, (0,0,0))                 
        
        # draw first 10 items in player inventory in bottom center
        firstTenInventorySlots = self.player.getInventory().getFirstTenInventorySlots()
        for i in range(len(firstTenInventorySlots)):
            inventorySlot = firstTenInventorySlots[i]
            if inventorySlot.isEmpty():
                # draw white square if item slot is empty
                self.graphik.drawRectangle(itemPreviewXPos, itemPreviewYPos, itemPreviewWidth, itemPreviewHeight, (255,255,255))
                if i == self.player.getInventory().getSelectedInventorySlotIndex():
                    # draw yellow square in the middle of the selected inventory slot
                    self.graphik.drawRectangle(itemPreviewXPos + itemPreviewWidth/2 - 5, itemPreviewYPos + itemPreviewHeight/2 - 5, 10, 10, (255,255,0))
                itemPreviewXPos += 50 + 5
                continue
            item = inventorySlot.getContents()[0]
            image = item.getImage()
            scaledImage = pygame.transform.scale(image, (50, 50))
            self.graphik.gameDisplay.blit(scaledImage, (itemPreviewXPos, itemPreviewYPos))
            
            if i == self.player.getInventory().getSelectedInventorySlotIndex():
                # draw yellow square in the middle of the selected inventory slot
                self.graphik.drawRectangle(itemPreviewXPos + itemPreviewWidth/2 - 5, itemPreviewYPos + itemPreviewHeight/2 - 5, 10, 10, (255,255,0))
            
            # draw item amount in bottom right corner of inventory slot
            self.graphik.drawText(str(inventorySlot.getNumItems()), itemPreviewXPos + itemPreviewWidth - 20, itemPreviewYPos + itemPreviewHeight - 20, 20, (255,255,255))
            
            itemPreviewXPos += 50 + 5
        
        # display tick count in top right corner
        self.graphik.drawText("tick: " + str(self.tickCounter.getTick()), self.graphik.getGameDisplay().get_width() - 100, 20, 20, (255,255,255))
        
        pygame.display.update()

    def handleMouseDownEvent(self):
        if self.showInventory:
            # disallow player to interact with the world while inventory is open
            self.status.set("close inventory to interact with the world")
            return
        if pygame.mouse.get_pressed()[0]: # left click
            self.player.setGathering(True)
        elif pygame.mouse.get_pressed()[2]: # right click
            self.player.setPlacing(True)

    def handleMouseUpEvent(self):
        if not pygame.mouse.get_pressed()[0]:
            self.player.setGathering(False)
        if not pygame.mouse.get_pressed()[2]:
            self.player.setPlacing(False)
    
    def handleMouseWheelEvent(self, event):
        if event.y > 0:
            currentSelectedInventorySlotIndex = self.player.getInventory().getSelectedInventorySlotIndex()
            newSelectedInventorySlotIndex = currentSelectedInventorySlotIndex - 1
            if newSelectedInventorySlotIndex < 0:
                newSelectedInventorySlotIndex = 9
            self.player.getInventory().setSelectedInventorySlotIndex(newSelectedInventorySlotIndex)
        elif event.y < 0:
            currentSelectedInventorySlotIndex = self.player.getInventory().getSelectedInventorySlotIndex()
            newSelectedInventorySlotIndex = currentSelectedInventorySlotIndex + 1
            if newSelectedInventorySlotIndex > 9:
                newSelectedInventorySlotIndex = 0
            self.player.getInventory().setSelectedInventorySlotIndex(newSelectedInventorySlotIndex)
    
    def handleMouseOver(self):
        location = self.getLocationAtMousePosition()
        if location == -1:
            # mouse is not over a location
            return
        for entityId in location.getEntities():
            entity = location.getEntity(entityId)
            if isinstance(entity, LivingEntity):
                # set status to age of entity
                self.status.set(entity.getName() + " (age: " + str(entity.getAge(self.tickCounter.getTick())) + " ticks)")

    def savePlayerLocationToFile(self):
        jsonPlayerLocation = {}
        
        jsonPlayerLocation["roomX"] = self.currentRoom.getX()
        jsonPlayerLocation["roomY"] = self.currentRoom.getY()
        
        playerLocationId = self.player.getLocationID()
        jsonPlayerLocation["locationId"] = str(playerLocationId)
        
        # validate
        playerLocationSchema = json.load(open("schemas/playerLocation.json"))
        jsonschema.validate(jsonPlayerLocation, playerLocationSchema)
        
        path = "data/playerLocation.json"
        json.dump(jsonPlayerLocation, open(path, "w"), indent=4)
    
    def loadPlayerLocationFromFile(self):
        path = "data/playerLocation.json"
        if not os.path.exists(path):
            return
        jsonPlayerLocation = json.load(open(path))
        
        # validate
        playerLocationSchema = json.load(open("schemas/playerLocation.json"))
        jsonschema.validate(jsonPlayerLocation, playerLocationSchema)
        
        roomX = jsonPlayerLocation["roomX"]
        roomY = jsonPlayerLocation["roomY"]        
        self.currentRoom = self.map.getRoom(roomX, roomY)
        
        locationId = jsonPlayerLocation["locationId"]
        location = self.currentRoom.getGrid().getLocation(locationId)
        self.currentRoom.addEntityToLocation(self.player, location)
    
    def savePlayerAttributesToFile(self):
        jsonPlayerAttributes = {}
        jsonPlayerAttributes["energy"] = ceil(self.player.getEnergy())
        
        # validate
        playerAttributesSchema = json.load(open("schemas/playerAttributes.json"))
        jsonschema.validate(jsonPlayerAttributes, playerAttributesSchema)
        
        path = "data/playerAttributes.json"
        json.dump(jsonPlayerAttributes, open(path, "w"), indent=4)
    
    def loadPlayerAttributesFromFile(self):
        path = "data/playerAttributes.json"
        if not os.path.exists(path):
            return
        jsonPlayerAttributes = json.load(open(path))
        
        # validate
        playerAttributesSchema = json.load(open("schemas/playerAttributes.json"))
        jsonschema.validate(jsonPlayerAttributes, playerAttributesSchema)
        
        energy = jsonPlayerAttributes["energy"]
        self.player.setEnergy(energy)

    def run(self):
        while not self.changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.printStatsToConsole()
                    return ScreenType.NONE
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
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
                elif event.type == pygame.MOUSEWHEEL:
                    self.handleMouseWheelEvent(event)
            
            # move living entities
            self.currentRoom.moveLivingEntities(self.tickCounter.getTick())
            self.currentRoom.reproduceLivingEntities(self.tickCounter.getTick())

            self.handleMouseOver()

            self.handlePlayerActions()
            self.removeEnergyAndCheckForDeath()
            self.status.checkForExpiration(self.tickCounter.getTick())
            self.draw()
            
            pygame.display.update()

            time.sleep(self.config.tickSpeed)
            self.tickCounter.incrementTick()
            
            if self.player.isDead():
                time.sleep(3)
                self.respawnPlayer()
        
        self.saveCurrentRoomToFile()
        self.savePlayerLocationToFile()
        self.savePlayerAttributesToFile()
        self.stats.save()
        self.tickCounter.save()
        
        self.changeScreen = False
        return self.nextScreen