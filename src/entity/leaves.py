import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Leaves(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Leaves", (0, random.randrange(50, 75), 0))