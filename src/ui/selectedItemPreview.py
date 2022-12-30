import pygame
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
        image = None

        if len(self.inventory.getContents()) != 0:
            selectedItem = self.inventory.getSelectedItem()
            if selectedItem != None:
                image = selectedItem.getImage()
            else:
                return
        else:
            return

        # draw outer square
        self.graphik.drawRectangle(xpos, ypos, width, height, borderColor)

        # draw image
        scaledImage = pygame.transform.scale(image, (width, height))
        self.graphik.gameDisplay.blit(scaledImage, (xpos, ypos))

        # draw Q to the left of the square
        self.graphik.drawText("Q", xpos - 20, ypos + height/2, 20, borderColor)

        # draw E to the right of the square
        self.graphik.drawText("E", xpos + width + 20, ypos + height/2, 20, borderColor)