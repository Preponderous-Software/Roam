import random

import pygame
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from entity.living.livingEntity import LivingEntity
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
            self.drawLocation(location, location.getX() * locationWidth - 1, location.getY() * locationHeight - 1, locationWidth + 2, locationHeight + 2)

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        if location.getNumEntities() > 0:
            # draw texture
            topEntityId = list(location.getEntities().keys())[-1]
            topEntity = location.getEntities()[topEntityId]
            image = topEntity.getImage()
            scaledImage = pygame.transform.scale(image, (width, height))
            self.graphik.gameDisplay.blit(scaledImage, (xPos, yPos))
        else:
            # draw background color
            self.graphik.drawRectangle(xPos, yPos, width, height, self.backgroundColor)
    
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
    
    def moveLivingEntities(self, tick):
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

            # search for food
            for targetEntityId in list(newLocation.getEntities().keys()):
                if targetEntityId == entity.getID():
                    continue
                targetEntity = newLocation.getEntity(targetEntityId)
                if entity.canEat(targetEntity):
                    if isinstance(targetEntity, LivingEntity) and targetEntity.getEnergy() > 0:
                        targetEntity.kill()
                        entity.addEnergy(targetEntity.getEnergy())
                    else:
                        self.removeEntity(targetEntity)
                        entity.addEnergy(10)
                    break
            
    def reproduceLivingEntities(self, tick):
        entityLocationMappings = []
        minAgeToReproduce = 30 * 60 * 5 # 5 minutes (at 30/ticks per second)
        reproductionCooldown = minAgeToReproduce/2 # 2.5 minutes
        for entityId in self.livingEntities:
            entity = self.livingEntities[entityId]
            if entity.getAge(tick) < minAgeToReproduce:
                continue
            locationId = entity.getLocationID()
            location = self.getGrid().getLocation(locationId)
            for targetEntityId in list(location.getEntities().keys()):
                targetEntity = location.getEntity(targetEntityId)
                # check if target entity is a living entity
                if isinstance(targetEntity, LivingEntity) == False:
                    continue
                # check if target entity is the entity itself
                if targetEntity.getID() == entity.getID():
                    continue
                # check if target entity is the same type as the entity
                if isinstance(targetEntity, type(entity)) == False:
                    continue
                # check if target entity is old enough to reproduce
                if targetEntity.getAge(tick) < minAgeToReproduce:
                    continue
                # check reproduction cooldown
                if entity.getTickLastReproduced() != None and entity.getTickLastReproduced() + reproductionCooldown > tick:
                    continue
                

                # throw dice
                if random.randrange(1, 101) > 1: # 1% chance
                    continue

                newEntity = None
                if isinstance(entity, Bear):
                    newEntity = Bear(tick)
                elif isinstance(entity, Chicken):
                    newEntity = Chicken(tick)

                if newEntity != None:
                    entityLocationMappings.append((newEntity, location))
                    entity.setTickLastReproduced(tick)
                    targetEntity.setTickLastReproduced(tick)
                
        for entityLocationMapping in entityLocationMappings:
            entity = entityLocationMapping[0]
            location = entityLocationMapping[1]
            self.addEntityToLocation(entity, location)
            self.addLivingEntity(entity)
                

    def locationContainsSolidEntity(self, location):
        for entityId in list(location.getEntities().keys()):
            entity = location.getEntity(entityId)
            if entity.isSolid():
                return True
        return False