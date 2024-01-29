from exif import Image
from datetime import datetime
from picamera import PiCamera

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

print(get_time_diffrence('image0.jpg','image1.jpg'))
