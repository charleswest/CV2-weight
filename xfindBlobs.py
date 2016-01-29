# -*- coding: utf-8 -*-
import numpy as np
import cv2
from cwUtils import cvs, cvd ,db, erode, dilate
def bdup(xy,z,t):
   ''' is xy in z '''
   #print 'look for xy', xy
   retVal = False
   for (x,y) in z:
         
         s =   3 * abs( x-xy[0] )+  abs(y-xy[1]) 
         sm = np.sqrt(s)
         if sm < t+1 and sm > t: print '{},{}\t{}'.format(x, y,  round( sm,2))
         if sm < t:             
             return(True)
            
def bfilter(blobs):
   ''' look for right sized blobs '''   
   print 'bfilter'
##   bs =  sorted( blobs, key = lambda b: b[0][0]  ) 
##   for (x,y), r,a, i in bs:                
##         print 'xy\t{},{}\tr {}'.format(x, y,  r)
    
# fs = findBlobs(img,threshval=tval,minsize=ms, maxsize= mx  )  
                  
def  findBlobs(imgx,ms,mx,T=xrange(0,255,26)):
    global db
    Tx = 5            #    Tx is tolerance in pixels for duplicate blob
    h , w  = imgx.shape[:2]
##    if rs == True:
##       imgx  =  cv2.resize(imgx, (4*w,4*h))  
##       ms = 16 * ms; mx = 16 * mx
     
    img = cv2.GaussianBlur(imgx, (5, 5), 0) 
    blobs = []   
    Blobs = np.array(blobs)
    bix = 0
    lim = 0  #j in 0 1 2
    for j, gray in enumerate(cv2.split(img)):        
        
        for thrs in T:        #  from 0 to 255 in steps of 26  ~ 10 steps
            print 'thrs ' , thrs
            if thrs == 0:
                binaryimg = cv2.Canny(gray, 0, 50, apertureSize=5)
                binaryimg = cv2.dilate(binaryimg, None)
                continue
            else:
                retval, binaryimg = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
##                binaryimg = erode(binaryimg,Erd)
##                binaryimg = dilate(binaryimg,1)
                #cvs(binaryimg,'Grey',0)
            im2, contours, hierarchy = cv2.findContours(binaryimg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for i,cnt in enumerate(contours):
                cnt_len = cv2.arcLength(cnt, True)
                               
                cntp = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
               
                if len(cntp) > 3 and cv2.contourArea(cntp) > ms \
                                 and cv2.contourArea(cntp) < mx \
                                 and cv2.isContourConvex(cntp):
                    #oshp = cntp.shape
                    cntp = cntp.reshape(-1, 2)   # number of vertexs on polygon
                    #print np.min(cntp[0])
                    (x,y),z   =  cv2.minEnclosingCircle(cnt)
                    area = cv2.contourArea(cnt)
                    cx=int(x ); cy = int( y) ; r = int(z )                    

                    dup = False
                    if not dup:                        
                        bix = bix + 1
                        blobs.append([  (cx,cy)  ,r ,area ,cntp    ])
                        Blobs = np.array(blobs)

 
        print 'end split 88 i {} blobs {}'.format(i, len(blobs))                          
        if j == lim:
           print 'early exit'
           bfilter(blobs)
           return  contours,np.array(blobs)      #  stop after first Blue color channel
    return contours,nparray.blobs
                      

if __name__ == '__main__':
    db = True
    fn = 'trouble.png'
    fn = 'h2oTest.png'

    img = cv2.imread(fn)
    h,w = img.shape[:2]  
    print ' input is {} width {} height {}  '.format(fn,w, h )
    cvs(img,'input', 500)
    ms = 150
    mx = 600
    x,Blobs =  findBlobs( img,ms,mx) # Tx dup tolerance
    
    print 'blobs found {}  ms {}'.format( len(Blobs), ms)
    sblb  = np.array(sorted( Blobs, key = lambda b: b[0][0] )  )     # sort on first x.
    # sblb = Blobs
    print ' sblb  circle', len(sblb)
    # print sblb[:,0:3]
    print 'sblb contours', ms, mx
 #   con = np.array(sblb[:,2:3])
    for c,r,a,i   in sblb:       
        cv2.drawContours( img, np.int32([i]), -1, (0, 255, 255), 5 )      
        #cv2.polylines(img, np.int32([i]),True, (0,255,255),2)      
        cv2.circle(img, c, int(r), (0,0,255) ,3)
        print 'c {}  r {}   a {}'.format(c, r, a ) 
        cvs(img,'sorted',200)


    cvs(img,'sorted',50)
    x = cv2.waitKey()
    cvd()
