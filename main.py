# import all necessary libraries
from picamera import PiCamera
from time import sleep
from exif import Image
from datetime import datetime
import cv2
import math

# (?)
import PIL

# (?) constant variables
num_pics = 4

# Setting up camera
cam = PiCamera()
cam.resolution = (4056, 3040)

# taking pictures with equal intervals
cam.capture("image0.png")
for i in range(num_pics-1):
    sleep(60 * (9/(num_pics-1)))
    cam.capture(f"image{i+1}.png")
cam.close()

# (?) making image variables
image0 = PIL.Image.open('image0.png')
image1 = PIL.Image.open('image1.png')
image2 = PIL.Image.open('image2.png')
image3 = PIL.Image.open('image3.png')

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
diff_2 = get_time_difference(image2, image3)

# function for converting images to cv format
def convert_to_cv(image_1, image_2):
    image0_cv = cv2.imread(image_1, 0)
    image1_cv = cv2.imread(image_2, 0)
    return image0_cv, image1_cv

# function for calculating features of two images
def calculate_features(image_1, image_2, feature_number):
    orb = cv2.ORB_create(nfeatures = feature_number)
    keypoints1, descriptors1 = orb.detectAndCompute(image0_cv, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image1_cv, None)
    return keypoints1, keypoints2, descriptors1, descriptors2

# function for calculating matches from two sets of descriptors
def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

# getting matches between two images
image0_cv, image1_cv = convert_to_cv(image0, image1)
keypoints0, keypoints1, descriptors0, descriptors1 = calculate_features(image0_cv, image1_cv, 1000)
matches = calculate_matches(descriptors0, descriptors1)
print(matches)
