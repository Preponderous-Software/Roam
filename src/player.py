from entity import Entity
from inventory import Inventory


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
        self.interacting = False
        self.placing = False
    
    def getColor(self):
        return self.color
    
    def getEnergy(self):
        return self.energy
    
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
    
    def isInteracting(self):
        return self.interacting

    def setInteracting(self, bool):
        self.interacting = bool
    
    def isPlacing(self):
        return self.placing
    
    def setPlacing(self, bool):
        self.placing = bool
    
    def isDead(self):
        return self.energy < 1