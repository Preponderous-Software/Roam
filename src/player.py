from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Player(Entity):
    def __init__(self):
        Entity.__init__(self, "Player")
        self.color = (0, 0, 0)
        self.energy = 100
        self.maxEnergy = 100
        self.direction = -1 # -1 when not moving
    
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
        self.direction = direction