import cv2
import numpy as np 
from cwUtils import cvd,cvs
import time, os, glob, timeit
from datetime import datetime

print __doc__
def tMatch(im1,typ,db):
    
    cvs(db,im1)
    path = ('C:\\Train\\pxl\\{}P*.png'.format( typ    ) )          #os.getcwd()
    #print path        
    files = glob.glob(path)  
    rtn = ['0','0','0','0','0','0','0']
    for n,f in enumerate(files):                # read templates from Train
        print f[9:-4],        
        im2 = cv2.imread(f,0)
        
        w1,  h1  = im1.shape[::-1]   # image
        w2,  h2 =  im2.shape[::-1]   # panel
        print 'image w {} h {} panel w {} h {}'.format(w1,h1,w2,h2)
        dv = h1-h2
        dh = (w1-w2)
            
        mv =  int (dv/2.0)      # vertical margin
        mh =  int (dh/2.0)      # horizontal margin
        #if db: print 'dv {} dh {}     mv {}   mh {}  '.format( dv, dh, mv,mh)

        yt1= abs(mv);     yt2 = yt1 +  min( h1,h2)    # set up panel crop
        xt1= abs(mh) ;    xt2 = xt1 +  min( w1,w2)
            
        y1 = max(0,mv);     x1 = max(0,mh);
        y2 = min(h1,h2);    x2 = min(w1,w2) 
     
 
        om1  =        im1[ y1:y2,   x1:x2] .copy()     #  image crop    
        om2  =        im2[yt1:yt2, xt1:xt2].copy()    #  template crop
        if db:
            cvs(1,om1,'x')
            cvs(1,om2,'y')
        w1,  h1  = om1.shape[::-1]   # image
        w2,  h2 =  om2.shape[::-1]   # panel
        #print 'om1 w {}, h {}   im2 w {}  h {}'.format(w1, h1,w2, h2)
        res = cv2.bitwise_and(om1,om2)
        pxlcnt = np.sum(res) / 255    # count of pixels 
        if db:
            print pxlcnt, 'count of pixels'
            cv2.waitKey(0)
        
        if pxlcnt  > 300 :
            rtn[n] = '1'
             
    
    drtn = ''.join(rtn)
   
    print 'ptrn ', rtn , drtn
    ''' ptrn translates the results of the pattern analysis into numbers '''
    ptrn = {
           '1110111' :  0,
           '1100000' :  1,                    
           '1011101' :  2,                    
           '0011111' :  3,
           '0101011' :  4,
           '0111110' :  5,
           '1111110' :  6,
           '0000111' :  7,  
           '1111111' :  8,
           '0111111' :  9
           }
    try:
        n = ptrn[drtn]    
        return(n)
    except  KeyError:
        return 'p'
    
if __name__ == '__main__':
    typ = 'wt'
    path = ('C:\\Train\\{}1.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = True
    fwt = 'wtTest.png'
    img = cv2.imread(fwt,0)
    cvs(db,img)
    pxls =  tMatch(img,typ,db)    # search for a number
    print 'number is',pxls
    
##    for f in files:                # read templates from Train
##        img = cv2.imread(f,0)
##        h,w = img.shape[:2] 
##        print 'img w h      file    ', w, h ,f 
##        

##      
##        cvs(1,img)
    cvd()

