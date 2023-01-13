import pygame
from config.config import Config

from lib.graphik.src.graphik import Graphik
from screen.screens import ScreenString

# @author Daniel McCoy Stephenson
class MainMenuScreen:
    def __init__(self, graphik: Graphik, config: Config, initializeWorldScreen):
        self.graphik = graphik
        self.config = config
        self.running = True
        self.initializeWorldScreen = initializeWorldScreen
        self.nextScreen = ScreenString.WORLD_SCREEN
        self.changeScreen = False
        
    def switchToWorldScreen(self):
        self.nextScreen = ScreenString.WORLD_SCREEN
        self.changeScreen = True

    def quitApplication(self):
        pygame.quit()
        quit()
    
    def drawText(self):
        x, y = self.graphik.getGameDisplay().get_size()
        xpos = x/2
        ypos = y/10
        self.graphik.drawText("Roam", xpos, ypos, 64, (255, 255, 255))
        ypos = y/3
        self.graphik.drawText("press any key to start!", xpos, ypos, 32, (255, 255, 255))

    def drawPlayButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2
        backgroundColor = (255, 255, 255)
        self.graphik.drawButton(xpos, ypos, width, height, backgroundColor, (0,0,0), 30, "play", self.switchToWorldScreen)

    def drawQuitButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 + width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "quit", self.quitApplication)

    def handleKeyDownEvent(self, key):
        self.switchToWorldScreen()

    def run(self):
        while not self.changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScreen = ScreenString.NONE
                    self.changeScreen = True
                    break
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
            
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawText()
            self.drawPlayButton()
            self.drawQuitButton()
            pygame.display.update()
        self.initializeWorldScreen()
        self.changeScreen = False
        return self.nextScreen