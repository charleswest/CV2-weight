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
        if db: print 'Tmatch', f[9:-4],        
        im2 = cv2.imread(f,0)
        
        w1,  h1  = im1.shape[::-1]   # image
        w2,  h2 =  im2.shape[::-1]   # panel
        if db: print 'image w {} h {} panel w {} h {}'.format(w1,h1,w2,h2)
        if  w1-w2 < -30:            
            yt1 =int(.5*(h2-h1)); yt2 = yt1 + h1  ;  xt1 = 0 ; xt2= w1
            if db: print 'crop ',yt1, yt2, xt1, xt2
            om2  =        im2[yt1:yt2, xt1:xt2].copy()    #  panel crop
        else:
             om2  =  cv2.resize(im2, ( w1, h1 )  )    # panel resize
      
        if db:
            print 'display im1 the image x'
            cvs(1,im1,'x')
            print 'display im2 the panel x'
            cvs(1,im2,'pp')
            print ('display om2 the template ')
            cvs(1,om2,'y')
        w1,  h1  = im1.shape[::-1]   # image
        w2,  h2 =  om2.shape[::-1]   # panel
        if db: print 'om1 w {}, h {}   im2 w {}  h {}'.format(w1, h1,w2, h2)
        res = cv2.bitwise_and(im1,om2)
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
    from findBlobs import findBlobs, boundsBlob, stdSize
    typ = 'wt'
    path = ('C:\\Train\\{}7.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = 1
    fwt =  typ + 'Test.png'
    imgx = cv2.imread(fwt,0)
    img = stdSize(imgx,typ)
    ret,thresh = cv2.threshold(img,127,255,0)
    img = thresh.copy()
    cvs(1,img,'x')
    y1 = 45; y2 = y1 + 322;  x1 = 152; x2=200
#    wtx00 = img[y1:y2,  x1:x2].copy()    
#    cvs(1,wtx00,'y')
    y1 = 45; y2 = y1 + 322;  x1 = 240; x2=360
    wtx01 = img[y1:y2,  x1:x2].copy()    
#    cvs(1,wtx01,'y')       
#    pxls =  tMatch(wtx01,typ,db)    # search for a number
    y1 = 45; y2 = y1 + 322;  x1 = 405; x2=535
    wtx02 = img[y1:y2,  x1:x2].copy()    
    cvs(1,wtx02,'yy')       
 #   pxls =  tMatch(wtx02,typ,db)
    y1 = 45; y2 = y1 + 322;  x1 = 580; x2=720
    wtx03 = img[y1:y2,  x1:x2].copy()    
    cvs(1,wtx03,'yy')       
    pxls =  tMatch(wtx03,typ,db)  
    print 'number is',pxls
    cvd()

        

      
    

