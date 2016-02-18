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
      
        w1,  h1  = im1.shape[::-1]   # image
        w2,  h2 =  om2.shape[::-1]   # panel
        if db: print 'om1 w {}, h {}   im2 w {}  h {}'.format(w1, h1,w2, h2)
        res = cv2.bitwise_and(im1,om2)
        pxlcnt = np.sum(res) / 255    # count of pixels 
        if db:
            print pxlcnt, 'count of pixels'
            cvs(1,res,'z')
        PL= {
                     #         pxl limit   
                 'wt' : [   300 ],
                 'fat': [   300 ],
                 'h2o': [   200 ]       
            }
        if pxlcnt  > PL[typ][0] :
                rtn[n] = '1'                 
        drtn = ''.join(rtn)
   
    
    ''' ptrn translates the results of the pattern analysis into numbers '''
    ptrn = {
           '1110111' :  0,
           '1100000' :  1,   #   leading 1 in weight
           '0000011' :  1,   #   internal 1 
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
        print 'number {} ptrn {}   '.format(n ,  drtn)
        return(n)
    except  KeyError:        
        print 'bad pattern here '  , drtn
        return 0
    
if __name__ == '__main__':
    from findBlobs import findBlobs, boundsBlob, stdSize
    typ = 'h2o'
    path = ('C:\\Train\\{}7.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = 1
    fwt =   'digTest.png'                   # usually saved from rdTyp
    img = cv2.imread(fwt,0)
    pxls =  tMatch(img,typ,db)  
    print 'number is',pxls
    cvd()

        

      
    

