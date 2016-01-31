# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
global db
from cwUtils import cvs, cvd , erode, dilate

db = True                   
def  findBlobs(imx,ms,mx,db,tval=127):
    
     
    Erd = 2
    print 'This is find blobs  1.0 ms mx db', ms, mx ,db
    imgray = cv2.cvtColor(imx,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,tval,255,0)
    thresh = erode(thresh,Erd)
    thresh = dilate(thresh,1)
    #print 'db findBlobs' , db
    cvs(db,thresh)
    im3,cnt, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #  note lamda is expression for leftmost extreme of the contour
    scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
 
    rvl = []
    for con in scon:
       area = cv2.contourArea(con)
#       if db: print  area
       cnt_len = cv2.arcLength(con, True)                          
       cntp = cv2.approxPolyDP(con, 0.02*cnt_len, True)
##        and cv2.contourArea(cntp) > ms \
##        and cv2.contourArea(cntp) < mx \
 #      print len(cntp)  #    look for suitable contours
       x,y,w,h = cv2.boundingRect(con)
       if len(cntp) > 3  \
          and cv2.isContourConvex(cntp) \
             and abs( 1.0 - float(w)/float(h) ) > .1 \
             and  area > ms and area < mx:
            rvl.append(con)
            cv2.drawContours(imx,[con], 0, (0,255,255), 2)    # yellow
        
       else:
          cv2.drawContours(imx,[con], 0, (0,0,255), 2)       #  red
          
#       if db:cvs(db,imx,'included')
    return rvl
   
if __name__ == '__main__':
    global db
   
    db = False
    print 'funny ', db
    fn = 'trouble.png'
    fn = 'h2oTest.png'
##    fn = 'cropTest.png'
##    fn = 'wtTest.png'
    fn = 'fatTest.png'
    imgx = cv2.imread(fn)
    img = cv2.resize(imgx, (1040,410))
    srt = img.copy()
    h,w = img.shape[:2]  
    print ' input is {} width {} height {}  '.format(fn,w, h )
    d = 0
##    img = erode(img,4)
##    img = dilate(img,0)
    #cvs(db,img)
    ms = 1500
    mx = 10000
    cnt =  findBlobs( img,ms,mx,db) # will modify img to show cnt
    cnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    for f in cnt:
        cv2.drawContours(srt,[f],0,(255,0,0),2)
        print 'array f ',  f[0] ,
        x,y,w,h = cv2.boundingRect(f)
        a =  cv2.contourArea(f)
        asp = round(abs( 1.00 - float(w)/float(h) ),2)
        print 'x {}  y {}\tw {}\th {}\ta {}\tasp {} '.format( x, y , w, h,a,asp)
        cvs(db,srt,'rtnd')
     
        
    print '{} blobs found'.format (len(cnt))
    cvs(db,img)
    cv2.drawContours(srt,cnt,-1,(0,255,255),2)            # green line w 3
    
    #print cnt
 

    cvs(db,srt,'rtnd',50)
    x = cv2.waitKey()
    cvd()
