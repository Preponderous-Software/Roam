from entity.apple import Apple
from entity.livingEntity import LivingEntity
from inventory.inventory import Inventory


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Player(LivingEntity):
    def __init__(self):
        LivingEntity.__init__(self, "Player", "assets/player.png", 100, [Apple])
        self.direction = -1 # -1 when not moving
        self.lastDirection = -1
        self.inventory = Inventory()
        self.gathering = False
        self.placing = False
        self.tickLastMoved = -1
        self.speed = 30
        self.crouching = False
        self.tickLastGathered = -1
        self.tickLastPlaced = -1
        self.solid = False
    
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
    
    def isSolid(self):
        return self.solid