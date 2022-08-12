import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Leaves(Entity):
    def __init__(self):
        Entity.__init__(self, "Leaves")
        self.color = ((0, random.randrange(50, 75), 0))
    
    def getColor(self):
        return self.color