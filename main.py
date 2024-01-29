from exif import Image
from datetime import datetime
from picamera import PiCamera
import cv2 as cv
import math

cam = PiCamera()
cam.resolution = (4056, 3040)

cam.capture("image0.jpg")
cam.capture("image1.jpg")

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image0, image1):
    time_1 = get_time(image0)
    time_2 = get_time(image1)
    time_difference = time_2 - time_1
    return time_difference.seconds

print(get_time_difference('image0.jpg','image1.jpg'))

def convert_to_cv(image0, image1):
    image0_cv = cv.imread(image0, 0)
    image1_cv = cv.imread(image1, 0)
    return image0_cv, image1_cv

def calculate_features(image0, image1, feature_number):
    orb = cv.ORB_create(nfeatures = feature_number)
    keypoints0, descriptors0 = orb.detectAndCompute(image0_cv, None)
    keypoints1, descriptors1 = orb.detectAndCompute(image1_cv, None)
    return keypoints0, keypoints1, descriptors0, descriptors1

def calculate_matches(descriptors0, descriptors1):
    brute_force = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors0, descriptors1)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def display_matches(image0_cv, keypoints0, image1_cv, keypoints1, matches):
    match_img = cv.drawMatches(image0_cv, keypoints0, image1_cv, keypoints1, matches[:100], None)
    resize = cv.resize(match_img, (1600,600), interpolation = cv.INTER_AREA)
    cv.imshow('matches', resize)
    cv.waitKey(0)
    cv.destroyWindow('matches')

image0_cv, image1_cv = convert_to_cv('image0.jpg','image1.jpg')
keypoints0, keypoints1, descriptors0, descriptors1 = calculate_features(image0_cv, image1_cv, 1000)
matches = calculate_matches(descriptors0, descriptors1)
display_matches(image0_cv, keypoints0, image1_cv, keypoints1, matches)
