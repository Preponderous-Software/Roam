# Copyright (c) 2022 Preponderous Software
# MIT License
import random
import uuid
from lib.pyenvlib.entity import Entity
from lib.pyenvlib.location import Location


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
#
# Represents a grid of locations.
class Grid(object):
    def __init__(self, columns, rows):
        self.id = uuid.uuid4()
        self.columns = columns
        self.rows = rows
        self.locations = dict()
        self.generateLocations()

    # Returns the ID of this grid.
    def getID(self):
        return self.id

    # Returns the number of columns that this grid has.
    def getColumns(self):
        return self.columns

    # Returns the number of rows that this grid has.
    def getRows(self):
        return self.rows

    # Returns the list of locations in this grid.
    def getLocations(self):
        return self.locations

    # Returns the first location in this grid.
    def getFirstLocation(self):
        return self.locations[0]

    # Returns the number of locations in this grid.
    def getSize(self):
        return len(self.locations)

    # Returns the number of entities in this grid.
    def getNumEntities(self):
        count = 0
        for locationId in self.locations:
            location = self.locations[locationId]
            count += location.getNumEntities()
        return count

    # Sets the ID of this grid.
    def setID(self, id):
        self.id = id

    # Sets the number of columns of this grid.
    def setColumns(self, columns):
        self.columns = columns

    # Sets the number of rows of this grid.
    def setRows(self, rows):
        self.rows = rows

    # Sets the locations for this grid.
    def setLocations(self, locations):
        self.locations = locations

    # Adds a location to this grid.
    def addLocation(self, location: Location):
        self.locations[location.getID()] = location

    # Removes a location from this grid.
    def removeLocation(self, location: Location):
        self.locations.remove(location)

    # Adds an entity to a random location in this grid.
    def addEntity(self, entity: Entity):
        entity.setGridID(self.getID())
        self.getRandomLocation().addEntity(entity)

    # Adds an entity to a specified location in this grid.
    def addEntityToLocation(self, entity: Entity, location):
        entity.setGridID(self.getID())

        self.locations[location.getID()].addEntity(entity)

    # Removes an entity from this grid.
    def removeEntity(self, entity: Entity):
        for locationId in self.getLocations():
            location = self.locations[locationId]
            if location.isEntityPresent(entity):
                location.removeEntity(entity)
                return

    # Checks if an entity is present in this grid.
    def isEntityPresent(self, entity: Entity):
        for locationId in self.grid.getLocations():
            location = self.locations[locationId]
            if location.isEntityPresent(entity):
                return True

    # Generates the locations based on the columns and rows. Assumes an empty locations array.
    def generateLocations(self):
        for x in range(self.getColumns()):
            for y in range(self.getRows()):
                location = Location(x, y)
                self.locations[location.getID()] = location

    # Returns a location with the specified ID.
    def getLocation(self, id):
        return self.locations[id]

    # Returns a random location.
    def getRandomLocation(self):
        index = random.randrange(0, len(self.locations))
        id = list(self.locations.keys())[index]
        return self.locations[id]

    # Returns a location at the specified coordinates.
    def getLocationByCoordinates(self, x, y):
        for locationId in self.locations:
            location = self.locations[locationId]
            if location.getX() == x and location.getY() == y:
                return location
        return -1

    # Returns the location above the specified location.
    def getUp(self, location: Location):
        if location == -1:
            return -1
        return self.getLocationByCoordinates(location.getX(), location.getY() - 1)

    # Returns the location to the right of the specified location.
    def getRight(self, location: Location):
        if location == -1:
            return -1
        return self.getLocationByCoordinates(location.getX() + 1, location.getY())

    # Returns the location underneath the specified location.
    def getDown(self, location: Location):
        if location == -1:
            return -1
        return self.getLocationByCoordinates(location.getX(), location.getY() + 1)

    # Returns the location to the left of the specified location.
    def getLeft(self, location: Location):
        if location == -1:
            return -1
        return self.getLocationByCoordinates(location.getX() - 1, location.getY())

    # Returns the entity with the specified ID.
    def getEntity(self, id):
        for locationId in self.locations:
            location = self.locations[locationId]
            entity = location.getEntity(id)
            if entity != None:
                return entity
        return None
