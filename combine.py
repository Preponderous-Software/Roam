# Description: Combines all the room images into one image

import os
from PIL import Image

# Get all the room images
room_images = os.listdir("roompngs")

# define number of rooms in each direction
num_rooms = 5

# define room size
roomSize = 100

# Create a new image to hold all the room images
combinedImageSize = (num_rooms * 2 + 1) * roomSize
new_image = Image.new("RGB", (combinedImageSize, combinedImageSize))

# save the new image
new_image.save("combined.png")

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
    new_image.paste(image, (int(combinedImageSize/2) + x * roomSize - int(roomSize/2), int(combinedImageSize/2) + y * roomSize - int(roomSize/2)))

# Save the new image
new_image.save("combined.png")