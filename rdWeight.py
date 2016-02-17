import cv2
import numpy as np 
from cwUtils import cvd,cvs
import time, os, glob, timeit
from datetime import datetime
from findBlobs import findBlobs, boundsBlob, stdSize
from TloopMatch import tMatch
def rdWeight(imgx,typ,db):
    img = stdSize(imgx,typ)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    img = thresh.copy()
    cvs(1,img,'x')
    y1 = 45; y2 = y1 + 322;  x1 = 152; x2=200
    wtx00 = img[y1:y2,  x1:x2].copy()
    w100  =  tMatch(wtx00,typ,db)    # search for a number
#    cvs(1,wtx00,'y')
    y1 = 45; y2 = y1 + 322;  x1 = 240; x2=360
    wtx01 = img[y1:y2,  x1:x2].copy()    
#    cvs(1,wtx01,'y')       
    w010     =  tMatch(wtx01,typ,db)    # search for a number
    y1 = 45; y2 = y1 + 322;  x1 = 405; x2=535
    wtx02 = img[y1:y2,  x1:x2].copy()    
    cvs(0,wtx02,'yy')       
    w001 =  tMatch(wtx02,typ,db)
    y1 = 45; y2 = y1 + 322;  x1 = 580; x2=720
    wtx03 = img[y1:y2,  x1:x2].copy()    
    cvs(0,wtx03,'yy')
    wp1 =  tMatch(wtx03,typ,db)
    print w100, w010, w001, wp1
    n = 100 * w100 + 10 * w010 + w001 + float(wp1 / 10.0)
    print n
if __name__ == '__main__':
    from findBlobs import findBlobs, boundsBlob, stdSize
    typ = 'wt'
    path = ('C:\\Train\\{}7.png'.format( typ    ) )          #os.getcwd()
    print path        
    files = glob.glob(path)  
    db = 0
    fwt =  typ + 'Test.png'
    imgx = cv2.imread(fwt )
    rdWeight(imgx,typ,db)    
    cvd()
