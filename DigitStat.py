''' load and analyse numbers  DigitStat'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
import itertools as it

class descriptor():
    lstN = 12
    head =   '''  lb, n  t0,  L,  R,  T  ,B  S   LR  TB, M3 Mv3 '''
    ahd  =   '''  lb n t0  L R  T  B  S  LR TB M3 Mv3 '''

def cwload_digits_lst(path):
    ''' load a set of saved numbers into a list for comparison to possible numbers
        returned by find numbers '''
    import os
    import glob
    print('loading {} ...'.format(path))
                
    files = glob.glob(path)
    dl = []; lbl = []
    for f in files:
        fn = int((f[-5:-4]))
        lbl.append(fn)                    #get n label from filename       
        img = cv2.imread(f,0)
       # img = erode(img,1)
        print( 'im  shape {} {}'.format( fn ,img.shape)  )
        #img = np.floaT2(cv2.resize(img,(40,35) ))
        dl.append(img)
    digits = dl    #np.array(dl)
    labels = np.array(lbl)
#   cv2.imshow('training set', mosaic(10, digits[:]))
    print 'training set labels', labels
    return(digits,labels)


def xrdTyp(img,typ,db):
    '''rdTyp finds the screen area of a digit based on the x y co-ordinates
        in the tables below.   It passes this area to tMatch which returns
        a number  '''
    #img = stdSize(imgx,typ)
    
    img = erode(img,3)
    img = dilate(img,5)
    d = 150
    #cvs(1,imgx,'rdTyp input')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    h = 46; s = 20; v = 212
    lower_blue = np.array([h,s,v])   #np.array([110,50,50])
    upper_blue = np.array( [h+d,s+d,v+d])   #np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
    thresh = cv2.inRange(hsv, lower_blue, upper_blue)

    img = thresh.copy()
    Y= {
                 #      y1  y2    j limit        
             'wt' : [   20, 320 , 4 ],
             'fat': [   35, 220 , 3 ],
             'h2o': [   10, 220 , 3 ]
                    
            }
    XX = {
           #        100          10           one      tenth   
         'wt' : [(95, 145) ,  (165,265) , (280,385  ),  (400,510)  ],             
         'fat': [(10, 55 ) ,   (65,125) , (135,200),  (0,0)  ],
         'h2o': [(5, 55) ,   (65,120 ) , (135,185),  (0,0)  ]
            }
    n = []
    h,w = img.shape
    #print 'id input w {} h {}'.format(w,h)
    # look at each digit in the image by xx position
    for j in range(0,Y[typ][2]):      #   loops across XX table above
        y1 = Y[typ][0];      x1 = XX[typ][j][0]
        y2 = Y[typ][1];      x2 = XX[typ][j][1]                          
        
        digit = img[y1:y2, x1:x2].copy()
        cv2.imwrite('digTest.png',digit)   # save for future debug
        h,w = digit.shape
        #print 'xid input w {} h {}'.format(w,h)
        cvs(1,digit,'input digit')
  #      n.append( tMatch(digit,typ,db))    # interpret as a number
        if db: print 'n is ', n
        n.append(identifyN(digit,0,0,typ) )              # train and test
        
    if db: print '       rdTyp n ',  n     #  exit here
    nn = 0; j = -1
    n.reverse()
    #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
    
    for j, xin in  enumerate(n):
        nn = nn + xin * 10**(j-1)
    cvs(db,img,typ,5000)
    return(nn)
def pxCount(d, msk ):
        jk,cnt4d, hier  = cv2.findContours(d,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        m = len(cnt4d)       
        if m: msk.append(m)
        else: msk.append(0)
        return(msk)
def identifyN(p,lb=0,db=0,typ='x'):
    ''' identify creates digit descriptor vectors by counting the contours under a set of
    masks applied to the digit being examined.  Masks are applied by setting the non mask
    area of the image to zero, black.   Other statistics collected are not used but could
    be input to some future machine learning algorithm'''
    d = np.zeros_like(p)
    dx = d.copy()                       # nothing to see here
    d = p.copy()
    h,w = d.shape
    #print 'id input w {} h {}'.format(w,h)
    im2 = d.copy()
    t0 = np.sum(im2) / 255
    #cvs(db,d,'digit  ' )
    db=1
    d = im2.copy()  
    d[:, w/3:] = 0        #    left 1/3    same as bitwise and
    L = np.sum(d)/255     #
    cvs(db,d,'digit Left ' )
    msk = []              #   initialize mask
    msk = pxCount(d,msk)

    d = im2.copy()         #  middle vert third
    d[ :,  :w/3  ] = 0        #    - left 1/3
    d[ :, 2*w/3:  ] = 0       #    - right 1/3
    Mv3 = np.sum(d)/255
    cvs(db,d,'digit  v Mid3' )
    msk =   pxCount(d ,msk )    #  
    if typ == 'wt': msk[1] = 9
    
    d = im2.copy()
    d[:, :2*w/3] = 0
    R = np.sum(d)/255        # right 1/3
    cvs(db,d,'digit Right ' )
    msk = pxCount(d,msk)

    d = im2.copy()         #  upper 1/3
    d[ h/3:, : ] = 0
    T = np.sum(d)/255
    cvs(db,d,'digit Top ' )
    msk = pxCount(d,msk)

    d = im2.copy()         #  middle horiz third
    d[   :h/3, : ] = 0        #    - upper 1/3
    d[ 2*h/3:, : ] = 0        #    - lower 1/3
    M3 = np.sum(d)/255
    cvs(db,d,' Mid 1/3' )
    msk = pxCount(d,msk)

    d = im2.copy()           #  lower 1/3
    d[ :2*h/3, : ] = 0       #  zero upper 2/3
    B = np.sum(d)/255
    cvs(1,d,'digit Bottom ' )
    mm = pxCount(d,msk)

    if 1: print 'elif mm ==  {}: n = {}  # {}   '.format( mm  , lb,typ)
    
    # statistics returned as descriptor
    S =  ( max(L,R,T,B) - min(L,R,T,B)) 
    LR =  abs(L-R) 
    TB =  abs(T-B)
  #  identify the input    
               # L  m  R  T  m  B        #  left right top bottom horiz vertical   
    if typ == 'wt':
      #  if 1 == 2: pass
        if   mm ==  [2, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 3  # wt   
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt   
        elif mm ==  [2, 9, 2, 1, 4, 1]: n = 0  # wt   
        elif mm ==  [2, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt   
        elif mm ==  [2, 9, 2, 1, 4, 1]: n = 0  # wt   
        elif mm ==  [1, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt   
        elif mm ==  [1, 9, 1, 1, 1, 1]: n = 8 # wt
        elif mm ==  [1, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 2, 2, 2, 1]: n = 4  # wt   
        elif mm ==  [3, 9, 3, 1, 4, 3]: n = 0  # wt   
        elif mm ==  [1, 9, 1, 1, 1, 1]: n = 8  # wt   
        elif mm ==  [1, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt   
        elif mm ==  [1, 9, 2, 1, 1, 1]: n = 2  # wt   
        elif mm ==  [1, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt   
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [2, 9, 2, 1, 2, 1]: n = 1  # wt
        elif mm ==  [1, 9, 2, 2, 2, 1]: n = 4  # wt
        elif mm ==  [2, 9, 3, 1, 4, 2]: n = 0  # wt
        elif mm ==  [1, 9, 1, 1, 1, 1]: n = 2  # wt
        elif mm ==  [1, 9, 2, 1, 2, 1]: n = 1  # wt   
        elif mm ==  [2, 9, 1, 1, 1, 1]: n = 3  # wt
        elif mm ==  [1, 9, 1, 2, 1, 1]: n = 4  # wt   
        elif mm ==  [1, 9, 2, 1, 1, 2]: n = 8  # wt   
        elif mm ==  [1, 9, 1, 1, 1, 1]: n = 8  # wt
        else                          : n = -1    
    elif typ in ['fat','h2o']:
        if 1 ==2 : pass        
        elif mm ==  [2, 2, 3, 1, 4, 2]: n = 0
        elif mm ==  [2, 3, 3, 1, 4, 2]: n = 0
        elif mm ==  [2, 2, 2, 1, 2, 1]: n = 0
        elif mm ==  [2, 2, 3, 1, 4, 2]: n = 0
        elif mm ==  [3, 2, 2, 1, 4, 2]: n = 0
        elif mm ==  [2, 2, 3, 1, 4, 2]: n = 0
        elif mm ==  [2, 3, 3, 1, 4, 2]: n = 0
        elif mm ==  [3, 2, 2, 1, 4, 2]: n = 0
        elif mm ==  [2, 3, 3, 1, 4, 2]: n = 0
        elif mm ==  [2, 2, 2, 1, 2, 1]: n = 1
        elif mm ==  [2, 2, 1, 1, 2, 1]: n = 1
        elif mm ==  [1, 2, 2, 1, 2, 1]: n = 1
        elif mm ==  [2, 2, 2, 1, 2, 1]: n = 1
        elif mm ==  [1, 0, 2, 1, 2, 2]: n = 1
        elif mm ==  [2, 2, 2, 1, 2, 1]: n = 1
        elif mm ==  [1, 2, 2, 1, 2, 1]: n = 1
        elif mm ==  [0, 1, 3, 1, 2, 2]: n = 1
        elif mm ==  [0, 1, 2, 1, 2, 1]: n = 1
        elif mm ==  [1, 4, 1, 1, 1, 1]: n = 2
        elif mm ==  [2, 3, 2, 1, 1, 2]: n = 2
        elif mm ==  [1, 3, 3, 1, 1, 2]: n = 2
        elif mm ==  [2, 3, 3, 1, 1, 2]: n = 2
        elif mm ==  [1, 3, 3, 1, 1, 2]: n = 2
        elif mm ==  [3, 2, 1, 1, 1, 1]: n = 3
        elif mm ==  [3, 2, 2, 1, 1, 2]: n = 3
        elif mm ==  [2, 2, 1, 1, 1, 1]: n = 3
        elif mm ==  [2, 3, 1, 1, 1, 2]: n = 3
        elif mm ==  [1, 1, 2, 2, 2, 1]: n = 4
        elif mm ==  [2, 1, 2, 1, 1, 1]: n = 5
        elif mm ==  [1, 1, 2, 1, 1, 1]: n = 6
        elif mm ==  [0, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [0, 2, 2, 1, 2, 1]: n = 7
        elif mm ==  [1, 1, 2, 1, 2, 2]: n = 7
        elif mm ==  [1, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [0, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [0, 2, 2, 1, 2, 1]: n = 7
        elif mm ==  [0, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [1, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [0, 3, 2, 1, 2, 1]: n = 7
        elif mm ==  [1, 1, 1, 1, 1, 1]: n = 8
        elif mm ==  [3, 2, 1, 1, 1, 2]: n = 9
        else                          : n = -1   
    else :n = -1       
    lb = int(lb)
    descriptor.lst = [lb,n,t0,L,R,T,B,S,LR,TB,M3,Mv3 ]
    d = d - d
    return n

def prtTable(digits,labels):
    db = 1
    dts = np.zeros((10,descriptor.lstN),dtype='int32' )   
    for d , lb in zip(digits,labels):
        #print '     ',descriptor.head 
##        if lb in range(10):
         n = identifyN(d,lb,db)
         #print 'input {} id n {} '.format(lb,n)
            
   
if  __name__ == '__main__':
    db =  1
    for typ in ['wt' ,'h2o','fat']:
        fwt =  typ + 'Test.png'
        imgx = cv2.imread(fwt )
        cvs(db,imgx,'DigitStat')
        print xrdTyp(imgx,typ,0)
        #identifyN(imgx,0,1)
        
    cvd()
##    print __doc__
##    digits, labels =     cwload_digits_lst("c:\\Train\\*.png" )
##    prtTable(digits,labels)
##    cvd()

         
        

