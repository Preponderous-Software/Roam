from lib.graphik.src.graphik import Graphik


# @author Daniel McCoy Stephenson
# since August 14th, 2022
class Status:
    def __init__(self, graphik: Graphik):
        self.graphik = graphik
        self.text = -1
        self.textSize = 18
        self.textColor = (0, 0, 0)
        self.tickLastSet = -1
        self.durationInTicks = 20
    
    def set(self, text, tick):
        self.text = text
        self.tickLastSet = tick
    
    def clear(self):
        self.text = -1
    
    def draw(self):
        if self.text == -1:
            return
        x, y = self.graphik.getGameDisplay().get_size()
        width = len(self.text) * 10
        height = self.textSize * 2
        xpos = x/2 - width/2
        ypos = y - y/12 - height/2
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), self.textColor, self.textSize, self.text, self.clear)
        # self.graphik.drawText(self.text, xpos, ypos, self.size, self.color)
    
    def getTickLastSet(self):
        return self.tickLastSet
    
    def checkForExpiration(self, currentTick):
        expiryTick = self.tickLastSet + self.durationInTicks
        if currentTick > expiryTick:
            self.clear()