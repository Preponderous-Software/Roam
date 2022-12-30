import random
from entity.chicken import Chicken
from entity.livingEntity import LivingEntity
from entity.player import Player


# @author Daniel McCoy Stephenson
# @since December 24th, 2022
class Bear(LivingEntity):
    def __init__(self):
        LivingEntity.__init__(self, "Bear", "assets/bear.png", random.randrange(20, 30), [Chicken, Player])
        self.solid = False

    def isSolid(self):
        return self.solid