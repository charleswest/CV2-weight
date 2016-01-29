import cv2
import numpy as np
import sys
global db
db = True
def cvd():
    #global db
    cv2.destroyAllWindows()
def cvs( img,d=['cvs'],t=0):
    global db
   # print 'cvs db', db
    
    ''' Display cv2 format image.  Quit program
    if q is input otherwise continue after t msec
    '''
    
    h,w = img.shape[:2]   #   h = rows,  w = cols
    #print'h x w', h, w
    if max(h,w) > 2400:
        imgC = cv2.resize(img, (w/6,h/6))     #   note h w on resize
    else:
        imgC = np.zeros((h,w))
        imgC = img.copy()
    ds = ''
    for s in d:
        ds = ds + str(s)+ ' '      #  cat list into single string for imshow 
    cv2.imshow(ds , imgC)
    #print 'width x height', w, h
    if db:
        print 'cvs db t', db  , t
        wt = t
    else:
        wt = 1
    key = cv2.waitKey(wt)
    imgC = imgC - imgC
    if key == ord('q'):
        cvd()
        sys.exit('usr killed with q')
    else:
        return(key-48)
        

def rotate(img,angle):
    '''
    rotate img angle around the center
    '''
    rows,cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return(dst)
def erode(img,iterations):
    '''
#Replace a pixel value with the maximum value of neighboors
#There is others like Erode which replace take the lowest value of the neighborhood
#Note: The Structuring element is optionnal
'''
    element_shape = cv2.MORPH_RECT
    kernal = cv2.getStructuringElement( element_shape, (3,3))   # numpy 3x3 array of 1's
    return(cv2.erode(img,kernal,iterations=iterations))

def dilate(img,iterations):
    '''
#Replace a pixel value with the maximum value of neighboors
#There is others like Erode which replace take the lowest value of the neighborhood
#Note: The Structuring element is optionnal
'''
    element_shape = cv2.MORPH_RECT
    kernal = cv2.getStructuringElement( element_shape, (3,3))   # numpy 3x3 array of 1's
    return(cv2.dilate(img,kernal,iterations=iterations))
    
     
    
def findLines(img,minLineLength,maxLineGap=10,a=180, b=False):
    
    height, width = img.shape[:2]
    if b: img = cv2.GaussianBlur(img, (5, 5), 0)                ###  may not needed
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    s = (10,4)
    wrk = np.zeros(s)     # workspace for HoughLines
    lines = cv2.HoughLinesP(edges ,1,np.pi/a ,100,wrk,minLineLength,maxLineGap)
    print 'findLines', len(lines)
    return(lines)

def order_pts(pts):
    # pts is a list of 4 xy pairs that define a rectangle
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect   
if  __name__ == '__main__':
    global db
    db = False
    fil = "cropTest.png"
    img = cv2.imread(fil)
    cvs(img,'continued 1/2 sec',5000)
    imgE = erode(img,3)
    imgD = dilate(imgE,3)
    cvs(imgE, ' eroded' ,0)
    cvs(imgD, 'dilated', 0)
    fil = "input.png"
    img = cv2.imread(fil)
    cvs(img,['input.png ', 27, 'list test'],2000)
    im2 = rotate(img,90)
    cvs(im2)
    ######################  test order pts
    pts =  np.array([
            [380,218],
            [382, 274],
            [535, 271] ,
            [535, 215]
            ])
    rect = order_pts(pts)
    (tl, tr, br, bl) = rect
    print pts
    print 'tl,{} tr,{} br,{} bl,{}'.format( tl, tr, br, bl)
    ##    find lines

    fn = r"lineTest.png"
    img = cv2.imread(fn)
##    cvs(img)  # display input image
##    lines = findLines(img,200,10  )
##    print 'lines shape ', lines.shape
##    print '__________________________________'
##    for x1,y1,x2,y2 in lines[0]:
##        angle =  np.arctan2( y2-y1 ,  x2-x1 ) * 180 /  np.pi   # angle in deg
##        print 'x1,y1 {},{}\t x2,y2 {},{} \tangle {}'.format(x1,y1,x2,y2,angle)
##        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
##    cvs(img)  # display marked up image
    cvd()
