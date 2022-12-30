import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Wood(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Wood", "assets/wood.png")
        self.solid = True
    
    def isSolid(self):
        return self.solid