import random
from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Wood(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Wood", (random.randrange(135, 145), random.randrange(65, 75), random.randrange(15, 25)))