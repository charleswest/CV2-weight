import cv2
import numpy as np 
from cwUtils import cvd,cvs
import time, os, glob, timeit
from datetime import datetime
from findBlobs import findBlobs, boundsBlob, stdSize
from tMatch import tMatch

def rdTyp(imgx,typ,db):
    '''rdTyp finds the screen area of a digit based on the x y co-ordinates
        in the tables below.   It passes this area to tMatch which returns
        a number  '''
    img = stdSize(imgx,typ)
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
             'wt' : [   45, 367 , 4 ],
             'fat': [   84, 344 , 3 ],
             'h2o': [   35, 230 , 3 ]
                    
            }
    XX = {
           #        100          10           one      tenth   
         'wt' : [(152, 200) , (240,360) , (415,530),  (580,720)  ],             
         'fat': [(20, 80) ,   (100,220) , (250,350),  (0,0)  ],
         'h2o': [(10, 90) ,   (110,210) , (235,320),  (0,0)  ]
            }
    n = []
    # look at each digit in the image by xx position
    for j in range(0,Y[typ][2]):      #   loops across XX table above
        y1 =Y[typ][0]; y2 = Y[typ][1];
        x1 =XX[typ][j][0]; x2=XX[typ][j][1]
        digit = img[y1:y2,  x1:x2].copy()
        cv2.imwrite('digTest.png',digit)   # save for future debug
        n.append( tMatch(digit,typ,db))    # interpret as a number      
        
    if db: print '       rdTyp n ',  n     #  exit here
    nn = 0; j = -1
    n.reverse()
    #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
    
    for j, xin in  enumerate(n):
        nn = nn + xin * 10**(j-1)
        cvs(db,img,typ)
    return(nn)                   # the decoded number
         
if __name__ == '__main__':
    db =  1
    typ = 'h2o'
    fwt =  typ + 'Test.png'
    imgx = cv2.imread(fwt )
    print rdTyp(imgx,typ,db)    
    cvd()
