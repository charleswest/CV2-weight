import cv2
import numpy as np
from cwUtils import *
from findBlobs import findBlobs
global db
''' Track Bar for Blob finding'''
def nothing(x):
    #print 'x is ', x     # the value of the slider
    pass

# Create a black image, a window
imgx = np.zeros((200,600,3), np.uint8)
cv2.namedWindow('image')


# create trackbars for color change
cv2.createTrackbar('min','image',0,1500,nothing)
cv2.createTrackbar('max','image',0,10000,nothing)
cv2.createTrackbar('tval','image',0,255,nothing)
cv2.createTrackbar('erd','image',0,20,nothing)
while(1):
    cv2.imshow('image',imgx)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cvd()
        break
    if k == ord('s'):
        fil = "img3c.png"
        fil = 'fatTest.png'
        db = False
        img = cv2.imread(fil)
        blobs = findBlobs(img,ms,mx,erd,db,tval)      # 500 3000 2 160
        if blobs is not None :
            print '{} blobs found  '.format(len(blobs))
            for i,f in enumerate (blobs):
                if i > 20: break
                cv2.drawContours(img,[f],0,(0,0,0),2)
                cvs(0,img,'contours')
           
        else: print 'no blobs found',

    ms = cv2.getTrackbarPos('min','image')
    mx = cv2.getTrackbarPos('max','image')
    erd = cv2.getTrackbarPos('erd','image')
    tval = cv2.getTrackbarPos('tval','image')

cv2.destroyAllWindows()
