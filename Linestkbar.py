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
#cv2.createTrackbar('B','image',0,255,nothing)

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
        img = cv2.imread(fil)
        lines = findLines(img,r,g )      # 300  30   
        print 'lines shape ', lines.shape
        print '__________________________________'

        for xx in lines:
            print xx
            for x1,y1,x2,y2 in xx:
                angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
                #print 'x1,y1 {},{}\t x2,y2 {},{} \tangle {}'.format(x1,y1,x2,y2,angle)
                cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        #print ' db',db
        #cvs(db,img)  # display marked up image
        #cvd()

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

##    if s == 0:
##        img[:] = 0
##    else:
##        img[:] = [b,g,r]
        

cv2.destroyAllWindows()
