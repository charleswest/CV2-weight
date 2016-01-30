import cv2
import numpy as np
from cwUtils import *

img = cv2.imread('input.png')
h,w = img.shape[:2]
print 'image h  w',  h, w
cvs(img)
YELLOW =  (0,255,255)   # useful color definition
# Take each frame
frame = img

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([50,50,110])   #np.array([110,50,50])
upper_blue = np.array( [255,255,255])   #np.array([130,255,255])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)
#  find the contour of the mask which needs to be greyscale
#imgx = cv2.cvtColor(mask,cv2.COLOR_HSV2BGR_FULL )
cvs(mask)
cv2.imwrite('tempgray.png',mask)
imgx = cv2.imread('tempgray.png',0)
ret,thresh = cv2.threshold(imgx,127,255,0)

im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) > 1000:
        x,y,w,h = cv2.boundingRect(cnt)
        #cv2.rectangle(img,(x,y),(x+w,y+h),YELLOW,5)
        print 'xy### wh', x , y, w, h , cv2.contourArea(cnt)
        img3c = img[ y-3:y+h+3 ,x:x+w ].copy()
        cv2.imwrite('img3c.png',img3c)
        cvs(img3c)
        break
# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)
cvs(res)
 
cvd() 
   
