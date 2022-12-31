# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Config:
    def __init__(self):
        self.displayWidth = 800
        self.displayHeight = 800
        self.debug = False
        self.fullscreen = False
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.ticksPerSecond = 30
        self.tickSpeed = 1/self.ticksPerSecond
        self.gridSize = 16
        self.playerMovementEnergyCost = 0.2
        self.playerInteractionEnergyCost= 0.05
        self.worldBorder = 16
        self.runSpeedFactor = 2
        self.energyDepletionRate = 0.01
        self.playerInteractionDistanceLimit = 5
        self.ticksPerSecond = 30
        self.autoEatFoodInInventory = True