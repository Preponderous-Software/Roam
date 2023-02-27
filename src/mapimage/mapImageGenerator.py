# Description: Combines all the room images into one image

import os
from PIL import Image

# @author Daniel McCoy Stephenson
# @since February 2nd, 2023
class MapImageGenerator:
    def __init__(self, config):
        self.config = config

        self.numRoomsInEachDirection = 5
        self.roomSizeInPixels = 100
        self.mapImageSizeInPixels = (
            self.numRoomsInEachDirection * 2 + 1
        ) * self.roomSizeInPixels

        self.roomImagesDirectoryPath = self.config.pathToSaveDirectory + "/roompngs"
        self.mapImagePath = self.config.pathToSaveDirectory + "/mapImage.png"

        if self.mapImageExists():
            self.mapImage = self.getExistingMapImage()
        else:
            self.mapImage = self.createNewMapImage()

    # public methods

    def generate(self):
        roomImages = self.getRoomImages()
        self.pasteRoomImagesAtCorrectCoordinates(roomImages)
        return self.mapImage

    def clearRoomImages(self):
        for file in os.listdir(self.roomImagesDirectoryPath):
            os.remove(self.roomImagesDirectoryPath + "/" + file)

    # private methods

    def mapImageExists(self):
        return os.path.exists(self.mapImagePath)

    def getExistingMapImage(self):
        if self.config.debug:
            print("Loading existing map image")
        return Image.open(self.mapImagePath)

    def createNewMapImage(self):
        if self.config.debug:
            print("Creating new map image")
        return Image.new(
            "RGB", (self.mapImageSizeInPixels, self.mapImageSizeInPixels), "white"
        )

    def getRoomImages(self):
        return os.listdir(self.roomImagesDirectoryPath)

    def pasteRoomImagesAtCorrectCoordinates(self, roomImages):
        # save the new image
        numPasted = 0
        numOutOfBounds = 0

        # Loop through all the room images
        for room_image in roomImages:
            # Open the room image
            image = Image.open(self.roomImagesDirectoryPath + "/" + room_image)

            # scale image down
            roomSize = 100
            image = image.resize((roomSize, roomSize))

            # Get the room number from the image name
            room_number = room_image.split(".")[0].split("_")
            # Get the x and y coordinates of the room
            x = int(room_number[0])
            y = int(room_number[1])

            # Paste the room image onto the new image at the correct coordinates
            picX = int(self.mapImageSizeInPixels / 2) + x * roomSize - int(roomSize / 2)
            picY = int(self.mapImageSizeInPixels / 2) + y * roomSize - int(roomSize / 2)
            if (
                picX >= 0
                and picY >= 0
                and picX < self.mapImageSizeInPixels
                and picY < self.mapImageSizeInPixels
            ):
                self.mapImage.paste(image, (picX, picY))
                numPasted += 1
            else:
                numOutOfBounds += 1

        if self.config.debug:
            print("Images pasted: " + str(numPasted))
            print("Images out of bounds: " + str(numOutOfBounds))
            print(
                "Percent of map updated: "
                + str(
                    int(numPasted / (self.numRoomsInEachDirection * 2 + 1) ** 2 * 100)
                )
                + "%"
            )
