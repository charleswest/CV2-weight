import cv2
import numpy as np 
from cwUtils import cvd,cvs
import time, os, glob, timeit
from datetime import datetime
def register(im1,im2,p):
    '''
       555     center im1 on im2 and return two cropped versions suitable
      2   7    for bitwise operations.  Must take into account the seven possible
      2   7    orientations of panels  given by p values at left
       444
      1   6
      1   6
       333
    '''
    w1,  h1  = im1.shape[::-1]   # image
    w2,  h2 =  im2.shape[::-1]   # panel
    print 'image w {} h {} panel w {} h {}'.format(w1,h1,w2,h2)
    dv = h1-h2
    dh = (w1-w2)
        
    mv =  int (dv/2.0)      # vertical margin
    mh =  int (dh/2.0)      # horizontal margin
    print 'dv {} dh {}     mv {}   mh {}  '.format( dv, dh, mv,mh)
    if p in [1,2,3,4,5,6,7 ]:
        # trim panel
        yt1= abs(mv);     yt2 = yt1 +  min( h1,h2)
        xt1= abs(mh) ;    xt2 = xt1 +  min( w1,w2)
        
        y1 = max(0,mv);  x1=max(0,mh); y2 = min(h1,h2);   x2= min(w1,w2) 
     
 
    om1  =        im1[ y1:y2,   x1:x2] .copy()     #  image crop    
    om2  =        im2[yt1:yt2, xt1:xt2].copy()    #  template crop
    w1,  h1  = om1.shape[::-1]   # image
    w2,  h2 =  om2.shape[::-1]   # panel
    print 'om1 w {}, h {}   im2 w {}  h {}'.format(w1, h1,w2, h2)
    res = cv2.bitwise_and(om1,om2)
    print np.sum(res) / 255    # count of pixels 
    return(om1,om2)   # image cropped to panel dimensions
    


if __name__ == '__main__':
    typ = 'wt'
    path = ('C:\\Train\\{}1.png'.format( typ    ) )          #os.getcwd()
    pxpath = ('C:\\Train\\pxl\\{}*.png'.format( typ    ) )    
    print path        
    files = glob.glob(path)  
    db = True
    for f in files:                # read templates from Train
        img = cv2.imread(f,0)
        h,w = img.shape[:2]
        cvs(1,img,'wt4')
              #os.getcwd()
        #print path        
        xfiles = glob.glob(pxpath)  
        for n,ft in enumerate(xfiles):
            imgT = cv2.imread(ft,0)
            print f , ft ,n+1
            imgx,imgy = register(img,imgT,n+1)
            
            cvs(0,imgx,'xxxxx')
            cvs(1,imgy,'yyyyy')
            cvd()
            
    cvd()
