import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 18th, 2022
class Stone(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Stone", "assets/stone.png")
        self.solid = True
    
    def isSolid(self):
        return self.solid