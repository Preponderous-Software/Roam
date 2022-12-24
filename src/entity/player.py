from lib.pyenvlib.entity import Entity
from inventory.inventory import Inventory


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Player(Entity):
    def __init__(self):
        Entity.__init__(self, "Player")
        self.color = (0, 0, 0)
        self.energy = 100
        self.maxEnergy = 100
        self.direction = -1 # -1 when not moving
        self.lastDirection = -1
        self.inventory = Inventory()
        self.gathering = False
        self.placing = False
        self.tickLastMoved = -1
        self.speed = 15
        self.crouching = False
        self.tickLastGathered = -1
        self.tickLastPlaced = -1
    
    def getColor(self):
        return self.color
    
    def getEnergy(self):
        return self.energy

    def getMaxEnergy(self):
        return self.maxEnergy
    
    def addEnergy(self, energy):
        self.energy += energy
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy
    
    def removeEnergy(self, energy):
        self.energy -= energy
    
    def getDirection(self):
        return self.direction
    
    def setDirection(self, direction):
        self.lastDirection = self.direction
        self.direction = direction
    
    def getLastDirection(self):
        return self.lastDirection
    
    def getInventory(self):
        return self.inventory
    
    def isGathering(self):
        return self.gathering

    def setGathering(self, bool):
        self.gathering = bool
    
    def isPlacing(self):
        return self.placing
    
    def setPlacing(self, bool):
        self.placing = bool
    
    def isDead(self):
        return self.energy < 1
    
    def setTickLastMoved(self, tick):
        self.tickLastMoved = tick
    
    def getTickLastMoved(self):
        return self.tickLastMoved
    
    def getSpeed(self):
        return self.speed
    
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
    
    def isCrouching(self):
        return self.crouching
    
    def setCrouching(self, bool):
        self.crouching = bool
    
    def getTickLastGathered(self):
        return self.tickLastGathered
    
    def setTickLastGathered(self, tick):
        self.tickLastGathered = tick

    def getTickLastPlaced(self):
        return self.tickLastPlaced
    
    def setTickLastPlaced(self, tick):
        self.tickLastPlaced = tick
    
    def isMoving(self):
        return self.direction != -1
    
    def cycleInventoryRight(self):
        self.inventory.cycleRight()
    
    def cycleInventoryLeft(self):
        self.inventory.cycleLeft()