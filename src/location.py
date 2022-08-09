# Copyright (c) 2022 Preponderous Software
# MIT License
import uuid
from entity import Entity


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
#
# Represents a location that can contain entities.
class Location(object):
    def __init__(self, x, y):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.entities = []
    
    # Returns the ID of this location.
    def getID(self):
        return self.id
    
    # Returns the X coordinate of this location.
    def getX(self):
        return self.x
    
    # Returns the Y coordinate of this location.
    def getY(self):
        return self.y

    # Returns the number ofe ntities in this location.
    def getNumEntities(self):
        return len(self.entities)
    
    # Adds an entity to this location.
    def addEntity(self, entity: Entity):
        if not self.isEntityPresent(entity):
            self.entities.append(entity)
            entity.setLocationID(self.getID())
        else:
            print("Warning: An entity was already present when attempting to add it to a location.")
    
    # Removes an entity from this location.
    def removeEntity(self, entity: Entity):
        if self.isEntityPresent(entity):
            self.entities.remove(entity)
        else:
            print("Warning: An entity was not present when attempting to remove it from a location.")
    
    # Checks if an entity is present in this location.
    def isEntityPresent(self, entity: Entity):
        return entity in self.entities
    
    # Returns the list of entities in this location.
    def getEntities(self):
        return self.entities