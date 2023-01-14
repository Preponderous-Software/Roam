from lib.graphik.src.graphik import Graphik
from entity.living.player import Player

# @author Daniel McCoy Stephenson
# @since August 16th, 2022
class EnergyBar:
    def __init__(self, graphik: Graphik, player: Player):
        self.graphik = graphik
        self.player = player
    
    def draw(self):
        x, y = self.graphik.getGameDisplay().get_size()
        xpos = 0
        ypos = y - y/64
        width = x * (self.player.getEnergy()/self.player.getTargetEnergy())
        height = y/64
        color = (255, 215, 73)
        self.graphik.drawRectangle(xpos, ypos, width, height, color)