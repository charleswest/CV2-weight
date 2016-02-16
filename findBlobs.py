# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
global db
from cwUtils import cvs, cvd , erode, dilate

db = True
def stdSize(imgx,typ):
    h,w = imgx.shape[:2]   #   h = rows,  w = cols
    if typ == 'wt':
        nw = 800
    else:
        nw = 400
   
    nh =   h * (float(nw) / float(w))  
    print 'stdSize height {} typ {} nw {}'.format( nh, typ, nw)
    imgy =  cv2.resize(imgx, ( nw, int (nh) )  )    # maintain aspect ratio
    
    return imgy.copy()
def  boundsBlob(grp):
    # x, y, w, h    given the following x,y pairs
#     [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
    x,y = grp[0][0][0]
    mxy = y
    #print x,y
    for  cn in grp:
        for blb in cn:
                #print y,
                cx,cy  = blb[0] 
                 
                if cx  < x: x = cx                #  find least x
                if cx  > x: w = cx - x
                
                if cy < y: y = cy                #  find max y
                if cy > mxy: mxy = cy
                #print 'y and mxy', y,mxy
    h = mxy - y
    return( x,y,w,h)
def  findBlobs(imx,ms,mx,erd,db,tval=127):
  
    Erd = erd
    Drd = int(Erd/2) 
    print 'This is find blobs  1.0 ms {} mx {} erd {} drd {}'.format( ms, mx , Erd ,Drd)
    imgray = cv2.cvtColor(imx,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,tval,255,0)
    thresh = erode(thresh,Erd)
    thresh = dilate(thresh,Drd)
    #print 'db findBlobs' , db
    cvs(db,thresh)
    cmask = thresh.copy()
    im3,cnt, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #  note lamda is expression for leftmost extreme of the contour
    scon  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
 
    rvl = []
    for con in scon:
       area = cv2.contourArea(con)
       #if db: print  area,
       
       cnt_len = cv2.arcLength(con, True)                          
       cntp = cv2.approxPolyDP(con, 0.02*cnt_len, True)
 #      print len(cntp)  #    look for suitable contours
       x,y,w,h = cv2.boundingRect(con)
       asp = abs(  w - h  )
       #if db: print 'abs|w-h| {}  w {} h {} '.format(asp,w,h)
       if (  len(cntp) > 3                   # at least 4  
             and  asp > .1                      # ie not round or square
             and  area > ms
             and  area < mx  ):          # note (   ...   ) for implied continuation
            rvl.append(con)
            cv2.drawContours(imx,[con], 0, (0,255,255), 2)    # yellow
        
       else:
          cv2.drawContours(imx,[con], 0, (0,0,255), 2)       #  red
          
      #  if db:cvs(db,imx,t=0)
    return (rvl,cmask)
   
if __name__ == '__main__':
    db = False
    tst = 'wt'
    imgx = cv2.imread(tst +'Test.png') 
    #imgx = cv2.imread(fn)
    img = stdSize(imgx,tst)   #cv2.resize(imgx, (1040,410))
    srt = img.copy()
    h,w = img.shape[:2]  
 
    #cvs(db,img)
    ms =  325;    mx = 10000;  erd =12; tx=160
    (cnt,cmask) =  findBlobs( img,ms,mx,erd,db,tx) # will modify img to show cnt
    cnt  =   sorted(cnt, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
    print ' input is {} width {} height {} ms {} mx {} tval {}   '\
          .format(tst,w, h,ms,mx,tx)
    x,y,w,h = boundsBlob(cnt)
    print (x,y,w,h)
    tl = (x-10,y-10) ; br = ( x  +  w+10, y+ h+10)       #  10 for more room
    cv2.rectangle(img,(tl),(br),(255,255,255),5)       # white rectangle
    for i, f in enumerate (cnt):
        
        cv2.drawContours(img,[f],0,(255,0,0),2)
##        x,y,w,h = cv2.boundingRect(f)
##        a =  cv2.contourArea(f)
##        asp = round(abs( 1.00 - float(w)/float(h) ),2)
##        print 'x {}  y {}\tw {}\th {}\ta {}\tasp {} '.format( x, y , w, h,a,asp)
    cvs(1,cmask)    
    cvs(1,img,t=0)
 
    cvd()
