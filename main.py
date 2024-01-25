# import all necessary libraries
from picamera import PiCamera
from time import sleep
from exif import Image
from datetime import datetime

# (?)
import PIL

# variables
num_pics = 2

# Setting up camera
cam = PiCamera()
cam.resolution = (4056, 3040)

# taking pictures with equal intervals
cam.capture("image0.png")
for i in range(num_pics-1):
    sleep(60 * (9/(num_pics-1)))
    cam.capture(f"image{i+1}.png")
cam.close()

# making image variables (?)
image0 = PIL.Image.open('image0.png')
image1 = PIL.Image.open('image1.png')

# function for returning time picture was taken
def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

# funtion for returning time diffrence between when two images were taken
def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

# getting time diffrence
diff_1 = get_time_difference(image0, image1)
