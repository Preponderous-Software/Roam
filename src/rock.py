import random
from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 18th, 2022
class Rock(Entity):
    def __init__(self):
        Entity.__init__(self, "Rock")
        self.color = (random.randrange(100, 110), random.randrange(100, 110), random.randrange(100, 110))
    
    def getColor(self):
        return self.color