import random
from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Grass(Entity):
    def __init__(self):
        Entity.__init__(self, "Grass")
        self.color = ((0, random.randrange(150, 200), 0))
    
    def getColor(self):
        return self.color