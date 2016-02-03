
import numpy as np
import cv2
from cwUtils import *
from findLines import findLines
import warnings
'''
This routine takes the imput full size photo and segments it into wt, fat and water
each of which are saved in a seperate .png file.  cropTest the segmented panel is also saved
'''
global db
def Cropx(db, img):
    
#    img =  img.getNumpyCv2()     ##    <<<<-----  SCV to OCV
    h,w = img.shape[:2] 
#    print ' w x h  db ', w , h, db
    if h == 2988:
        img = rotate(img,90)   #  all Dec set rotate
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([50,50,110])   #np.array([110,50,50])
    upper_blue = np.array( [255,255,255])   #np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #  find the contour of the mask which needs to be greyscale
    #imgx = cv2.cvtColor(mask,cv2.COLOR_HSV2BGR_FULL )
    #cvs(db,mask)
    cv2.imwrite('tempgray.png',mask)
    imgx = cv2.imread('tempgray.png',0)
    ret,thresh = cv2.threshold(imgx,127,255,0)

    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    imdb = img.copy()
    if contours:
        for cnt in contours:
            #print 'found', cv2.contourArea(cnt)
            if cv2.contourArea(cnt) > 100000:
                x,y,w,h = cv2.boundingRect(cnt)
                if db:                   
                    cv2.rectangle(imdb,(x,y),(x+w,y+h),(0,255,255),5)
                    cvs(db,imdb)
                print 'xy### wh', x , y, w, h , cv2.contourArea(cnt)
                if y > 3:
                    img3c = img[ y-3:y+h+3 ,x:x+w ].copy()
                else:
                    img3c = img[ y:y+h+3 ,x:x+w ].copy()
                cv2.imwrite('img3c.png',img3c)
                cvs(db,img3c)
                break
    else:
        print 'no contours'
    if db: cvs(db,img3c,t=1000)
    angle = tstInvert(db,img3c)  # cv2 img
    
  #  scv_image = scv_image.rotate(angle,fixed=False)  
    cv_image = rotate(img3c,angle)         # remove skew or inversion
    cvs(db,cv_image,t=0)
    cv2.imwrite('cropTest.png',cv_image)   #  save intermediate results
    return(cv_image)

def angle_cos(p0, p1, p2):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d1, d2 = p0-p1, p2-p1
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )     
    


def tstInvert(db,img):
  ' inverted images have a horizontal line at .3 instead of .7 '
  height, width = img.shape[:2]
  stuff = findLines(img,300,30)
  v7 =  0 ; v3 = 0; maxA = 0
  for line in stuff:
      for x1,y1,x2,y2  in line :
#         print 'line' ,x1, y1, x2, y2
         angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
         if db:
             print 'Angle for skew ', angle, maxA,
             cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
             
         
         if abs(angle) > abs(maxA) and abs(angle) < 3:
             maxA = angle
             
         yh = round( y2 / float(height),1 )  # % dist on y axis
         if db: print 'yh is ' , yh
         if   yh == 0.3: v3 = v3 + 1
         elif yh == 0.7: v7 = v7 + 1
  if db:
      print 'V3 {} V7 {} maxA {} lines found {} '.format(v3, v7, maxA, len(stuff))
      cvs(db,img)
  
  if( v3 > v7):
      return(maxA + 180)
  else:
      if db: print ' remove skew', maxA
      return( maxA )  #  largest < 2 deg
      #return(0)        # try with skew

def Part(self,img,db):
    h,w = img.shape[:2] 
    fv1 = int(.65 * w )   #.7
    fv2 = int(.5 * fv1)
    x1cut = int(.3 * fv2)
   
    x2cut = int(.77 * w)
 
    fy = int(.65 * h)
 
   #cv2.line(img,(x1,y1),    (x2,y2),   (0,255,0)             ,2) 
    cv2.line(img,(x1cut,0),  (x1cut,h),   (0,0,0)        ,thickness=3)
    cv2.line(img,( 0,fy),    ( w, fy ),   (0,255,0)        ,thickness=3)
    cv2.line(img, (fv1,0),   ( fv1,h),    (0,0,0)        ,thickness=3)
#   ROI = imgC[ y1:y2,     x1:x2   ].copy()
    wt  = img [  0:fy,   x1cut:fv1  ].copy()  #  100  x 300   st at 150   asp = .33
    cv2.line(img,(x2cut,0), (x2cut,h), (255,255,255)     ,thickness=3)
 
    fat  = img[ 0:fy,     x2cut:w  ].copy()
    h2o =  img[ fy:h,     x1cut:fv2   ].copy()

    if db: cvs(db,img )

 
    
    return([wt,fat,h2o])
  
if  __name__ == '__main__':
    global db     
    db = True
    iHunt = []
    fil = "input.png"
    #fil = 'C:\\github\\cvWeight\\Thin.JPG' 
    print 'sworks.py', fil
    imgC = cv2.imread(fil)
    if not fil == "input.png":  img.save("input.png")
    cvs(db,imgC)
    imtC = Cropx(db, imgC)  # returns cv img 
    cv2.imwrite('cropTest.png',imtC) 
    cvs(db,imtC,t=0)
    [wt,fat,h2o]=Part(1,imtC,db)
    print 'db is', db
    cvs(db,h2o)
    cvs(db,wt,t=0)
    cvs(db,fat,t=0)

    cvd()
    print('end sworks')
    
    
