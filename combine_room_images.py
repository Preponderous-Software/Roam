# Description: Combines all the room images into one image

import os
import time
from PIL import Image

def combineRoomImages():
    # Get all the room images
    room_images = os.listdir("roompngs")

    # define number of rooms in each direction
    num_rooms = 5

    # define room size
    roomSize = 100

    if not os.path.exists("combined.png"):
        # Create a new image to hold all the room images
        combinedImageSize = (num_rooms * 2 + 1) * roomSize
        new_image = Image.new("RGB", (combinedImageSize, combinedImageSize))
        print("Created new image")
    else:
        new_image = Image.open("combined.png")
        combinedImageSize = new_image.size[0]
        print("Loaded existing image")

    # save the new image
    new_image.save("combined.png")

    numPasted = 0
    numOutOfBounds = 0

    # Loop through all the room images
    for room_image in room_images:
        # Open the room image
        image = Image.open("roompngs/" + room_image)

        # scale image down
        roomSize = 100
        image = image.resize((roomSize, roomSize))

        # Get the room number from the image name
        room_number = room_image.split(".")[0].split("_")
        # Get the x and y coordinates of the room
        x = int(room_number[0])
        y = int(room_number[1])
        
        # Paste the room image onto the new image at the correct coordinates
        picX = int(combinedImageSize/2) + x * roomSize - int(roomSize/2)
        picY = int(combinedImageSize/2) + y * roomSize - int(roomSize/2)
        if picX >= 0 and picY >= 0 and picX < combinedImageSize and picY < combinedImageSize:
            new_image.paste(image, (picX, picY))
            numPasted += 1
        else:
            numOutOfBounds += 1

    # clear roompngs folder
    for room_image in room_images:
        os.remove("roompngs/" + room_image)
        
    print("Images pasted: " + str(numPasted))
    print("Images out of bounds: " + str(numOutOfBounds))

    print("Percent of map updated: " + str(int(numPasted / (num_rooms * 2 + 1) ** 2 * 100)) + "%")

    # Save the new image
    new_image.save("combined.png")
    print("Saved combined.png")

while True:
    combineRoomImages()

    # wait 30 seconds
    time.sleep(30)