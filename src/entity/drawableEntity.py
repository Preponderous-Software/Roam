from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 5th, 2022
class DrawableEntity(Entity):
    def __init__(self, name, color):
        Entity.__init__(self, name)
        self.color = color
        
    # Returns the color of the entity.
    def getColor(self):
        return self.color