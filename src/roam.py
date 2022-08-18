import pygame
from config import Config
from graphik import Graphik
from optionsScreen import OptionsScreen
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
        self.worldScreen = WorldScreen(self.graphik, self.config, self.status, self.tick)
        self.optionsScreen = OptionsScreen(self.graphik, self.config, self.status)
        self.currentScreen = self.worldScreen
    
    def initializeGameDisplay(self):
        if self.config.fullscreen:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)
    
    def quitApplication(self):
        pygame.quit()
        quit()
    
    def run(self):
        while True:
            result = self.currentScreen.run()
            if result == "world":
                self.currentScreen = self.worldScreen
            elif result == "options":
                self.currentScreen = self.optionsScreen
            elif result == "exit":
                self.quitApplication()

roam = Roam()
roam.run()