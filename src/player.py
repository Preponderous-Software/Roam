from entity import Entity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Player(Entity):
    def __init__(self):
        Entity.__init__(self, "Player")
        self.color = (0, 0, 0)
    
    def getColor(self):
        return self.color