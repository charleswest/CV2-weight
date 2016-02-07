import cv2
import numpy as np
from cwUtils import *
from findLines import findLines 
global db
def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):     # rgb  113 192 119
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:        
        break
    if k == ord('s'):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h,s,v = hsv[0][0]
        h = int(h); s = int(s); v= int(v)
        print 'hsv',h,s,v
        fil = "img3c.png"
        #fil = 'lineTest.png'
        db = True
        imgx = cv2.imread(fil )
        cvs(0,img)
        hsvx = cv2.cvtColor(imgx, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([h,s,v])   #np.array([110,50,50])
        #lower_blue = np.array([23,7,154])   #np.array([110,50,50])
        upper_blue = np.array( [255,255,255])   #np.array([130,255,255])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsvx, lower_blue, upper_blue)
        cvs(0,mask,'mask')

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
        

cv2.destroyAllWindows()
