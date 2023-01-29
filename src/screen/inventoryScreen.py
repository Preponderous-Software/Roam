import datetime
from config.config import Config
from inventory.inventory import Inventory
from inventory.inventorySlot import InventorySlot
from lib.graphik.src.graphik import Graphik
from screen.screenType import ScreenType
from ui.status import Status
import pygame

# @author Daniel McCoy Stephenson
class InventoryScreen:
    def __init__(self, graphik: Graphik, config: Config, status: Status, inventory: Inventory):
        self.graphik = graphik
        self.config = config
        self.status = status
        self.inventory = inventory
        self.nextScreen = ScreenType.WORLD_SCREEN
        self.changeScreen = False
        self.cursorSlot = InventorySlot()
    
    # @source https://stackoverflow.com/questions/63342477/how-to-take-screenshot-of-entire-display-pygame
    def captureScreen(self, name, pos, size): # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(self.graphik.getGameDisplay(), (0,0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk**
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_i or key == pygame.K_ESCAPE:
            self.switchToWorldScreen()
        elif key == pygame.K_PRINTSCREEN:
            x, y = self.graphik.getGameDisplay().get_size()
            self.captureScreen("screenshot-" + str(datetime.datetime.now()).replace(" ", "-").replace(":", ".") +".png", (0,0), (x,y))
        
    def switchToWorldScreen(self):
        self.nextScreen = ScreenType.WORLD_SCREEN
        self.changeScreen = True

    def quitApplication(self):
        pygame.quit()
        quit()

    def drawPlayerInventory(self):
        # draw inventory background that is 50% size of screen and centered
        backgroundX = self.graphik.getGameDisplay().get_width()/4
        backgroundY = self.graphik.getGameDisplay().get_height()/4
        backgroundWidth = self.graphik.getGameDisplay().get_width()/2
        backgroundHeight = self.graphik.getGameDisplay().get_height()/2
        self.graphik.drawRectangle(backgroundX, backgroundY, backgroundWidth, backgroundHeight, (0,0,0))
            
        # draw contents inside inventory background
        itemsPerRow = 5
        row = 0
        column = 0
        margin = 5
        for inventorySlot in self.inventory.getInventorySlots():
            itemX = backgroundX + column*backgroundWidth/itemsPerRow + margin
            itemY = backgroundY + row*backgroundHeight/itemsPerRow + margin
            itemWidth = backgroundWidth/itemsPerRow - 2*margin
            itemHeight = backgroundHeight/itemsPerRow - 2*margin

            if inventorySlot.isEmpty():
                self.graphik.drawRectangle(itemX, itemY, itemWidth, itemHeight, (255,255,255))
                if row*itemsPerRow + column == self.inventory.getSelectedInventorySlotIndex():
                    # draw yellow square in the middle of the selected inventory slot (may be on any row)
                    self.graphik.drawRectangle(itemX + itemWidth/2 - 5, itemY + itemHeight/2 - 5, 10, 10, (255,255,0))
                column += 1
                if column == itemsPerRow:
                    column = 0
                    row += 1
                continue
            
            item = inventorySlot.getContents()[0]
            image = item.getImage()
            scaledImage = pygame.transform.scale(image, (itemWidth, itemHeight))
            self.graphik.gameDisplay.blit(scaledImage, (itemX, itemY))
            
            if row*itemsPerRow + column == self.inventory.getSelectedInventorySlotIndex():
                # draw yellow square in the middle of the selected inventory slot
                self.graphik.drawRectangle(itemX + itemWidth/2 - 5, itemY + itemHeight/2 - 5, 10, 10, (255,255,0))
            
            # draw item amount in bottom right corner of inventory slot
            self.graphik.drawText(str(inventorySlot.getNumItems()), itemX + itemWidth - 20, itemY + itemHeight - 20, 20, (255,255,255))
            
            column += 1
            if column == itemsPerRow:
                column = 0
                row += 1
        
        # draw '(press I to close)' text below inventory
        self.graphik.drawText("(press I to close)", backgroundX, backgroundY + backgroundHeight + 20, 20, (255,255,255))

    def drawBackButton(self):
        x, y = self.graphik.getGameDisplay().get_size()
        width = 100
        height = 50
        xpos = x - width - 10
        ypos = y - height - 10
        self.graphik.drawButton(xpos, ypos, width, height, (255,255,255), (0,0,0), 30, "back", self.switchToWorldScreen)

    def handleMouseClickEvent(self, pos):
        # get inventory slot that was clicked
        backgroundX = self.graphik.getGameDisplay().get_width()/4
        backgroundY = self.graphik.getGameDisplay().get_height()/4
        backgroundWidth = self.graphik.getGameDisplay().get_width()/2
        backgroundHeight = self.graphik.getGameDisplay().get_height()/2
        itemsPerRow = 5
        row = 0
        column = 0
        margin = 5
        for inventorySlot in self.inventory.getInventorySlots():
            itemX = backgroundX + column*backgroundWidth/itemsPerRow + margin
            itemY = backgroundY + row*backgroundHeight/itemsPerRow + margin
            itemWidth = backgroundWidth/itemsPerRow - 2*margin
            itemHeight = backgroundHeight/itemsPerRow - 2*margin

            # if mouse click was inside inventory slot
            if pos[0] > itemX and pos[0] < itemX + itemWidth and pos[1] > itemY and pos[1] < itemY + itemHeight:
                index = row*itemsPerRow + column
                
                # select that inventory slot if right mouse button was clicked
                if pygame.mouse.get_pressed()[2]:
                    self.inventory.setSelectedInventorySlotIndex(index)
                    return

                # move item from inventory slot to cursor slot
                inventorySlotContents = inventorySlot.getContents()
                cursorSlotContents = self.cursorSlot.getContents()
                inventorySlot.setContents(cursorSlotContents)
                self.cursorSlot.setContents(inventorySlotContents)
                
            
            column += 1
            if column == itemsPerRow:
                column = 0
                row += 1
    
    def drawCursorSlot(self):
        if self.cursorSlot.isEmpty():
            return
        
        item = self.cursorSlot.getContents()[0]
        image = item.getImage()
        scaledImage = pygame.transform.scale(image, (50, 50))
        self.graphik.gameDisplay.blit(scaledImage, pygame.mouse.get_pos())

    def run(self):
        while not self.changeScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.nextScreen = ScreenType.NONE
                    self.changeScreen = True
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleMouseClickEvent(event.pos)
            
            self.graphik.getGameDisplay().fill((0, 0, 0))
            self.drawPlayerInventory()
            self.drawBackButton()
            self.drawCursorSlot()
            pygame.display.update()
        
        # empty cursor slot when exiting inventory screen
        if not self.cursorSlot.isEmpty():
            for item in self.cursorSlot.getContents():
                self.inventory.placeIntoFirstAvailableInventorySlot(item)
            self.cursorSlot.setContents([])
            
        self.changeScreen = False
        return self.nextScreen
    
    def setInventory(self, inventory):
        self.inventory = inventory