import cv2
import numpy as np 
from cwUtils import cvd,cvs
import time, os, glob, timeit
from datetime import datetime
from findBlobs import findBlobs, boundsBlob, stdSize
from TloopMatch import tMatch

def rdTyp(imgx,typ,db):
    img = stdSize(imgx,typ)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    img = thresh.copy()
    Y= {
                 #      y1  y2    j limit        
             'wt' : [   45, 367 , 4 ],
             'fat': [   84, 344 , 3  ],
             'h2o': [   41, 231 , 3 ]
                    
            }
    XX = {
           #        100          10           one      tenth   
         'wt' : [(152, 200) , (240,360) , (405,535),  (580,720)  ],             
         'fat': [(20, 80) ,   (100,240) , (250,350),  (0,0)  ],
         'h2o': [(25, 90) ,   (110,210) , (235,320),  (0,0)  ]
            }
    # look at each digit in the image by xx position
    for j in range(0,Y[typ][2]):      #   loops across XX table above
        y1 =Y[typ][0]; y2 = Y[typ][1];
        x1 =XX[typ][j][0]; x2=XX[typ][j][1]
        digit = img[y1:y2,  x1:x2].copy()
        w100  =  tMatch(digit,typ,db)    # search for a number
        print w100
         
if __name__ == '__main__':
   
    typ = 'wt'
    path = ('C:\\Train\\{}7.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = 1
    fwt =  typ + 'Test.png'
    imgx = cv2.imread(fwt )
    rdTyp(imgx,typ,db)    
    cvd()
