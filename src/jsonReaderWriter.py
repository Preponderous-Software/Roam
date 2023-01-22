import json
import os
from uuid import UUID

import jsonschema
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
from inventory.inventory import Inventory


class JsonReaderWriter:

    def saveInventory(self, inventory: Inventory):
        print("Saving inventory...")
        toReturn = {}
        toReturn['inventorySlots'] = []
        slotIndex = 0
        for slot in inventory.getInventorySlots():
            slotContents = []
            for entity in slot.getContents():
                toAppend = {}
                toAppend = {
                    'entityId': str(entity.getID()),
                    'entityClass': entity.__class__.__name__,
                    'name': entity.getName(),
                    'assetPath': entity.getImagePath()
                }
                if (isinstance(entity, Food)):
                    toAppend['energy'] = entity.getEnergy()
                if (isinstance(entity, LivingEntity)):
                    toAppend['energy'] = entity.getEnergy()
                    toAppend['tickCreated'] = entity.getTickCreated()
                slotContents.append(toAppend)
            toReturn['inventorySlots'].append({
                'slotIndex': slotIndex,
                'slotContents': slotContents
            })
            slotIndex += 1
        
        # Validate the JSON
        with open('schemas/inventory.json') as f:
            inventorySchema = json.load(f)
        try:
            jsonschema.validate(toReturn, inventorySchema)
        except jsonschema.exceptions.ValidationError as e:
            print(e)

        # create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # print the JSON to file
        with open('data/inventory.json', 'w') as f:
            json.dump(toReturn, f, indent=4)

    def loadInventory(self):
        print("Loading inventory...")
        inventory = Inventory()
        if not os.path.exists('data/inventory.json'):
            return inventory
        with open('data/inventory.json') as f:
            inventoryJson = json.load(f)
        for slot in inventoryJson['inventorySlots']:
            for entity in slot['slotContents']:
                entityClass = entity['entityClass']
                if entityClass == "Apple":
                    apple = Apple()
                    apple.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(apple)
                elif entityClass == "CoalOre":
                    coalOre = CoalOre()
                    coalOre.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(coalOre)
                elif entityClass == 'Grass':
                    grass = Grass()
                    grass.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(grass)
                elif entityClass == "IronOre":
                    ironOre = IronOre()
                    ironOre.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(ironOre)
                elif entityClass == 'JungleWood':
                    jungleWood = JungleWood()
                    jungleWood.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(jungleWood)
                elif entityClass == "Leaves":
                    leaves = Leaves()
                    leaves.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(leaves)
                elif entityClass == 'OakWood':
                    oakWood = OakWood()
                    oakWood.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(oakWood)
                elif entityClass == "Stone":
                    stone = Stone()
                    stone.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(stone)
                elif entityClass == "Bear":
                    bear = Bear(entity['tickCreated'])
                    bear.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(bear)
                elif entityClass == "Chicken":
                    chicken = Chicken(entity['tickCreated'])
                    chicken.setID(UUID(entity['entityId']))
                    inventory.placeIntoFirstAvailableInventorySlot(chicken)
                else:
                    print("Unknown entity class: " + entity['entityClass'])
        return inventory