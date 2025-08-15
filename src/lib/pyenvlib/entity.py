# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import uuid


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
#
# Represents an entity that can exist in a location.
class Entity(object):
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.environmentID = -1
        self.gridID = -1
        self.locationID = -1

    # Returns the ID of this entity.
    def getID(self):
        return self.id

    # Returns the name of this entity.
    def getName(self):
        return self.name

    # Returns the ID of the environment that this entity is in.
    def getEnvironmentID(self):
        return self.environmentID

    # Returns the creation timestamp for this entity.
    def getCreationDate(self):
        return self.creationDate

    # Returns the ID of the grid that this entity is in.
    def getGridID(self):
        return self.gridID

    # Returns the ID of the location that this entity is in.
    def getLocationID(self):
        return self.locationID

    # Sets the ID of this entity.
    def setID(self, id):
        self.id = id

    # Sets the name of this entity.
    def setName(self, name):
        self.name = name

    # Sets the environment ID for this entity.
    def setEnvironmentID(self, environmentID):
        self.environmentID = environmentID

    # Sets the creation timestamp for this entity.
    def setCreationDate(self, creationDate):
        self.creationDate = creationDate

    # Sets the grid ID for this entity.
    def setGridID(self, gridID):
        self.gridID = gridID

    # Sets the location ID for this entity.
    def setLocationID(self, locationID):
        self.locationID = locationID

    # Prints information about this entity to the console.
    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Environment ID: ", self.getEnvironmentID())
        print("Grid ID: ", self.getGridID())
        print("Location ID: ", self.getLocationID())
        print("\n")
