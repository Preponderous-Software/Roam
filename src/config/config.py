# @author Daniel McCoy Stephenson
# @since August 6th, 2022
import pygame


class Config:
    def __init__(self):
        # static (cannot be changed in game)
        self.displayWidth = pygame.display.Info().current_h * 0.90
        self.displayHeight = pygame.display.Info().current_h * 0.90
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.ticksPerSecond = 30
        self.tickSpeed = 1/self.ticksPerSecond
        self.playerMovementEnergyCost = 0.2
        self.playerInteractionEnergyCost= 0.05
        self.runSpeedFactor = 2
        self.energyDepletionRate = 0.01
        self.playerInteractionDistanceLimit = 5
        self.ticksPerSecond = 30
        self.gridSize = 16 # TODO: allow player to set in config menu
        self.worldBorder = 0 # 0 = no border

        # dynamic (can be changed in game)
        self.debug = False
        self.fullscreen = False
        self.autoEatFoodInInventory = True
