from graphik import Graphik


# @author Daniel McCoy Stephenson
# since August 14th, 2022
class Status:
    def __init__(self, graphik: Graphik):
        self.text = -1
        self.graphik = graphik
        x, y = self.graphik.getGameDisplay().get_size()
        self.xpos = x/2
        self.ypos = y - y/10
        self.size = 20
        self.color = (0, 0, 0)
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
        self.graphik.drawText(self.text, self.xpos, self.ypos, self.size, self.color)
    
    def getTickLastSet(self):
        return self.tickLastSet
    
    def checkForExpiration(self, currentTick):
        expiryTick = self.tickLastSet + self.durationInTicks
        if currentTick > expiryTick:
            self.clear()