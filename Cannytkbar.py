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
cv2.createTrackbar('R50','image',0,500,nothing)
cv2.createTrackbar('G150','image',0,500,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cvd()
        break
    if k == ord('s'):
#        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print 'r {}g {} b{} s{}'.format(r,g,b,s)

        fil = "img3c.png"
        #fil = 'lineTest.png'
        db = True
        img = cv2.imread(fil )
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([108,40,223])   #np.array([110,50,50])
        upper_blue = np.array( [255,255,255])   #np.array([130,255,255])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        cvs(0,mask,'mask') 
        

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R50','image')
    g = cv2.getTrackbarPos('G150','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

##    if s == 0:
##        img[:] = 0
##    else:
##        img[:] = [b,g,r]
        

cv2.destroyAllWindows()
