import numpy as np
import cv2
from cwUtils import *
import warnings
def findLines(img,minLineLength,maxLineGap=10,a=180, b=False):
    
    height, width = img.shape[:2]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    print 'findLines', len(lines)
    return(lines)
if  __name__ == '__main__':
    global db
    db = True
    fil = "cropTest.png"
    img = cv2.imread(fil)
    lines = findLines(img,200,10  )
    print 'lines shape ', lines.shape
    print '__________________________________'
 
    for xx in lines:
        print xx
        for x1,y1,x2,y2 in xx:
            angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
            print 'x1,y1 {},{}\t x2,y2 {},{} \tangle {}'.format(x1,y1,x2,y2,angle)
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    cvs(img)  # display marked up image
    cvd()
