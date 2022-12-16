import random
from py_env_lib.src.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Wood(Entity):
    def __init__(self):
        Entity.__init__(self, "Wood")
        self.color = (random.randrange(135, 145), random.randrange(65, 75), random.randrange(15, 25))
    
    def getColor(self):
        return self.color