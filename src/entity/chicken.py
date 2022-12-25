import random
from entity.grass import Grass
from entity.livingEntity import LivingEntity


# @author Daniel McCoy Stephenson
# @since July 7th, 2022
class Chicken(LivingEntity):
    def __init__(self):
        LivingEntity.__init__(self, "Chicken", (random.randrange(245, 249), random.randrange(245, 249), random.randrange(245, 249)), random.randrange(20, 30), [Grass])