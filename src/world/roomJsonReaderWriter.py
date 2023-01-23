import json
import os
from uuid import UUID

import jsonschema
from config.config import Config
from entity.apple import Apple
from entity.coalOre import CoalOre
from entity.food import Food
from entity.grass import Grass
from entity.ironOre import IronOre
from entity.jungleWood import JungleWood
from entity.leaves import Leaves
from entity.living.bear import Bear
from entity.living.chicken import Chicken
from entity.living.livingEntity import LivingEntity
from entity.oakWood import OakWood
from entity.stone import Stone
from lib.graphik.src.graphik import Graphik
from lib.pyenvlib.entity import Entity
from lib.pyenvlib.grid import Grid
from lib.pyenvlib.location import Location

from world.room import Room
from world.tickCounter import TickCounter

class RoomJsonReaderWriter:
    def __init__(self, gridSize, graphik: Graphik, tickCounter: TickCounter):
        self.gridSize = gridSize
        self.graphik = graphik
        self.tickCounter = tickCounter

    # save and load methods
    def saveRoom(self, room, path):
        roomJson = self.generateJsonForRoom(room)
        if not os.path.exists("data/rooms"):
            os.makedirs("data/rooms")
        with open(path, 'w') as outfile:
            json.dump(roomJson, outfile, indent=4)

    def loadRoom(self, path):
        with open(path) as json_file:
            roomJson = json.load(json_file)
            return self.generateRoomFromJson(roomJson)

    # generate json methods
    def generateJsonForRoom(self, room):
        roomJson = {}
        roomJson["backgroundColor"] = str(room.getBackgroundColor())
        roomJson["x"] = room.getX()
        roomJson["y"] = room.getY()
        roomJson["name"] = room.getName()
        roomJson["id"] = str(room.getID())
        roomJson["livingEntityIds"] = [str(entityId) for entityId in room.getLivingEntities().keys()]
        roomJson["grid"] = self.generateJsonForGrid(room.getGrid())
        roomJson["creationDate"] = str(room.getCreationDate())

        # validate json with scema``
        roomSchema = json.load(open("schemas/room.json"))
        jsonschema.validate(roomJson, roomSchema)
        return roomJson
    
    def generateJsonForGrid(self, grid):
        gridJson = {}
        gridJson["id"] = str(grid.getID())
        gridJson["columns"] = grid.getColumns()
        gridJson["rows"] = grid.getRows()
        gridJson["locations"] = self.generateJsonForLocations(grid.getLocations())
        return gridJson
    
    def generateJsonForLocations(self, locations):
        locationsJson = []
        for locationId in locations:
            location = locations[locationId]
            locationsJson.append(self.generateJsonForLocation(location))
        return locationsJson

    def generateJsonForLocation(self, location):
        locationJson = {}
        locationJson["id"] = str(location.getID())
        locationJson["x"] = location.getX()
        locationJson["y"] = location.getY()
        locationJson["entities"] = self.generateJsonForEntities(location.getEntities())
        return locationJson

    def generateJsonForEntities(self, entities):
        entitiesJson = []
        for entityId in entities:
            entity = entities[entityId]
            entitiesJson.append(self.generateJsonForEntity(entity))
        return entitiesJson

    def generateJsonForEntity(self, entity):
        entityJson = {}
        entityJson["id"] = str(entity.getID())
        entityJson["entityClass"] = entity.__class__.__name__
        entityJson["name"] = entity.getName()
        entityJson["creationDate"] = str(entity.getCreationDate())
        entityJson["environmentId"] = str(entity.getEnvironmentID())
        entityJson["gridId"] = str(entity.getGridID())
        entityJson["locationId"] = str(entity.getLocationID())
        if isinstance(entity, Food):
            entityJson["energy"] = entity.getEnergy()
        elif isinstance(entity, LivingEntity):
            entityJson["energy"] = entity.getEnergy()
            entityJson["tickCreated"] = entity.getTickCreated()
        return entityJson
    
    # generate room methods
    def generateRoomFromJson(self, roomJson):
        room = Room(roomJson["name"], self.gridSize, (0, 0, 0), roomJson["x"], roomJson["y"], self.graphik)
        room.setID(roomJson["id"])
        # room.setCreationDate(roomJson["creationDate"])
        room.setGrid(self.generateGridFromJson(roomJson["grid"]))
        return room

    def generateGridFromJson(self, gridJson):
        grid = Grid(self.gridSize, self.gridSize)
        grid.setID(gridJson["id"])
        # grid.setCreationDate(gridJson["creationDate"])
        grid.setLocations(self.generateLocationsFromJson(gridJson["locations"]))
        return grid

    def generateLocationsFromJson(self, locationsJson):
        locations = {}
        for locationJson in locationsJson:
            location = self.generateLocationFromJson(locationJson)
            locations[location.getID()] = location
        return locations

    def generateLocationFromJson(self, locationJson):
        location = Location(locationJson["x"], locationJson["y"])
        location.setID(locationJson["id"])
        # location.setCreationDate(locationJson["creationDate"])
        location.setEntities(self.generateEntitiesFromJson(locationJson["entities"]))
        return location

    def generateEntitiesFromJson(self, entitiesJson):
        entities = {}
        for entityJson in entitiesJson:
            entity = self.generateEntityFromJson(entityJson)
            entities[entity.getID()] = entity
        return entities

    def generateEntityFromJson(self, entityJson):
        entityClass = entityJson['entityClass']
        entity = None
        if entityClass == "Apple":
            entity = Apple()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "CoalOre":
            entity = CoalOre()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == 'Grass':
            entity = Grass()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "IronOre":
            entity = IronOre()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == 'JungleWood':
            entity = JungleWood()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "Leaves":
            entity = Leaves()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == 'OakWood':
            entity = OakWood()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "Stone":
            entity = Stone()
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "Bear":
            entity = Bear(entityJson['tickCreated'])
            entity.setID(UUID(entityJson['id']))
        elif entityClass == "Chicken":
            entity = Chicken(entityJson['tickCreated'])
            entity.setID(UUID(entityJson['id']))
        else:
            print("Unknown entity class: " + entity['entityClass'])
        return entity