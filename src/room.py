from environment import Environment
from graphik import Graphik


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class Room(Environment):
    def __init__(self, name, gridSize, backgroundColor, x, y, graphik: Graphik):
        Environment.__init__(self, name, gridSize)
        self.backgroundColor = backgroundColor
        self.x = x
        self.y = y
        self.graphik = graphik
    
    def getBackgroundColor(self):
        return self.backgroundColor
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def draw(self, locationWidth, locationHeight):
        for location in self.grid.getLocations():
            self.drawLocation(location, location.getX() * locationWidth, location.getY() * locationHeight, locationWidth, locationHeight)

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)

    # Returns the color that a location should be displayed as.
    def getColorOfLocation(self, location):
        if location == -1:
            color = (255, 255, 255)
        else:
            color = self.backgroundColor
            if location.getNumEntities() > 0:
                topEntity = location.getEntities()[-1]
                return topEntity.getColor()
        return color