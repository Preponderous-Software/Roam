from config.config import Config
from lib.graphik.src.graphik import Graphik
from screen.screens import ScreenString
from ui.status import Status
import pygame


class OptionsScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.running = True
        self.nextScreen = ScreenString.WORLD_SCREEN
        self.changeScreen = False
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            self.switchToWorldScreen()
    
    def switchToWorldScreen(self):
        self.nextScreen = ScreenString.WORLD_SCREEN
        self.changeScreen = True
    
    def switchToStatsScreen(self):
        self.nextScreen = ScreenString.STATS_SCREEN
        self.changeScreen = True
    
    def switchToMainMenuScreen(self):
        self.nextScreen = ScreenString.MAIN_MENU_SCREEN
        self.changeScreen = True

    def quitApplication(self):
        self.nextScreen = ScreenString.NONE
        self.changeScreen = True

    def drawMainMenuButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/3
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 - width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "main menu", self.switchToMainMenuScreen)
    
    def drawStatsButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/3
        height = y/10
        
        # in between main menu and quit
        xpos = x/2 - width/2
        ypos = y/2 - height/2
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "stats", self.switchToStatsScreen)

    def drawQuitButton(self):
        # draw in bottom right corner
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/3
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 + width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "quit", self.quitApplication)

    def run(self):
        while not self.changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ScreenString.NONE
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)           
    
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawMainMenuButton()
            self.drawStatsButton()
            self.drawQuitButton()
            pygame.display.update()
            
        self.changeScreen = False
        return self.nextScreen