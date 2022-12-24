from lib.graphik.src.graphik import Graphik
from inventory.inventory import Inventory

# @author Daniel McCoy Stephenson
# @since August 17th, 2022
class SelectedItemPreview:
    def __init__(self, graphik: Graphik, inventory: Inventory):
        self.graphik = graphik
        self.inventory = inventory
    
    def draw(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = 30
        height = 30
        xpos = x - x/10 - width
        ypos = y/10
        borderWidth = 2
        borderColor = (0,0,0)
        innerColor = (255,255,255)

        if len(self.inventory.getContents()) != 0:
            selectedItem = self.inventory.getSelectedItem()
            if selectedItem != None:
                innerColor = selectedItem.getColor()
            else:
                return
        else:
            return

        # draw outer square
        self.graphik.drawRectangle(xpos, ypos, width, height, borderColor)

        # draw inner square
        self.graphik.drawRectangle(xpos + borderWidth, ypos + borderWidth, width - borderWidth*2, height - borderWidth*2, innerColor)