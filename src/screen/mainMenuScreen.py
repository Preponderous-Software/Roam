import pygame
from config.config import Config

from lib.graphik.src.graphik import Graphik

class MainMenuScreen:
    def __init__(self, graphik: Graphik, config: Config, initializeWorldScreen):
        self.graphik = graphik
        self.config = config
        self.running = True
        self.initializeWorldScreen = initializeWorldScreen
        
    def stop(self):
        self.running = False

    def quitApplication(self):
        pygame.quit()
        quit()
    
    def setGridSizeToSmall(self):
        self.config.gridSize = self.config.smallGridSize
        self.stop()

    def setGridSizeToMedium(self):
        self.config.gridSize = self.config.mediumGridSize
        self.stop()

    def setGridSizeToLarge(self):
        self.config.gridSize = self.config.largeGridSize
        self.stop()
    
    def drawText(self):
        x, y = self.graphik.getGameDisplay().get_size()
        xpos = x/2
        ypos = y/10
        self.graphik.drawText("Roam", xpos, ypos, 64, (255, 255, 255))
        ypos = y/3
        self.graphik.drawText("choose your grid size!", xpos, ypos, 32, (255, 255, 255))

    def drawSmallButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2 - width*1.5
        ypos = y/2 - height/2
        backgroundColor = (255, 255, 255)
        self.graphik.drawButton(xpos, ypos, width, height, backgroundColor, (0,0,0), 30, "small", self.setGridSizeToSmall)

    def drawMediumButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2
        backgroundColor = (255, 255, 255)
        self.graphik.drawButton(xpos, ypos, width, height, backgroundColor, (0,0,0), 30, "medium", self.setGridSizeToMedium)
    
    def drawLargeButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2 + width*1.5
        ypos = y/2 - height/2
        backgroundColor = (255, 255, 255)
        self.graphik.drawButton(xpos, ypos, width, height, backgroundColor, (0,0,0), 30, "large", self.setGridSizeToLarge)

    def drawQuitButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 + width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "quit", self.quitApplication)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawText()
            self.drawSmallButton()
            self.drawMediumButton()
            self.drawLargeButton()
            self.drawQuitButton()
            pygame.display.update()
        self.initializeWorldScreen()
        return "world"