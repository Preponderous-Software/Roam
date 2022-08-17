from math import ceil, floor
import pygame
from config import Config
from graphik import Graphik
from status import Status
from worldScreen import WorldScreen


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Roam:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Roam")
        pygame.display.set_icon(pygame.image.load('src/icon.PNG'))
        self.config = Config()
        self.running = True
        self.tick = 0
        self.gameDisplay = self.initializeGameDisplay()
        self.graphik = Graphik(self.gameDisplay)
        self.status = Status(self.graphik)
        self.status.set("entered the world", self.tick)
        self.worldScreen = WorldScreen(self.graphik, self.config, self.status, self.tick)
    
    def initializeGameDisplay(self):
        if self.config.fullscreen:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)
    
    def quitApplication(self):
        pygame.quit()
        quit()
    
    def run(self):
        self.worldScreen.run()

roam = Roam()
roam.run()