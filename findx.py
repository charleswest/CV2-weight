import cv2
import numpy as np
from cwUtils import *

img = cv2.imread('input.png',1)
cvs(1,img)

# Take each frame
frame = img

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)

 
cvs(1,mask,'mask')
cvs(1,res,'res')

cvd() 
   
