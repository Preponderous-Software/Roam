import pygame
from config.config import Config
from lib.graphik.src.graphik import Graphik
from screen.mainMenuScreen import MainMenuScreen
from screen.optionsScreen import OptionsScreen
from screen.screens import ScreenString
from screen.statsScreen import StatsScreen
from stats.stats import Stats
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
        self.stats = Stats()
        self.worldScreen = WorldScreen(self.graphik, self.config, self.status, self.tick, self.stats)
        self.optionsScreen = OptionsScreen(self.graphik, self.config, self.status)
        self.mainMenuScreen = MainMenuScreen(self.graphik, self.config, self.initializeWorldScreen)
        self.statsScreen = StatsScreen(self.graphik, self.config, self.status, self.stats)
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
            if result == ScreenString.MAIN_MENU_SCREEN:
                return "restart"
            if result == ScreenString.WORLD_SCREEN:
                self.currentScreen = self.worldScreen
            elif result == ScreenString.OPTIONS_SCREEN:
                self.currentScreen = self.optionsScreen
            elif result == ScreenString.STATS_SCREEN:
                self.currentScreen = self.statsScreen
            elif result == ScreenString.NONE:
                self.quitApplication()
            else:
                print("unrecognized screen: " + result)
                self.quitApplication()

roam = Roam()
while True:
    result = roam.run()
    if result is not "restart":
        break
    roam = Roam()