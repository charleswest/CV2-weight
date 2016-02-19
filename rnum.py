import numpy as np
import cv2
import sys
from findBlobs import findBlobs, stdSize ,boundsBlob
from tMatch import tMatch
from cwUtils import *
global db
''' Trnum  writes each located digit to a test file for training future
    character recognition  TCleanrnum
    '''
Rtyp = ['wt']
#Gd  = Display((1040,410)) 
iHunt = []
db = False
d = {}                      # global dictionary of n : xy values
xtyp = ''
tfile = ''                  #  this is where we are going to write training data

def hunt(imgx,typ ,db):
    global xtyp,tfile
    imgy = stdSize(imgx,typ)
    hcnt = 0
    xtyp = typ
    typex = {
                 #    lim   limh    ms     mx      dz   
             'wt' : [130.0,150.0,  450,    4000,   60],    
             'h2o': [ 60.0, 80.0,  300,    1500,   35],
             'fat': [  9.0, 15.0,  500,    3000,   45]   #300      
            }
   
    exlist = {
            'wt' :  [8, 2, 11  ],
            'h2o' : [2,  8   ],
            'fat' : [7,  2 ]
              }                             #  200 5 600  3000   works h20
    txlist = {
            'wt' :  [ 160, 140   ],
            'h2o' : [ 127 ,190, 160, 140 ],  #160, 140, 205 ],
            'fat' : [ 160, 190, 205 ]
             }
    lim  =  typex[typ][0]    #limt[0]
    limh =  typex[typ][1]
    ms =    typex[typ][2]
    mx =    typex[typ][3]
    dz =    typex[typ][4]
    #imgy.save(Gd)
    for iex in exlist[typ]:
        if db: print '-----rdNumber    ms', ms, ' mx',  mx #, imgy.area()

        if db: print( ['erode image',iex])
        for tx in txlist[typ]:
            #img = imgy.binarize(tx).invert()
            #img = imgy.erode(iex)
            img =  imgy.copy()
            cvs(db,img)
            hcnt = hcnt + 1
            # n is the pattern, rmx the max size, rms min size for iHunt logs
            n,rmx,rms = rdNumber(img,ex=iex, ms=ms   ,dz=dz , mx = mx ,tval=tx )
          
            if db: print '       Hunt 1 n ', hcnt,  n     #  exit here
            nn = 0; j = -1
            n.reverse()
            #nn = 100 * n[1] + 10 * n[2] + n[3] + n[4]/10.0
            if db :
                print 'n' ,n
                #cpause(['nreverse',n],Gd)
            for j, xin in  enumerate(n):
                nn = nn + xin * 10**(j-1)
            if (nn > lim) and nn < limh:
                iHunt.append((typ, hcnt, iex, tx, ms,rms, mx,rmx,  nn ))
                print 'hunt rtn' ,nn
                cvs(db,img,typ)
                return(nn)
            
                
             
    print '>>>>>>>>>>>>>>>>>hunt  ' ,typ, 'failed'
    return (0)                          #  eliminate hunt2 for now
#    return(hunt2(imgx,typ,hcnt))
def rdNumber(img, tval=160, ex=2, ms=1.0,mx=3, dz = 60):
    
    '''
    analyse the img and pass a likely set of features to qnumb for
    interpretation
    '''
    global db, tfile
    fz = 0; h= 0; v = 0;
    tgrp = [] ;numb = []
    dx = dz     
    
    print '-----rdNumber   tval',tval,' ex',ex,'ms', ms, 'mxsize', mx 
    
    fs,mask = findBlobs(img, ms, mx ,ex, db,tval=tval )
    if not fs:
        if db: print ' no features found'
        cvs(db,img,'nothing in rdnumbr')
        return ([0,0,0,0],0,0)
    else:
#       fs = sorted(fs, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
        fs = sorted(fs, key = lambda cnt:cv2.contourArea(cnt))
        cv2.drawContours( img, fs, -1, (0, 0, 255), 5 )      
   
        rmx = cv2.contourArea(fs[0])        #  left most area
        rmn = rmx         
        fz = 0        
        fs = sorted(fs, key = lambda cnt: tuple(cnt[cnt[:,:,0].argmin()][0]))
        # sorted left to right
        for ix, f   in enumerate( fs):
            x,y,w,h = cv2.boundingRect(f)                       
            #fx = x 
            if cv2.contourArea(f) < rmn: rmn = cv2.contourArea(f)
            if cv2.contourArea(f) > rmx: rmx = cv2.contourArea(f)
            xd = x - fz        # xd is horizontal dist between blobs  
            if xd > dx:         #   dx is parm   here is where the number is detected
                numb.append(qnumb(tgrp,mask))  #,mask,img))    #  process the number
                tnumb(tgrp,img)      # black rectangle and training output
                tgrp = []                                 # start a new group 
            if db: print    'ix {} w {} h {} dx {} xd {} area {}'\
                      .format(ix,w,h,dx,xd,cv2.contourArea(f))                               
            tgrp.append(f)
##            cv2.drawContours( img, [f], 0, (0, 255, 255), 5 ) 
##            cvs(db,img)
            fz = x
        numb.append(qnumb(tgrp,mask))  #,mask,img))      # process the last group
        tnumb(tgrp,img )
        
        print 'last numb', numb
        tpat = numb 
        if  all(i == 'p' for i in tpat):
             return([0,0,0,0],rmx,rmn)     #    nfg return True zero
        if len(tpat)>3:
            while tpat[-1] == 'p':
                tpat.pop()
               
            while( tpat[0] == 'p'):
                tpat.pop(0)
      #  if db: cpause(['end rd',tpat],Gd)
        if 'p' in tpat:
            return([0,0,0,0],rmx,rmn)     #    nfg return True zero
        else:             
            return(tpat,rmx,rmn) # maybe good numeric value
def tnumb(grp,img):
    ''' process a possible digit and output a mask to a file '''
    if not len(grp) > 0: return(0)
    x,y, wg, hg  = boundsBlob(grp)

    # compute bounds for the possible digit   top left bottom right
    tl = (x-10,y-10) ; br = ( x  +  wg+10, y+ hg+10)       #  10 for more room
    cv2.rectangle(img,(tl),(br),(0,0,0),5)       # black rectangle
    
    x1= x; y1 = hg/2 + y; x2=x + wg; y2 = y1
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)   # horizontal center

    x1= wg/2 +  x; y1=y;   x2=x1; y2=hg+y
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)   # vertical center
    #cvs(db,img)
    zh,zw = img.shape[:2] 
 #    print ' w x h  db ', w , h, db 
    if db: print 'rectangle tl{} br{}  img w{}  h{}'.format(tl,br, zw, zh)   

def qnumb(grp,mask):      #   what number does this group encode??
    '''
    we count horizontal bars.   The we create an encoding of the four
    possible vertical bars upper left and right lower left and right
    An 8 has three horizontal bars and all four vertical bars for an
    encoding of 3 1 1 1 1.
    '''
    
    #xd = 999
    global tfile
 #   mask = stdSize(mask,xtyp)  #cv2.resize(img, (1040,410))
    if not len(grp) > 0:
        if db: ( 'zero len group. -- quitting')
        return(0)
##    x,y, w, h  = boundsBlob(grp)
##    #w = 110; h = 300                         #  nasty hack w and h 
##    tmsk = mask[y:y+h , x:x+w].copy()
##    pxls =  tMatch(tmsk,xtyp,db)    # search for a number
##    print 'number is',pxls
##    cvs(db,tmsk,'tmsk')
##    return(pxls)
    xll =0; xlh=0; xrl=0; xrh = 0    #  pixel counts 
    v=0 ;  h=0;                      #  pixel groups  
    x, y, wg, hg = boundsBlob(grp)
    for b in grp:
        bx,by,bw,bh = cv2.boundingRect(b)
        if bh   < 1.1 * bw:
            h = h + 1                         # add to the horizontal count
        else: #v
            v = v + 1
            if (bx < wg/2 +  x) :             # if left side
                if (by > hg/2 + y):        # if low 
                    xll = 1                   # count vertical left  low 
                else:                    
                    xlh = 1                   #                      high   
            else:                             # must be right side 
                if (by > hg/2 + y):        # so if low              
                    xrl = 1                   # count vertical right low
                else:
                    xrh = 1                   #                 else high
       
        #if db: print( 'p so far is h {} v {} xll {} xlh {} xrl {} xrh {}'
        #                  .format(h,   v,   xll,   xlh,    xrl, xrh) )
                    
    

    p = h * 10000 +  xll *  1000 + xlh * 100 +  xrl *  10 + xrh

    ''' ptrn translates the results of the pattern analysis into numbers '''
    ptrn = {
            1100: 1,   #                
           31001: 2,                    
           30011: 3,
           10111: 4,
           30110: 5,
           31110: 6,
           10011: 7,  #?
           11001: 7,  
           31111: 8,
           30111: 9,
           21111: 0
          }
    if p in ptrn:       #  HOO RAY we found a digit                 
        if db: print '>>>>>>found a {}  {}   '.format( ptrn[p] , p)
        writeNumb(ptrn[p],grp,mask)      #      keep the mask image for future use
        return ptrn[p]
    else:                  #  we don't seem to have a number
        print   '<<<<<<<qptrn - pattern problem p is >{}<'.format( p)
        #return('p')
        x,y, w, h  = boundsBlob(grp)
        w = 110; h = 300                         #  nasty hack w and h 
        tmsk = mask[y:y+h , x:x+w].copy()
        pxls =  tMatch(tmsk,xtyp,db)    # search for a number
        print 'number is',pxls
        cvs(db,tmsk,'tmsk')
        return(pxls)
def writeNumb(n,grp,mask):
    return()
       
    x,y, w, h  = boundsBlob(grp)
    tmplate = mask[y:y+h , x:x+w].copy()
    
    fil = 'C:\\Train\\{}{}.png'.format(xtyp,n)
    print 'writeNumb n {} to file {}'.format(n,fil)
    cv2.imwrite(fil,tmplate)
    cvs(db,tmplate,fil)
    
import time
 

if  __name__ == '__main__':
    print ' rnum  module regression Test'
    db = True
    tfile = 'T'
    Rtyp = [  'fat']
    for tst in [ 'wt']:   #['fat']:      #['fat','wt', 'h2o']; 
        img = cv2.imread(tst +'Test.png') 
       
        #cvs(db,img )
        if db:
            cvs(db,img,t=0)
            h,w = img.shape[:2]   #   h = rows,  w = cols
            print 'h {} w{}'.format(h,w)
        wt  = hunt(img,tst,db )     
        print  'result  is', wt 
        print 'iHunt',iHunt

    cvd()
