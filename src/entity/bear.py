import random
from entity.chicken import Chicken
from entity.livingEntity import LivingEntity
from entity.player import Player


# @author Daniel McCoy Stephenson
# @since December 24th, 2022
class Bear(LivingEntity):
    def __init__(self):
        LivingEntity.__init__(self, "Bear", (random.randrange(100, 110), random.randrange(50, 60), random.randrange(20, 30)), random.randrange(20, 30), [Chicken, Player])
        self.solid = False

    def isSolid(self):
        return self.solid