import json

import jsonschema


class TickCounter:
    def __init__(self):
        self.tick = 0
    
    def getTick(self):
        return self.tick
    
    def incrementTick(self):
        self.tick += 1
    
    def save(self):
        jsonTick = {}
        jsonTick["tick"] = self.getTick()
        
        # validate
        tickSchema = json.load(open("schemas/tick.json"))
        jsonschema.validate(jsonTick, tickSchema)
        
        path = "data/tick.json"
        json.dump(jsonTick, open(path, "w"), indent=4)
    
    def load(self):
        path = "data/tick.json"
        jsonTick = json.load(open(path))
        
        # validate
        tickSchema = json.load(open("schemas/tick.json"))
        jsonschema.validate(jsonTick, tickSchema)
        
        self.tick = int(jsonTick["tick"])