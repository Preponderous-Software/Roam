# @author Daniel McCoy Stephenson
# @since August 6th, 2022
import random


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Config:
    def __init__(self):
        self.displayWidth = 500
        self.displayHeight = 500
        self.debug = False
        self.fullscreen = False
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.tickSpeed = 0.1
        self.limitTickSpeed = True
        self.gridSize = random.randrange(8, 16)