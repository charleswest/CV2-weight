import cv2
import numpy as np
from cwUtils import *
from findLines import findLines 
global db
def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((500,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('minline','image',0,500,nothing)
cv2.createTrackbar('maxgap','image',0,500,nothing)
cv2.createTrackbar('votes','image',0,100,nothing)
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cvd()
        break
    if k == ord('s'):
    #        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print 'minline {}  maxgap {} '.format(r,g)

        fil = "img3c.png"
        #fil = 'lineTest.png'
        db = False
        img = cv2.imread(fil)
        minline = r
        maxgap = g
        lines = findLines(img,minline,maxgap,v)      # 300  30
        if lines is not None and lines.any:
            print '{} lines found  '.format(len(lines))
            for i,xx in enumerate (lines):
                if i > 10: break
                for x1,y1,x2,y2 in xx:
                    angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
                    #print 'x1,y1 {},{}\t x2,y2 {},{} \tangle {}'.format(x1,y1,x2,y2,angle)
                    cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
           
        else: print 'no lines found',

    r = cv2.getTrackbarPos('minline','image')
    g = cv2.getTrackbarPos('maxgap','image')
    v = cv2.getTrackbarPos('votes','image')

cv2.destroyAllWindows()
