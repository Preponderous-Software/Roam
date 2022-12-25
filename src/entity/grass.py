import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Grass(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Grass", (0, random.randrange(150, 200), 0))