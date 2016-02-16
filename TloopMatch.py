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
        print 'Tmatch', f[9:-4],        
        im2 = cv2.imread(f,0)
        
        w1,  h1  = im1.shape[::-1]   # image
        w2,  h2 =  im2.shape[::-1]   # panel
        if db: print 'image w {} h {} panel w {} h {}'.format(w1,h1,w2,h2)
        dv = h1-h2
        dh = (w1-w2)
            
        mv =  int (dv/2.0)      # vertical margin
        mh =  int (dh/2.0)      # horizontal margin
        if db: print 'dv {} dh {}     mv {}   mh {}  '.format( dv, dh, mv,mh)
        
        
        y1 = max(0,mv);     x1 = max(0,mh);
        y2 = min(h1,h2);    x2 = min(w1,w2) 
        om1  =        im1[ y1:y2,   x1:x2] .copy()     #  image crop

        yt1= abs(mv);     yt2 = yt1 +  min( h1,h2)    # set up panel crop

        if mh == 0:
            xt1= 0 #abs(mh) ;
            xt2 = xt1 +  min( w1,w2)       
        elif mh > 0:      #  eg on 2 
            xt1 = mh
            xt2 = xt1 + min(w1,w2)
        elif mh < -15:              # large neg mh on 1
            xt1= 0 #abs(mh) ;
            xt2 = xt1 +  min( w1,w2)
        else:
             print ' three here'
             xt1 = abs(mh)  
             xt2 = xt1 + min(w1,w2)

            
        om2  =        im2[yt1:yt2, xt1:xt2].copy()    #  panel crop
        
        if db:
            print 'display om1 the image x'
            cvs(1,om1,'x')
            print ('display om2 the template y1 {} y2 {}  x1 {} x2 {}'
                         .format(yt1,yt2,xt1,xt2))
            cvs(1,om2,'y')
        w1,  h1  = om1.shape[::-1]   # image
        w2,  h2 =  om2.shape[::-1]   # panel
        if db: print 'om1 w {}, h {}   im2 w {}  h {}'.format(w1, h1,w2, h2)
        res = cv2.bitwise_and(om1,om2)
        pxlcnt = np.sum(res) / 255    # count of pixels 
        if db:
            print pxlcnt, 'count of pixels'
            cvs(1,res,'z')
            cvd()
        
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
    path = ('C:\\Train\\{}*.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = True
##    fwt = 'wtTest.png'
##    img = cv2.imread(fwt,0)
##    cvs(db,img)
## #   pxls =  tMatch(img,typ,db)    # search for a number
##    print 'number is',pxls
    
    for f in files:                # read templates from Train
        img = cv2.imread(f,0)
        h,w = img.shape[:2] 
        print 'img w h      file    ', w, h ,f
        pxls =  tMatch(img,typ,db)    # search for a number
        print 'number is',pxls
        

      
        cvs(1,img)
    cvd()

