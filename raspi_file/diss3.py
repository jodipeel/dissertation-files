#import all necessary libraries
import cv2 as cv
from picamera2 import Picamera2, Preview
from PIL import Image, ImageEnhance
import urllib
import http.client
import time
import os

#api key for thingspeak channel
key="1JJJC4CZVAUIW7CZ"

#function to preprocess the image: brighten the image, image thresholding and then resizing for
#less computation time
def process_img():
    img = Image.open("/home/pi/Desktop/img.jpg")
    enh = ImageEnhance.Brightness(img)
    enh.enhance(2.0)
    img.save("/home/pi/Desktop/img.jpg")
    
    image = cv.imread("/home/pi/Desktop/img.jpg", cv.IMREAD_GRAYSCALE)
    image = cv.resize(image, (640, 480), interpolation=cv.INTER_AREA)
    #cv.imwrite("/home/pi/Desktop/imgbw.jpg", image)
    
    _, thresh = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    #cv.imwrite("/home/pi/Desktop/threshed_please.jpg", thresh)
    return thresh

#function for sending data to thingspeak, post request script using http.client and urllib
def send_to_ts(data, key):
    params = urllib.parse.urlencode({'field1': data, 'api_key': key})
    print(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPSConnection("api.thingspeak.com:443")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
    except:
        print("didnt work")
    
#function for running the camera and taking an image
#no prview shown to reduce processing
def run_cam():
    cam = Picamera2()
    cam.start_preview(Preview.NULL)
    cam.start_and_capture_file("/home/pi/Desktop/img.jpg")
    cam.stop()
    cam.stop_preview()
    
#function for instantiating the model and returning the number of people in the image
#captured by the connected camera
def detect_people():   
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    image = process_img()
    (regions, _) = hog.detectMultiScale(image, winStride=(3, 3), padding=(3, 3), scale=1.05)
    x = len(regions)
    return x



#while True:   while loop commented out while not in use
    try:
        time.sleep(2)
        run_cam()
        time.sleep(1)
        num = detect_people()
        time.sleep(1)
        send_to_ts(num, key)
        if os.path.exists("/home/pi/Desktop/img.jpg"):
            os.remove("/home/pi/Desktop/img.jpg")
    except:
        print("Something went wrong.")
        break


