# Import all necessary libraries
from picamera import PiCamera
from time import sleep

# Variables
num_pics = 3


# Setting up camera
cam = PiCamera()
cam.resolution = (4056, 3040)

# Taking 4 pictures with equal intervals
cam.capture("image0.png")
for i in range(num_pics-1):
    sleep(60 * (9/(num_pics-1)))
    cam.capture(f"image{i+1}.png")
cam.close()
