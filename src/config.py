# @author Daniel McCoy Stephenson
# @since August 6th, 2022


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Config:
    def __init__(self):
        self.displayWidth = 600
        self.displayHeight = 600
        self.debug = False
        self.fullscreen = False
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.tickSpeed = 0.1
        self.limitTickSpeed = True
        self.gridSize = 16
        self.playerMovementEnergyCost = 0.5
        self.worldBorder = 10