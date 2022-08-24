from config import Config
from graphik import Graphik
from status import Status
import pygame


class OptionsScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.running = True
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            return "world"
        
    def stop(self):
        self.running = False

    def quitApplication(self):
        pygame.quit()
        quit()

    def drawMainMenuButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/3
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 - width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "main menu", self.stop)

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
                elif event.type == pygame.KEYDOWN:
                    result = self.handleKeyDownEvent(event.key)
                    if result == "world":
                        return "world"
            
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawMainMenuButton()
            self.drawQuitButton()
            pygame.display.update()
        return "menu"