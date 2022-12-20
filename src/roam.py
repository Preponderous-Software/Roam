import pygame
from config.config import Config
from lib.graphik.src.graphik import Graphik
from screen.mainMenuScreen import MainMenuScreen
from screen.optionsScreen import OptionsScreen
from ui.status import Status
from screen.worldScreen import WorldScreen


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Roam:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Roam")
        # pygame.display.set_icon(pygame.image.load('src/media/icon.PNG'))
        self.config = Config()
        self.running = True
        self.tick = 0
        self.gameDisplay = self.initializeGameDisplay()
        self.graphik = Graphik(self.gameDisplay)
        self.status = Status(self.graphik)
        self.worldScreen = WorldScreen(self.graphik, self.config, self.status, self.tick)
        self.optionsScreen = OptionsScreen(self.graphik, self.config, self.status)
        self.mainMenuScreen = MainMenuScreen(self.graphik, self.config, self.initializeWorldScreen)
        self.currentScreen = self.mainMenuScreen

    def initializeGameDisplay(self):
        if self.config.fullscreen:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            return pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)
    
    def initializeWorldScreen(self):
        self.worldScreen.initialize()

    def quitApplication(self):
        pygame.quit()
        quit()
    
    def run(self):
        while True:
            result = self.currentScreen.run()
            if result == "menu":
                self.currentScreen = self.mainMenuScreen
            if result == "world":
                self.currentScreen = self.worldScreen
            elif result == "options":
                self.currentScreen = self.optionsScreen
            elif result == "exit":
                self.quitApplication()

roam = Roam()
roam.run()