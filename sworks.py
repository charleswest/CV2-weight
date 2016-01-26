from cwUtils import *
import numpy as np
import cv2
import warnings
'''
This routine takes the imput full size photo and segments it into wt, fat and water
each of which are saved in a seperate .png file.  cropTest the segmented panel is also saved
'''
db = False
def Cropx( img):
    global db,Gd
#    img =  img.getNumpyCv2()     ##    <<<<-----  SCV to OCV
    h,w = img.shape[:2] 
    print ' w x h', w , h
    if h == 2988:
        img = rotate(img,90)   #  all Dec set rotate

#    imgC =  img.getNumpyCv2()     ##    <<<<-----  SCV to OCV
    imgC = cv2.resize(img, (w/4,h/4))               # **************  shrink for detection
    fc =  find_squares(imgC)
    y1,y2 = fc[0][1],fc[2][1]
    x1,x2 = fc[0][0],fc[2][0]                 ####   needs work rectangle picked at random
 #   img3c = imgC[ y1:y2 ,x1:x2 ].copy()
    y2 = y2 +5  
    img3c = img[ 4*y1:4*y2, 4*x1:4*x2].copy()    #  **********  restore original size 
    if db: cvs(img3c)
    angle = tstInvert(img3c)  # cv2 img
    
  #  scv_image = scv_image.rotate(angle,fixed=False)  
    cv_image = rotate(img3c,angle)         # remove skew or inversion
    cv2.imwrite('cropTest.png',cv_image)   #  save intermediate results
    return(cv_image)

def angle_cos(p0, p1, p2):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d1, d2 = p0-p1, p2-p1
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )     
    
def find_squares(img):     ## cv2 img
    global db
    #img = cv2.GaussianBlur(img, (5, 5), 0)
 #   img =  img.getNumpyCv2()
    
    squares = []
    for gray in cv2.split(img):
        #cvs(gray)
        if db:
            cv2.imshow('gray',gray)
            cv2.waitKey()
        
        for thrs in xrange(0, 255, 26):        #  from 0 to 255 in steps of 26  ~ 10 steps
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)

##      im = cv2.imread('test.jpg')
##    5 imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##    6 ret,thresh = cv2.threshold(imgray,127,255,0)
##    7 im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                
          
            im2, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for j,cnt in enumerate(contours):
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 10000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    fc = order_pts(cnt)        #     fc now tl, tr, br, bl
                    y1,y2 = fc[0][1],fc[2][1]
                    x1,x2 = fc[0][0],fc[2][0]
                    sh = abs(y1-y2); sw = abs(x1-x2)
                    aspect = round (sh / sw ,3)
                    
                    if aspect > .35 and aspect < .40:
                        print 'fc  y1,y2 {},{} x1,x2 {},{}  asp {}'.format( y1,y2 ,x1,x2,aspect)
                        squares.append(fc)
                        return(fc)
                    
           
    return squares

def tstInvert(img):
  ' inverted images have a horizontal line at .3 instead of .7 '
  height, width = img.shape[:2]
  fset = findLines(img,minLineLength=100)
##  fh = fset.filter(abs(fset.angle()) < 2 )    #   near horizon
  v7 =  0 ; v3 = 0; maxA = 0
  for x1,y1,x2,y2 in fset[0]:
     angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
     if db: print 'Angle for skew ', angle, maxA
     
     if abs(angle) > abs(maxA) and abs(angle) < 3:
         maxA = angle
         
     yh = round( y2 / float(height),1 )  # % dist on y axis
     if   yh == 0.3: v3 = v3 + 1
     elif yh == 0.7: v7 = v7 + 1

  if( v3 > v7):
      return(180)
  else:
      if db: print ' remove skew', maxA
      return( maxA )  #  largest < 2 deg
      #return(0)        # try with skew

def Part(self,img):
    h,w = img.shape[:2] 
    fv1 = int(.67 * w )   #.7
    fv2 = int(.5 * fv1)
    x1cut = int(.3 * fv2)
    x2cut = int(.95*(fv1 + x1cut))
    dy = .15 * h
    fy = int(.67 * h)
    fyc =   fy           #   cut line for h20 allow some slack
   #cv2.line(img,(x1,y1),    (x2,y2),   (0,255,0)             ,2) 
    cv2.line(img,(x1cut,0),  (x1cut,h),   (0,0,0)        ,thickness=3)
    cv2.line(img,( 0,fy),    ( w, fy ),   (0,0,0)        ,thickness=3)
    cv2.line(img, (fv1,0),   ( fv1,h),    (0,0,0)        ,thickness=3)
#   ROI = imgC[ y1:y2,     x1:x2   ].copy()
    wt  = img [  0:fy,   x1cut:fv1  ].copy()  #  100  x 300   st at 150   asp = .33
    cv2.line(img,(x2cut,0), (x2cut,h), (255,255,255)     ,thickness=3)
    dy = .15 * h
    fat  = img[ 0:fy,    x2cut:w  ].copy()
    h2o =  img[ fy:h,     x1cut:fv2   ].copy()

    if db: cvs(img )

##    h2o = img.crop((x1cut,fyc), (fv2, img.height)  )
    
    return([wt,fat,h2o])
  
if  __name__ == '__main__':
     
    db = True
    iHunt = []
    fil = "input.png"
    #fil = 'C:\\github\\cvWeight\\Thin.JPG' 
    print 'sworks.py', fil
    imgC = cv2.imread(fil)
    if not fil == "input.png":  img.save("input.png")
    cvs(imgC,fil)
    imtC = Cropx( imgC)  # returns cv img 
    cv2.imwrite('cropTest.png',imtC) 
    cvs(imtC,'croptest')
    [wt,fat,h2o]=Part(1,imtC)
    cvs(h2o,'h2o',0)
    cvs(wt,'wt',0)
    cvs(fat,'fat',0)

    cvd()
    print('end sworks')
    
    
