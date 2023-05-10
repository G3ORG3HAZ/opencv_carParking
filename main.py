import cv2
import pickle
import cvzone
import numpy as np
import threading
import time

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

#get the size of the list the holds the x,y values of each parking space
# the index in the list represents the place of the parking spot    
list_size = len(posList)

#false meaning occupied while true means that it is available
boolean_list = [False for _ in range(list_size)]

print(boolean_list)


width, height = 107, 48


def task():
    while True:
        # Your code here
        print("print boolean list")
        for index, item in enumerate(boolean_list):
            if item:
                print(f'\033[1;32m{index}: True\033[0m')  # Green color for True
            else:
                print(f'\033[1;31m{index}: False\033[0m')  # Red color for False
        time.sleep(5)
        print("\n" * 5)



        
thread = threading.Thread(target=task)
thread.start()





def checkParkingSpace(imgPro):
    spaceCounter = 0#initilizes a counter for the number of free parking spaces

    for index, pos in enumerate(posList):#iterates over each parking space
        x, y = pos#extracts the x and y coordinates of the top-left corner of the parking space

        imgCrop = imgPro[y:y + height, x:x + width]#crops the input image to the size of the parking space
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)#counts the number of non-zero (white) pixels in the cropped image

        #less than 900 meaning it is empty spot
        if count < 900:# Checks if the count of non-zero pixels is less than a certain threshold (900 in this case).
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            boolean_list[index] = True
        else:
            color = (0, 0, 255)
            thickness = 2
            boolean_list[index] = False

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#converts the frame to grayscale using cv2.cvtColor()
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)#to reduce noise and smooth the image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)#it applies adaptive thresholding  to segment the image into foreground and background pixels
    imgMedian = cv2.medianBlur(imgThreshold, 5)# further remove noise.
    kernel = np.ones((3, 3), np.uint8)#
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)# fill in small gaps and connect nearby edges.

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)





