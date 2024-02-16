# import all libraries needed
from exif import Image
from time import sleep
from datetime import datetime
from picamera import PiCamera
import cv2 as cv
import math

# define PiCamera reference as 'cam' variable
cam = PiCamera()
cam.resolution = (4056, 3040)

# take 2 pictures with 7 seconds between and repeat this process 3 times with 30 seconds between
cam.capture("image0.jpg")
sleep(7)
cam.capture("image1.jpg")
sleep(30)
cam.capture("image2.jpg")
sleep(7)
cam.capture("image3.jpg")
sleep(30)
cam.capture("image4.jpg")
sleep(7)
cam.capture("image5.jpg")

# function that returns the exact time a picture was taken
def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time 

# function for returning time diffence between two pictures utilizing the get_time function
def get_time_difference(image0, image1):
    time_1 = get_time(image0)
    time_2 = get_time(image1)
    time_difference = time_2 - time_1
    return time_difference.seconds

# function that converts two images into cv format for further processing
def convert_to_cv(image0, image1):
    image0_cv = cv.imread(image0, 0)
    image1_cv = cv.imread(image1, 0)
    return image0_cv, image1_cv

# function that returns 2 lists of keypoints and 2 list of descriptors from 2 pictures
def calculate_features(image0_cv, image1_cv, feature_number):
    orb = cv.ORB_create(nfeatures = feature_number)
    keypoints0, descriptors0 = orb.detectAndCompute(image0_cv, None)
    keypoints1, descriptors1 = orb.detectAndCompute(image1_cv, None)
    return keypoints0, keypoints1, descriptors0, descriptors1

# function that takes 2 sets of descriptors from diffrent pictures and returns a list of matches between them
def calculate_matches(descriptors0, descriptors1):
    brute_force = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors0, descriptors1)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

# function that uses 2 lists of keypoints to return the corresponding coordinates
def find_matching_coordinates(keypoints0, keypoints1, matches):
    coordinates0 = []
    coordinates1 = []
    for match in matches:
        image0_idx = match.queryIdx
        image1_idx = match.trainIdx
        (x1,y1) = keypoints0[image0_idx].pt
        (x2,y2) = keypoints1[image1_idx].pt
        coordinates0.append((x1,y1))
        coordinates1.append((x2,y2))
    return coordinates0, coordinates1 

# function that uses the 2 list of coordinates to calculate the mean coordinates
def calculate_mean_distance(coordinates0, coordinates1):
    all_distances = 0
    merged_coordinates = list(zip(coordinates0, coordinates1))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

# function that uses feature distance and time diffeence to return the speed
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference
    return speed 

# finds the time diffrences between the pictures in all picture pairs
diff0 = get_time_difference('image0.jpg','image1.jpg')
diff1 = get_time_difference('image2.jpg','image3.jpg')
diff2 = get_time_difference('image4.jpg','image5.jpg')

# converts all 6 pictures to cv format
image0_cv, image1_cv = convert_to_cv('image0.jpg','image1.jpg')
image2_cv,image3_cv = convert_to_cv('image2.jpg','image3.jpg')
image4_cv,image5_cv = convert_to_cv('image4.jpg','image5.jpg')

# calculates all the sets of keypoints and descriptors using the calculate_features function
keypoints0, keypoints1, descriptors0, descriptors1 = calculate_features(image0_cv, image1_cv, 1000)
keypoints2, keypoints3, descriptors2, descriptors3 = calculate_features(image2_cv, image3_cv, 1000)
keypoints4, keypoints5, descriptors4, descriptors5 = calculate_features(image4_cv, image5_cv, 1000)

# finds the matches between the sets of descriptors using the calculate_matches function
matches0 = calculate_matches(descriptors0, descriptors1)
matches1 = calculate_matches(descriptors2, descriptors3)
matches2 = calculate_matches(descriptors4, descriptors5)

# finds the coordinates that match the previously calculated sets of keypoints and matches(between descriptors)
coordinates0, coordinates1 = find_matching_coordinates(keypoints0, keypoints1, matches0)
coordinates2, coordinates3 = find_matching_coordinates(keypoints2, keypoints3, matches1)
coordinates4, coordinates5 = find_matching_coordinates(keypoints4, keypoints5, matches2)

# uses the calculate_mean_distance function to find the average feature distance from the sets of coordinates
average_feature_distance0 = calculate_mean_distance(coordinates0, coordinates1)
average_feature_distance1 = calculate_mean_distance(coordinates2, coordinates3)
average_feature_distance2 = calculate_mean_distance(coordinates4, coordinates5)

# calculates the speeds for all 3 sets of pictures
speed0 = calculate_speed_in_kmps(average_feature_distance0, 12648, diff0)
speed1 = calculate_speed_in_kmps(average_feature_distance1, 12648, diff1)
speed2 = calculate_speed_in_kmps(average_feature_distance2, 12648, diff2) 

# calculates mean distance of all speeds and converts it to a string format for writing in .txt file
speed = str((speed0+speed1+speed2)/3)

# opens/creates the result.txt file
result_txt = open('result.txt', 'w')
if(speed[1]=="."): # checks whether there are 1 or 2 characters before the dot in the speed variable
    result_txt.write(speed[:6]) # write the first six characters if there is only one before the dot
else:
    result_txt.write(speed[:7]) # write the first seven characters if there are 2 before the dot
result_txt.close() #close the the result.txt file
