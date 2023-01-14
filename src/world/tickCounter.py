class TickCounter:
    def __init__(self):
        self.tick = 0
    
    def getTick(self):
        return self.tick
    
    def incrementTick(self):
        self.tick += 1