from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 5th, 2022
class LivingEntity(DrawableEntity):
    def __init__(self, name, color, energy, edibleEntityTypes, tickCreated):
        DrawableEntity.__init__(self, name, color)
        self.energy = energy
        self.edibleEntityTypes = edibleEntityTypes
        self.targetEnergy = energy
        self.tickCreated = tickCreated
        self.tickLastReproduced = None
    
    def getEnergy(self):
        return self.energy

    def setEnergy(self, energy):
        self.energy = energy

    def addEnergy(self, amount):
        self.energy += amount
    
    def removeEnergy(self, amount):
        self.energy -= amount

    def needsEnergy(self):
        return self.energy < self.targetEnergy
    
    def getTargetEnergy(self):
        return self.targetEnergy

    def canEat(self, entity):
        for entityType in self.edibleEntityTypes:
            if type(entity) is entityType:
                return True
        return False
    
    def kill(self):
        self.energy = 0
    
    def getTickCreated(self):
        return self.tickCreated
    
    def setTickCreated(self, tick):
        self.tickCreated = tick
    
    def getAge(self, tick):
        return tick - self.tickCreated
    
    def getTickLastReproduced(self):
        return self.tickLastReproduced
    
    def setTickLastReproduced(self, tick):
        self.tickLastReproduced = tick