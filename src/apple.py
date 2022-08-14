import random
from food import Food


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Apple(Food):
    def __init__(self):
       Food.__init__(self, "Apple", (random.randrange(150, 200), random.randrange(5, 10), random.randrange(5, 10)), random.randrange(5, 11))