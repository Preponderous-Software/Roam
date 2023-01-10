from config.config import Config
from lib.graphik.src.graphik import Graphik
from screen.screens import ScreenString
from stats.stats import Stats
from ui.status import Status
import pygame


class StatsScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status, stats: Stats):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.stats = stats
        self.nextScreen = ScreenString.OPTIONS_SCREEN
        self.changeScreen = False
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_ESCAPE:
            self.switchToOptionsScreen()
        
    def switchToOptionsScreen(self):
        self.nextScreen = ScreenString.OPTIONS_SCREEN
        self.changeScreen = True

    def quitApplication(self):
        pygame.quit()
        quit()

    def drawStats(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/3
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 - width
        
        # draw score
        text = "score: " + str(self.stats.getScore())
        self.graphik.drawText(text, xpos, ypos, 30, (255,255,255))
        
        # draw rooms explored
        self.xpos = xpos
        self.ypos = ypos + height
        text = "rooms explored: " + str(self.stats.getRoomsExplored())
        self.graphik.drawText(text, xpos, ypos + height, 30, (255,255,255))
        
        # draw apples eaten
        self.xpos = xpos
        self.ypos = ypos + height*2
        text = "apples eaten: " + str(self.stats.getApplesEaten())
        self.graphik.drawText(text, xpos, ypos + height*2, 30, (255,255,255))
        
        # draw items in inventory
        self.xpos = xpos
        self.ypos = ypos + height*3
        text = "items in inventory: " + str(self.stats.getItemsInInventory())
        self.graphik.drawText(text, xpos, ypos + height*3, 30, (255,255,255))
        
        # draw number of deaths
        self.xpos = xpos
        self.ypos = ypos + height*4
        text = "number of deaths: " + str(self.stats.getNumberOfDeaths())
        self.graphik.drawText(text, xpos, ypos + height*4, 30, (255,255,255))

    def drawBackButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = x/5
        height = y/10
        xpos = x/2 - width/2
        ypos = y/2 - height/2 + width
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "back", self.switchToOptionsScreen)

    def run(self):
        while not self.changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScreen = ScreenString.NONE
                    self.changeScreen = True
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
            
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawStats()
            self.drawBackButton()
            pygame.display.update()
            
        self.changeScreen = False
        return self.nextScreen