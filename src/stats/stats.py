class Stats:
    def __init__(self):
        self.score = 0
        self.roomsExplored = 0
        self.applesEaten = 0
        self.itemsInInventory = 0
        self.numberOfDeaths = 0
    
    def getScore(self):
        return self.score
    
    def setScore(self, score):
        self.score = score
    
    def getRoomsExplored(self):
        return self.roomsExplored
    
    def setRoomsExplored(self, roomsExplored):
        self.roomsExplored = roomsExplored
    
    def getApplesEaten(self):
        return self.applesEaten
    
    def setApplesEaten(self, applesEaten):
        self.applesEaten = applesEaten
    
    def getItemsInInventory(self):
        return self.itemsInInventory
    
    def setItemsInInventory(self, itemsInInventory):
        self.itemsInInventory = itemsInInventory
    
    def getNumberOfDeaths(self):
        return self.numberOfDeaths
    
    def setNumberOfDeaths(self, numberOfDeaths):
        self.numberOfDeaths = numberOfDeaths