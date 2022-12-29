from lib.pyenvlib.environment import Environment
from lib.graphik.src.graphik import Graphik


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
        for locationId in self.grid.getLocations():
            location = self.grid.getLocation(locationId)
            self.drawLocation(location, location.getX() * locationWidth - 1, location.getY() * locationHeight - 1, locationWidth + 2, locationHeight + 2)

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
                topEntityId = list(location.getEntities().keys())[-1]
                topEntity = location.getEntities()[topEntityId]
                return topEntity.getColor()
        return color