''' load and analyse numbers  DigitStat'''
import numpy as np
import cv2
from cwUtils import cvd, cvs, erode, dilate
from idGRule import idRule
import itertools as it

##class descriptor():
##    lstN = 12
##    head =   '''  lb, n  t0,  L,  R,  T  ,B  S   LR  TB, M3 Mv3 '''
##    ahd  =   '''  lb n t0  L R  T  B  S  LR TB M3 Mv3 '''


def xrdTyp(img,typ,db,trb):
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
             'h2o': [   30, 220 , 3 ]
                    
            }
    XX = {
           #        100          10           one      tenth   
         'wt' : [(95, 145) , (165,265) , (280,385  ),  (400,510)  ],             
         'fat': [(10, 55 ) , (65,125) , (135,200),  (0,0)  ],
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
        cvs(db,digit,'input digit')
  #      n.append( tMatch(digit,typ,db))    # interpret as a number
        if db: print 'n is ', n
        n.append(identifyN(digit,trb,0,0,typ) )              # train and test
        
    if db: print '       rdTyp n ',  n     #  exit here
    nn = 0; j = -1
    n.reverse()
    #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
    
    for j, xin in  enumerate(n):
        nn = nn + xin * 10**(j-1)
    cvs(db,img,typ,50)
    return(nn)
def pxCount(d, msk ):
        jk,cnt4d, hier  = cv2.findContours(d,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        m = len(cnt4d)       
        if m: msk.append(m)
        else: msk.append(0)
        return(msk)
def identifyN(p,trb,lb=0,db=0,typ='x'):
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
    db=0
    msk = []              #   initialize mask
    d = im2.copy()  
    d[:, w/3:] = 0        #    left 1/3    same as bitwise and
    L = np.sum(d)/255     #
    cvs(db,d,'digit Left ' )
   
    msk = pxCount(d,msk)
 
    d = im2.copy()         #  middle vert third
    d[ :,  :2*w/5  ] = 0        #    - left 1/3
    d[ :, 3*w/5:  ] = 0       #    - right 1/3
    Mv3 = np.sum(d)/255
    cvs(db,d,'digit  v Mid 5th' )
    msk =   pxCount(d ,msk )    #  
 #   if typ == 'wt': msk[1] = 9
    
    d = im2.copy()
    d[:, :2*w/3] = 0
    R = np.sum(d)/255        # right 1/3
    cvs(db,d,'digit Right ' )
    msk = pxCount(d,msk)

    d = im2.copy()         #  upper 2nd Q
    d[ :1*h/5, : ] = 0        #    - upper 2/5
    d[ 2*h/6:, : ] = 0        #    - lower   
    T = np.sum(d)/255
    cvs(db,d,'digit T Q ' )
    msk = pxCount(d,msk)

##    d = im2.copy()         #  middle horiz third
##    d[   :h/3, : ] = 0        #    - upper 1/3
##    d[ 2*h/3:, : ] = 0        #    - lower 1/3
##    M3 = np.sum(d)/255
##    cvs(db,d,' Mid 1/3' )
##    msk = pxCount(d,msk)

    d = im2.copy()           #  lower 1/4
    d[ :3*h/5, : ] = 0        #    - upper 2/5
    d[ 4*h/5:, : ] = 0      
    B = np.sum(d)/255
    cvs(db,d,'digit Bottom  Q' )


    msk.insert(0,typ )    
    mm = pxCount(d,msk)
    

    trb.write( '\telif mm ==  {}: n = {} \n'.format( mm  , lb ) )
    print 'digit mask  {}'.format(mm)

    n = idRule(  mm)
    d = d - d
    return n
def idGen(s,trb):
    if s == True:
        
        line = '''
def idRule(mm):
\tn = -1
\tif 1 == 2: pass
'''
            
    else:
        print 'finishing idGen'
        line = '''
\treturn n
if  __name__ == '__main__':
    db =  1
    print idRule(['wt', 3,1,1])
'''                               
    trb.write(line)
                                           
if  __name__ == '__main__':
    db =  1
    trb = open('0idGRule.py','w')     ##  open file fo r write
    idGen(1,trb)    # open file
    
    for typ in ['h2o']:#,'wt' , 'fat']:        
        fwt =  typ + 'Test.png'
        imgx = cv2.imread(fwt )
        print xrdTyp(imgx,typ,db,trb )
        cvs(db,imgx,'DigitStat')
        
        #identifyN(imgx,0,1)
    #cvs(db,imgx,'Digitstat')
    idGen(0,trb)   # close file and cleanup
    trb.close()
    cvd()


         
        

