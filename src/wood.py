from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Wood(Entity):
    def __init__(self):
        Entity.__init__(self, "Wood")
        self.color = (139, 69, 19)
    
    def getColor(self):
        return self.color