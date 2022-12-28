import random
from entity.livingEntity import LivingEntity
from entity.player import Player
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
        self.livingEntities = dict()
    
    def getBackgroundColor(self):
        return self.backgroundColor
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def draw(self, locationWidth, locationHeight):
        for locationId in self.grid.getLocations():
            location = self.grid.getLocation(locationId)
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
                topEntityId = list(location.getEntities().keys())[-1]
                topEntity = location.getEntities()[topEntityId]
                return topEntity.getColor()
        return color
    
    def addLivingEntity(self, entity):
        self.livingEntities[entity.getID()] = entity
    
    def removeLivingEntity(self, entity):
        del self.livingEntities[entity.getID()]
    
    def getRandomAdjacentLocation(self, location):
        num = random.randrange(0, 4)
        if num == 0:
            return self.getGrid().getUp(location)
        elif num == 1:
            return self.getGrid().getRight(location)
        elif num == 2: 
            return self.getGrid().getDown(location)
        elif num == 3:
            return self.getGrid().getLeft(location)
    
    def checkEntityMovementCooldown(self, tickToCheck, entity):
        ticksPerSecond = self.config.ticksPerSecond
        return tickToCheck + ticksPerSecond/entity.getSpeed() < self.tick
    
    def moveLivingEntities(self):
        for entityId in self.livingEntities:
            # 1% chance to skip
            if random.randrange(1, 101) > 1:
                continue

            entity = self.livingEntities[entityId]
            locationId = entity.getLocationID()
            location = self.getGrid().getLocation(locationId)
            newLocation = self.getRandomAdjacentLocation(location)

            if newLocation == -1 or self.locationContainsSolidEntity(newLocation):
                continue
            
            # move entity
            location.removeEntity(entity)
            newLocation.addEntity(entity)
            entity.setLocationID(newLocation.getID())

            # if target is edible and living, kill it
            for targetId in list(newLocation.getEntities().keys()):
                target = newLocation.getEntity(targetId)
                if entity.canEat(target) and isinstance(target, LivingEntity):
                    target.kill()

    def locationContainsSolidEntity(self, location):
        for entityId in list(location.getEntities().keys()):
            entity = location.getEntity(entityId)
            if entity.isSolid():
                return True
        return False