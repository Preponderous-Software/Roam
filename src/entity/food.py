from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Food(Entity):
    def __init__(self, name, color, energy):
        Entity.__init__(self, name)
        self.color = color
        self.energy = energy
    
    def getColor(self):
        return self.color
    
    def getEnergy(self):
        return self.energy